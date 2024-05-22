from pythfinder.Components.BetterClasses.edgeDetectorEx import *
from pythfinder.Components.Constants.constants import *
from pythfinder.Components.Menu.enums import *
from pythfinder.Components.controls import *
from abc import ABC, abstractmethod

from typing import List
import pygame

# file used for managing menu button-logic
#
# contains:
#       - abstract class to be inherited when creating a different button type.
#            Moving through the buttons is done with a dictionary, which 'links'
#            every possible direction (UP, DOWN, LEFT, RIGHT) with another button.
#            
#            Other feature is the remembrance. This is another dictionary for all 4
#            directions, which 'remembers' the button which you came from last time.
#            It's basically an inverse link, but if there are more buttons linked to
#            the current button from that direction, it remembers the last one
#            selected. JUST if you came from that button.
#
#            Links for different states are also used with toggle buttons. These enable
#            different connections when ON/OFF. These are the first crietrion looked 
#            when moving from a button to another.
#            
#            Remembrance is second to be looked, then it's the normal links. If none of
#            these exist, you do nothing trying to move in that direction.
# 
#       - empty button: used only for moving through buttons. Can't be pressed
#                       but can be selected
#       - dynamic button: used for faster moving through buttons. When clicked, they
#                         automatically select other button
#       - toggle button: used for ON/OFF menu applications. Supports different
#                        links for each state
#       - input button: it's a modified toggle button. It gets input from the
#                       keyboard. It supports: cms, percents, colors, paths and
#                       fonts, tho not all are implemented
#       - bool button: maybe the most simple button, is the base of the toggle
#                      button. Just sets constants ON/OFF, doesn't have any 
#                      impact on the interface appearance.


#CONVENTION: surface list goes from smaller -> larger value (ex: FALSE -> TRUE )
class AbsButton(ABC):
    def __init__(self, 
                 name: Selected,
                 quadrant_surface: pygame.Surface | None, 
                 title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 selected_title_surface: List[pygame.Surface] | pygame.Surface | None,
                 value = None, 
                 size: int | None = None, 
                 font = default_system_font) -> None:
        
        self.name = name
        self.selected = None
        self.index = 0

        self.remember_other = None

        try: self.font = pygame.font.SysFont(font, size)
        except: self.font = None

        try: self.display_quadrant = quadrant_surface[self.index]
        except: self.display_quadrant = quadrant_surface

        try: self.display_title = title_surface[self.index]
        except: self.display_title = title_surface

        try: self.original = value.get()
        except: self.original = value

        self.raw_value = value

        try: self.display_value = self.font.render(str(value), True, default_text_color)
        except: self.display_value = None

        try: self.display_quadrant_rect = self.display_quadrant.get_rect()
        except: self.display_quadrant_rect = None

        try: self.display_title_rect = self.display_title.get_rect()
        except: self.display_title_rect = None

        try: self.display_value_rect = self.display_value.get_rect()
        except: self.display_value_rect = None

        self.title = title_surface
        self.quadrant = quadrant_surface
        self.selected_title = selected_title_surface

        self.quadrant_center = None
        self.title_center = None
        self.value_center = None

        self.SELECTED = EdgeDetectorEx()
        self.type = self.getType()

        self.next = None

        self.links = {
            Dpad.UP: None,
            Dpad.RIGHT: None,
            Dpad.DOWN: None,
            Dpad.LEFT: None
        }
        self.remember_links = {
            Dpad.UP: [False, None],
            Dpad.RIGHT: [False, None],
            Dpad.DOWN: [False, None],
            Dpad.LEFT: [False, None]
        }



    #resets button to the default value
    @abstractmethod
    def default(self, default: bool):
        ...

    #checks if the current button display is matching the value it stores
    @abstractmethod
    def check(self):
        ...

    # gets the value stored by the button
    def getType(self) -> ButtonType:
        if isinstance(self.raw_value, (int, float)):
            return ButtonType.INT
        if isinstance(self.raw_value, (bool, BooleanEx)):
            return ButtonType.BOOL
        if isinstance(self.raw_value, str):
            return ButtonType.STRING
        return ButtonType.UNDEFINED

    # links directions to other buttons
    def link(self, 
             key: Dpad | List[Dpad], 
             value: Selected | List[Selected], 
             next: Selected | None = None):
        try:
            if len(key) == len(value):
                for each in range(len(key)):
                    self.links[key[each]] = value[each]
        except: self.links[key] = value

        if isinstance(next, Selected):
            self.next = next
    
    # remembers the button who led to the current button, pressing an arbitrary key
    #
    # default value to remember is needed, as it's how it knows to remember for that specific key
    def remember(self, 
                 key: Dpad | List[Dpad], 
                 value: Selected | List[Selected]):
        
        if isinstance(key, Dpad):
            if value is None:
                self.remember_links[key][0] = False
            else: self.remember_links[key][0] = True

            self.remember_links[key][1] = value
            return None
        
        if len(key) == len(value):
            for each in range(len(key)):

                if value[each] is None:
                    self.remember_links[key[each]][0] = False
                else: self.remember_links[key[each]][0] = True

                self.remember_links[key[each]][1] = value[each]
        

    # remembers the the same buttons as the other button
    # 
    # helps chaining remember relationships
    def rememberAsButton(self, other):
        if isinstance(other, AbsButton):
            self.remember_other = other

    def quadrantCenter(self, center: tuple):
        try: self.display_quadrant_rect.center = center
        except: pass
        finally: self.quadrant_center = center

    def titleCenter(self, center: tuple):
        try: self.display_title_rect.center = center
        except: pass
        finally: self.title_center = center
    
    def valueCenter(self, center: tuple):
        try: self.display_value_rect.center = center
        except: pass
        finally: self.value_center = center

    @abstractmethod
    def change(self):
        ...
    
    @abstractmethod
    def update(self, selected: Selected, clicked: bool, value = None):
        self.selected = selected
        ...
    
    def move(self, direction: Dpad | None) -> Selected:
        if self.selected is self.name:  # if this button is selected
            try: 
                if self.on()[1]:  # only for toggle buttons
                    return self.toggle_links[direction]  # other links when toggle is on
                raise Exception("wise words here")  # handle usual links when toggle is off
            except:
                try:
                    if self.remember_other is not None:  # remembrance has priority
                        if self.remember_other.remember_links[direction][0]:
                            return self.remember_other.remember_links[direction][1]
                    elif self.remember_links[direction][0]: # if there is nothing to remember, use the default link
                        return self.remember_links[direction][1]
                
                    return self.links[direction]
                except: pass
        return None
    
    def display(self, screen: pygame.Surface):    
        try: screen.blit(self.display_quadrant, self.display_quadrant_rect) 
        except: pass

        try: screen.blit(self.display_title, self.display_title_rect)
        except: pass

        try: screen.blit(self.display_value, self.display_value_rect)
        except: pass



