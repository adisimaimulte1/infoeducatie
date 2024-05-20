from pythfinder.Components.Controllers.PIDCoefficients import *
from pythfinder.Components.BetterClasses.booleanEx import *
from pythfinder.Components.Constants.screenSize import *
from pythfinder.Components.Constants.constraints import *
from pythfinder.Components.BetterClasses.mathEx import *

import pygame
import math
import os

# file containing:
#           - default constant values, image manipulation for the interface and Constants class
#           - default keys for joystick control
#           - helper methods for conversion


device_relative_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Images')

screenshot_path = os.path.join(device_relative_path, 'Screenshots\\')

default_robot_image_name = 'bot_from_above'
default_robot_image_path = 'Robot/'
default_robot_image_extension = 'png'
default_robot_image_source = os.path.join(device_relative_path, 'Robot/bot_from_above.png')

default_robot_scaling_factor = 1
default_robot_height_cm = 20
default_robot_width_cm = 15 
default_robot_real_max_velocity = 27.7 # cm/s

default_coordinate_system_color = "white"
default_grid_color = (63, 63, 63) #rgb
default_background_color = "black"

default_frame_rate = 1000 #fps
default_system_font = 'graffitiyouthregular'
default_text_color = "white"

default_width_percent = 25

default_time_until_fade = 0.4
default_fade_percent = 1

default_use_screen_border = True
default_field_centric = True
default_draw_robot_border = False
default_menu_entered = False
default_head_selection = False
default_forwards = True
default_erase_trail = True
default_joystick_enabled = True
default_freeze_trail = False
default_draw_table = False

default_kP_joystick_head = 6
default_kI_joystick_head = 0
default_kD_joystick_head = 0



#pixels
default_max_trail_length = math.inf
default_max_segment_length = 100

default_drawing_trail_threshold = 20
default_trail_color = "darkmagenta"
default_trail_loops = 300
default_trail_width = 2

default_pixels_to_decimeters = 100

default_positive_direction_arrow_offset = 25
default_half_unit_measure_line = 10

default_backing_distance = 1


if default_system_font not in pygame.font.get_fonts():
    print("\n\nunable to find the default font '{0}'.".format(default_system_font))
    print("\nplease install the font from the files provided in the root")
    print("library project or from the following link:")
    print("      https://www.dafont.com/graffiti-youth.font")
    print("\n\n")
    raise Exception("FONT NOT FOUND")



