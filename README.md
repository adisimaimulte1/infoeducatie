<div align="center">

<img src="https://i.ibb.co/YbtktKX/pyth-finder-logo.png" alt="PythFinder logo">

### Pre-calculated motion planning for reliable competition robots.

![Alpha 0.0.5](https://img.shields.io/badge/ALPHA-0.0.5-62E39E?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.10%2B-62E39E?style=for-the-badge&logo=python&logoColor=15251D)
![FLL](https://img.shields.io/badge/FIRST%20LEGO%20LEAGUE-MOTION%20PLANNING-62E39E?style=for-the-badge&logo=first&logoColor=15251D)
![MIT License](https://img.shields.io/badge/LICENSE-MIT-62E39E?style=for-the-badge)

$\color{#62E39E}{\textsf{Build, simulate, inspect and export repeatable robot trajectories before match day.}}$

[Installation](#installation) · [Why PythFinder](#why-pythfinder) · [Usage](#usage) · [Trajectory API](#trajectory-usage) · [Documentation][17]

</div>

---

## At a glance

| | |
|---|---|
| $\color{#62E39E}{\textsf{Purpose}}$ | Generate reliable, pre-calculated robot trajectories for autonomous routines. |
| $\color{#62E39E}{\textsf{Workflow}}$ | Build → simulate → inspect → export → run on the robot. |
| $\color{#62E39E}{\textsf{Original platform}}$ | EV3 with MicroPython and the [PythFinder quick-start][11]. |
| $\color{#62E39E}{\textsf{Hardware support}}$ | Hardware-independent output that can be adapted for EV3, SPIKE Prime, NXT or other compatible processors. |

## Installation

Before diving in, make sure you have:

- Python 3.10 or newer ([the latest version][1] is recommended);
- [pip][2] installed on your device—usually `pip3` for Python 3;
- the team's [Graffiti Youth][5] font installed, as it is used by the interface.

Installation is then a single command in your terminal:

<p align="center">
      <img src="https://github.com/omegacoreFLL/PythFinder/assets/159171107/1734dba9-d9a7-4ad4-a3d9-1485a205c082" width = 100% alt="pyth-finder-install" border="0">
</p>

---

## Why PythFinder

$\color{#62E39E}{\textsf{PythFinder}}$ was developed by team [Omega Core][6] to improve motion planning for the FIRST LEGO League competition.

Teams commonly use blocks for autonomous routines because of the limited MicroPython and Python documentation available online.
This approach may be faster to compile, but it sacrifices reliability.

With this in mind, we chose MicroPython as the main language for our `EV3` brick. Throughout the 2023–2024 [MASTERPIECE season][8], we experimented with on-the-go motion calculations and concluded that they were $\color{#62E39E}{\textsf{far too slow}}$ for competitive use. Our focus therefore shifted toward pre-calculated motion, also known as [feedforward control][9].

Because the processors inside [LEGO®][10]-approved bricks cannot perform these calculations quickly, moving that work to a separate tool was the practical solution.

PythFinder is a $\color{#62E39E}{\textsf{local trajectory generator}}$ that produces a `.txt` file containing everything the robot needs to reproduce the planned motion. Copy that file into the robot's code folder and load it during initialization.

On the robot, a simplified follower reconstructs trajectories from the exported `.txt` data.

For an average maximum-points routine with seven or eight launches, loading all trajectory data can take approximately one to three minutes. The exact time depends on the amount of exported data and the generation settings described later.

> $\color{#62E39E}{\textsf{Competition note:}}$ Start the program at least four minutes before the match.

Why use this method? $\color{#62E39E}{\textsf{Consistency}}$. PythFinder applies ideas used in industrial robotics control systems, including acceleration-limited motion profiles and multithreaded markers for operating other motors alongside robot movement.

It's a small price to have one of the most reliable autonomous programs in the FLL competition.

PythFinder is $\color{#62E39E}{\textsf{not EV3-dependent}}$, even though that was its original development platform. Because hardware is separated from the generator, `SPIKE Prime`, `NXT` and other microprocessors capable of reading a `.txt` file can use the exported data—including robots outside FLL.

The plug-and-play [PythFinder quick-start][11] currently targets $\color{#62E39E}{\textsf{EV3}}$. Other bricks require a custom implementation for reading and applying the data. We recommend keeping all launches in one program so the trajectories are loaded only once before the match.

If you need implementation help, have an improvement in mind or simply want to learn more, contact [@omega.core][12] on Instagram.

The original roadmap aimed to create a quick-start for every FLL-legal brick, including a `SPIKE Prime` version around the launch of the $\color{#62E39E}{\textsf{SUBMERGED}}$ season. Contributions and collaboration are welcome. 💚🤍

---

## Usage

To start using this library in your environment, simply create a new python file and import the library:

```python
import pythfinder
```

### Create a robot
To enable the robot-visualization elements, create a `Simulator` object. This class encapsulates every component into one control center, taking care of the pygame window, joystick input and other pygame events (see [Advanced usage](#advanced-usage)).

```python
sim = pythfinder.Simulator()
```
This creates a simulator with $\color{#62E39E}{\textsf{default constants}}$. To override them, create a `Constants` object with your desired values and pass it to the constructor:

```python 
# pass your values here
custom_constants = pythfinder.Constants(...) 

sim = pythfinder.Simulator(custom_constants)
```


Every time you run the simulator, it starts with your dataset of constants. You'll learn another way to change them in [Interface settings](#interface-settings).
Finally, display your simulation:

```python
while sim.RUNNING():
    sim.update()
```
<p align="center">
      <img src="https://i.ibb.co/CKtP4wg/first-impresion.png" width = 100% alt="pyth-finder-joystick" border="0">
</p>


The code runs until you exit the simulator window. Connecting a [supported controller](#joystick-control) allows you to move freely on the field.

### Joystick control

PythFinder is built on top of pygame's functionalities, from which it inherits support for XBOX, PS4, and PS5 controllers.

Connecting them is as easy as plugging in through $\color{#62E39E}{\textsf{USB}}$ or connecting through $\color{#62E39E}{\textsf{Bluetooth}}$. The simulator will recognize it most of the time; otherwise, it'll raise an error.

All of the Nintendo controllers are currently not supported and will raise an error.

As of version 0.0.5.0-alpha, the latest release introduces enhanced functionality for controlling settings, robot movement not included. In addition to the existing controller-based controls, users can now also utilize keyboard buttons to access and operate most of the functionalities previously limited to the controller interface.

The controls used to manipulate the simulator are listed below. Button order is $\color{#62E39E}{\textsf{PS4 / Xbox / keyboard}}$.

| Controller | Keyboard | Action |
|---|---|---|
| `△ / Y` | `Space` | Move forward or backward when field-centric control is enabled. |
| `□ / X` | `Escape` | Enter or exit the interface settings menu. |
| `○ / B` | `Tab` | Reset the robot pose to the origin, or press buttons while the menu is active. |
| `X / A` | — | Show or hide the trail. |
| Left bumper | `Delete` | Erase the trail, or restore default values while the menu is active. |
| Right bumper | — | Hold to enter selection mode. |
| D-pad | Arrow keys | Navigate the interface or select robot orientation in selection mode. |
| Left joystick | — | Control linear and angular velocity when field-centric control is enabled. |
| Right joystick | — | Control angular velocity only when field-centric control is disabled. |
| Options / Start | `S` | Save a screenshot to the library's local `Screenshots` folder. |
<p align="center">
      <img src="https://github.com/omegacoreFLL/PythFinder/assets/159171107/7be00ab0-aa3b-433c-968d-4bc78f33f0b3" width = 100% alt="pyth-finder-joystick" border="0">
</p>

### Trajectory usage

#### What are trajectories?

First, we define a specific set of data regarding the robot's position, speed, and distance traveled as a $\color{#62E39E}{\textsf{state of motion}}$.

Multiple states of motion that exhibit certain similarities are referred to as $\color{#62E39E}{\textsf{motion segments}}$. These segments are further categorized by $\color{#62E39E}{\textsf{complexity}}$. `Primitives` denote movements with a single degree of freedom (1D), such as pure rotation, pure linear movement, or even stationary states (waiting). These primitives serve as building blocks for `complex` segments, which incorporate two or more primitives and characterize movements with two or three degrees of freedom, primarily intended for $\color{#62E39E}{\textsf{omnidirectional robots}}$. For FLL purposes, you'll mostly use primitives, but any motion segment adapts automatically to the chassis used.

Ultimately, all motion segments and auxiliary elements that perform other functions—known as $\color{#62E39E}{\textsf{markers}}$—collectively constitute a `trajectory`.
#### How to create trajectories

Trajectories are constructed using the `TrajectoryBuilder` class. This class requires a `Simulator` object as a parameter, and optionally, a `starting position` and a `preset` to use. By default, the initial position is set at the origin of the Cartesian coordinate system.

The constructor offers intuitive methods for crafting precise trajectories, incorporating personalised $\color{#62E39E}{\textsf{motion functions}}$. These functions are engineered to accommodate both omnidirectional and unidirectional robots.

The constructor identifies the type of chassis in use and $\color{#62E39E}{\textsf{adjusts}}$ the provided functions accordingly, as certain chassis types may have physical limitations that render some movements $\color{#62E39E}{\textsf{impossible}}$. By default, non-holonomic chassis are `tangent` to the trajectory, whereas holonomic chassis are given the option to `interpolate` orientation.

Here is a list of available motion functions:
- `wait()`
- `inLineCM()`
- `turnToDeg()`
- `toPoint()` or `toPointTangentHead()`
- `toPose()`, `toPoseTangentHead()` or `toPoseLinearHead()`
#### What are markers?

These functionalities can be integrated with $\color{#62E39E}{\textsf{markers}}$, facilitating the management of parallel tasks that are independent of the robot's movement by employing `multithreading` techniques. Markers can be configured to activate after a certain $\color{#62E39E}{\textsf{time}}$ or $\color{#62E39E}{\textsf{distance}}$, either $\color{#62E39E}{\textsf{relative}}$ to the last motion function or $\color{#62E39E}{\textsf{absolute}}$ with respect to the start of the trajectory.
The library also includes special types of markers:

| Type | Purpose |
|---|---|
| $\color{#62E39E}{\textsf{Interrupts}}$ | Break trajectory continuity at a selected time or distance, similar to sudden braking. |
| $\color{#62E39E}{\textsf{Dynamic constraints}}$ | Change the speed of selected trajectory sections without sacrificing continuity. |

Available marker methods:

- `interruptTemporal()` or `interruptDisplacement()`
- `addTemporalMarker()` or `addDisplacementMarker()`
- `addRelativeTemporalMarker()` or `addRelativeDisplacementMarker()`
- `addRelativeTemporalConstraints()` or `addRelativeDisplacementConstraints()`
`Interrupts` and `Constraints` are $\color{#62E39E}{\textsf{strictly relative}}$, as we have observed that users find it $\color{#62E39E}{\textsf{difficult}}$ to visualize the trajectory segments to which they apply. They modify the trajectory's course itself, as opposed to markers that call functions and might adversely affect the trajectory's construction. However, if users $\color{#62E39E}{\textsf{request}}$ it, I will reintroduce these functionalities, as they were included in the library's initial prototypes.

Markers can also include $\color{#62E39E}{\textsf{negative}}$ values, which are interpreted as relative to the end of the trajectory or motion segment, while $\color{#62E39E}{\textsf{positive}}$ values are interpreted as relative to the beginning of these elements.
#### Complete example

After specifying the desired motion, call `.build()` to compute the trajectory values.

Putting it all together, we obtain:

```python
# first launch from our Masterpiece code

START_POSE = Pose(-47, 97, -45)
PRESET = 1

trajectory = (TrajectoryBuilder(sim, START_POSE, PRESET)
              .inLineCM(75)
                    .addRelativeDisplacementMarker(35, lambda: print('womp womp'))
                    .addRelativeDisplacementMarker(-12, lambda: print('motor goes brr'))
                    .addRelativeDisplacementConstraints(cm = 30, 
  						constraints2d = Constraints2D(linear = Constraints(
                                                               vel = 10, 
                                                               dec = -50)))                                                   
                    .addRelativeDisplacementConstraints(cm = 36, 
  						constraints2d = Constraints2D(linear = Constraints(
 										   vel = 27.7, 
                                                               acc = 35, 
                                                               dec = -30)))
                    .interruptDisplacement(cm = 66)
              .wait(2600)
                    .addRelativeTemporalMarker(-1, lambda: print('motor goes :('))
              .inLineCM(-30)
              .turnToDeg(90)
              .inLineCM(-20)
              .turnToDeg(105)
              .inLineCM(-47)
              .turnToDeg(20)
              .wait(ms = 1200)
                    .addRelativeTemporalMarker(0, lambda: print("spin'n'spin'n'spin.."))
                    .addRelativeTemporalMarker(-1, lambda: print("the party's over :("))
              .turnToDeg(80)
              .inLineCM(-120)
              .build())
```

### Trajectory visualisation

After creating your trajectory, call the `.follow()` method and pass the `Simulator` object to see your code in action.

The follower supports two modes:

| Mode | Behaviour |
|---|---|
| `perfect` | Iterates through each motion state and displays the robot at its pre-calculated position. Increasing the step size makes the on-screen robot move faster. |
| `real` | Sends the calculated powers to the simulated robot, reproducing real-time behaviour. This is the recommended visualisation mode. |

The last optional parameter is `wait`. When set to `True`, it waits until the simulator is fully rendered before beginning the trajectory. This is useful with perfect following and a large step value because it keeps the beginning visible. Our fifth run looks something like this:

```python
# default values
PERFECT_STEPS = 40
PERFECT_FOLLOWING = False
WAIT = True 

trajectory.follow(sim, PERFECT_FOLLOWING, WAIT, PERFECT_STEPS)
```
<p align="center">
      <img src="https://github.com/omegacoreFLL/PythFinder/assets/159171107/2449776e-9608-4199-a631-119ef2d28aa1" width = 100% alt="pyth-finder-traj-follow" border="0">
</p>

### Velocity graph

To facilitate the understanding of the 'trajectory' concept, I have implemented an easy-to-use graphical visualization method for motion profiles.

I truly believe that this library represents one of the best ways to begin learning concepts $\color{#62E39E}{\textsf{used in industry}}$, aiming to assist and inspire future engineers and programmers.

Calling the `.graph()` function will display a Matplotlib graph of the $\color{#62E39E}{\textsf{velocity}}$ and $\color{#62E39E}{\textsf{acceleration}}$ for the left and right wheels. There are also optional parameters to display each value separately. Additionally, users can choose whether they want to view the velocity and acceleration of the wheels or the chassis.

An interesting aspect is the `connect` parameter. By default, it is set to `True`, causing lines to be drawn between points. Setting it to `False` reveals discontinuities in acceleration, as velocity is optimized for continuity.

```python
# default values
CONNECT = True
VELOCITY = True
ACCELERATION = True
WHEEL_SPEEDS = True

trajectory.graph(CONNECT, VELOCITY, ACCELERATION, WHEEL_SPEEDS)
```
<p align="center">
      <img src="https://i.ibb.co/V2Ts2QG/simulator-trajgraph.png" width = 100% alt="pyth-finder-graph" border="0">
</p>

### Generate velocities

To make the robot move like it does in the simulator, you need to $\color{#62E39E}{\textsf{transfer}}$ the data through a `.txt` file. This is accomplished with the `.generate()` method. Pass the file name or path and the step size:

```python
STEPS = 6
FILE_NAME = 'test'
WHEEL_SPEEDS = True
SEPARATE_LINES = False

trajectory.generate(FILE_NAME, STEPS, WHEEL_SPEEDS, SEPARATE_LINES)
```

Now you can copy the '.txt' file and load it into the quick-start to see it running!
<p align="center">
      <img src="https://i.ibb.co/8BBsxFF/traj-generator.png" width = 100% alt="pyth-finder-generate" border="0">
</p>

### Interface settings

There are two main ways you can manipulate your simulator environment through constants.

The first way is to pass a new instance of `Constants` when creating the simulator object, changing any of the following values:

```python 
# constants.py -- simplification

# all modifiable values:
class Constants():
def __init__(self, 
                 pixels_to_dec,
                 fps,
                 robot_img_source,
                 robot_scale,
                 robot_width,
                 robot_height,
                 text_color,
                 text_font,
                 max_trail_len,
                 max_trail_segment_len,
                 draw_trail_threshold,
                 trail_color,
                 trail_loops,
                 trail_width,
                 background_color,
                 axis_color,
                 grid_color,
                 width_percent,
                 backing_distance,
                 arrow_offset,
                 time_until_fade,
                 fade_percent,
                 real_max_velocity,
                 max_power,
                 
                 screen_size,
                 constraints2d,
                 kinematics):
    ...
```

As described in the [Create a Robot](#create-a-robot) section, these changes will be automatically applied at the start of the simulation. For an in-depth explanation of the constants, see the [documentation](#advanced-usage).

The second way is through the interface menu with joystick control. This is $\color{#62E39E}{\textsf{not fully implemented yet}}$ and is intended for on-the-go changes that reset whenever the simulator restarts.
<p align="center">
      <img src="https://i.ibb.co/R2HMqKW/simulator-intefacemenu.png" width = 100% alt="pyth-finder-presets" border="0">
</p>

### Presets

A $\color{#62E39E}{\textsf{remarkable innovation}}$ introduced by this library is the feature called `presets`. These allow you to completely transform the interface appearance, robot configuration, and chassis type with the press of a button. You can utilize the number keys from `1` to `9` on the keyboard, each assigned to a distinct set of constants that adjust the simulation in various ways. The `0` key resets the interface to its $\color{#62E39E}{\textsf{default settings}}$.

Beyond these predefined options, you can create your $\color{#62E39E}{\textsf{own custom presets}}$, tailored to your individual needs and preferences. This adds another level of $\color{#62E39E}{\textsf{flexibility}}$ and $\color{#62E39E}{\textsf{control}}$ over the `interface`, `robot behavior`, and `simulator parameters`.

By default, button $\color{#62E39E}{\textsf{1}}$ loads the latest `FLL` field and button $\color{#62E39E}{\textsf{2}}$ loads the latest `FTC` field:
<p align="center">
      <img src="https://github.com/omegacoreFLL/PythFinder/assets/159171107/0ea2aa63-31f7-41cb-b267-3ee00500d26b" width = 100% alt="pyth-finder-presets" border="0">
</p>

### Painting
In response to a community request, we have implemented a new feature that allows users to draw shapes on the screen. This feature proves to be particularly useful when engaging in discussions or explaining strategies to team members or judges.

To access the drawing functionality, toggle the `HAND DRAWING` option in the $\color{#62E39E}{\textsf{Other Menu}}$. Users can then choose from a variety of colors through the color picker in the $\color{#62E39E}{\textsf{Draw Menu}}$.

Accessing the painting tools can be done using keyboard shortcuts. Simply press the designated keys to activate the desired painting tool:
- `E` — erase tool;
- `L` — line tool;
- `R` — rectangle tool;
- `C` — circle tool;
- `T` — triangle tool;
- `Enter` — exit tools.

The functionality is similar to that of a painting program. Selecting different tools $\color{#62E39E}{\textsf{changes the cursor icon}}$, providing visual feedback about the active tool.

<p align="center">
      <img src="https://i.ibb.co/f1nTKKT/simulator-paint.png" width = 100% alt="pyth-finder-paint" border="0">
</p>




---

## Advanced usage

Explore the complete [PythFinder documentation][17] for the deeper API reference and implementation details.

## Credits

| | |
|---|---|
| Libraries | [pygame][3] · [Matplotlib][4] · [Pybricks][7] |
| Robot model | [BrickLink Studio 2.0][14] |
| Visual design | [Adobe Illustrator][16] |
| Motion-planning inspiration | [Road Runner FTC][13] |
| Interface font | [Graffiti Youth][5] |
| Field imagery | [Reddit][15] |

## License

PythFinder is available under the [MIT License](LICENSE.txt).

<div align="center">

Developed by [Omega Core][6] for the 2023–2024 FIRST LEGO League MASTERPIECE season.

`v0.0.5.0-alpha`

</div>


[1]: https://www.python.org/downloads/             "python download page"
[2]: https://pip.pypa.io/en/stable/installation/   "pip download page"
[3]: https://www.pygame.org/docs/                  "pygame quick start"
[4]: https://matplotlib.org/stable/                "matplot quick start"
[5]: https://www.dafont.com/graffiti-youth.font    "our team's use-free font"
[6]: https://linktr.ee/omega.core                  "our team's socials"
[7]: https://pybricks.com/ev3-micropython/startinstall.html "pybricks instalation for EV3 robots"
[8]: https://www.first-lego-league.org/en/2023-24-season/the-masterpiece-season "fll masterpiece"
[9]: https://www.youtube.com/watch?v=FW_ay7K4jPE "very well explained feedforward control video"
[10]: https://lego.com "lego official"
[11]: https://github.com/omegacoreFLL/pythfinder-quickstart.git "PythFinder quick start for EV3"
[12]: https://www.instagram.com/omegacoreFLL "instagram link"
[13]: https://github.com/acmerobotics/road-runner "roadrunner"
[14]: https://www.bricklink.com/v3/studio/download.page "lego cad software"
[15]: https://www.reddit.com "field images"
[16]: https://www.adobe.com/ro/products/illustrator.html "adobe illustrator"
[17]: https://github.com/omegacoreFLL/PythFinder/wiki "pythfinder's extended documentation"
