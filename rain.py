from blessed import Terminal
import time
import random
import os

try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except Exception:
    pass


SPAWN_SPEED = 40
RAIN_SPEED = 75
LIGHTNING_CHANCE = 250
LIGHTNING_TIME = 10

term = Terminal()

screen_width = 1
screen_height = 1

drops = []
lightning = 0

umbrella = None
umbrella_credit = ''


class Umbrella:
    def __init__(self, text):
        self.width = text.index('\n')
        self.text = text.replace('\n', '')
        self.height = int(len(self.text) / self.width)
        self.pos = (0, 0)
    
    def center(self):
        update_size()
        self.pos = ((screen_width - self.width) // 2 - 2, 20 - self.height)


def echo(buffer):
    if lightning > 0:
        buffer = term.black_on_white(buffer)
    print(buffer, end='', flush=True)


def load_umbrella():
    global umbrella
    global umbrella_credit

    with open('umbrella.txt') as f:
        lines = list(f)
        umbrella = Umbrella(''.join(lines[:-1]))
        umbrella.center()
        umbrella_credit = lines[-1]


def update_size():
    global screen_width
    global screen_height

    size = os.get_terminal_size()
    screen_width = size.columns
    screen_height = size.lines


def main():
    global lightning

    load_umbrella()

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            # Update internal screen size
            update_size()

            # Spawn drops
            for _ in range(SPAWN_SPEED):
                drops.append([random.randrange(screen_width), 0])
            
            # Handle lightning
            lightning -= 1
            if lightning < 0 and random.randrange(LIGHTNING_CHANCE) == 0:
                lightning = LIGHTNING_TIME

            # Create start string
            s = (' ' * screen_width) * (screen_height - 1) + '-' * screen_width

            # Draw drops
            for drop in drops:
                pos = drop[1] * screen_width + drop[0]
                if drop[1] < screen_height - 1:
                    s = s[:pos] + '|' + s[pos+1:]
                elif drop[1] == screen_height - 1:
                    s = s[:pos] + '*' + s[pos+1:]
            
            # Move and destroy drops
            for drop in drops:
                drop[1] += 1
                if drop[1] >= screen_height:
                    drops.remove(drop)
                x = umbrella.pos[0]
                y = umbrella.pos[1]
                if x <= drop[0] < x + umbrella.width and drop[1] > y + 4:
                    if drop in drops:
                        drops.remove(drop)
            
            # Print umbrella
            for x in range(umbrella.width):
                for y in range(umbrella.height):
                    string_pos = x+y*umbrella.width
                    global_pos = (umbrella.pos[1] + y) * screen_width + (umbrella.pos[0] + x)

                    if umbrella.text[string_pos] != 'X':
                        s = s[:global_pos] + umbrella.text[string_pos] + s[global_pos+1:]
            
            # Add umbrella_credit
            s = umbrella_credit + s[len(umbrella_credit):]

            # Output
            echo(term.home + term.clear + s)

            # Wait
            time.sleep(1.0 / RAIN_SPEED)
            

if __name__ == '__main__':
    main()
