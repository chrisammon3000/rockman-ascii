# rockman-ascii

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](https://github.com/chrisammon3000/rockman-ascii/releases) [![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/chrisammon3000/rockman-ascii)

Rockman is an ASCII-based terminal game where you control 'X' (Rockman) to avoid falling rocks.

## Description

In this game, you control Rockman ('X') at the bottom of the screen, moving horizontally to avoid rocks ('o') falling from the top. The game increases in difficulty over time, with rocks falling faster and more frequently. Your goal is to survive as long as possible and achieve the highest score.

## Features

- ASCII graphics for a retro gaming experience
- Increasing difficulty as the game progresses
- Simple controls using arrow keys
- Teleportation ability for quick escapes
- Comprehensive scoring system with combos and bonuses
- Pause functionality
- Game over screen with final score display

## Installation

1. Ensure you have Python 3.7 or higher installed.
2. Clone this repository:
   ```
   git clone https://github.com/chrisammon3000/rockman-ascii.git
   cd rockman-ascii
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```
4. Install dependencies (if any):
   ```
   pip install -r requirements.txt
   ```

## How to Play

1. Activate the virtual environment if not already active:
   ```
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```
2. Run the game:
   ```
   python main.py
   ```
3. Use the left and right arrow keys to move Rockman.
4. Use Shift + left/right arrow keys to teleport Rockman.
5. Avoid the falling rocks for as long as possible.
6. Press Spacebar to pause/unpause the game.
7. Press 'q' or ESC to quit the game.

## Controls

- Left Arrow: Move Rockman left
- Right Arrow: Move Rockman right
- Shift + Left Arrow: Teleport Rockman to the left
- Shift + Right Arrow: Teleport Rockman to the right
- Spacebar: Pause/Unpause the game
- 'q' or ESC: Quit the game
- 'm': Secret pause (freezes the screen without any indication)

## Scoring System

The game features a comprehensive scoring system. For detailed information about how scores are calculated, please refer to the [SCORING.md](SCORING.md) file.

## Development
Rockman was developed entirely with AI generated code using [Cursor](https://www.cursor.com/). No python was written by any human.

This project is structured with a main game loop in `main.py`. The current implementation includes:

- Rockman's movement and teleportation
- Falling rock generation and physics
- Collision detection
- Scoring and difficulty progression
- Pause functionality
- Game over screen

For future improvements and feature ideas, please check the [IMPROVEMENTS.md](IMPROVEMENTS.md) file.

## Logging

The game uses Python's logging module to log debug information to a file named `rockman_debug.log`. This can be useful for troubleshooting or understanding the game's behavior.

## Contributing

Contributions to Rockman are welcome! Please feel free to submit a Pull Request.

## Contact
[@chrisammon3000](https://github.com/chrisammon3000)

## License

[MIT License](LICENSE)