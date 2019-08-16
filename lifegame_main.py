from joystick import Joystick
from ledmatrix import LedMatrix
from lifegame import LifeGame
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
            for y in range(0, LifeGameMain.HEIGHT):
                for x in range(0, LifeGameMain.WIDTH):
                    if cells[y][x]:
                        merged_cells[y][x] |= color

        return merged_cells

class Cursor:
    __INITIAL_ACTIVE_COUNT = 30

    def __init__(self, color):
        self.__color = color
        self.__coords = (0, 0)
        self.__width = LifeGameMain.WIDTH
        self.__height = LifeGameMain.HEIGHT
        self.__active_count = Cursor.__INITIAL_ACTIVE_COUNT

    def get_color(self):
        return self.__color

    def get_coords(self):
        return self.__coords

    def up(self):
        (x, y) = (self.__coords)
        y = y + 1 if y < self.__height - 1 else 0
        self.__coords = (x, y)
        self.activate()

    def down(self):
        (x, y) = (self.__coords)
        y = y - 1 if y > 0 else self.__height - 1
        self.__coords = (x, y)
        self.activate()

    def left(self):
        (x, y) = (self.__coords)
        x = x - 1 if x > 0 else self.__width - 1
        self.__coords = (x, y)
        self.activate()

    def right(self):
        (x, y) = (self.__coords)
        x = x + 1 if x < self.__width - 1 else 0
        self.__coords = (x, y)
        self.activate()

    def next(self):
        self.__active_count -= 1

    def activate(self):
        self.__active_count = Cursor.__INITIAL_ACTIVE_COUNT

    def is_visible(self):
        if self.__active_count > 0:
            return True
        else:
            return False

class LifeGameMain:
    WIDTH = 16
    HEIGHT = 16

    def __init__(self, lm, joy):
        self._layers = Layers()
        self._layers.add(LifeGame(LifeGameMain.WIDTH, LifeGameMain.HEIGHT), 1)
        self._layers.add(LifeGame(LifeGameMain.WIDTH, LifeGameMain.HEIGHT), 2)
        self._lm = lm
        self._joy = joy

        self._lm.set_fps(60)
        self._ctx = lm.getContext()

        self._cursor = Cursor(7)
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
        self._cursor.next()
        if state.up.pressed():
            self._cursor.up()
        if state.down.pressed():
            self._cursor.down()
        if state.left.pressed():
            self._cursor.left()
        if state.right.pressed():
            self._cursor.right()
        (x, y) = self._cursor.get_coords()

        if state.button1.down():
            self._cursor.activate()
            target = self._layers.selected_layer()
            if not target == None:
                status = target.flip(x, y)
                self._pause = True
        if state.button2.down():
            self._cursor.activate()
            self._layers.switch_layer()
        if state.button4.down():
            self._pause = not self._pause;

    def _draw(self):
        cells = self._layers.merge_cells()

        for y in range(0, LifeGameMain.HEIGHT):
            for x in range(0, LifeGameMain.WIDTH):
                ry = 15 - y
                if self._cursor.is_visible() and self._cursor.get_coords() == (x, ry):
                    color = self._cursor.get_color()
                else:
                    color = cells[ry][x]
                self._ctx.dot(x, ry, color)

        self._draw_text()

    def _draw_text(self):
        print(chr(27) + "[2J")

        cells = self._layers.merge_cells()

        for y in range(0, LifeGameMain.HEIGHT):
            for x in range(0, LifeGameMain.WIDTH):
                ry = 15 - y
                if self._cursor.is_visible() and self._cursor.get_coords() == (x, ry):
                    color = self._cursor.get_color()
                else:
                    color = cells[ry][x]
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

