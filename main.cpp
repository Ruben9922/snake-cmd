#include <ncurses.h>
#include "Snake.h"
#include <utility>
#include <list>

// From: https://stackoverflow.com/a/14997413/3806231
int positive_modulo(int i, int n) {
    return (i % n + n) % n;
}

int main()
{
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    clear();
    addstr("Snake");
    getch();

    Snake snake(COLS, LINES);
    timeout(500);
    int key;
    do {
        key = getch();
        switch (key) {
            case KEY_LEFT:
                snake.direction = {-1, 0};
                break;
            case KEY_RIGHT:
                snake.direction = {1, 0};
                break;
            case KEY_UP:
                snake.direction = {0, -1};
                break;
            case KEY_DOWN:
                snake.direction = {0, 1};
                break;
        }

        std::pair<int,int> current_front = snake.cells.front();
        std::pair<int,int> new_front = {
                positive_modulo(current_front.first + snake.direction.first, COLS),
                positive_modulo(current_front.second + snake.direction.second, LINES)
        };
        snake.cells.push_front(new_front);

        snake.cells.pop_back();

        clear();
        for (std::pair<int,int> cell : snake.cells) {
            mvaddch(cell.second, cell.first, 'x');
        }
    } while (key != 27 && key != 'q');

    endwin();

    return 0;
}
