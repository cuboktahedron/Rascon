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

        left = self.state.left.pressed()
        right = self.state.right.pressed()
        down = self.state.down.pressed()
        up = self.state.up.pressed()
        button1 = self.state.button1.pressed()
        button2 = self.state.button2.pressed()
        button3 = self.state.button3.pressed()
        button4 = self.state.button4.pressed()

        for ev in events:
            if ev.type == pygame.locals.JOYHATMOTION:
                x, y = ev.value
                left = x < 0
                right = x > 0
                down = y < 0
                up = y > 0
            elif ev.type == pygame.locals.JOYBUTTONUP:
                if ev.button == 0:
                    button1 = False
                if ev.button == 1:
                    button2 = False
                if ev.button == 2:
                    button3 = False
                if ev.button == 3:
                    button4 = False
            elif ev.type == pygame.locals.JOYBUTTONDOWN:
                if ev.button == 0:
                    button1 = True
                if ev.button == 1:
                    button2 = True
                if ev.button == 2:
                    button3 = True
                if ev.button == 3:
                    button4 = True

        self.state.left.refresh(left)
        self.state.right.refresh(right)
        self.state.down.refresh(down)
        self.state.up.refresh(up)
        self.state.button1.refresh(button1)
        self.state.button2.refresh(button2)
        self.state.button3.refresh(button3)
        self.state.button4.refresh(button4)

        #    self.__show_events(events)

    def __str__(self):
        return "name:{0}\n{1}".format(self.joy.get_name(), self.state)

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
            self.up = Joystick.ButtonStatus("up")
            self.left = Joystick.ButtonStatus("left")
            self.right = Joystick.ButtonStatus("right")
            self.down = Joystick.ButtonStatus("down")
            self.button1 = Joystick.ButtonStatus("BTN1")
            self.button2 = Joystick.ButtonStatus("BTN2")
            self.button3 = Joystick.ButtonStatus("BTN3")
            self.button4 = Joystick.ButtonStatus("BTN4")

        def __str__(self):
            return "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}".format(
                self.up, self.down, self.left, self.right,
                self.button1, self.button2, self.button3, self.button4)

    class ButtonStatus:
        def __init__(self, name):
            self._name = name
            self._pressed = False
            self._button_up = False
            self._button_down = False

        def refresh(self, currentState):
            if self._pressed:
                if currentState:
                    self._button_down = False
                    self._button_up = False
                else:
                    self._button_down = False
                    self._button_up = True
            else:
                if currentState:
                    self._button_down = True
                    self._button_up = False
                else:
                    self._button_down = False
                    self._button_up = False

            self._pressed = currentState

        def pressed(self):
            return self._pressed

        def down(self):
            return self._button_down

        def up(self):
            return self._button_up

        def __str__(self):
            return "{0} pressed:{1} up:{2} down:{3}".format(
                self._name, self._T(self._pressed), self._T(self._button_up), self._T(self._button_down))

        def _T(self, b):
            return "T" if b else "F"

def main():
    pygame.init()
    pygame.joystick.init()

    joy = Joystick(0)

    while True:
        joy.refresh()
        print(joy)
        time.sleep(1 / 60)

if __name__ == '__main__':
    try:
        main()
    except pygame.error:
        print(traceback.format_exc())

