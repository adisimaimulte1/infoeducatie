from pythfinder.Components.BetterClasses.booleanEx import *
from pythfinder.Components.Constants.constants import *

import pygame 


# file containing the robot's trail logic.
#
# we define the trail as the array of points representing positions in time, stored in a list.
#
# because loop time can mess up the appearance of the trail, the solution we came up was drawing a line between
#   each 2 consecutive points to ensure continuity. This further expanded to the notions of trail width and trail
#   segments.
#
# trail segments are trail parts, characterized by close-up points. We defined a threshold for a min
#   distance (in pixels) between two consecutive points, which delimits individual segments. Each segment
#   has a color and a width. The only way to get a new segment is, somehow, register a position further 
#   than the threshold, which can be done by turning ON and OFF trail drawing.
#
# trail can have a maximum length, removing the first point from the list when reached, tho this length can
#   be set to infinity and not use this feature. 
#
# no duplicate points are stored in the list.
#
# after a time threshold of not moving, the trail can start erase itself. This can be stopped with a setting

class TrailPoint():
    def __init__(self, point_in_cm: Point, point_in_pixels: tuple) -> None:
        self.CM = point_in_cm
        self.point = point_in_pixels

class TrailSegment():
    def __init__(self, constants: Constants, points: List[TrailPoint] | None = None):
        if points is not None:
            self.points = points
        else: self.points = []

        self.hide = BooleanEx(False)

        self.constants = constants
    
    def draw(self, screen):
        if self.hide.compare(False):
            for point in range(1, len(self.points)):     
                pygame.draw.line(screen, self.constants.TRAIL_COLOR, 
                    self.points[point - 1].point, self.points[point].point, 
                width = self.constants.TRAIL_WIDTH)
    
    def recalculate(self):
        for each in self.points:
            each.point = self.to_window_point(each.CM).tuple()
    
    def to_window_point(self, point: Point):
        return Point(self.constants.screen_size.half_w + point.y * self.constants.PIXELS_2_DEC / 10, 
                     self.constants.screen_size.half_h - point.x * self.constants.PIXELS_2_DEC / 10)


class Trail():
    def __init__(self, constants: Constants):
        self.segments = [TrailSegment(constants)]
        self.DRAW_TRAIL = BooleanEx(False)
        self.HIDE_TRAIL = BooleanEx(False)

        self.pop_trail_loop = 0
        self.past_trail_length = 0
        self.current_segment = 0

        self.constants = constants
    
    def hide(self, segment_number: int, hide = False):
        self.segments[segment_number].hide.set(hide)
    


    def erase_trail_segment(self, number: int):
        self.segments.pop(number - 1)
        self.current_segment -= 1
    
    def erase_trail(self):
        self.segments = [TrailSegment(self.constants)]
        self.current_segment = 0



    def draw_trail(self, 
                  screen: pygame.Surface, 
                  pose: Pose):
        if self.DRAW_TRAIL.compare():
            self.build_trail(pose)

        if self.HIDE_TRAIL.compare():
            self.erase_trail()
            self.hide_trail.set(False)
        else:
            for segment in self.segments:
                segment.draw(screen)
    
    def build_trail(self, pose: Pose):
        if self.constants.FREEZE_TRAIL.compare():
            return 0
        
        trail_length = 0

        for segment in self.segments:
            trail_length += len(segment.points)

        if self.should_erase_point(trail_length):
            if len(self.segments[0].points) == 0:
                self.segments.pop(0)
                self.current_segment -= 1
            self.segments[0].points.pop(0)
            trail_length -= 1

        segment_length = len(self.segments[self.current_segment].points)

        if segment_length == 0:
            self.segments[self.current_segment].points.append(
                    TrailPoint(point_in_cm = pose,
                               point_in_pixels = self.to_window_point(pose).tuple()))

        elif self.segments[self.current_segment].points[-1].point != self.to_window_point(pose).tuple():
            last_point = self.segments[self.current_segment].points[-1].point
            current_point = self.to_window_point(pose).tuple()

            if distance(last_point, current_point) > self.constants.DRAW_TRAIL_THRESHOLD:
                self.segments.append(TrailSegment(self.constants))
                self.current_segment += 1

            self.segments[self.current_segment].points.append(
                    TrailPoint(point_in_cm = pose,
                               point_in_pixels = self.to_window_point(pose).tuple()))
        
        self.past_trail_length = trail_length

    def should_erase_point(self, length: int) -> bool:
        if self.constants.ERASE_TRAIL.compare(False):
            return False
        
        if length == self.past_trail_length:
            self.pop_trail_loop += 1
        else: self.pop_trail_loop = 0

        if length == self.constants.MAX_TRAIL_LEN:
            return True
        if self.pop_trail_loop >= self.constants.TRAIL_LOOPS:
            return True
    
        return False
    
    
    def to_window_point(self, pose: Pose):
        return Point(self.constants.screen_size.half_w + pose.y * self.constants.PIXELS_2_DEC / 10, 
                self.constants.screen_size.half_h - pose.x * self.constants.PIXELS_2_DEC / 10)
    
    def recalculate(self):
        for each in self.segments:
            each.recalculate()

      