import pygame
import traceback
from pygame.locals import *
import time

class Joystick:
    def __init__(self, joy_no):
        self.joy = pygame.joystick.Joystick(joy_no)
        self.joy.init()
        self.state = Joystick.JoystickState()

    def refresh(self):
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.locals.JOYHATMOTION:
                x, y = ev.value
                self.state.left = x < 0
                self.state.right = x > 0
                self.state.down = y < 0
                self.state.up = y > 0
            elif ev.type == pygame.locals.JOYBUTTONUP:
                self.state.button1 = False if ev.button == 0 else self.state.button1
                self.state.button2 = False if ev.button == 1 else self.state.button2
                self.state.button3 = False if ev.button == 2 else self.state.button3
                self.state.button4 = False if ev.button == 3 else self.state.button4
            elif ev.type == pygame.locals.JOYBUTTONDOWN:
                self.state.button1 = True if ev.button == 0 else self.state.button1
                self.state.button2 = True if ev.button == 1 else self.state.button2
                self.state.button3 = True if ev.button == 2 else self.state.button3
                self.state.button4 = True if ev.button == 3 else self.state.button4

        #    self.__show_events(events)

    def __str__(self):
        return "name:{0} state:{1}".format(self.joy.get_name(), self.state)

    def __show_events(self, events):
        for ev in events:
            if ev.type == pygame.locals.ACTIVEEVENT:
                print ("type:{0} game:{1}, state:{3}".format(ev.type, ev.gain, ev.state))
            elif ev.type == pygame.locals.KEYDOWN:
                print ("type:{0} unicode:{1}, key:{2}, mod:{3}".format(ev.type, ev.unicode, ev.key, ev.mod))
            elif ev.type == pygame.locals.KEYUP:
                print ("type:{0} key:{1}, mod:{2}".format(ev.type, ev.key, ev.mod))
            elif ev.type == pygame.locals.JOYAXISMOTION:
                print ("type:{0} joy:{1}, axis:{2}, value:{3}".format(ev.type, ev.joy, ev.axis, ev.value))
            elif ev.type == pygame.locals.JOYBALLMOTION:
                print ("type:{0} joy:{1}, ball:{2}, rel:{3}".format(ev.type, ev.joy, ev.ball, ev.rel))
            elif ev.type == pygame.locals.JOYHATMOTION:
                print ("type:{0} joy:{1}, hat:{2}, value:{3}".format(ev.type, ev.joy, ev.hat, ev.value))
            elif ev.type == pygame.locals.JOYBUTTONUP:
                print ("type:{0} joy:{1}, button:{2}".format(ev.type, ev.joy, ev.button))
            elif ev.type == pygame.locals.JOYBUTTONDOWN:
                print ("type:{0} joy:{1}, button:{2}".format(ev.type, ev.joy, ev.button))

    class JoystickState:
        def __init__(self):
            self.up = False
            self.left = False
            self.right = False
            self.down = False
            self.button1 = False
            self.button2 = False
            self.button3 = False
            self.button4 = False

        def __str__(self):
            return "up:{0} left:{1} right:{2} down:{3} BTN1:{4} BTN2:{5} BTN3:{6} BTN4:{7}".format(
                T(self.up), T(self.left), T(self.right), T(self.down),
                T(self.button1), T(self.button2), T(self.button3), T(self.button4))


def main():
    pygame.init()
    pygame.joystick.init()

    joy = Joystick(0)

    while True:
        joy.refresh()
        print(joy)
        time.sleep(1 / 60)

def T(b):
    return "T" if b else "F"

if __name__ == '__main__':
    try:
        main()
    except pygame.error:
        print(traceback.format_exc())

