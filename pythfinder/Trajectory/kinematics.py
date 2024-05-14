from abc import ABC, abstractmethod
from pythfinder.Components.BetterClasses.mathEx import *
from pythfinder.Components.Constants.constants import *

# file containing robot drive kinematics
#
# an abstract kinematics class is used for ease of using
#
# for FLL purpose, the only kinematic model addressed in this file is
#   for the two wheel differential drive (also known as 'Tank Drive').
#   For a brief overview of the math, check out the wiki page:
#     (https://en.wikipedia.org/wiki/Differential_wheeled_robot)


class Kinematics(ABC):

    @abstractmethod
    def inverseKinematics(self, velocity, angular_velocity):
        pass

    @abstractmethod
    def forwardKinematics(self, speeds: tuple):
        pass

class TankKinematics(Kinematics):
    def __init__(self, track_width = default_track_width):
        self.track_width = track_width

    def forwardKinematics(self, speeds: tuple):
        left_speed = speeds[0]
        right_speed = speeds[1]

        velocity = (right_speed + left_speed) / 2.0
        angular_velocity = (left_speed - right_speed) / self.track_width # rad / sec

        return (velocity, angular_velocity)

    def inverseKinematics(self, velocity, angular_velocity):
        left_speed = velocity + self.track_width / 2.0 * angular_velocity
        right_speed = velocity - self.track_width / 2.0 * angular_velocity

        return (left_speed, right_speed)
    
    def angular2LinearVel(self, angular_velocity):
        return self.track_width / 2.0 * angular_velocity

