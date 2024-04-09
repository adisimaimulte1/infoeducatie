from ev3sim.Components.BetterClasses.booleanEx import *
from ev3sim.Components.Constants.constants import *
from ev3sim.Components.background import *
from ev3sim.Components.controls import *
from ev3sim.Components.robot import *
from ev3sim.Components.fade import *
from ev3sim.Components.menu import *

import pygame
import math




class Simulator():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FLL PythFinder simulator")
        self.running = BooleanEx(True)
        self.manual_control = BooleanEx(True)

        self.constants = Constants()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.constants.screen_size.get())

        self.dt = 0

        self.background = Background(self.constants)
        self.robot = Robot(self.constants)
        self.fade = Fade(self.constants)
        self.menu = Menu(self.constants)
        self.controls = Controls()
        


    def chooseFieldCentric(self, fun: Fun, bool = None):
        self.constants.FIELD_CENTRIC.choose(fun, bool)
        self.constants.FORWARDS.set(True)
    
    def chooseDrawRobotBorder(self, fun: Fun, bool = None):
        self.constants.DRAW_ROBOT_BORDER.choose(fun, bool)
    
    def chooseUsingScreenBorder(self, fun: Fun, bool = None):
        self.constants.USE_SCREEN_BORDER.choose(fun, bool)
    
    def chooseMenuEntered(self, fun: Fun, bool = None):
        self.constants.MENU_ENTERED.choose(fun, bool)
    
    def chooseHeadSelection(self, fun: Fun, bool = None):
        self.constants.HEAD_SELECTION.choose(fun, bool)
    
    def chooseForward(self, fun: Fun, bool = None):
        self.constants.FORWARDS.choose(fun, bool)

    def chooseJoystickEnabled(self, fun: Fun, bool = None):
        self.constants.JOYSTICK_ENABLED.choose(fun, bool)


    def recalculate(self):
        if self.constants.recalculate.compare(False):
            return 0
        
        self.menu.recalculate()
        self.fade.recalculate()
        self.robot.recalculate()
        self.background.recalculate()


    def matchScreenSize(self, image: pygame.Surface, width):
        size_multiplier = self.constants.WIDTH_PERCENT / 100 * width / self.constants.screen_size.MAX_WIDTH

        return pygame.transform.scale(image, 
            (size_multiplier * image.get_width(),
            size_multiplier * image.get_height()))

    def RUNNING(self):
        return self.running.compare()



    def update(self):
        self.recalculate()
        self.__updateEventManager()

        #reset frame
        self.screen.fill(default_background_color)

        if self.manual_control.compare():
            self.__updateControls()
        self.robot.update(self.dt)

        self.background.onScreen(self.screen)
        self.robot.onScreen(self.screen)
        self.fade.onScreen(self.screen)
        if self.constants.MENU_ENTERED.compare():
            self.menu.onScreen(self.screen, self.controls)

                
            

        pygame.display.update()
        self.dt = self.clock.tick(self.constants.FPS) / 1000
    


    def __updateEventManager(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                self.controls.addJoystick(pygame.joystick.Joystick(event.device_index))
            
            elif event.type == pygame.JOYDEVICEREMOVED:
                self.controls.addJoystick(None)
            
            if event.type == pygame.KEYDOWN and self.menu.input_bool.get():
            
                if event.key == pygame.K_RETURN:
                    self.menu.input_bool.set(False)
                    self.menu.stopTextReciever()

                elif event.key == pygame.K_BACKSPACE:
                    if len(self.menu.input_text) > 1:
                        self.menu.input_text = self.menu.input_text[:-1]
                    else: self.menu.input_text = "_"
                
                else:
                    if self.menu.input_text == "_":
                        if self.menu.just_numbers.compare():
                            if self.menu.isDigit(event.key):
                                self.menu.input_text = event.unicode
                        else: self.menu.input_text = event.unicode
                    else:
                        if self.menu.just_numbers.compare():
                            if self.menu.isDigit(event.key):
                                self.menu.input_text += event.unicode
                        else: self.menu.input_text += event.unicode

            if event.type == pygame.QUIT:
                self.running.set(False)
                pygame.quit()

    def __updateControls(self):
        self.controls.update()

        if self.controls.using_joystick.compare() and self.constants.JOYSTICK_ENABLED.compare():
            self.__updateJoystick()



    def __updateJoystick(self):
        left_x = self.controls.joystick.get_axis(self.controls.keybinds.left_x)
        left_y = self.controls.joystick.get_axis(self.controls.keybinds.left_y)
        right_x = self.controls.joystick.get_axis(self.controls.keybinds.right_x)

        self.__updateJoystickButtons()

        if self.constants.FIELD_CENTRIC.compare():
            joy_x, joy_y = self.__updateJoystickFieldCentric((left_x, left_y))
        else: joy_x, joy_y = self.__updateJoystickRobotCentric((right_x, left_y))

        joy_vel = joy_y * self.robot.constrains.vel
        joy_ang_vel = joy_x * self.robot.constrains.ang_vel

        self.robot.setVelocities(joy_vel, joy_ang_vel)

    def __updateJoystickFieldCentric(self, values):    
        left_x, left_y = values
        joystick_threshold = self.controls.keybinds.threshold

        if self.constants.MENU_ENTERED.compare():
            return (0,0)

        if (abs(left_x) > joystick_threshold or abs(left_y) > joystick_threshold):
            self.robot.target_head = normalizeDegrees(math.degrees(math.atan2(left_y, left_x) + math.pi / 2))
            joy_y = math.hypot(left_y, left_x)

            if self.constants.FORWARDS.compare(False):
                joy_y = -joy_y
                self.robot.target_head = normalizeDegrees(self.robot.target_head + 180)

        else: 
            joy_y = 0
        
        error = findShortestPath(self.robot.target_head, self.robot.pose.head) / 180
        joy_x = self.robot.head_controller.calculate(error)

        if abs(joy_x) < joystick_threshold:
            joy_x = 0

        return (joy_x, joy_y)

    def __updateJoystickRobotCentric(self, values):
        right_x, left_y = values
        joystick_threshold = self.controls.keybinds.threshold

        if self.constants.MENU_ENTERED.compare():
            return (0,0)

        if abs(right_x) > joystick_threshold:
            joy_x = right_x
        else: joy_x = 0

        if abs(left_y) > joystick_threshold:
            joy_y = -left_y
        else: joy_y = 0

        return (joy_x, joy_y)

    def __updateJoystickButtons(self):
        if self.controls.joystick_detector[self.controls.keybinds.disable_button].rising:
            self.constants.MENU_ENTERED.negate()

            if self.constants.MENU_ENTERED.compare():
                self.constants.FREEZE_TRAIL.set(True)
                self.menu.reset()
            else: 
                self.constants.FREEZE_TRAIL.set(False)
        
        if self.constants.MENU_ENTERED.compare():
            return 0
        
        if self.controls.joystick_detector[self.controls.keybinds.erase_trail_button].rising:
            self.robot.trail.hide_trail.set(True)

        if self.constants.FIELD_CENTRIC.compare():
            if self.controls.joystick_detector[self.controls.keybinds.direction_button].rising:
                self.constants.FORWARDS.negate()

                if self.constants.FORWARDS.compare():  
                    self.fade.reset(self.matchScreenSize(img_forwards, self.constants.screen_size.width))
                else: self.fade.reset(self.matchScreenSize(img_backwards, self.constants.screen_size.width))


        if self.controls.joystick_detector[self.controls.keybinds.zero_button].rising:
            self.robot.setPoseEstimate(Pose(0,0,0))
        


        if self.controls.joystick_detector[self.controls.keybinds.head_selection_button].high:
            self.constants.HEAD_SELECTION.set(True)
        else: self.constants.HEAD_SELECTION.set(False)

        if self.controls.joystick_detector[self.controls.keybinds.head_selection_button].rising:
                self.fade.reset(self.matchScreenSize(img_selecting_on, self.constants.screen_size.width))
        elif self.controls.joystick_detector[self.controls.keybinds.head_selection_button].falling:
                self.fade.reset(self.matchScreenSize(img_selecting_off, self.constants.screen_size.width))

        
        if self.controls.joystick_detector[self.controls.keybinds.trail_button].rising:
            self.robot.trail.draw_trail.negate()

            if self.robot.trail.draw_trail.compare():
                self.fade.reset(self.matchScreenSize(img_show_trail, self.constants.screen_size.width))
            else: self.fade.reset(self.matchScreenSize(img_hide_trail, self.constants.screen_size.width))



        if self.constants.HEAD_SELECTION.compare():
            target = self.robot.pose.head

            if self.controls.keybinds.state is JoyType.PS4:
                if self.controls.joystick_detector[self.controls.keybinds.turn_0].rising:
                    target = 0
                elif self.controls.joystick_detector[self.controls.keybinds.turn_90].rising:
                    target = 90
                elif self.controls.joystick_detector[self.controls.keybinds.turn_180].rising:
                    target = 180
                elif self.controls.joystick_detector[self.controls.keybinds.turn_270].rising:
                    target = 270
            elif self.controls.keybinds.calculate(self.controls.joystick.get_hat(0)) != None:
                target = self.controls.keybinds.calculate(self.controls.joystick.get_hat(0))
            
            self.robot.pose.head = self.robot.target_head = target




    