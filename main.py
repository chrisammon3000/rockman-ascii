import curses
import time
import random

class Rockman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = 'X'
        self.last_move_time = time.time()

    def move(self, dx):
        self.x += dx
        self.last_move_time = time.time()

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = 'o'

    def fall(self):
        self.y += 1

class Score:
    def __init__(self):
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

    def update(self, elapsed_time, rocks_avoided, near_misses, rocks_per_wave):
        self.time_score = int(elapsed_time)
        self.rock_avoidance_score += rocks_avoided * 5 * self.combo
        self.near_miss_score += near_misses * 2
        
        # Update difficulty multiplier
        if elapsed_time - self.last_difficulty_increase >= 30:
            self.difficulty_multiplier += 0.1
            self.last_difficulty_increase = elapsed_time
        
        # Level-up bonus
        if rocks_per_wave > self.level_up_bonus // 100:
            self.level_up_bonus += 100
        
        # Survival milestone bonuses
        if elapsed_time >= 300 and self.survival_milestone_bonus < 2000:
            self.survival_milestone_bonus = 2000
        elif elapsed_time >= 120 and self.survival_milestone_bonus < 1000:
            self.survival_milestone_bonus = 1000
        elif elapsed_time >= 60 and self.survival_milestone_bonus < 500:
            self.survival_milestone_bonus = 500
        
        # Score decay
        if elapsed_time >= 300 and elapsed_time - self.last_decay_time >= 10:
            self.score_decay += 1
            self.last_decay_time = elapsed_time

    def get_total_score(self):
        return int((self.base_score + self.time_score + self.rock_avoidance_score + 
                    self.near_miss_score + self.level_up_bonus + 
                    self.survival_milestone_bonus - self.score_decay) * 
                   self.difficulty_multiplier)

def draw_header(win, rocks_count, elapsed_time, score):
    height, width = win.getmaxyx()
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    header = f"Rockman | Rocks: {rocks_count} | Time: {minutes:02d}:{seconds:02d} | Score: {score.get_total_score()}"
    
    # Draw the box
    win.addch(0, 0, curses.ACS_ULCORNER)
    win.addch(0, width - 1, curses.ACS_URCORNER)
    win.hline(0, 1, curses.ACS_HLINE, width - 2)
    win.vline(1, 0, curses.ACS_VLINE, 1)
    win.vline(1, width - 1, curses.ACS_VLINE, 1)
    
    # Draw the text
    start_x = (width - len(header)) // 2
    win.addstr(1, start_x, header)

def check_collision(rockman, rocks):
    for rock in rocks:
        if rock.x == rockman.x and rock.y == rockman.y:
            return True
    return False

def main(stdscr):
    # Setup
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(1)
    stdscr.timeout(50)  # Reduced timeout for faster updates
    stdscr.scrollok(False)

    # Get screen dimensions
    screen_height, screen_width = stdscr.getmaxyx()

    # Create a new window
    win = curses.newwin(screen_height, screen_width, 0, 0)

    # Create Rockman
    rockman = Rockman(screen_width // 2, screen_height - 2)

    # Create rocks list and score
    rocks = []
    score = Score()

    # Game loop
    frame_count = 0
    rocks_per_wave = 1
    start_time = time.time()
    game_over = False
    while not game_over:
        # Handle input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT and rockman.x > 1:
            rockman.move(-1)
            score.combo = 0
        elif key == curses.KEY_RIGHT and rockman.x < screen_width - 2:
            rockman.move(1)
            score.combo = 0

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
            game_over = True

        # Render
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
        win.addstr(rockman.y, rockman.x, rockman.symbol)

        # Draw rocks
        for rock in rocks:
            if 2 < rock.y < screen_height - 1:
                win.addstr(rock.y, rock.x, rock.symbol)

        win.refresh()

        # Control frame rate
        time.sleep(0.02)  # Approx. 50 FPS

    # Game over screen
    if game_over:
        win.clear()
        game_over_text = "GAME OVER"
        win.addstr(screen_height // 2 - 2, (screen_width - len(game_over_text)) // 2, game_over_text)
        
        final_score_text = f"Final Score: {score.get_total_score()}"
        win.addstr(screen_height // 2, (screen_width - len(final_score_text)) // 2, final_score_text)
        
        press_key_text = "Press any key to exit"
        win.addstr(screen_height // 2 + 2, (screen_width - len(press_key_text)) // 2, press_key_text)
        
        win.refresh()
        
        # Wait for user input
        win.nodelay(False)  # Make getch() blocking
        win.getch()  # Wait for any key press

    # Cleanup
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)