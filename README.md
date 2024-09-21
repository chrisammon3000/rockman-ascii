# Rockman

Rockman is an ASCII-based terminal game where you control 'X' (Rockman) to avoid falling rocks.

## Description

In this game, you control Rockman ('X') at the bottom of the screen, moving horizontally to avoid rocks ('o') falling from the top. The game increases in difficulty over time, with rocks falling faster and more frequently.

## Features

- ASCII graphics for a retro gaming experience
- Increasing difficulty as the game progresses
- Simple controls using arrow keys

## Installation

1. Ensure you have Python 3.7 or higher installed.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/rockman.git
   cd rockman
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
4. Avoid the falling rocks for as long as possible.
5. Press 'q' to quit the game.

## Development

This project is structured with a main game loop in `main.py`. Future development will include:

- Implementing Rockman's movement
- Adding falling rock generation and physics
- Implementing collision detection
- Adding scoring and difficulty progression

## License

[MIT License](LICENSE)