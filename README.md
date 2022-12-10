# Snake

[![Build Status](https://travis-ci.com/Ruben9922/snake-cmd.svg?branch=master)](https://travis-ci.com/Ruben9922/snake-cmd)
[![PyPI](https://img.shields.io/pypi/v/ruben-snake-cmd)](https://pypi.org/project/ruben-snake-cmd/)
[![ruben-snake-cmd](https://snapcraft.io//ruben-snake-cmd/badge.svg)](https://snapcraft.io/ruben-snake-cmd)
[![GitHub](https://img.shields.io/github/license/Ruben9922/snake-cmd)](https://github.com/Ruben9922/snake-cmd/blob/master/LICENSE)

Command-line version of the classic Snake game.

![GIF showing gameplay](https://raw.githubusercontent.com/Ruben9922/snake-cmd/master/screenshot.gif)

## Installation

Install as usual:

```bash
pip install ruben-snake-cmd
```

You may wish to [create a virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) beforehand.

### Installation on Windows
The game requires the curses library. This should already be installed on Linux and macOS so no additional steps are required. However, it is not included in the Windows version of Python, as noted in the [curses documentation](https://docs.python.org/3.7/howto/curses.html#what-is-curses). On Windows, you can install the `windows-curses` package (see [this comment](https://gist.github.com/sanchitgangwar/2158089#gistcomment-3029530)), using `pip install windows-curses`.

## Usage
Run the game using the following command:
```bash
ruben-snake-cmd
```
Note that I've only tested this on Linux.

The application should generally be self-explanatory.

One thing to note is the settings screen, reached by pressing <kbd>S</kbd> on the title screen. Currently, the only option is to enable/disable the snake wrapping around the edge of the window by pressing <kbd>B</kbd>. If disabled, the snake will "die" on reaching the edge of the window.

There is also a controls screen, reached by pressing <kbd>C</kbd> on the title screen.

## In-Game Controls

| Key(s) | Action |
|-------------------------------------------------------|------------------|
| <kbd>←</kbd>, <kbd>↑</kbd>, <kbd>→</kbd>, <kbd>↓</kbd> | Change direction |
| <kbd>Q</kbd> | End game |

Note that these only apply in-game and not on other screens, such as the title screen or settings screen.
