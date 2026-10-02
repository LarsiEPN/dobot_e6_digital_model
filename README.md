# Dobot Magician E6 Digital Model

Digital model of the **Dobot Magician E6** for ROS 2 and Gazebo simulation.

## 1. Introduction

The **Dobot Magician E6** is a 6-DOF collaborative robotic manipulator designed for education, research, and robotics development.

This repository provides a ROS 2 digital model of the robot that can be simulated in Gazebo using two joint-control modes:

- **Joint position control**
- **Joint velocity control**

The control mode can be selected directly when launching the simulation.

### TF Tree

The main kinematic chain of the robot is:

```text
world
└── base_link
    └── link1
        └── link2
            └── link3
                └── link4
                    └── link5
                        └── link6
```

The six actuated joints of the manipulator are:

```text
joint1
joint2
joint3
joint4
joint5
joint6
```

---

## 2. Download

Clone the repository:

```bash
git clone https://github.com/LarsiEPN/dobot_e6_digital_model.git
```

Move the package into your ROS 2 workspace if necessary and build the workspace:

```bash
cd ~/dobot_ws

colcon build --symlink-install

source install/setup.bash
```

---

## 3. Running the Gazebo Simulation

The simulation can be launched using either position or velocity joint control.

### Position Control

```bash
ros2 launch dobot_e6_gazebo run_gazebo.launch.py \
    controller_type:=position_control
```

### Velocity Control

```bash
ros2 launch dobot_e6_gazebo run_gazebo.launch.py \
    controller_type:=velocity_control
```

The selected controller determines both the command interface exposed by `ros2_control` and the controller loaded by the ROS 2 controller manager.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1c961c08-fcba-48d1-96cc-797273ab11ed" />

---

## 4. Relevant ROS 2 Topics

The following topics are useful for interacting with the simulated robot.

### Joint States

```text
/joint_states
```

This topic provides the current joint states of the robot.

It can be inspected using:

```bash
ros2 topic echo /joint_states
```

### Velocity Commands

When the simulation is launched with:

```text
controller_type:=velocity_control
```

joint velocity commands are received through:

```text
/velocity_control/commands
```

The command contains six values corresponding to:

```text
[joint1, joint2, joint3, joint4, joint5, joint6]
```

### Position Commands

When the simulation is launched with:

```text
controller_type:=position_control
```

joint position commands are received through:

```text
/position_control/commands
```

The command contains six values corresponding to:

```text
[joint1, joint2, joint3, joint4, joint5, joint6]
```

---

## 5. Command Examples

### Velocity Control Example

First, launch the simulation using the velocity controller:

```bash
ros2 launch dobot_e6_gazebo run_gazebo.launch.py \
    controller_type:=velocity_control
```

A velocity command can then be continuously published using:

```bash
ros2 topic pub -r 20 \
    /velocity_control/commands \
    std_msgs/msg/Float64MultiArray \
    "{data: [0.1, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

This commands `joint1` with a velocity of `0.1 rad/s`, while the remaining joints are commanded to zero velocity.

To stop all joints:

```bash
ros2 topic pub --once \
    /velocity_control/commands \
    std_msgs/msg/Float64MultiArray \
    "{data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

### Position Control Example

First, launch the simulation using the position controller:

```bash
ros2 launch dobot_e6_gazebo run_gazebo.launch.py \
    controller_type:=position_control
```

A joint position command can then be sent using:

```bash
ros2 topic pub --once \
    /position_control/commands \
    std_msgs/msg/Float64MultiArray \
    "{data: [0.0, 0.3, -0.3, 0.0, 0.2, 0.0]}"
```

The six values represent the desired positions, in radians, for:

```text
[joint1, joint2, joint3, joint4, joint5, joint6]
```

---

## 6. Visualizing the Robot Description

The robot description can also be launched independently from the Gazebo simulation.

To visualize the robot using the joint-state GUI:

```bash
ros2 launch dobot_e6_description description_e6.launch.py \
    use_joint_state_gui:=true
```

This mode is useful for inspecting the robot model, kinematic structure, TF frames, and joint motion without running the complete Gazebo simulation.

The `joint_state_publisher_gui` can be used to manually modify the joint positions and inspect the resulting robot configuration in RViz.
<img width="1450" height="843" alt="image" src="https://github.com/user-attachments/assets/2e204884-dc39-4076-b006-8f981968d80b" />

---

## Repository Structure

The repository is organized into two main ROS 2 packages:

```text
dobot_e6_digital_model/
├── dobot_e6_description/
│   ├── config/
│   ├── launch/
│   ├── meshes/
│   ├── rviz/
│   └── urdf/
│
└── dobot_e6_gazebo/
    ├── config/
    ├── launch/
    └── worlds/
```

`dobot_e6_description` contains the robot description, Xacro/URDF files, RViz configuration, and ROS 2 control configuration.

`dobot_e6_gazebo` contains the Gazebo simulation launch files, world configuration, and ROS-Gazebo bridge configuration.
