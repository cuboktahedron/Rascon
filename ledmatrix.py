from datetime import datetime
import RPi.GPIO as GPIO
import time

delay = 1 / 500

class LedMatrix:
    DEFAULT_FPS = 10

    RED1_PORT = 17
    GREEN1_PORT = 18
    BLUE1_PORT = 22
    RED2_PORT = 23
    GREEN2_PORT = 24
    BLUE2_PORT = 25
    CLOCK_PORT = 3
    A_PORT = 7
    B_PORT = 8
    C_PORT = 9
    LATCH_PORT = 4
    OE_PORT = 2

    LPS = 32

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LedMatrix.RED1_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.GREEN1_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.BLUE1_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.RED2_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.GREEN2_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.BLUE2_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.CLOCK_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.A_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.B_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.C_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.LATCH_PORT, GPIO.OUT)
        GPIO.setup(LedMatrix.OE_PORT, GPIO.OUT)

        self.context = LedMatrixContext()
        self.fps = LedMatrix.DEFAULT_FPS

    def getContext(self):
        return self.context

    def set_fps(self, fps):
        self.fps = fps

    def __clock(self):
        GPIO.output(LedMatrix.CLOCK_PORT, 1)
        GPIO.output(LedMatrix.CLOCK_PORT, 0)

    def __latch(self):
        GPIO.output(LedMatrix.LATCH_PORT, 1)
        GPIO.output(LedMatrix.LATCH_PORT, 0)

    def term(self):
        GPIO.cleanup()

    def select_section(self, no):
        a_bit = (no & 1) >> 0
        b_bit = (no & 2) >> 1
        GPIO.output(LedMatrix.A_PORT, a_bit)
        GPIO.output(LedMatrix.B_PORT, b_bit)

    def __set_color1(self, color):
        red = (color & 1) >> 0
        green = (color & 2) >> 1
        blue = (color & 4) >> 2
        GPIO.output(LedMatrix.RED1_PORT, red)
        GPIO.output(LedMatrix.GREEN1_PORT, green)
        GPIO.output(LedMatrix.BLUE1_PORT, blue)

    def __set_color2(self, color):
        red = (color & 1) >> 0
        green = (color & 2) >> 1
        blue = (color & 4) >> 2
        GPIO.output(LedMatrix.RED2_PORT, red)
        GPIO.output(LedMatrix.GREEN2_PORT, green)
        GPIO.output(LedMatrix.BLUE2_PORT, blue)

    def refresh(self):
        next_ts = datetime.now().timestamp() + (1 / self.fps)
        cur_ts = datetime.now().timestamp()
        while cur_ts <= next_ts:
            cur_ts = datetime.now().timestamp()
            self.__refresh()

        next_ts = cur_ts + (1 / self.fps)

    def __refresh(self):
        for section in range(4):
            self.select_section(section)
            GPIO.output(LedMatrix.OE_PORT, 1)

        for i in range(8):
            self.__set_color1(self.context.screen[section][i + 8])
            self.__set_color2(self.context.screen[section + 8][i + 8])
            self.__clock()

        for i in range(8):
            self.__set_color1(self.context.screen[section + 4][15 - i])
            self.__set_color2(self.context.screen[section + 12][15 - i])
            self.__clock()

        for i in range(8):
            self.__set_color1(self.context.screen[section][i])
            self.__set_color2(self.context.screen[section + 8][i])
            self.__clock()

        for i in range(8):
            self.__set_color1(self.context.screen[section + 4][7 - i])
            self.__set_color2(self.context.screen[section + 12][7 - i])
            self.__clock()

        self.__latch()
        GPIO.output(LedMatrix.OE_PORT, 0)
        time.sleep(delay)

class LedMatrixContext:
    SIZE = 16

    def __init__(self):
        self.screen = [[0 for x in range(LedMatrixContext.SIZE)] for x in range(LedMatrixContext.SIZE)]

    def clear(self):
        self.fill_rect(0, 0, LedMatrixContext.SIZE, LedMatrixContext.SIZE, 0)

    def dot(self, x, y, color):
        self.screen[y][x] = color

    def rect(self, x1, y1, x2, y2, color):
        for x in range(x1, x2):
            for y in range(y1, y2):
                if x == x1 or x == x2 - 1 or y == y1 or y == y2 - 1:
                    self.screen[y][x] = color

    def fill_rect(self, x1, y1, x2, y2, color):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self.screen[y][x] = color

    def circle(self, px, py, pr, color):
        x1 = px - pr
        x2 = px + pr
        y1 = py - pr
        y2 = py + pr
        x1 = 0 if x1 < 0 else x1
        x2 = LedMatrixContext.SIZE if x2 >= LedMatrixContext.SIZE else x2
        y1 = 0 if y1 < 0 else y1
        y2 = LedMatrixContext.SIZE if y2 >= LedMatrixContext.SIZE else y2

        rr = pr * pr
        for x in range(x1, x2):
            xx1 = (x - px) * (x - px)
            xx2 = ((x + 1) - px) * ((x + 1) - px)
            for y in range(y1, y2):
                yy1 = (y - py) * (y - py)
                yy2 = ((y + 1) - py) * ((y + 1) - py)

                zs = [xx1 + yy1, xx1 + yy2, xx2 + yy1, xx2 + yy2]
                inner_point_num = len(list(filter((lambda z: z < rr), zs)))

                if 2 <= inner_point_num <= 3:
                    self.screen[y][x] = color

    def fill_circle(self, px, py, pr, color):
        x1 = px - pr
        x2 = px + pr
        y1 = py - pr
        y2 = py + pr
        x1 = 0 if x1 < 0 else x1
        x2 = LedMatrixContext.SIZE if x2 >= LedMatrixContext.SIZE else x2
        y1 = 0 if y1 < 0 else y1
        y2 = LedMatrixContext.SIZE if y2 >= LedMatrixContext.SIZE else y2

        rr = pr * pr
        for x in range(x1, x2):
            xx1 = (x - px) * (x - px)
            xx2 = ((x + 1) - px) * ((x + 1) - px)
            for y in range(y1, y2):
                yy1 = (y - py) * (y - py)
                yy2 = ((y + 1) - py) * ((y + 1) - py)

                zs = [xx1 + yy1, xx1 + yy2, xx2 + yy1, xx2 + yy2]
                inner_point_num = len(list(filter((lambda z: z <= rr), zs)))

                if inner_point_num >= 2:
                    self.screen[y][x] = color

    def show_screen(self):
        for y in range(0, LedMatrixContext.SIZE):
            for x in range(0, LedMatrixContext.SIZE):
                print (self.screen[(LedMatrixContext.SIZE - 1) - y][x], end = "")
            print ("")

if __name__ == '__main__':
    try:
        lm = LedMatrix()
        lm.set_fps(10)
        ctx = lm.getContext()
        notDone = True
        sign = 1
        color = 1
        i = 0
        while notDone:
            i = i + sign
            if i == 0:
                sign = -sign
                color = color + 1
            elif i == 8:
                sign = -sign
                ctx.clear()
                ctx.fill_circle(8, 8, i, color)

                lm.refresh()

    except KeyboardInterrupt:
        pass

    lm.term()

