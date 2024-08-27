from pythfinder.Components.BetterClasses.edgeDetectorEx import *
from pythfinder.Components.BetterClasses.booleanEx import *
from pythfinder.Components.Constants.constants import *
from enum import Enum
import pygame

# file containing user-friendly control for both joystick and keyboard buttons,
#       which each have an afferent edge detector

# [RIGHT, LEFT, DOWN, UP]
smallest_arrow_key = 1073741903

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

        self.joystick: pygame.joystick.Joystick = None
        self.joystick_type: pygame.joystick.JoystickType = None

        self.keyboard_detector = self.__init_keyboard_detector()
        self.joystick_detector = self.__init_joystick_detector()

        self.arrows_detector = [EdgeDetectorEx() for _ in range(4)]
        self.arrows_len = 4

    # general use controls for different joysticks
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
            self.screenshot_button = 0

            self.turn_0 = 0
            self.turn_45 = 0
            self.turn_90 = 0
            self.turn_135 = 0
            self.turn_180 = 0
            self.turn_225 = 0
            self.turn_270 = 0
            self.turn_315 = 0

            self.state = None
            self.dpad_detector = None
        
        # set type based on the pygame's controller names
        def set_type(self, joystick_type):
            match joystick_type: 
                case "Xbox 360 Controller":
                    self.set_xbox()
                case "PS4 Controller":
                    self.set_ps4()
                case "Sony Interactive Entertainment Wireless Controller":
                    self.set_ps5()
                case _:
                    raise Exception ("Not a supported controller")

        def set_xbox(self):
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
            self.screenshot_button = xbox_screenshot_button

            self.turn_0 = xbox_turn_0
            self.turn_45 = xbox_turn_45
            self.turn_90 = xbox_turn_90
            self.turn_135 = xbox_turn_135
            self.turn_180 = xbox_turn_180
            self.turn_225 = xbox_turn_225
            self.turn_270 = xbox_turn_270
            self.turn_315 = xbox_turn_315

            self.dpad_detector = {
                Dpad.UP : EdgeDetectorEx(),
                Dpad.RIGHT : EdgeDetectorEx(), 
                Dpad.DOWN : EdgeDetectorEx(), 
                Dpad.LEFT : EdgeDetectorEx()
            }
        
        def set_ps4(self):
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
            self.screenshot_button = ps4_screenshot_button

            self.turn_0 = ps4_turn_0
            self.turn_45 = ps4_turn_45
            self.turn_90 = ps4_turn_90
            self.turn_135 = ps4_turn_135
            self.turn_180 = ps4_turn_180
            self.turn_225 = ps4_turn_225
            self.turn_270 = ps4_turn_270
            self.turn_315 = ps4_turn_315

            self.dpad_detector = None
        
        def set_ps5(self):
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
            self.screenshot_button = ps5_screenshot_button

            self.turn_0 = ps5_turn_0
            self.turn_45 = ps5_turn_45
            self.turn_90 = ps5_turn_90
            self.turn_135 = ps5_turn_135
            self.turn_180 = ps5_turn_180
            self.turn_225 = ps5_turn_225
            self.turn_270 = ps5_turn_270
            self.turn_315 = ps5_turn_315

            self.dpad_detector = {
                Dpad.UP : EdgeDetectorEx(),
                Dpad.RIGHT : EdgeDetectorEx(), 
                Dpad.DOWN : EdgeDetectorEx(), 
                Dpad.LEFT : EdgeDetectorEx()
            }

        def calculate(self, value: tuple):
            if self.state is JoyType.PS4:
                return None
            
            match value:
                case self.turn_0:
                    return 0
                case self.turn_45:
                    return 45
                case self.turn_90:
                    return 90
                case self.turn_135:
                    return 135
                case self.turn_180:
                    return 180
                case self.turn_225:
                    return 225
                case self.turn_270:
                    return 270
                case self.turn_315:
                    return 315
                case _:
                    return None

        # from raw values to enum
        def get_key(self, value: tuple):
            match value:
                case self.turn_0:
                    return Dpad.UP
                case self.turn_90:
                    return Dpad.RIGHT
                case self.turn_180:
                    return Dpad.DOWN
                case self.turn_270:
                    return Dpad.LEFT
                case _:
                    return None

        def update_dpad(self, value):
            if self.state is JoyType.PS4:
                return None
            
            current_key = self.get_key(value)

            for key in self.dpad_detector:
                if key is not current_key:
                    self.dpad_detector[key].set(False)
                else: self.dpad_detector[key].set(True)
                self.dpad_detector[key].update()
            
            if current_key is None:
                return None
            
            if self.dpad_detector[current_key].rising:
                return current_key
    
            return None

        @staticmethod
        def inverse(key: Dpad) -> Dpad:
            match key:
                case Dpad.UP:
                    return Dpad.DOWN
                case Dpad.RIGHT:
                    return Dpad.LEFT
                case Dpad.DOWN:
                    return Dpad.UP
                case Dpad.LEFT:
                    return Dpad.RIGHT



    def __init_keyboard_detector(self):
        keyboard_detector: List[EdgeDetectorEx] = []
        key_states = pygame.key.get_pressed()

        for _ in key_states:
            keyboard_detector.append(EdgeDetectorEx())
        
        self.keyboard_len = len(key_states)
        return keyboard_detector
    
    def __init_joystick_detector(self):
        joystick_detector: List[EdgeDetectorEx] = []
        if self.joystick is not None:
            self.joystick_len = self.joystick.get_numbuttons()                                                                    

            for _ in range(self.joystick_len):
                joystick_detector.append(EdgeDetectorEx())
        
        return joystick_detector


 
    def update(self):
        if self.using_joystick.compare():
            self.__update_joystick()

        self.__update_keyboard()
        self.__update_arrow()
    
    def __update_keyboard(self):
        key_states = pygame.key.get_pressed() 

        for key in range(self.keyboard_len):
            self.keyboard_detector[key].update()
            self.keyboard_detector[key].set(key_states[key])
    
    def __update_joystick(self):
        for button in range(self.joystick_len):
            self.joystick_detector[button].update()

            if self.joystick.get_button(button) == 0:
                boolean = False
            else: boolean = True

            self.joystick_detector[button].set(boolean)
    
    def __update_arrow(self):
        for arrow in range(self.arrows_len):
            self.arrows_detector[arrow].update()

            try:
                if arrow == self.event.key - smallest_arrow_key:
                    boolean = True
                else: boolean = False
            except: boolean = False

            self.arrows_detector[arrow].set(boolean)



    def add_joystick(self, joystick):
        self.joystick = joystick
        
        if joystick is not None:
            self.using_joystick.set(True)
            self.joystick_detector = self.__init_joystick_detector()
            self.joystick_type = self.joystick.get_name()
            self.keybinds.set_type(self.joystick_type)
        else: 
            self.using_joystick.set(False)
            self.joystick_type = None

    def add_key(self, event):
        self.event = event
    


    def get_arrow(self) -> Dpad:
        if self.arrows_detector[0].rising:
            return Dpad.RIGHT
        if self.arrows_detector[1].rising:
            return Dpad.LEFT
        if self.arrows_detector[2].rising:
            return Dpad.DOWN
        if self.arrows_detector[3].rising:
            return Dpad.UP
        
        return None