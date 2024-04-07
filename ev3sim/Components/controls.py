from ev3sim.Components.BetterClasses.edgeDetectorEx import *
from ev3sim.Components.BetterClasses.booleanEx import *
from ev3sim.Components.Constants.constants import *
from enum import Enum
import pygame

class Dpad(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class JoyType(Enum):
    PS4 = auto()
    PS5 = auto()
    XBOX = auto()

class Controls():
    def __init__(self):
        self.using_joystick = BooleanEx(False)
        self.keybinds = self.Keybinds()

        self.keyboard_len = 0
        self.joystick_len = 0

        self.joystick = None
        self.joystick_type = None

        self.keyboard_detector = self.__initKeyboardDetector()
        self.joystick_detector = self.__initJoystickDetector()

    class Keybinds():
        def __init__(self):
            self.threshold = 0
            self.left_x = 0
            self.left_y = 0
            self.right_x = 0

            self.disable_button = 0
            self.direction_button = 0
            self.zero_button = 0
            self.head_selection_button = 0
            self.trail_button = 0
            self.erase_trail_button = 0

            self.turn_0 = 0
            self.turn_45 = 0
            self.turn_90 = 0
            self.turn_135 = 0
            self.turn_180 = 0
            self.turn_225 = 0
            self.turn_270 = 0
            self.turn_315 = 0

            self.state = None
        
        def setType(self, joystick_type):
            if joystick_type == "Xbox 360 Controller":
                self.setXbox()
            elif joystick_type == "PS4 Controller":
                self.setPS4()
            elif joystick_type == "Sony Interactive Entertainment Wireless Controller":
                self.setPS5()
            else: raise Exception ("Not a supported controller")

        def setXbox(self):
            self.state = JoyType.XBOX
            self.threshold = xbox_threshold
            self.left_x = xbox_left_x
            self.left_y = xbox_left_y
            self.right_x = xbox_right_x

            self.disable_button = xbox_disable_button
            self.direction_button = xbox_direction_button
            self.zero_button = xbox_zero_button
            self.head_selection_button = xbox_head_selection_button
            self.trail_button = xbox_trail_button
            self.erase_trail_button = xbox_erase_trail_button

            self.turn_0 = xbox_turn_0
            self.turn_45 = xbox_turn_45
            self.turn_90 = xbox_turn_90
            self.turn_135 = xbox_turn_135
            self.turn_180 = xbox_turn_180
            self.turn_225 = xbox_turn_225
            self.turn_270 = xbox_turn_270
            self.turn_315 = xbox_turn_315
        
        def setPS4(self):
            self.state = JoyType.PS4
            self.threshold = ps4_threshold
            self.left_x = ps4_left_x
            self.left_y = ps4_left_y
            self.right_x = ps4_right_x

            self.disable_button = ps4_disable_button
            self.direction_button = ps4_direction_button
            self.zero_button = ps4_zero_button
            self.head_selection_button = ps4_head_selection_button
            self.trail_button = ps4_trail_button
            self.erase_trail_button = ps4_erase_trail_button

            self.turn_0 = ps4_turn_0
            self.turn_45 = ps4_turn_45
            self.turn_90 = ps4_turn_90
            self.turn_135 = ps4_turn_135
            self.turn_180 = ps4_turn_180
            self.turn_225 = ps4_turn_225
            self.turn_270 = ps4_turn_270
            self.turn_315 = ps4_turn_315
        
        def setPS5(self):
            self.state = JoyType.PS5
            self.threshold = ps5_threshold
            self.left_x = ps5_left_x
            self.left_y = ps5_left_y
            self.right_x = ps5_right_x

            self.disable_button = ps5_disable_button
            self.direction_button = ps5_direction_button
            self.zero_button = ps5_zero_button
            self.head_selection_button = ps5_head_selection_button
            self.trail_button = ps5_trail_button
            self.erase_trail_button = ps5_erase_trail_button

            self.turn_0 = ps5_turn_0
            self.turn_45 = ps5_turn_45
            self.turn_90 = ps5_turn_90
            self.turn_135 = ps5_turn_135
            self.turn_180 = ps5_turn_180
            self.turn_225 = ps5_turn_225
            self.turn_270 = ps5_turn_270
            self.turn_315 = ps5_turn_315

        def calculate(self, value):
            if self.state is JoyType.PS4:
                return None
            if value == self.turn_0:
                return 0
            if value == self.turn_45:
                return 45
            if value == self.turn_90:
                return 90
            if value == self.turn_135:
                return 135
            if value == self.turn_180:
                return 180
            if value == self.turn_225:
                return 225
            if value == self.turn_270:
                return 270
            if value == self.turn_315:
                return 315

            return None

        def getKey(self, value):
            if self.state is JoyType.PS4:
                return None
            if value == self.turn_0:
                return Dpad.UP
            if value == self.turn_90:
                return Dpad.RIGHT
            if value == self.turn_180:
                return Dpad.LEFT
            if value == self.turn_270:
                return Dpad.RIGHT

            #if you selected a combo
            return None

    
    def __initKeyboardDetector(self):
        keyboard_detector = []
        key_states = pygame.key.get_pressed()

        for key in key_states:
            keyboard_detector.append(EdgeDetectorEx())
        
        self.keyboard_len = len(key_states)
        return keyboard_detector
    
    def __initJoystickDetector(self):
        joystick_detector = []
        if exists(self.joystick):
            self.joystick_len = self.joystick.get_numbuttons()                                                                    

            for button in range(self.joystick_len):
                joystick_detector.append(EdgeDetectorEx())
        
        return joystick_detector
    
    def update(self):
        if self.using_joystick.compare():
            self.__updateJoystick()
        else: self.__updateKeyboard()
    
    def __updateKeyboard(self):
        key_states = pygame.key.get_pressed() 

        for key in range(self.keyboard_len):
            self.keyboard_detector[key].update()
            self.keyboard_detector[key].set(key_states[key])
    
    def __updateJoystick(self):
        for button in range(self.joystick_len):
            self.joystick_detector[button].update()

            if self.joystick.get_button(button) == 0:
                boolean = False
            else: boolean = True

            self.joystick_detector[button].set(boolean)
    
    def addJoystick(self, joystick):
        self.joystick = joystick
        
        if exists(joystick):
            self.using_joystick.set(True)
            self.joystick_detector = self.__initJoystickDetector()
            self.joystick_type = self.joystick.get_name()
            self.keybinds.setType(self.joystick_type)
        else: 
            self.using_joystick.set(False)
            self.joystick_type = None
