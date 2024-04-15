from ev3sim.Components.BetterClasses.edgeDetectorEx import *
from ev3sim.Components.Constants.constants import *
from ev3sim.Components.Menu.buttons import *
from ev3sim.Components.Menu.enums import *
from abc import ABC, abstractmethod
from typing import List
import pygame

class AbsMenu(ABC):
    def __init__(self, name: MenuType, constants: Constants, background: pygame.Surface | None, 
                 always_display: bool = False, overlap: bool = False):
        self.name = name
        self.ENABLED = BooleanEx(False)
        self.constants = constants

        self.overlap = overlap
        self.always_display = always_display

        self.selected = None
        self.buttons = None
        self.pressed = False

        try: self.background_rect = background.get_rect()
        except: self.background_rect = None
        finally: self.background = background
    
    def setSelected(self, selected: Selected):
        self.selected = selected
    
    def setButtons(self, buttons: List[AbsButton]):
        self.buttons = buttons
    
    def setPressed(self, value: bool):
        self.pressed = value
    
    def backgroundCenter(self, center: tuple):
        self.background_rect.center = center




    def update(self, selected: Selected, clicked: bool, value = None):
        for button in self.buttons:
            button.update(selected, clicked, value)

    def updateSelections(self, direction: Dpad | None) -> Selected:
        FINAL = None

        for button in self.buttons:
            move_to = button.move(direction)
            
            try: 
                next = button.getNext()
                if not next == None:
                    FINAL = next
            except: pass

            if not move_to == None:
                FINAL = move_to

        return FINAL

    def getToggles(self):
        list = []
        for button in self.buttons:
            try: list.append(button.on())
            except: pass
        
        return list

    def resetToggles(self):
        for button in self.buttons:
            try: button.reset()
            except: pass

    def move(self, direction: Dpad | None):
        for button in self.buttons:
            next = button.move(direction)
            if not next == None:
                return next
        return None

    def getNext(self):
        for button in self.buttons:
            try: 
                next = button.getNext()
                if not next == None:
                    return next
            except: pass
        return None



    def onScreen(self, screen: pygame.Surface):
        if self.ENABLED.compare(False) and not self.always_display:
            return 0
        
        try: screen.blit(self.background, self.background_rect)
        except: pass

        for button in self.buttons:
            button.display(screen)
    

class Submenu(AbsMenu):
    def __init__(self, name: MenuType, constants: Constants, background: pygame.Surface | None, 
                 always_display: bool = False, overlap: bool = False):
        super().__init__(name, constants, background, always_display, overlap)