class EmptyButton(AbsButton):
    def __init__(self, 
                 name: Selected, 
                 quadrant_surface: pygame.Surface | None, 
                 title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 selected_title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 value = None, 
                 size = None, 
                 font = default_system_font) -> None:
        super().__init__(name, quadrant_surface, title_surface, selected_title_surface, value, size, font)
    
    def default(self, default: bool):
        if not default:
            return 0

    def change(self):
        ...
    
    def check(self):
        return None
    
    def update(self, selected, clicked: bool, value = None):
        super().update(selected, clicked, value)

        if selected is self.name:
            self.SELECTED.set(True)
        else: self.SELECTED.set(False)

        self.SELECTED.update()

        if self.SELECTED.rising:
            self.display_title = self.selected_title
        elif self.SELECTED.falling:
            self.display_title = self.title

class DynamicButton(AbsButton):
    def __init__(self, 
                 name: Selected, 
                 quadrant_surface: pygame.Surface | None, 
                 title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 selected_title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 value = None, 
                 size = None, 
                 font = default_system_font) -> None:
        super().__init__(name, quadrant_surface, title_surface, selected_title_surface, value, size, font)

        self.go_next = False
    
    def default(self, default: bool):
        if not default:
            return 0
        ...
    
    def getNext(self) -> Selected:
        if self.go_next:
            self.go_next = False
            return self.next
        return None
    
    def change(self):
        self.go_next = True
    
    def check(self):
        return None

    def update(self, selected: Selected, clicked: bool, value = None):
        super().update(selected, clicked, value)

        if selected is self.name:
            if clicked:
                self.change()
            self.SELECTED.set(True)
        else: self.SELECTED.set(False)

        self.SELECTED.update()

        if self.SELECTED.rising:
            self.display_title = self.selected_title
        if self.SELECTED.falling:
            self.display_title = self.title

