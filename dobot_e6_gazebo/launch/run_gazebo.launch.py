#!/usr/bin/env python3

import os

from launch import LaunchDescription

from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction
)

from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution
)

from launch.launch_description_sources import (
    PythonLaunchDescriptionSource
)

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # ============================================================
    # LAUNCH ARGUMENTS
    # ============================================================

    x_position_robot_spawn_arg = DeclareLaunchArgument(
        "x_spawn",
        default_value="0.5",
        description="Robot spawn position in X"
    )

    x_position_robot_spawn = LaunchConfiguration(
        "x_spawn"
    )


    y_position_robot_spawn_arg = DeclareLaunchArgument(
        "y_spawn",
        default_value="0.5",
        description="Robot spawn position in Y"
    )

    y_position_robot_spawn = LaunchConfiguration(
        "y_spawn"
    )


    world_name_arg = DeclareLaunchArgument(
        "world_name",
        default_value="empty.sdf",
        description="Gazebo world file"
    )

    world_name = LaunchConfiguration(
        "world_name"
    )


    # ------------------------------------------------------------
    # Controller type
    # ------------------------------------------------------------

    controller_type_arg = DeclareLaunchArgument(
        "controller_type",
        default_value="position_control",
        description="Controller type: position_control or velocity_control"
    )

    controller_type = LaunchConfiguration(
        "controller_type"
    )


    # ============================================================
    # ROBOT DESCRIPTION
    # ============================================================

    include_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("dobot_e6_description"),
                "launch",
                "description_e6.launch.py"
            ])
        ),
        launch_arguments={
            "use_joint_state_gui": "false",
            "controller_type": controller_type
        }.items()
    )


    # ============================================================
    # GAZEBO
    # ============================================================

    gazebo_launch = PathJoinSubstitution([
        FindPackageShare("ros_gz_sim"),
        "launch",
        "gz_sim.launch.py"
    ])


    pkg_gazebo = FindPackageShare(
        "dobot_e6_gazebo"
    )


    world_sdf = PathJoinSubstitution([
        pkg_gazebo,
        "worlds",
        world_name
    ])


    gazebo_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            gazebo_launch
        ),
        launch_arguments={
            "gz_args": [
                "-r ",
                world_sdf
            ]
        }.items()
    )


    # ============================================================
    # SPAWN ROBOT
    # ============================================================

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_dobot_e6",
        arguments=[
            "-name", "dobot_e6",
            "-topic", "robot_description",
            "-x", x_position_robot_spawn,
            "-y", y_position_robot_spawn,
            "-z", "0.01"
        ],
        output="screen"
    )


    # ============================================================
    # GAZEBO <-> ROS BRIDGE
    # ============================================================

    gz_bridge_params_path = os.path.join(
        get_package_share_directory(
            "dobot_e6_gazebo"
        ),
        "config",
        "arm_bridge.yaml"
    )


    gz_bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="gz_bridge",
        arguments=[
            "--ros-args",
            "-p",
            f"config_file:={gz_bridge_params_path}"
        ],
        output="screen"
    )


    # ============================================================
    # JOINT STATE BROADCASTER
    # ============================================================

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="joint_state_broadcaster_spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager"
        ],
        parameters=[
            {
                "use_sim_time": True
            }
        ],
        output="screen"
    )


    # ============================================================
    # ARM CONTROLLER
    # ============================================================

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="arm_controller_spawner",
        arguments=[
            controller_type,
            "--controller-manager",
            "/controller_manager"
        ],
        parameters=[
            {
                "use_sim_time": True
            }
        ],
        output="screen"
    )


    # ============================================================
    # DELAY CONTROLLER SPAWNING
    # ============================================================

    spawn_controllers = TimerAction(
        period=3.0,
        actions=[
            joint_state_broadcaster_spawner,
            arm_controller_spawner
        ]
    )


    # ============================================================
    # LAUNCH DESCRIPTION
    # ============================================================

    ld = LaunchDescription()

    # Arguments
    ld.add_action(controller_type_arg)
    ld.add_action(x_position_robot_spawn_arg)
    ld.add_action(y_position_robot_spawn_arg)
    ld.add_action(world_name_arg)

    # Gazebo
    ld.add_action(gazebo_node)

    # Robot description
    ld.add_action(include_description)

    # Spawn robot
    ld.add_action(spawn_robot)

    # ROS <-> Gazebo bridge
    ld.add_action(gz_bridge_node)

    # Controllers
    ld.add_action(spawn_controllers)

    return ld
