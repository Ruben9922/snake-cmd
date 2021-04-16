import curses
import numpy as np
import game_utilities as gu


class Snake:
    def __init__(self, initial_length):
        self.cells = np.stack([
            np.arange(initial_length) + (Game.max_size[0] // 2),
            np.zeros(initial_length, dtype="int64") + (Game.max_size[1] // 2),
        ], axis=1)
        self.direction = np.array([-1, 0])

    @property
    def length(self):
        return self.cells.shape[0]

    def intersected_itself(self):
        return self.cells.shape[0] != np.unique(self.cells, axis=0).shape[0]


class Game:
    max_size = np.array([24, 80])

    def __init__(self, stdscr):
        self.stdscr = stdscr

    @property
    def window_size(self):
        return np.amin(np.stack([
            self.stdscr.getmaxyx(),
            Game.max_size,
        ]), axis=0)

    def show_game_screen(self, settings):
        snake = Snake(1)
        pellet = np.random.randint(Game.max_size, size=2)

        key = None
        # getch return value of 27 corresponds to escape key - doesn't look like curses has a constant for this
        # 3rd condition checks if snake has "eaten" (intersected with) itself, i.e. whether any cells re-appear in the list
        while key != 27 and key != ord("q") and not snake.intersected_itself():
            # Set the maximum amount of time to block for a key press
            # This is effectively the update interval
            self.stdscr.timeout(max(20, 250 // (snake.length // 5 + 1)))
            key = self.stdscr.getch()  # TODO: Do this last to prevent waiting before drawing game screen

            # Update
            (game_over, pellet) = self.update_game_screen(key, snake, pellet, settings)
            if game_over:
                break

            # Draw
            self.draw_game_screen(snake, pellet)

        # For user input, remove the timeout but keep blocking enabled
        self.stdscr.nodelay(False)

        # Return score
        return snake.length

    def update_game_screen(self, key, snake, pellet, settings):
        # Set new direction based on the key input
        # If an arrow key wasn't pressed then continue in same direction
        if key == curses.KEY_LEFT:
            new_direction = gu.LEFT
        elif key == curses.KEY_RIGHT:
            new_direction = gu.RIGHT
        elif key == curses.KEY_UP:
            new_direction = gu.UP
        elif key == curses.KEY_DOWN:
            new_direction = gu.DOWN
        else:
            new_direction = snake.direction

        # Prevent the snake reversing on itself, i.e. check that the snake's current and new directions aren't the reverse
        # of one another
        if not np.array_equal(snake.direction, -new_direction):
            snake.direction = new_direction

        # Add a cell to the front of the snake, in the given direction
        current_front = snake.cells[0]
        new_front = current_front + snake.direction
        if not settings["snake_wrapping"]["value"] and not (np.zeros(2) <= new_front < Game.max_size):
            return True, pellet
        new_front = new_front % Game.max_size
        snake.cells = np.insert(snake.cells, 0, new_front, axis=0)

        # If the snake just "ate" (intersected with) a pellet:
        # * Effectively increase the length by 1, by not removing a cell to compensate for the one just added
        # * Move the pellet to a random position
        # If the snake didn't just "eat" a pellet:
        # * Remove a cell to compensate for the one just added, so length of the snake stays the same
        # * Obviously leave the pellet where it is
        if (snake.cells == pellet).all(axis=1).any():
            pellet = np.random.randint(Game.max_size, size=2)
        else:
            snake.cells = np.delete(snake.cells, -1, axis=0)

        return False, pellet

    def draw_game_screen(self, snake, pellet):
        self.stdscr.clear()

        # Display score
        self.stdscr.addstr(0, 0, f"Score: {snake.length}")

        # Display hint
        if snake.length <= 3:
            self.stdscr.attron(curses.A_STANDOUT)
            message = "Hint: To move faster, repeatedly press or hold the arrow key."
            self.stdscr.addstr(0, Game.max_size[1] - len(message), message)
            self.stdscr.attroff(curses.A_STANDOUT)

        # Draw pellet
        if curses.has_colors():
            self.stdscr.attron(curses.color_pair(2))

        try:
            self.stdscr.addch(pellet[0], pellet[1], "o")
        except curses.error as e:  # Ignore error when writing to bottom-right corner of window
            pass

        if curses.has_colors():
            self.stdscr.attroff(curses.color_pair(2))

        # Draw snake
        for cell in snake.cells:
            if curses.has_colors():
                self.stdscr.attron(curses.color_pair(1))

            try:
                self.stdscr.addch(cell[0], cell[1], "x")
            except curses.error as e:  # Ignore error when writing to bottom-right corner of window
                pass

            if curses.has_colors():
                self.stdscr.attroff(curses.color_pair(1))


def curses_main(stdscr):
    # Initialise colours
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Show cursor
    curses.curs_set(1)

    settings = {
        "snake_wrapping": {
            "name": "Snake wraps around screen edge",
            "key": "b",
            "value": True
        }
    }
    show_title_screen(stdscr, settings)

    # Hide cursor
    curses.curs_set(0)

    game = Game(stdscr)
    score = game.show_game_screen(settings)

    # Show cursor
    curses.curs_set(1)

    show_game_over_screen(stdscr, score)

    # TODO: For actual game, make window fixed size so you can't cheat by making the terminal window bigger (just don't
    #  use LINES or COLS variables)
    # TODO: Allow option of borders on or off, i.e. to end game or just wrap around (respectively) when snake reaches
    #  edge of the screen
    # TODO: Refactor screens into separate classes (?)
    # TODO: Fix error when resizing window during playing (?)
    # TODO: Fix text potentially covering up snake or pellets (e.g. change background of text character to match
    #  snake/pellet character colour or alternate between text character and snake/pellet character)
    # TODO: Add animation


def show_title_screen(stdscr, settings):
    finished = False
    while not finished:
        stdscr.clear()

        gu.addstr_multiline_aligned(stdscr, [
            " ____              _        \n"
            "/ ___| _ __   __ _| | _____ \n"
            "\\___ \\| '_ \\ / _` | |/ / _ \\\n"
            " ___) | | | | (_| |   <  __/\n"
            "|____/|_| |_|\\__,_|_|\\_\\___|",
            "",
            "Ruben Dougall",
            "",
            "Press C to view controls...",
            "Press S to change settings...",
            "Press any key to start..."
        ], gu.HorizontalAlignment.CENTER, gu.VerticalAlignment.CENTER)

        key = stdscr.getch()
        if key == ord("c"):
            show_controls_screen(stdscr)
        elif key == ord("s"):
            show_settings_screen(stdscr, settings)
        else:
            finished = True


def show_controls_screen(stdscr):
    stdscr.clear()
    gu.addstr_multiline_aligned(stdscr, [
        "In-Game Controls",
        "",
        "← ↑ → ↓ - Change direction (hold to move faster)",
        "Q - End game",
        "",
        "Press any key to close this screen..."
    ], gu.HorizontalAlignment.CENTER, gu.VerticalAlignment.CENTER)
    stdscr.getch()


def show_settings_screen(stdscr, settings):
    finished = False
    while not finished:
        stdscr.clear()
        gu.addstr_multiline_aligned(stdscr, [
            "Settings",
            ""
        ] + [f"{x['key'].upper()} - {x['name']} ({x['value']})" for x in settings.values()] + [
                                     "",
                                     "Press any key to close this screen..."
                                 ], gu.HorizontalAlignment.CENTER, gu.VerticalAlignment.CENTER)

        key = stdscr.getch()
        setting = next((x for x in settings.values() if key == ord(x["key"])), None)
        if setting is None:
            finished = True
        else:
            setting["value"] = not setting["value"]


def show_game_over_screen(stdscr, score):
    stdscr.clear()
    gu.addstr_multiline_aligned(stdscr, [
        "Game over!",
        f"Score: {score}",
        "",
        "Press any key to exit..."
    ], gu.HorizontalAlignment.CENTER, gu.VerticalAlignment.CENTER)
    stdscr.getch()


def main():
    curses.wrapper(curses_main)


if __name__ == "__main__":
    main()
