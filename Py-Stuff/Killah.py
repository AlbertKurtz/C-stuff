import time
import sys
import subprocess
import random
from collections import deque
import threading


N = 10

class InputListener(threading.Thread):

    def __init__(self, buff):
        super(InputListener, self).__init__()
        self._buff = buff
        self.stop_event = threading.Event()

    def run(self):
        import termios, fcntl, sys, os
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            while self.stop_event.is_set() == False:
                try:
                    c = sys.stdin.read(1)
                    self._buff.append(c)
                except IOError: pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

        def stop(self):
            if self.isAlive() == True:
                # set event to signal thread to terminate
                self.stop_event.set()
                # block calling thread until thread really has terminated
                self.join()


class RandomListener(threading.Thread):

    def __init__(self, buff):
        super(RandomListener, self).__init__()
        self._buff = buff
        self.stop_event = threading.Event()

    def run(self):
        while self.stop_event.is_set() == False:
            time.sleep(0.2)
            c = random.choice("wasd")
            self._buff.append(c)

    def stop(self):
        if self.isAlive() == True:
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()


class agent(object):

    def __init__(self, x, y, sy, player = False):
        self.x = x
        self.y = y
        self.symb = sy
        self.player = player
        self.buff = deque()
        if not player:
            self.brain = RandomListener(self.buff)
            self.brain.start()
        else:
            self.brain = InputListener(self.buff)
            self.brain.start()


    def move(self, ch):
        if ch == 'w':
            if self.y:
                self.y -= 1
            else:
                self.y = N-1
        elif ch == 's':
            if self.y is N-1:
                self.y = 0
            else:
                self.y +=1
        elif ch == 'a':
            if self.x:
                self.x -= 1
            else:
                self.x = N-1
        elif ch == 'd':
            if self.x is N-1:
                self.x = 0
            else:
                self.x +=1



class arena(object):

    def __init__(self, n):
        self.n = n
        self._matrix = self.matrix(n)
        self._agents = []


    def __str__(self):
        return "\n".join(" ".join(row) for row in self._matrix)

    def matrix(self, n):
        return [['X'] * (n+2)] + [['X']+[' ' for _ in range(n)]+['X'] for _ in range(n)] + [['X'] * (n+2)]

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
    ARENA = arena_init(3)
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




if __name__ == "__main__":
    status = main()
    sys.exit(status)
