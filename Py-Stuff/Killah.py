import time
import sys
import subprocess
import random
from collections import deque
import threading
from utility import Singleton


N = 15


class InputListener(Singleton, threading.Thread):

    def __init__(self):
        super(InputListener, self).__init__()
        self.buff = deque(maxlen=5)
        self.stop_event = threading.Event()

    def run(self):
        import termios
        import fcntl
        import sys
        import os

        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            while not self.stop_event.is_set():
                try:
                    c = sys.stdin.read(1)
                    self.buff.append(c)
                except IOError:
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    def stop(self):
        if self.isAlive():
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()


class RandomListener(threading.Thread):

    def __init__(self):
        super(RandomListener, self).__init__()
        self.buff = deque()
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(0.1)
            c = random.choice("wasd")
            self.buff.append(c)

    def stop(self):
        if self.isAlive():
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()


class agent(object):

    def __init__(self, x, y, sy, player=False):
        self.x = x
        self.y = y
        self.symb = sy
        self.player = player
        self.last = 'w'
        if not player:
            self.brain = RandomListener()
            self.buff = self.brain.buff
            self.brain.start()
        else:
            self.brain = InputListener()
            self.buff = self.brain.buff
            self.brain.start()

    def move(self, ch=''):
        if not ch or ch not in "wasd":
            ch = self.last

        if ch == 'w':
            if self.y:
                self.y -= 1
            else:
                pass
        elif ch == 's':
            if self.y is N-1:
                pass
            else:
                self.y += 1
        elif ch == 'a':
            if self.x:
                self.x -= 1
            else:
                pass
        elif ch == 'd':
            if self.x is N-1:
                pass
            else:
                self.x += 1
        self.last = ch


class arena(object):

    def __init__(self, n):
        self.n = n
        self._matrix = self.matrix(n)
        self._agents = []

    def __str__(self):
        return "\n".join(" ".join(row) for row in self._matrix)

    def matrix(self, n):
        border = [['X'] * (n+2)]
        content = [['X']+[' ' for _ in range(n)]+['X'] for _ in range(n)]
        return border + content + border

    def add(self, agent):
        self._agents.append(agent)

    def get(self, agent):
        i = self._agents.index(agent)
        return self._agents[i]

    def update(self):
        self._matrix = self.matrix(self.n)
        for ag in self._agents:
            if not ag.player:
                if ag.buff:
                    c = ag.buff.popleft()
                    ag.move(c)
            self._matrix[ag.y+1][ag.x+1] = ag.symb
        refresh()

    def stop(self):
        for ag in self._agents:
            if ag.brain.isAlive():
                ag.brain.stop()


def clear():
    subprocess.call("clear", shell=True)


def refresh():
    for i in range(N + 5):
        sys.stdout.write("\033[A\033[2K")
    sys.stdout.flush()


def arena_init(enemies):
    ar = arena(N)
    for _ in range(enemies):
        enemy = agent(9, 9, '0')
        ar.add(enemy)
    return ar


def main():
    exit = False
    clear()
    print "\t\tEAT IT\t\t\n\n\t\tKurtz+Dodo\n\n"
    print "\n You are the W and you have to eat the X.\n Ready?\n"
    time.sleep(1)
    raw_input("press Enter")
    ARENA = arena_init(1)
    player = agent(0, 0, 'W', True)
    ARENA.add(player)
    while not exit:
        ARENA.update()
        print ARENA
        time.sleep(0.1)
        if player.buff:
            c = player.buff.popleft()
            if c == 'q':
                exit = True
            player.move(c)
        else:
            player.move()
    ARENA.stop()


if __name__ == "__main__":
    status = main()
    sys.exit(status)