class Constants():
    def __init__(self, 
                 pixels_to_dec: int = default_pixels_to_decimeters,
                 fps: int = default_frame_rate,
                 robot_img_source: str = default_robot_image_source,
                 robot_scale: int = default_robot_scaling_factor,
                 robot_width: int = default_robot_width_cm,
                 robot_height: int = default_robot_height_cm,
                 text_color = default_text_color,
                 text_font: str = default_system_font,
                 max_trail_len: int = default_max_trail_length,
                 max_trail_segment_len: int = default_max_segment_length,
                 draw_trail_threshold: int = default_drawing_trail_threshold,
                 trail_color = default_trail_color,
                 trail_loops: int = default_trail_loops,
                 trail_width: int = default_trail_width,
                 background_color = default_background_color,
                 axis_color = default_coordinate_system_color,
                 grid_color = default_grid_color,
                 width_percent: int = default_width_percent,
                 backing_distance: int = default_backing_distance,
                 arrow_offset: int = default_positive_direction_arrow_offset,
                 half_unit_measure_line: int = default_half_unit_measure_line,
                 time_until_fade: int = default_time_until_fade,
                 fade_percent: int = default_fade_percent,
                 screen_size: ScreenSize = ScreenSize()):
        
        self.recalculate = BooleanEx(False)

        self.PIXELS_2_DEC = pixels_to_dec
        self.FPS = fps

        self.ROBOT_IMG_NAME = default_robot_image_name
        self.ROBOT_IMG_EX = default_robot_image_extension
        self.ROBOT_IMG_PATH = default_robot_image_path
        self.ROBOT_IMG_SOURCE = robot_img_source

        self.ROBOT_SCALE = robot_scale
        self.ROBOT_WIDTH = robot_width
        self.ROBOT_HEIGHT = robot_height

        self.TEXT_COLOR = text_color
        self.TEXT_FONT = text_font

        self.MAX_TRAIL_LEN = max_trail_len
        self.MAX_TRAIL_SEGMENT_LEN = max_trail_segment_len

        self.DRAW_TRAIL_THRESHOLD = draw_trail_threshold
        self.TRAIL_COLOR = trail_color
        self.TRAIL_LOOPS = trail_loops
        self.TRAIL_WIDTH = trail_width

        self.BACKGROUND_COLOR = background_color
        self.AXIS_COLOR = axis_color
        self.GRID_COLOR = grid_color

        self.WIDTH_PERCENT = width_percent

        self.BACKING_DISTANCE = backing_distance

        self.ARROW_OFFSET = arrow_offset
        self.HALF_UNIT_MEASURE_LINE = half_unit_measure_line

        self.TIME_UNTIL_FADE = time_until_fade
        self.FADE_PERCENT = fade_percent

        self.screen_size = screen_size

        self.COEFF_JOY_HEAD = PIDCoefficients(kP = default_kP_joystick_head,
                                              kI = default_kI_joystick_head,
                                              kD = default_kD_joystick_head)

        self.DRAW_ROBOT_BORDER = BooleanEx(default_draw_robot_border)
        self.FIELD_CENTRIC = BooleanEx(default_field_centric)
        self.USE_SCREEN_BORDER = BooleanEx(default_use_screen_border)
        self.MENU_ENTERED = BooleanEx(default_menu_entered)
        self.HEAD_SELECTION = BooleanEx(default_head_selection)
        self.FORWARDS = BooleanEx(default_forwards)
        self.ERASE_TRAIL = BooleanEx(default_erase_trail)
        self.JOYSTICK_ENABLED = BooleanEx(default_joystick_enabled)
        self.FREEZE_TRAIL = BooleanEx(default_freeze_trail)
        self.DRAW_TABLE = BooleanEx(default_draw_table)



    #resets all the values to default
    def default(self):
        self.PIXELS_2_DEC = default_pixels_to_decimeters
        self.FPS = default_frame_rate

        self.ROBOT_IMG_NAME = default_robot_image_name
        self.ROBOT_IMG_EX = default_robot_image_extension
        self.ROBOT_IMG_PATH = default_robot_image_path
        self.updateRobotImgSource()

        self.ROBOT_SCALE = default_robot_scaling_factor
        self.ROBOT_WIDTH = default_robot_width_cm
        self.ROBOT_HEIGHT = default_robot_height_cm

        self.TEXT_COLOR = default_text_color
        self.TEXT_FONT = default_system_font

        self.MAX_TRAIL_LEN = default_max_trail_length
        self.MAX_TRAIL_SEGMENT_LEN = default_max_segment_length

        self.DRAW_TRAIL_THRESHOLD = default_drawing_trail_threshold
        self.TRAIL_COLOR = default_trail_color
        self.TRAIL_LOOPS = default_trail_loops
        self.TRAIL_WIDTH = default_trail_width

        self.BACKGROUND_COLOR = default_background_color
        self.AXIS_COLOR = default_coordinate_system_color
        self.GRID_COLOR = default_grid_color

        self.WIDTH_PERCENT = default_width_percent

        self.BACKING_DISTANCE = default_backing_distance

        self.ARROW_OFFSET = default_positive_direction_arrow_offset
        self.HALF_UNIT_MEASURE_LINE = default_half_unit_measure_line

        self.TIME_UNTIL_FADE = default_time_until_fade
        self.FADE_PERCENT = default_fade_percent

        self.COEFF_JOY_HEAD = PIDCoefficients(kP = default_kP_joystick_head,
                                              kI = default_kI_joystick_head,
                                              kD = default_kD_joystick_head)

        self.DRAW_ROBOT_BORDER = BooleanEx(default_draw_robot_border)
        self.FIELD_CENTRIC = BooleanEx(default_field_centric)
        self.USE_SCREEN_BORDER = BooleanEx(default_use_screen_border)
        self.MENU_ENTERED = BooleanEx(default_menu_entered)
        self.HEAD_SELECTION = BooleanEx(default_head_selection)
        self.FORWARDS = BooleanEx(default_forwards)
        self.ERASE_TRAIL = BooleanEx(default_erase_trail)
        self.JOYSTICK_ENABLED = BooleanEx(default_joystick_enabled)
        self.FREEZE_TRAIL = BooleanEx(default_freeze_trail)
        self.DRAW_TABLE = BooleanEx(default_draw_table)

        self.screen_size = ScreenSize()
    
    def updateRobotImgSource(self, 
                             path = None, 
                             name = None, 
                             extension = None):
        
        if path is not None:
            self.ROBOT_IMG_PATH = path
        if name is not None:
            self.ROBOT_IMG_NAME = name
        if extension is not None:
            self.ROBOT_IMG_EX = extension

        self.ROBOT_IMG_SOURCE = os.path.join(device_relative_path, "{0}{1}.{2}".format(self.ROBOT_IMG_PATH, 
                                                    self.ROBOT_IMG_NAME, 
                                                    self.ROBOT_IMG_EX))
          
    def pixelsToCm(self, 
                   val: int):
        
        return val / self.PIXELS_2_DEC * 10

    def cmToPixels(self, 
                   val: int | float):
        
        return val * self.PIXELS_2_DEC / 10
    
    def pixelsToCmPoint(self, 
                        point: Point):
        
        return Point(self.pixelsToCm(point.x), self.pixelsToCm(point.y))
        
    


