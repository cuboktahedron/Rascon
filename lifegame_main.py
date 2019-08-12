from joystick import Joystick
from ledmatrix import LedMatrix
from lifegame import LifeGame
import os
import pygame
import traceback

class Layer:
    def __init__(self, lifegame, color):
        self._lifegame = lifegame
        self._color = color

    def action(self):
        self._lifegame.next()

    def color(self):
        return self._color

    def get_cells(self):
        return self._lifegame.get_cells()

    def flip(self, x, y):
        status = self._lifegame.get(x, y)
        self._lifegame.set(x, y, not status)

class Layers:
    def __init__(self):
        self.layers = []
        self._selected_layer_num = -1

    def action(self):
        for layer in self.layers:
            layer.action()

    def add(self, lifegame, color):
        self.layers.append(Layer(lifegame, color));

    def selected_layer(self):
        if self._selected_layer_num < 0:
            return None
        else:
            return self.layers[self._selected_layer_num]

    def switch_layer(self):
        self._selected_layer_num = (self._selected_layer_num + 1)
        if self._selected_layer_num >= len(self.layers):
            self._selected_layer_num = -1

    def merge_cells(self):
        merged_cells = [[0 for x in range(0, LifeGameMain.WIDTH)] for y in range(0, LifeGameMain.HEIGHT)]
        for layer in self.layers:
            cells = layer.get_cells()
            color = layer.color()
            for y in range(0, LifeGameMain.WIDTH):
                for x in range(0, LifeGameMain.HEIGHT):
                    if cells[y][x]:
                        merged_cells[y][x] |= color

        return merged_cells

class LifeGameMain:
    WIDTH = 16
    HEIGHT = 16

    def __init__(self, lm, joy):
        self._layers = Layers()
        self._layers.add(LifeGame(LifeGameMain.WIDTH, LifeGameMain.HEIGHT), 1)
        self._layers.add(LifeGame(LifeGameMain.WIDTH, LifeGameMain.HEIGHT), 2)
        self._lm = lm
        self._joy = joy

        self._lm.set_fps(10)
        self._ctx = lm.getContext()

        self._cursor = (0, 0)
        self._pause = True

    def start(self):
        while True:
            self._joy.refresh()
            if not self._pause:
                self._layers.action()

            self._action()
            self._draw()
            self._lm.refresh()

    def _action(self):
        state = self._joy.state
        self._interact(state)

    def _interact(self, state):
        (x, y) = self._cursor
        if state.up.pressed():
            y = y + 1 if y < LifeGameMain.HEIGHT - 1 else 0
        if state.down.pressed():
            y = y - 1 if y > 0 else LifeGameMain.HEIGHT - 1
        if state.left.pressed():
            x = x - 1 if x > 0 else LifeGameMain.WIDTH - 1
        if state.right.pressed():
            x = x + 1 if x < LifeGameMain.WIDTH - 1 else 0
        self._cursor = (x, y)

        if state.button1.down():
            target = self._layers.selected_layer()
            if not target == None:
                status = target.flip(x, y)
                self._pause = True
        if state.button2.down():
            self._layers.switch_layer()
        if state.button4.down():
            self._pause = not self._pause;

    def _draw(self):
       print(chr(27) + "[2J")

       cells = self._layers.merge_cells()

       for y in range(0, LifeGameMain.WIDTH):
           for x in range(0, LifeGameMain.HEIGHT):
               ry = 15 - y
               if self._cursor == (x, ry):
                   color = 7
               else:
                   color = cells[ry][x]
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

