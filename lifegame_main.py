from joystick import Joystick
from ledmatrix import LedMatrix
from lifegame import LifeGame
import os
import pygame
import traceback

class LifeGameMain:
    WIDTH = 16
    HEIGHT = 16

    def __init__(self, lm, joy):
        self._lifegame = LifeGame(LifeGameMain.WIDTH, LifeGameMain.HEIGHT)
        self._lm = lm
        self._joy = joy

        self._lm.set_fps(10)
        self._ctx = lm.getContext()

        self._cursor = (0, 0)

    def start(self):
        while True:
            self._joy.refresh()
            self._lifegame.next()

            self._action()
            self._draw()
            self._lm.refresh()

    def _action(self):
        state = self._joy.state
        (x, y) = self._cursor
        if state.up:
            y = y + 1 if y < LifeGameMain.HEIGHT - 1 else 0
        elif state.down:
            y = y - 1 if y > 0 else LifeGameMain.HEIGHT - 1
        elif state.left:
            x = x - 1 if x > 0 else LifeGameMain.WIDTH - 1
        elif state.right:
            x = x + 1 if x < LifeGameMain.WIDTH - 1 else 0
        self._cursor = (x, y)

    def _draw(self):
       cells = self._lifegame.get_cells()
       print(chr(27) + "[2J")

       for y in range(0, LifeGameMain.WIDTH):
           for x in range(0, LifeGameMain.HEIGHT):
               ry = 15 - y
               if self._cursor == (x, ry):
                   color = 7
               else:
                   color = 2 if cells[ry][x] else 0
#               self._ctx.dot(x, y, color)
               print(color, end="")
           print ("")

def main():
    lm = LedMatrix()

    pygame.init()
    pygame.joystick.init()
    joy = Joystick(0)

    gameMain = LifeGameMain(lm, joy)
    try:
        gameMain.start()
    except KeyboardInterrupt:
        pass
    except:
        print(traceback.format_exc())

    if lm != None:
        lm.term()

if __name__ == '__main__':
    main()