def point2Tuple(point: Point):
    return (point.x, point.y)

def tuple2Point(tuple: tuple):
    return Point(tuple[0], tuple[1])

def percent2Alpha(value):
    return value * 2.25

def distance(p1: tuple, p2: tuple):
    return hypot(p2[0] - p1[0], p2[1] - p1[1])

def exists(value):
    return value is not None


#KEY BINDS
left_wheel_forward_key = pygame.K_q
right_wheel_forward_key = pygame.K_w

left_wheel_backward_key = pygame.K_a
right_wheel_backward_key = pygame.K_s

turn_0_key = pygame.K_1
turn_45_key = pygame.K_2
turn_90_key = pygame.K_3
turn_135_key = pygame.K_4
turn_180_key = pygame.K_5
turn_225_key = pygame.K_6
turn_270_key = pygame.K_7
turn_315_key = pygame.K_8




#XBOX
xbox_threshold = 0.0001
xbox_left_x = 0
xbox_left_y = 1
xbox_right_x = 2

xbox_disable_button = 2
xbox_direction_button = 3
xbox_zero_button = 1
xbox_head_selection_button = 5
xbox_trail_button = 0
xbox_erase_trail_button = 4
xbox_screenshot_button = 8

xbox_turn_0 = (0, 1)
xbox_turn_45 = (1, 1)
xbox_turn_90 = (1, 0)
xbox_turn_135 = (1, -1)
xbox_turn_180 = (0, -1)
xbox_turn_225 = (-1, -1)
xbox_turn_270 = (-1, 0)
xbox_turn_315 = (-1, 1)

#PS4
ps4_threshold = 0.06
ps4_left_x = 0
ps4_left_y = 1
ps4_right_x = 2

ps4_disable_button = 2
ps4_direction_button = 3
ps4_zero_button = 1
ps4_head_selection_button = 10
ps4_trail_button = 0
ps4_erase_trail_button = 9
ps4_screenshot_button = 8

ps4_turn_0 = 11
ps4_turn_45 = None
ps4_turn_90 = 14
ps4_turn_135 = None
ps4_turn_180 = 12
ps4_turn_225 = None
ps4_turn_270 = 13
ps4_turn_315 = None

