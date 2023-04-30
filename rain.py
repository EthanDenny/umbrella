from blessed import Terminal
import time
import random

try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except Exception:
    pass

drops = []
lightning = 0

term = Terminal()

def echo(buffer):
    if lightning > 0:
        buffer = term.black_on_white(buffer)
    print(buffer, end='', flush=True)

def clear():
    echo(term.home + term.clear)

width = 120
height = 30
speed = 75

class Umbrella:
    def __init__(self, text):
        row_length = text[1:].index('\n')
        self.text = text.replace('\n', '') + ' '
        self.size = (row_length, int(len(self.text) / row_length))
        self.pos = ((width - self.size[0]) // 2 - 2, 20 - self.size[1])

umbrella = Umbrella("""
XXXXXXXX__.|.__XXXXXXXX
XXXX.n887.d8`qb`"-.XXXX
XX.d88' .888  q8b. `.XX
Xd8P'  .8888   .88b. \X
d88_._ d8888_.._9888 _\\
  '   '    |    '   '  
           |           
           |           
           |           
           |           
           |           
         `='           """)


def main():
    global lightning

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            # Spawn drops
            for _ in range(4):
                drops.append([random.randrange(width), 0])
            
            # Handle lightning
            lightning -= 1
            if lightning < 0 and random.randrange(250) == 0:
                lightning = 10

            # Clear screen
            clear()

            # Create start string
            s = (' ' * width) * (height - 1) + '-' * width

            # Draw drops
            for drop in drops:
                pos = drop[1] * width + drop[0]
                if drop[1] < height - 1:
                    s = s[:pos] + '|' + s[pos+1:]
                elif drop[1] == height - 1:
                    s = s[:pos] + '*' + s[pos+1:]
            
            # Move and destroy drops
            for drop in drops:
                drop[1] += 1
                if drop[1] >= height:
                    drops.remove(drop)
                x = umbrella.pos[0]
                y = umbrella.pos[1]
                if x <= drop[0] < x + umbrella.size[0] and drop[1] > y + 4:
                    drops.remove(drop)
            
            # Print umbrella
            for x in range(umbrella.size[0]):
                for y in range(umbrella.size[1]):
                    if umbrella.text[x+y*umbrella.size[0]] != 'X':
                        pos = (umbrella.pos[1] + y) * width + (umbrella.pos[0] + x)
                        s = s[:pos] + umbrella.text[x+y*umbrella.size[0]] + s[pos+1:]
            
            # Add credits
            credit = 'Umbrella by mh'
            s = credit + s[len(credit):]

            # Output
            echo(s)

            # Wait
            time.sleep(1.0 / speed)
            

if __name__ == '__main__':
    main()
