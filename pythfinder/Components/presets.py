from pythfinder.Components.BetterClasses.edgeDetectorEx import *
from pythfinder.Components.Constants.constants import *


# file containing the Preset class


class Preset():
    def __init__(self, 
                 name: str,
                 constants: Constants,
                 preset_constants: Constants,
                 image: None | pygame.Surface = None,
                 image_size: None | Size = None):
        
        self.name = name
        
        self.constants = constants
        self.ON = EdgeDetectorEx()

        self.original_constants = constants.copy() # deep copy
        self.preset_constants = preset_constants

        self.img = self.original = image
        self.img_size_cm: ScreenSize = image_size
        self.img_size_px: ScreenSize = None
        self.rectangle = None

        self.recalculate()
    
    def setImage(self,
                 image: None | pygame.Surface = None,
                 image_size: None | Size = None):
        
        if image is not None:
            self.img = image
        if image_size is not None:
            self.img_size_cm = image_size

    def recalculate(self):
        try:
            self.getImgSizeInPixels()

            self.img = pygame.transform.scale(self.original, 
                                              self.img_size_px.get())
            
            self.rectangle = self.img.get_rect()
            self.rectangle.center = (self.constants.screen_size.getHalf()) 
        except:
            pass # no image found
    
    def getImgSizeInPixels(self):
        self.img_size_px = Size(
                    self.constants.cmToPixels(self.img_size_cm.width),
                    self.constants.cmToPixels(self.img_size_cm.height)
        )


    def onScreen(self, screen: pygame.Surface):
        self.ON.update()

        if self.ON.high:
            try:
                screen.blit(self.img, self.rectangle)
            except: 
                pass # no image found
        
        elif self.ON.rising:
            self.constants.check(self.preset_constants)
    
    def off(self):
        self.constants.check(self.original_constants)
        

class PresetManager():
    def __init__(self, constants: Constants):
        self.presets: List[Preset] = [None for _ in range(10)]

        self.value = None
        self.previous = -1
        self.WRITING = EdgeDetectorEx()

        self.constants = constants
    
    def add(self, preset: Preset, key: None | int = None):
        if key is None:
            hasSpace = False

            for i in range(len(self.presets)):
                if self.presets[i] is None:

                    self.presets[i] = preset
                    hasSpace = True
                    break
            
            if not hasSpace:
                print("\n\n you've reached the presets limit")
            return self
            
        if isinstance(key, int):
            if key > 0 and key < 10:

                if self.presets[key - 1] is not None:
                    print("\n\nyou already had a preset on key {0}".format(key))
                    print("I deleted it for you, no worries, but maybe you wanted that preset 🤷🏻‍♂️")

                self.presets[key - 1] = preset 
                return self
                
        print("\n\nnot a valid key")

        return self
    
    def recalculate(self):
        for preset in self.presets:
            if preset is not None:
                preset.recalculate()
    
    def addKey(self, key):
        self.value = key
    
    def on(self, number: int):
        if self.presets[number - 1] is None and not number == 0:
            print("no preset for key {0}".format(number))
            return None

        for i in range(len(self.presets)):
            if self.presets[i] is None: 
                continue
            
            if i + 1 == number:
                self.presets[i].ON.set(True)
            else: self.presets[i].ON.set(False)

            if i + 1 == self.previous and not number == self.previous:
                self.presets[i].off()
        
        self.previous = number

    

    def onScreen(self, screen: pygame.Surface):
        self.WRITING.update()

        for preset in self.presets:
            if preset is not None:
                preset.onScreen(screen)

        if self.value is None or not self.WRITING.high:
                return None
        on = None


        match self.value.key:
            case pygame.K_1:
                on = 1
            case pygame.K_2:
                on = 2
            case pygame.K_3:
                on = 3
            case pygame.K_4:
                on = 4
            case pygame.K_5:
                on = 5
            case pygame.K_6:
                on = 6
            case pygame.K_7:
                on = 7
            case pygame.K_8:
                on = 8
            case pygame.K_9:
                on = 9
            case pygame.K_0:
                on = 0 # reset key

        if on is None:
            return None

        self.on(on)
            
    def get(self, number: int) -> Preset:
        if not inOpenInterval(number, 0, 9):
            return None
        return self.presets[number - 1]