#PS5
ps5_threshold = 0.05 #to be tuned
ps5_left_x = 0
ps5_left_y = 1
ps5_right_x = 2

ps5_disable_button = 2
ps5_direction_button = 3
ps5_zero_button = 1
ps5_head_selection_button = 10
ps5_trail_button = 0
ps5_erase_trail_button = 9
ps5_screenshot_button = 11

ps5_turn_0 = (0, 1)
ps5_turn_45 = (1, 1)
ps5_turn_90 = (1, 0)
ps5_turn_135 = (1, -1)
ps5_turn_180 = (0, -1)
ps5_turn_225 = (-1, -1)
ps5_turn_270 = (-1, 0)
ps5_turn_315 = (-1, 1)







img_main_menu_source = "Menu/Main/menu_main.png"
img_forwards_source = "Controls/btn_forwards.png"
img_backwards_source = "Controls/btn_backwards.png"
img_menu_button_source = "Menu/Main/menu_button.png"
img_show_trail_source = "Controls/btn_show_trail.png"
img_hide_trail_source = "Controls/btn_hide_trail.png"
img_home_button_source = "Menu/Main/menu_home_button.png"
img_selecting_on_source = "Controls/btn_selecting_on.png"
img_selecting_off_source = "Controls/btn_selecting_off.png"
img_selected_menu_button_source = "Menu/Main/selected_menu_button.png"
img_selected_home_button_source = "Menu/Main/selected_menu_home_button.png"


img_other_button_source = "Menu/Selection/other_button.png"
img_robot_button_source = "Menu/Selection/robot_button.png"
img_trail_button_source = "Menu/Selection/trail_button.png"
img_selection_menu_source = "Menu/Selection/selection_menu.png"
img_pathing_button_source = "Menu/Selection/pathing_button.png"
img_interface_button_source = "Menu/Selection/interface_button.png"
img_selected_other_button_source = "Menu/Selection/selected_other_button.png"
img_selected_robot_button_source = "Menu/Selection/selected_robot_button.png"
img_selected_trail_button_source = "Menu/Selection/selected_trail_button.png"
img_selected_pathing_button_source = "Menu/Selection/selected_pathing_button.png"
img_selected_interface_button_source = "Menu/Selection/selected_interface_button.png"


img_general_menu_source = "Menu/General/general_menu.png"
img_left_arrow_source = "Menu/General/Arrows/Left/left_arrow.png"
img_right_arrow_source = "Menu/General/Arrows/Right/right_arrow.png"
img_selected_left_arrow_source = "Menu/General/Arrows/Left/selected_left_arrow.png"
img_selected_right_arrow_source = "Menu/General/Arrows/Right/selected_right_arrow.png"


img_other_quadrant_source = "Menu/Other/other_quadrant.png"
img_selected_none_source = "selected_none.png"
img_none_source = "none.png"


img_field_centric_on_source = "Menu/Other/FieldCentric/field_centric_on.png"
img_field_centric_off_source = "Menu/Other/FieldCentric/field_centric_off.png"
img_selected_field_centric_on_source = "Menu/Other/FieldCentric/selected_field_centric_on.png"
img_selected_field_centric_off_source = "Menu/Other/FieldCentric/selected_field_centric_off.png"


img_robot_border_on_source = "Menu/Other/RobotBorder/robot_border_on.png"
img_robot_border_off_source = "Menu/Other/RobotBorder/robot_border_off.png"
img_selected_robot_border_on_source = "Menu/Other/RobotBorder/selected_robot_border_on.png"
img_selected_robot_border_off_source = "Menu/Other/RobotBorder/selected_robot_border_off.png"


img_screen_border_on_source = "Menu/Other/ScreenBorder/screen_border_on.png"
img_screen_border_off_source = "Menu/Other/ScreenBorder/screen_border_off.png"
img_selected_screen_border_on_source = "Menu/Other/ScreenBorder/selected_screen_border_on.png"
img_selected_screen_border_off_source = "Menu/Other/ScreenBorder/selected_screen_border_off.png"