class ToggleButton(AbsButton):
    def __init__(self, 
                 name: Selected, 
                 quadrant_surface: pygame.Surface | None, 
                 title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 selected_title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 toggle, 
                 value = None, 
                 size = None, 
                 font = default_system_font) -> None:
        super().__init__(name, quadrant_surface, title_surface, selected_title_surface, value, size, font)

        self.toggle = toggle
        self.ON = BooleanEx(False)
        self.toggle_links = {
            Dpad.UP: None,
            Dpad.RIGHT: None,
            Dpad.DOWN: None,
            Dpad.LEFT: None
        }
        if not isinstance(self.toggle, MenuType):
            raise Exception("please select a MenuType")


    def change(self):
        self.ON.negate()
    
    def linkToggle(self, key: Dpad | List[Dpad], value: Selected | List[Selected]):
        try:
            if len(key) == len(value):
                for each in range(len(key)):
                    self.toggle_links[key[each]] = value[each]
        except: self.toggle_links[key] = value

    def default(self, default: bool):
        if not default:
            return 0
    
    def on(self):
        return (self.toggle, self.ON.get())
    
    def reset(self):
        self.ON.set(False)
    
    def check(self):
        ...

    def update(self, selected: Selected, clicked: bool, value=None):
        super().update(selected, clicked, value)

        if selected is self.name:
            if clicked:
                self.change()
            self.SELECTED.set(True)
        else: self.SELECTED.set(False)

        self.SELECTED.update()

        if self.SELECTED.rising:
            self.display_title = self.selected_title
        if self.SELECTED.falling:
            self.display_title = self.title

class InputButton(AbsButton):
    def __init__(self, 
                 name: Selected, 
                 quadrant_surface: pygame.Surface | None, 
                 title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 selected_title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 constants: Constants,
                 value = None, 
                 size = None, 
                 font = default_system_font,
                 limit: int = math.inf) -> None:
        super().__init__(name, quadrant_surface, title_surface, selected_title_surface, value, size, font)

        self.WRITING = EdgeDetectorEx()
        self.write = BooleanEx(False)
        self.constants = constants

        self.type = None
        self.dimension = None
        self.selected = None
        self.original_value = None
        self.input = '_'
        self.limit = limit
    
    def setInputType(self, type: InputType, dimension: tuple | int):
        self.type = type
        self.dimension = dimension

        if self.type is InputType.PERCENT:
            self.raw_value *= 100
            self.original *= 100

        self.displayValue(self.raw_value)
    
    def isDigit(self, value):
        return (value == pygame.K_0 or 
                value == pygame.K_1 or
                value == pygame.K_2 or
                value == pygame.K_3 or
                value == pygame.K_4 or 
                value == pygame.K_5 or
                value == pygame.K_6 or
                value == pygame.K_7 or
                value == pygame.K_8 or 
                value == pygame.K_9)

    def default(self, default: bool):
        if not default or not self.selected is self.name or self.write.get():
            return 0

        self.input = self.original
        self.change()
    
    def inRange(self, value):
        try: return self.dimension[0] < value and value < self.dimension[1]
        except: pass

    def displayValue(self, value):
        if isinstance(self.type.value, str):
            suffix = self.type.value
        else: suffix = ''

        if len(str(value)) > self.limit:
            self.display_value = self.font.render('...' + str(value)[-self.limit:] + suffix, True, default_text_color)
        else: self.display_value = self.font.render(str(value) + suffix, True, default_text_color)

        self.display_value_rect = self.display_value.get_rect()
        try: self.display_value_rect.center = self.value_center
        except: pass

    def change(self):

        if self.write.get():
            self.input = '_'
            self.displayValue(self.input)
            return 0

        if self.input == '_':
            self.displayValue(self.raw_value)
            return 0
    
        match self.type:
            case InputType.DIMENSION:
                try:
                    self.raw_value = int(self.input)
                    setattr(self.constants, self.name.name, self.raw_value)
                except: pass
            case InputType.PERCENT:
                try:
                    self.raw_value = int(self.input)
                    setattr(self.constants, self.name.name, self.raw_value / 100)
                except: pass
            case InputType.FONT:
                ...
            case InputType.COLOR:
                ...
            case InputType.IMAGE_PATH:
                try: 
                    pygame.image.load(self.input)
                    self.raw_value = self.input
                    setattr(self.constants, self.name.name, self.raw_value)
                except: pass
        
        self.check()
    
    def check(self):
        if not self.original_value == getattr(self.constants, self.name.name):
            self.original_value = getattr(self.constants, self.name.name)
            self.constants.recalculate.set(True)
            
        self.displayValue(self.raw_value)

    
    def update(self, selected: Selected, clicked: bool, value = None):
        if not isinstance(self.type, InputType):
            raise Exception("please initialize {0}'s input type".format(self.name))
        super().update(selected, clicked, value)
        self.selected = selected
        
        if selected is self.name:
            if clicked:
                self.write.negate()
                self.change()
            self.SELECTED.set(True)
        else: self.SELECTED.set(False)
            

        self.WRITING.set(self.write.get())

        self.WRITING.update()
        self.SELECTED.update()

        if self.SELECTED.rising:
            self.display_title = self.selected_title
        elif self.SELECTED.falling:
            self.write.set(False)
            self.change()
            self.display_title = self.title
        
        if self.WRITING.high and value is not None:
            match value.key:
                case pygame.K_RETURN:
                    self.write.set(False)
                    self.change()
                case pygame.K_BACKSPACE:
                    if len(self.input) > 1:
                        self.input = self.input[:-1]
                    else: self.input = '_'
                    self.displayValue(self.input)
                case _:
                    key_val = value.unicode

                    if self.input == '_':
                        match self.type:
                            case InputType.DIMENSION:
                                try: 
                                    if self.isDigit(value.key):
                                        if self.inRange(int(key_val)):
                                            self.input = key_val
                                except: pass
                            case InputType.PERCENT:
                                if self.isDigit(value.key):
                                    if self.inRange(int(key_val)):
                                        self.input = key_val
                            case InputType.FONT:
                                ...
                            case InputType.COLOR:
                                ...
                            case InputType.IMAGE_PATH:
                                self.input = key_val
                    else: 
                        match self.type:
                            case InputType.DIMENSION:
                                try:
                                    if self.isDigit(value.key):
                                        if self.inRange(int(self.input + key_val)):
                                            self.input += key_val
                                except: pass
                            case InputType.PERCENT:
                                if self.isDigit(value.key):
                                    if self.inRange(int(self.input + key_val)):
                                        self.input += key_val
                            case InputType.FONT:
                                ...
                            case InputType.COLOR:
                                ...
                            case InputType.IMAGE_PATH:
                                if len(self.input) + 1 <= self.dimension:
                                    self.input += key_val

                    self.displayValue(self.input)

