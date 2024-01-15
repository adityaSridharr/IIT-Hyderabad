from time import sleep
from random import randint, choice
import curses
from curses import wrapper
from threading import Thread


class MainWindow:

    def __init__(self) -> None:
        l = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(48, 58)]
        self.characters = "".join(l) + "`~!@#$%^&*()_+[]{}\\|'\";:,<.>/?"

        self.stripes = []
        self.height = self.width = 0

    def start(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        Thread(target=self.add_stripes).start()
        
        try: 
            while True:
                for i in self.stripes:
                    i.next()
                    stdscr.refresh()
                sleep(0.05)
                if (self.height, self.width) != stdscr.getmaxyx():
                    self.height, self.width = stdscr.getmaxyx()
                    stdscr.clear()
                    self.stripes.clear()
                    Thread(target=self.add_stripes).start()
        except KeyboardInterrupt:
                pass

    def add_stripes(self):
        l = [i for i in range(self.width) if i%2==0]
        for i in range(len(l)):
            x = choice(l)
            self.stripes.append(Stripe(x, self.stdscr, self.characters))
            l.remove(x)
            sleep(0.05)


class Line:

    def __init__(self, x, height, parent, stdscr: curses.window) -> None:
        self.x = x
        self.height = height
        self.parent = parent
        self.stdscr = stdscr

        self.length = randint(int(height/5), int(height*2/3))
        self.space = randint(int(height/6), int(height/2))
        self.current = 0

    def next(self):

        if 0 < self.current < self.height+1:
            try:
                self.stdscr.addstr(self.current-1, self.x, chr(self.stdscr.inch(self.current-1, self.x) & curses.A_CHARTEXT), curses.color_pair(1))
            except curses.error as e:
                with open("log.txt", "a") as f:
                    f.write(f"{self.current} {self.length}  {self.x} {self.stdscr.getmaxyx()} {67}\n")

        if 0 <= self.current < self.height:
            try:
                self.stdscr.addstr(self.current, self.x, choice(self.parent.characters), curses.A_BOLD)
            except curses.error as e:
                with open("log.txt", "a") as f:
                    f.write(f"{self.current} {self.length} {self.x} {self.stdscr.getmaxyx()} {75}\n")

        if self.height > self.current - self.length >=0:
            try:
                self.stdscr.addstr(self.current-self.length, self.x, " ")
            except curses.error as e:
                with open("log.txt", "a") as f:
                    f.write(f"{self.current} {self.length} {self.x} {self.stdscr.getmaxyx()} {83}\n")

        if self.current - self.length - self.space >= self.height - 1:
            self.parent.lines.remove(self)

        if self.current - self.length - self.space == 0:
            self.parent.new_line()

        self.current += 1


class Stripe:

    def __init__(self, x, stdscr: curses.window, characters = None, **kwargs):

        self.height = stdscr.getmaxyx()[0]
        self.stdscr = stdscr
        self.x = x

        if characters is None:
            l = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(48, 58)]
            self.characters = "".join(l) + "`~!@#$%^&*()_+[]{}\\|'\";:,<.>/?"
        else:
            self.characters = characters

        self.lines = [Line(self.x, self.height, self, self.stdscr)]

    def new_line(self):
        self.lines.append(Line(self.x, self.height, self, self.stdscr))

    def next(self):
        for line in self.lines:
            line.next()


if __name__ == "__main__":
    wrapper(MainWindow().start)