img_draw_table_on_source = "Menu/Other/DrawTable/draw_table_on.png"
img_draw_table_off_source = "Menu/Other/DrawTable/draw_table_off.png"
img_selected_draw_table_on_source = "Menu/Other/DrawTable/selected_draw_table_on.png"
img_selected_draw_table_off_source = "Menu/Other/DrawTable/selected_draw_table_off.png"


img_scale_source = "Menu/Robot/scale.png"
img_width_source = "Menu/Robot/width.png"
img_height_source = "Menu/Robot/height.png"
img_robot_image_path_source = "Menu/Robot/robot_path.png"
img_selected_scale_source = "Menu/Robot/selected_scale.png"
img_selected_width_source = "Menu/Robot/selected_width.png"
img_selected_height_source = "Menu/Robot/selected_height.png"
img_path_quadrant_source = "Menu/Robot/robot_path_quadrant.png"
img_specs_quadrant_source = "Menu/Robot/robot_specs_quadrant.png"
img_selected_robot_image_path_source = "Menu/Robot/selected_robot_path.png"

img_robot_indicator_source = "Menu/Robot/robot_indicator.png"
img_other_indicator_source = "Menu/Other/other_indicator.png"


img_forwards = pygame.image.load(os.path.join(device_relative_path, img_forwards_source))
img_main_menu = pygame.image.load(os.path.join(device_relative_path, img_main_menu_source))
img_backwards = pygame.image.load(os.path.join(device_relative_path, img_backwards_source))
img_show_trail = pygame.image.load(os.path.join(device_relative_path, img_show_trail_source))
img_hide_trail = pygame.image.load(os.path.join(device_relative_path, img_hide_trail_source))
img_menu_button = pygame.image.load(os.path.join(device_relative_path, img_menu_button_source))
img_home_button = pygame.image.load(os.path.join(device_relative_path, img_home_button_source))
img_selecting_on = pygame.image.load(os.path.join(device_relative_path, img_selecting_on_source))
img_selecting_off = pygame.image.load(os.path.join(device_relative_path, img_selecting_off_source))
img_selected_menu_button = pygame.image.load(os.path.join(device_relative_path, img_selected_menu_button_source))
img_selected_home_button = pygame.image.load(os.path.join(device_relative_path, img_selected_home_button_source))


img_other_button = pygame.image.load(os.path.join(device_relative_path, img_other_button_source))
img_robot_button = pygame.image.load(os.path.join(device_relative_path, img_robot_button_source))
img_trail_button = pygame.image.load(os.path.join(device_relative_path, img_trail_button_source))
img_pathing_button= pygame.image.load(os.path.join(device_relative_path, img_pathing_button_source))
img_selection_menu = pygame.image.load(os.path.join(device_relative_path, img_selection_menu_source))
img_interface_button = pygame.image.load(os.path.join(device_relative_path, img_interface_button_source))
img_selected_other_button= pygame.image.load(os.path.join(device_relative_path, img_selected_other_button_source))
img_selected_robot_button = pygame.image.load(os.path.join(device_relative_path, img_selected_robot_button_source))
img_selected_trail_button = pygame.image.load(os.path.join(device_relative_path, img_selected_trail_button_source))
img_selected_pathing_button = pygame.image.load(os.path.join(device_relative_path, img_selected_pathing_button_source))
img_selected_interface_button= pygame.image.load(os.path.join(device_relative_path, img_selected_interface_button_source))


img_general_menu = pygame.image.load(os.path.join(device_relative_path, img_general_menu_source))
img_left_arrow = pygame.image.load(os.path.join(device_relative_path, img_left_arrow_source))
img_right_arrow = pygame.image.load(os.path.join(device_relative_path, img_right_arrow_source))
img_selected_left_arrow = pygame.image.load(os.path.join(device_relative_path, img_selected_left_arrow_source))
img_selected_right_arrow = pygame.image.load(os.path.join(device_relative_path, img_selected_right_arrow_source))