class BoolButton(AbsButton):
    def __init__(self, 
                 name: Selected, quadrant_surface: pygame.Surface | None, 
                 title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 selected_title_surface: List[pygame.Surface] | pygame.Surface | None, 
                 value = None, 
                 size = None, 
                 font = default_system_font) -> None:
        super().__init__(name, quadrant_surface, title_surface, selected_title_surface, value, size, font)
        self.selected = None
        self.getIndex()
    
    def getIndex(self):
        try: 
            if self.raw_value.compare():
                self.index = 1
            else: self.index = 0
        except:
            if self.raw_value:
                self.index = 1
            else: self.index = 0
        finally:
            if self.selected is self.name:
                self.display_title = self.selected_title[self.index]
            else: self.display_title = self.title[self.index]

    def default(self, default: bool):
        if not default or not self.selected is self.name:
            return 0

        try:
            self.raw_value.set(self.original)
        except: self.raw_value = self.original
        finally: self.getIndex()

    def change(self): 
        try:
            self.raw_value.negate()
        except: self.raw_value = not self.raw_value
        finally:
            self.check()
    
    def check(self):
        try:
            if self.raw_value.compare():
                self.index = 1
            else: self.index = 0
        except:
            if self.raw_value:
                self.index = 1
            else: self.index = 0
        finally:
            if self.SELECTED.rising or self.SELECTED.high:
                self.display_title = self.selected_title[self.index]
            else: self.display_title = self.title[self.index]

    def update(self, selected, clicked: bool, value = None):
        super().update(selected, clicked, value)
        self.selected = selected

        if selected is self.name:
            if clicked:
                self.change()
            self.SELECTED.set(True)
        else: self.SELECTED.set(False)

        self.SELECTED.update()

        if self.SELECTED.rising:
            self.display_title = self.selected_title[self.index]
        elif self.SELECTED.falling:
            self.display_title = self.title[self.index]
