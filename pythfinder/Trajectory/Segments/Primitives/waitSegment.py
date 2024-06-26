from pythfinder.Trajectory.Segments.Primitives.generic import *

class WaitSegment(MotionSegment):
    def __init__(self, 
                 last_state: MotionState,
                 ms: int):
        
        self.last_state = last_state
        self.ms = ms

        # early exit when empty segment
        if last_state is None:
            return None
        
        super().__init__(last_state)
        
        self.total_time = ms
        self.end_time = self.start_time + self.total_time - 1
    

    def addConstraintsSegmTime(self, time: int, constraints2d: Constraints2D, auto_build: bool = True):
        # what did you expect? Sure, speed constraints when staying in one place, sure
        # go to sleep man
        pass

    def generate(self):
        for i in range(self.ms):
            self.states.append(
                MotionState(time = self.start_time + i, 
                            field_vel = ChassisState(),                  # no velocities when stationary
                            displacement = self.last_state.displacement, # same displacement
                            pose = self.last_state.pose))                # same pose
        
        # empty segment
        if len(self.states) == 0:
            self.states.append(self.last_state)

        self.built = True
    


    def getAction(self) -> MotionAction:
        return MotionAction.WAIT

    def copy(self, last_state: MotionState):
        return WaitSegment(last_state,
                           self.ms)