img_other_quadrant = pygame.image.load(os.path.join(device_relative_path, img_other_quadrant_source))
img_selected_none = pygame.image.load(os.path.join(device_relative_path, img_selected_none_source))
img_none = pygame.image.load(os.path.join(device_relative_path, img_none_source))

img_field_centric_on = pygame.image.load(os.path.join(device_relative_path, img_field_centric_on_source))
img_field_centric_off = pygame.image.load(os.path.join(device_relative_path, img_field_centric_off_source))
img_selected_field_centric_on = pygame.image.load(os.path.join(device_relative_path, img_selected_field_centric_on_source))
img_selected_field_centric_off = pygame.image.load(os.path.join(device_relative_path, img_selected_field_centric_off_source))

img_robot_border_on = pygame.image.load(os.path.join(device_relative_path, img_robot_border_on_source))
img_robot_border_off = pygame.image.load(os.path.join(device_relative_path, img_robot_border_off_source))
img_selected_robot_border_on = pygame.image.load(os.path.join(device_relative_path, img_selected_robot_border_on_source))
img_selected_robot_border_off = pygame.image.load(os.path.join(device_relative_path, img_selected_robot_border_off_source))

img_screen_border_on = pygame.image.load(os.path.join(device_relative_path, img_screen_border_on_source))
img_screen_border_off = pygame.image.load(os.path.join(device_relative_path, img_screen_border_off_source))
img_selected_screen_border_on = pygame.image.load(os.path.join(device_relative_path, img_selected_screen_border_on_source))
img_selected_screen_border_off = pygame.image.load(os.path.join(device_relative_path, img_selected_screen_border_off_source))

img_draw_table_on = pygame.image.load(os.path.join(device_relative_path, img_draw_table_on_source))
img_draw_table_off = pygame.image.load(os.path.join(device_relative_path, img_draw_table_off_source))
img_selected_draw_table_on = pygame.image.load(os.path.join(device_relative_path, img_selected_draw_table_on_source))
img_selected_draw_table_off = pygame.image.load(os.path.join(device_relative_path, img_selected_draw_table_off_source))

img_scale = pygame.image.load(os.path.join(device_relative_path, img_scale_source))
img_width = pygame.image.load(os.path.join(device_relative_path, img_width_source))
img_height = pygame.image.load(os.path.join(device_relative_path, img_height_source))
img_path_quadrant = pygame.image.load(os.path.join(device_relative_path, img_path_quadrant_source))
img_specs_quadrant = pygame.image.load(os.path.join(device_relative_path, img_specs_quadrant_source))
img_selected_scale = pygame.image.load(os.path.join(device_relative_path, img_selected_scale_source))
img_selected_width = pygame.image.load(os.path.join(device_relative_path, img_selected_width_source))
img_selected_height = pygame.image.load(os.path.join(device_relative_path, img_selected_height_source))
img_robot_image_path = pygame.image.load(os.path.join(device_relative_path, img_robot_image_path_source))
img_selected_robot_image_path = pygame.image.load(os.path.join(device_relative_path, img_selected_robot_image_path_source))

img_robot_indicator = pygame.image.load(os.path.join(device_relative_path, img_robot_indicator_source))
img_other_indicator = pygame.image.load(os.path.join(device_relative_path, img_other_indicator_source))






img_main_menu = pygame.transform.scale(img_main_menu, (900, 700))
img_general_menu = pygame.transform.scale(img_general_menu, (900, 700))

img_home_button = pygame.transform.scale(img_home_button, (50, 51))
img_menu_button = pygame.transform.scale(img_menu_button, (63, 52))

img_selected_home_button = pygame.transform.scale(img_selected_home_button, (50, 51))
img_selected_menu_button = pygame.transform.scale(img_selected_menu_button, (63, 52))

img_selection_menu = pygame.transform.scale(img_selection_menu, (279, 516))

