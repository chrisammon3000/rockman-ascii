#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import time
import random
import logging

# Set up logging for debugging
logging.basicConfig(filename='rockman_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Rockman:
    """
    Represents the player character in the Rockman game.
    
    Attributes:
        x (int): The x-coordinate of Rockman.
        y (int): The y-coordinate of Rockman.
        symbol (str): The character used to represent Rockman on the screen.
        width (int): The width of Rockman's representation.
        last_move_time (float): The timestamp of Rockman's last movement.
        is_alive (bool): Indicates whether Rockman is alive or not.
    """

    def __init__(self, x, y):
        """
        Initialize a new Rockman instance.

        Args:
            x (int): The initial x-coordinate.
            y (int): The initial y-coordinate.
        """
        self.x = x
        self.y = y
        self.symbol = 'X'
        self.width = 1
        self.last_move_time = time.time()
        self.is_alive = True

    def move(self, dx):
        """
        Move Rockman horizontally.

        Args:
            dx (int): The distance to move (-1 for left, 1 for right).
        """
        self.x += dx
        self.last_move_time = time.time()

    def teleport(self, min_x, max_x, direction):
        """
        Teleport Rockman to a random position in the specified direction.

        Args:
            min_x (int): The minimum x-coordinate for teleportation.
            max_x (int): The maximum x-coordinate for teleportation.
            direction (str): The direction to teleport ('left' or 'right').
        """
        if direction == 'left':
            new_x = random.randint(min_x, self.x - 1)
        else:  # direction == 'right'
            new_x = random.randint(self.x + 1, max_x)
        self.x = new_x
        self.last_move_time = time.time()

    def die(self):
        """
        Change Rockman's appearance when he dies.
        """
        if self.is_alive:
            self.is_alive = False
            self.symbol = '* *'
            self.x -= 1  # Move left by 1 to center the explosion
            self.width = 3  # Increase width to 3 for the explosion effect
            logging.debug(f"Rockman died at x={self.x}, y={self.y}")

class Rock:
    """
    Represents a falling rock in the Rockman game.

    Attributes:
        x (int): The x-coordinate of the rock.
        y (int): The y-coordinate of the rock.
        symbol (str): The character used to represent the rock on the screen.
    """

    def __init__(self, x, y):
        """
        Initialize a new Rock instance.

        Args:
            x (int): The initial x-coordinate.
            y (int): The initial y-coordinate.
        """
        self.x = x
        self.y = y
        self.symbol = 'o'

    def fall(self):
        """
        Move the rock down by one unit.
        """
        self.y += 1

class Score:
    """
    Manages the scoring system for the Rockman game.

    Attributes:
        Various score components and game statistics.
    """

    def __init__(self):
        """
        Initialize a new Score instance with default values.
        """
        # Initialize various score components
        self.base_score = 0
        self.time_score = 0
        self.rock_avoidance_score = 0
        self.near_miss_score = 0
        self.level_up_bonus = 0
        self.survival_milestone_bonus = 0
        self.score_decay = 0
        self.difficulty_multiplier = 1.0
        self.combo = 0
        self.last_difficulty_increase = 0
        self.last_decay_time = 0
        self.teleport_penalty = 50  # Penalty for each teleport
        self.teleport_penalty_total = 0  # Track total teleport penalties

    def update(self, elapsed_time, rocks_avoided, near_misses, rocks_per_wave):
        """
        Update the score based on game events.

        Args:
            elapsed_time (float): The total game time elapsed.
            rocks_avoided (int): The number of rocks avoided in this update.
            near_misses (int): The number of near misses in this update.
            rocks_per_wave (int): The current number of rocks per wave.
        """
        # Update score based on game events
        self.time_score = int(elapsed_time)
        self.rock_avoidance_score += rocks_avoided * 5 * self.combo
        self.near_miss_score += near_misses * 2
        
        # Increase difficulty over time
        if elapsed_time - self.last_difficulty_increase >= 30:
            self.difficulty_multiplier += 0.1
            self.last_difficulty_increase = elapsed_time
        
        # Award level-up bonus
        if rocks_per_wave > self.level_up_bonus // 100:
            self.level_up_bonus += 100
        
        # Award survival milestone bonuses
        if elapsed_time >= 300 and self.survival_milestone_bonus < 2000:
            self.survival_milestone_bonus = 2000
        elif elapsed_time >= 120 and self.survival_milestone_bonus < 1000:
            self.survival_milestone_bonus = 1000
        elif elapsed_time >= 60 and self.survival_milestone_bonus < 500:
            self.survival_milestone_bonus = 500
        
        # Apply score decay for long-running games
        if elapsed_time >= 300 and elapsed_time - self.last_decay_time >= 10:
            self.score_decay += 1
            self.last_decay_time = elapsed_time

    def apply_teleport_penalty(self):
        """
        Apply a penalty for teleporting.
        """
        penalty = int(self.teleport_penalty * self.difficulty_multiplier)
        self.teleport_penalty_total += penalty
        logging.debug(f"Teleport penalty applied: Penalty: {penalty}, Total penalty: {self.teleport_penalty_total}")

    def get_total_score(self):
        """
        Calculate and return the total score.

        Returns:
            int: The total score.
        """
        total = max(0, int((self.base_score + self.time_score + self.rock_avoidance_score + 
                    self.near_miss_score + self.level_up_bonus + 
                    self.survival_milestone_bonus - self.score_decay - self.teleport_penalty_total) * 
                   self.difficulty_multiplier))
        logging.debug(f"Score components: Base: {self.base_score}, Time: {self.time_score}, " 
                      f"Rock Avoidance: {self.rock_avoidance_score}, Near Miss: {self.near_miss_score}, "
                      f"Level-up Bonus: {self.level_up_bonus}, Survival Bonus: {self.survival_milestone_bonus}, "
                      f"Decay: {self.score_decay}, Teleport Penalty: {self.teleport_penalty_total}, "
                      f"Multiplier: {self.difficulty_multiplier}, Total: {total}")
        return total

def draw_header(win, rocks_count, elapsed_time, score):
    """
    Draw the game information header.

    Args:
        win (curses.window): The curses window to draw on.
        rocks_count (int): The current number of rocks on screen.
        elapsed_time (float): The total game time elapsed.
        score (Score): The current game score.
    """
    # Draw the game information header
    height, width = win.getmaxyx()
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    current_score = score.get_total_score()
    header = f"Rocks: {rocks_count} | Time: {minutes:02d}:{seconds:02d} | Score: {current_score}"
    
    # Draw the box around the header
    win.addch(0, 0, curses.ACS_ULCORNER)
    win.addch(0, width - 1, curses.ACS_URCORNER)
    win.hline(0, 1, curses.ACS_HLINE, width - 2)
    win.vline(1, 0, curses.ACS_VLINE, 1)
    win.vline(1, width - 1, curses.ACS_VLINE, 1)
    
    # Draw the header text
    start_x = (width - len(header)) // 2
    win.addstr(1, start_x, header)

def check_collision(rockman, rocks):
    """
    Check if Rockman collides with any rocks.

    Args:
        rockman (Rockman): The Rockman instance.
        rocks (list): List of Rock instances.

    Returns:
        bool: True if a collision is detected, False otherwise.
    """
    # Check if Rockman collides with any rocks
    for rock in rocks:
        if rock.x == rockman.x and rock.y == rockman.y:
            logging.debug(f"Collision detected at x={rock.x}, y={rock.y}")
            return True
    return False

def show_startup_screen(win):
    """
    Display the startup screen.

    Args:
        win (curses.window): The curses window to draw on.

    Returns:
        bool: True if the game should start, False if it should exit.
    """
    # Display the startup screen
    height, width = win.getmaxyx()
    startup_win = curses.newwin(7, width - 4, height // 2 - 3, 2)
    startup_win.box()
    
    title = "ROCKMAN"
    subtitle = "Press any key to start"
    exit_text = "Press ESC to exit"
    
    startup_win.addstr(1, (width - 6 - len(title)) // 2, title, curses.A_BOLD)
    startup_win.addstr(3, (width - 6 - len(subtitle)) // 2, subtitle)
    startup_win.addstr(5, (width - 6 - len(exit_text)) // 2, exit_text)
    
    startup_win.refresh()
    win.refresh()  # Refresh the main window to ensure it's still visible
    
    # Wait for 2 seconds
    time.sleep(2)
    
    # Wait for user input
    curses.curs_set(0)
    win.nodelay(False)
    key = win.getch()
    win.nodelay(True)

    # Check if ESC key was pressed
    return key != 27  # 27 is the ASCII code for ESC

def main(stdscr):
    """
    The main game loop and initialization.

    Args:
        stdscr (curses.window): The main curses window.
    """
    logging.debug("Game started")
    
    # Setup curses environment
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(1)
    stdscr.timeout(50)  # Reduced timeout for faster updates
    stdscr.scrollok(False)

    # Get screen dimensions
    screen_height, screen_width = stdscr.getmaxyx()
    logging.debug(f"Screen dimensions: {screen_width}x{screen_height}")

    # Create a new window
    win = curses.newwin(screen_height, screen_width, 0, 0)

    # Create Rockman
    rockman = Rockman(screen_width // 2, screen_height - 2)
    logging.debug(f"Rockman created at x={rockman.x}, y={rockman.y}")

    # Initialize game objects
    rocks = []
    score = Score()

    # Draw initial game screen
    win.clear()
    draw_header(win, 0, 0, score)
    win.box()
    win.refresh()

    # Show startup screen
    if not show_startup_screen(win):
        logging.debug("Game exited from startup screen")
        return  # Exit the game if ESC was pressed

    # Game loop variables
    frame_count = 0
    rocks_per_wave = 1
    start_time = time.time()
    game_over = False
    paused = False
    secret_paused = False  # New variable for secret pause
    pause_start_time = 0
    logging.debug("Entering main game loop")

    # Main game loop
    while not game_over:
        # Handle input
        key = stdscr.getch()
        if key == 27:  # ESC key
            logging.debug("ESC key pressed, exiting game")
            game_over = True
            break
        elif key == ord('q'):
            break
        elif key == ord(' '):  # Spacebar
            paused = not paused
            if paused:
                pause_start_time = time.time()
                logging.debug("Game paused")
            else:
                start_time += time.time() - pause_start_time
                logging.debug("Game resumed")
        elif key == ord('m'):  # Secret pause button
            secret_paused = not secret_paused
            if secret_paused:
                logging.debug("Game secretly paused")
            else:
                logging.debug("Game secretly resumed")
        elif not paused and not secret_paused:
            if key in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_SLEFT, curses.KEY_SRIGHT]:
                if key in [curses.KEY_SLEFT, curses.KEY_SRIGHT]:  # Shift + Arrow keys for teleportation
                    direction = 'left' if key == curses.KEY_SLEFT else 'right'
                    rockman.teleport(1, screen_width - 2, direction)
                    score.apply_teleport_penalty()  # Apply teleport penalty
                    logging.debug(f"Rockman teleported {direction} to x={rockman.x}, Teleport penalty applied")
                    logging.debug(f"Teleport penalty applied, new total score: {score.get_total_score()}")
                    # Check for collision immediately after teleportation
                    if check_collision(rockman, rocks):
                        rockman.die()
                        game_over = True
                        logging.debug("Collision detected after teleportation, game over set to True")
                elif key == curses.KEY_LEFT and rockman.x > 1:
                    rockman.move(-1)
                elif key == curses.KEY_RIGHT and rockman.x < screen_width - 2:
                    rockman.move(1)
                score.combo = 0

        if not paused and not secret_paused:
            # Update game state
            frame_count += 1
            elapsed_time = time.time() - start_time

            # Generate new rocks
            if frame_count % 20 == 0:  # Spawn rocks every 20 frames (about 1 second)
                for _ in range(rocks_per_wave):
                    x = random.randint(1, screen_width - 2)
                    y = random.randint(-5, 0)  # Start rocks above the screen with random offsets
                    new_rock = Rock(x, y)
                    rocks.append(new_rock)
                if frame_count % 100 == 0:  # Increase rocks per wave every 5 seconds
                    rocks_per_wave += 1

            # Update rocks
            rocks_avoided = 0
            near_misses = 0
            if frame_count % 2 == 0:  # Make rocks fall every 2 frames
                for rock in rocks:
                    rock.fall()
                    if rock.y == screen_height - 2 and abs(rock.x - rockman.x) <= 1:
                        near_misses += 1
                        score.combo += 1

            # Remove rocks that have fallen off the screen
            rocks_avoided = len([rock for rock in rocks if rock.y >= screen_height - 1])
            rocks = [rock for rock in rocks if rock.y < screen_height - 1]

            # Update score
            score.update(elapsed_time, rocks_avoided, near_misses, rocks_per_wave)

            # Check for collision
            if check_collision(rockman, rocks):
                rockman.die()
                game_over = True
                logging.debug("Collision detected, game over set to True")

            # Render game state
            win.clear()
            
            # Draw header
            draw_header(win, len(rocks), elapsed_time, score)
            
            # Draw game area border
            win.hline(2, 0, curses.ACS_HLINE, screen_width - 1)
            win.addch(2, 0, curses.ACS_LTEE)
            win.addch(2, screen_width - 1, curses.ACS_RTEE)
            win.vline(3, 0, curses.ACS_VLINE, screen_height - 4)
            win.vline(3, screen_width - 1, curses.ACS_VLINE, screen_height - 4)
            win.addch(screen_height - 1, 0, curses.ACS_LLCORNER)
            win.hline(screen_height - 1, 1, curses.ACS_HLINE, screen_width - 2)

            # Safely draw the bottom-right corner
            try:
                win.addch(screen_height - 1, screen_width - 1, curses.ACS_LRCORNER)
            except curses.error:
                pass
            
            # Draw Rockman
            if rockman.is_alive:
                win.addstr(rockman.y, rockman.x, rockman.symbol)
            else:
                win.addstr(rockman.y, rockman.x, rockman.symbol)

            # Draw rocks
            for rock in rocks:
                if 2 < rock.y < screen_height - 1:
                    win.addstr(rock.y, rock.x, rock.symbol)

            win.refresh()

            # If game over, pause briefly to show the death animation
            if game_over:
                logging.debug("Game over, showing death animation")
                time.sleep(0.5)

            # Control frame rate
            time.sleep(0.02)  # Approx. 50 FPS
        else:
            # Display pause message in a box
            pause_win = curses.newwin(5, screen_width - 4, screen_height // 2 - 2, 2)
            pause_win.box()
            pause_text = "PAUSED"
            resume_text = "Press SPACE to resume"
            pause_win.addstr(1, (screen_width - 6 - len(pause_text)) // 2, pause_text, curses.A_BOLD)
            pause_win.addstr(3, (screen_width - 6 - len(resume_text)) // 2, resume_text)
            pause_win.refresh()
            win.refresh()  # Refresh the main window to ensure it's still visible

    logging.debug("Exited main game loop")

    # Game over screen
    if game_over:
        logging.debug("Entering game over screen")
        try:
            # Create a new window for the game over text
            game_over_win = curses.newwin(5, screen_width - 4, screen_height // 2 - 2, 2)
            logging.debug(f"Game over window created: height=5, width={screen_width-4}, y={screen_height//2-2}, x=2")
            game_over_win.box()

            game_over_text = "GAME OVER"
            game_over_win.addstr(1, (screen_width - 6 - len(game_over_text)) // 2, game_over_text, curses.A_BOLD)
            
            final_score_text = f"Final Score: {score.get_total_score()}"
            game_over_win.addstr(2, (screen_width - 6 - len(final_score_text)) // 2, final_score_text)
            
            press_key_text = "Press any key to exit"
            game_over_win.addstr(3, (screen_width - 6 - len(press_key_text)) // 2, press_key_text)
            
            game_over_win.refresh()
            win.refresh()  # Refresh the main window to ensure it's still visible
            logging.debug("Game over screen rendered")
            
            # Wait for user input
            stdscr.nodelay(False)  # Make getch() blocking
            key = stdscr.getch()  # Wait for any key press
            logging.debug(f"Key pressed to exit game over screen: {key}")
        except Exception as e:
            logging.error(f"Error displaying game over screen: {str(e)}")
        finally:
            logging.debug("Game over screen displayed")

        # Add a delay to ensure the game over screen is visible
        time.sleep(2)

    # Cleanup curses settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    logging.debug("Game ended")

if __name__ == "__main__":
    curses.wrapper(main)