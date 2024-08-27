from pythfinder.Trajectory.Segments import *
from pythfinder.core import *

import matplotlib.pyplot as mplt

class TrajectoryGrapher():
    def __init__(self,
                 sim: Simulator,
                 motion_states: List[MotionState]
                 ):
        
        self.sim = sim
        self.STATES = motion_states
        self.spike_threshold = 0.9 # means an instant dec of 9 m/s
                                   # (which is still a lot, but keep it for bigger robots, like FRC)

   
    
    def graph_wheel_speeds(self, connect: bool = False, velocity: bool = True, acceleration: bool = True):
        VEL = []
        ACC = []

        # get wheel speeds
        for state in self.STATES:
            robot_centric_vel = state.velocities.field_to_robot(state.pose)
            wheel_speeds = self.sim.constants.kinematics.inverse(robot_centric_vel)

            for i in range(len(wheel_speeds)):
                try: VEL[i].append(wheel_speeds[i].VELOCITY)
                except: 
                    VEL.append([])
                    VEL[-1].append(wheel_speeds[i].VELOCITY)
        
        # make sure acc ends on the X axis
        for each in VEL: 
            each.append(0) 
            each.append(0)
        
        # get the time
        time = linspace(0, len(VEL[-1]), len(VEL[-1]))

        # get wheel accelerations
        for vel in VEL:
            ACC.append(self.__get_derivative(vel))
        


        mplt.style.use('dark_background')

        if acceleration:
            self.__plot_wheel_acceleration_window(time, ACC, connect, "red")
            mplt.tight_layout()

        if velocity:
            self.__plot_wheel_velocity_window(time, VEL, connect, "green")
            mplt.tight_layout()

        mplt.show()

    def __plot_wheel_velocity_window(self, t: List[int], vel: List[list],
                                  connect: bool, color: str):
        
        figure = mplt.figure(figsize = (7, 7), facecolor = 'black')
        figure.canvas.manager.set_window_title("Wheel velocities")

        columns = len(vel) / 2 if len(vel) % 2 == 0 else int(len(vel) / 2) + 1

        for i in range(len(vel)):
            nr = int(200 + 10 * columns + i + 1)

            ax = figure.add_subplot(nr)
            ax.set_xlabel('time (ms)', fontsize = 14)
            ax.set_ylabel('velocity (cm / s)', fontsize = 14)
            ax.set_title('wheel {0}'.format(i + 1))

            if connect:
                    ax.plot(t, vel[i], color = color, linewidth = 3)
            else: ax.scatter(t, vel[i], color = color, s = 1)

            ax.axhline(0, color = 'white', linewidth = 0.5)

    def __plot_wheel_acceleration_window(self, t: List[int], acc: List[list],
                                      connect: bool, color: str):
        
        figure = mplt.figure(figsize = (7, 7), facecolor = 'black')
        figure.canvas.manager.set_window_title("Wheel accelerations")

        columns = len(acc) / 2 if len(acc) % 2 == 0 else int(len(acc) / 2) + 1

        for i in range(len(acc)):
            nr = int(200 + 10 * columns + i + 1)

            ax = figure.add_subplot(nr)
            ax.set_xlabel('time (ms)', fontsize = 14)
            ax.set_ylabel('acceleration (cm / s^2)', fontsize = 14)
            ax.set_title('wheel {0}'.format(i + 1))

            if connect:
                    ax.plot(t, acc[i], color = color, linewidth = 3)
            else: ax.scatter(t, acc[i], color = color, s = 1)

            ax.axhline(0, color = 'white', linewidth = 0.5)



    def graph_chassis_speeds(self, connect: bool = False, velocity: bool = True, acceleration: bool = True):
        VEL_X = []
        VEL_Y = []
        ANG_VEL = []

        # get all velocities into separate lists
        for state in self.STATES:
            robot_centric_vel = state.velocities.field_to_robot(state.pose)

            VEL_X.append(robot_centric_vel.VEL.x)
            VEL_Y.append(robot_centric_vel.VEL.y)
            ANG_VEL.append(robot_centric_vel.ANG_VEL)
        
        plots = [VEL_X, VEL_Y, ANG_VEL]

        # make sure acc ends on the X axis
        for each in plots:
            each.append(0)
            each.append(0)

        time = linspace(0, len(VEL_X), len(VEL_X))
        plots_deriv = [self.__get_derivative(vel) for vel in plots]
        


        mplt.style.use('dark_background')

        if acceleration:
            self.__plot_chassis_acceleration_window(time, plots_deriv, connect, color = 'red')
            mplt.tight_layout()
        if velocity:
            self.__plot_chassis_velocity_window(time, plots, connect, color = 'green')
            mplt.tight_layout()

        mplt.show()
            
    def __plot_chassis_velocity_window(self, t: List[int], vel: List[list], 
                                    connect: bool, color: str):

        figure = mplt.figure(figsize = (10, 4), facecolor = 'black')
        figure.canvas.manager.set_window_title("Velocities")

        titles = ["x velocity", "y velocity", "angular velocity"]

        for i in range(3):
            nr = 130 + i + 1

            ax = figure.add_subplot(nr)
            ax.set_xlabel('time (ms)', fontsize = 14)
            ax.set_ylabel('velocity (cm / s)' if not i == 2 else "velocity (rad / s)", fontsize = 14)
            ax.set_title(titles[i])

            if connect:
                    ax.plot(t, vel[i], color = color, linewidth = 3)
            else: ax.scatter(t, vel[i], color = color, s = 1)

            ax.axhline(0, color = 'white', linewidth = 0.5)

    def __plot_chassis_acceleration_window(self, t: List[int], acc: List[list], 
                                        connect: bool, color: str):
        
        figure = mplt.figure(figsize = (10, 4), facecolor = 'black')
        figure.canvas.manager.set_window_title("Accelerations")

        titles = ["x acceleration", "y acceleration", "angular acceleration"]

        for i in range(3):
            nr = 130 + i + 1

            ax = figure.add_subplot(nr)
            ax.set_xlabel('time (ms)', fontsize = 14)
            ax.set_ylabel('acceleration (cm / s^2)' if not i == 2 else "acceleration (rad / s^2)", fontsize = 14)
            ax.set_title(titles[i])

            if connect:
                    ax.plot(t, acc[i], color = color, linewidth = 3)
            else: ax.scatter(t, acc[i], color = color, s = 1)

            ax.axhline(0, color = 'white', linewidth = 0.5)



    def __get_derivative(self, vel: List[float]):
        ACC = []

        for i in range(len(vel)):
            acceleration = 0

            if i > 1 :
                dt = 0.001                  # default dt is 1 ms
                dv = vel[i] - vel[i-1]
                    
                if abs(dv) < self.spike_threshold and not vel[i-1] == 0:
                    acceleration = dv / dt

            ACC.append(acceleration)

        return ACC

            