img_robot_button = pygame.transform.scale(img_robot_button, (176, 51))
img_selected_robot_button = pygame.transform.scale(img_selected_robot_button, (176, 51))

img_interface_button = pygame.transform.scale(img_interface_button, (245, 51))
img_selected_interface_button = pygame.transform.scale(img_selected_interface_button, (245, 51))

img_trail_button = pygame.transform.scale(img_trail_button, (175, 51))
img_selected_trail_button = pygame.transform.scale(img_selected_trail_button, (175, 51))

img_other_button = pygame.transform.scale(img_other_button, (185, 51))
img_selected_other_button = pygame.transform.scale(img_selected_other_button, (185, 51))

img_pathing_button = pygame.transform.scale(img_pathing_button, (248, 51))
img_selected_pathing_button = pygame.transform.scale(img_selected_pathing_button, (248, 51))

img_other_quadrant = pygame.transform.scale(img_other_quadrant, (310, 103))
img_selected_none = pygame.transform.scale(img_selected_none, (230, 100))
img_none = pygame.transform.scale(img_none, (230, 100))

img_field_centric_on = pygame.transform.scale(img_field_centric_on, (390, 110))
img_field_centric_off = pygame.transform.scale(img_field_centric_off, (390, 110))
img_selected_field_centric_on = pygame.transform.scale(img_selected_field_centric_on, (390, 110))
img_selected_field_centric_off = pygame.transform.scale(img_selected_field_centric_off, (390, 110))

img_robot_border_on = pygame.transform.scale(img_robot_border_on, (390, 110))
img_robot_border_off = pygame.transform.scale(img_robot_border_off, (390, 110))
img_selected_robot_border_on = pygame.transform.scale(img_selected_robot_border_on, (390, 110))
img_selected_robot_border_off = pygame.transform.scale(img_selected_robot_border_off, (390, 110))

img_screen_border_on = pygame.transform.scale(img_screen_border_on, (390, 110))
img_screen_border_off = pygame.transform.scale(img_screen_border_off, (390, 110))
img_selected_screen_border_on = pygame.transform.scale(img_selected_screen_border_on, (390, 110))
img_selected_screen_border_off = pygame.transform.scale(img_selected_screen_border_off, (390, 110))

img_draw_table_on = pygame.transform.scale(img_draw_table_on, (390, 110))
img_draw_table_off = pygame.transform.scale(img_draw_table_off, (390, 110))
img_selected_draw_table_on = pygame.transform.scale(img_selected_draw_table_on, (390, 110))
img_selected_draw_table_off = pygame.transform.scale(img_selected_draw_table_off, (390, 110))

img_robot_indicator = pygame.transform.scale(img_robot_indicator, (170, 95))
img_other_indicator = pygame.transform.scale(img_other_indicator, (170, 95))

img_path_quadrant = pygame.transform.scale(img_path_quadrant, (700, 200))
img_specs_quadrant = pygame.transform.scale(img_specs_quadrant, (193, 240))

img_selected_robot_image_path = pygame.transform.scale(img_selected_robot_image_path, (700, 95))
img_robot_image_path = pygame.transform.scale(img_robot_image_path, (700, 95))

img_width = pygame.transform.scale(img_width, (170, 85))
img_selected_width = pygame.transform.scale(img_selected_width, (170, 85))
img_height = pygame.transform.scale(img_height, (175, 100))
img_selected_height = pygame.transform.scale(img_selected_height, (175, 100))
img_scale = pygame.transform.scale(img_scale, (170, 85))
img_selected_scale = pygame.transform.scale(img_selected_scale, (170, 85))



fll_table_width_cm = 227 # og - 93in
fll_table_height_cm = 120 # og - 45in

fll_table_source = 'Table/FLL_table_MP.jpg'
fll_table_image = pygame.image.load(os.path.join(device_relative_path, fll_table_source))




#pathing constants
kP_head = 30
kD_head = 1
kS_head = 0.6

REAL_MAX_VEL = 27.7
kS_fwd = 20 




