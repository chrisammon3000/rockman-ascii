import curses
import time
import random

class Rockman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = 'X'

    def move(self, dx):
        self.x += dx

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = 'o'

    def fall(self):
        self.y += 1

def draw_header(win, rocks_count, minutes, seconds, milliseconds):
    height, width = win.getmaxyx()
    header = f"Rockman | Rocks: {rocks_count} | Time: {minutes:02d}:{seconds:02d}:{milliseconds:02d}"
    
    # Draw the box
    win.addch(0, 0, curses.ACS_ULCORNER)
    win.addch(0, width - 1, curses.ACS_URCORNER)
    win.hline(0, 1, curses.ACS_HLINE, width - 2)
    win.vline(1, 0, curses.ACS_VLINE, 1)
    win.vline(1, width - 1, curses.ACS_VLINE, 1)
    
    # Draw the text
    start_x = (width - len(header)) // 2
    win.addstr(1, start_x, header)

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

    # Create rocks list
    rocks = []

    # Game loop
    frame_count = 0
    rocks_per_wave = 1
    start_time = time.time()
    while True:
        # Handle input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT and rockman.x > 1:
            rockman.move(-1)
        elif key == curses.KEY_RIGHT and rockman.x < screen_width - 2:
            rockman.move(1)

        # Update game state
        frame_count += 1

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
        if frame_count % 2 == 0:  # Make rocks fall every 2 frames
            for rock in rocks:
                rock.fall()

        # Remove rocks that have fallen off the screen
        rocks = [rock for rock in rocks if rock.y < screen_height - 1]

        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time % 1) * 100)

        # Render
        win.clear()
        
        # Draw header
        draw_header(win, len(rocks), minutes, seconds, milliseconds)
        
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

    # Cleanup
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)