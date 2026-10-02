#!/usr/bin/env python3

import os

from launch import LaunchDescription

from launch.actions import (
    DeclareLaunchArgument,
    LogInfo
)

from launch.conditions import IfCondition

from launch.substitutions import (
    LaunchConfiguration,
    Command
)

from launch_ros.actions import Node

from launch_ros.parameter_descriptions import (
    ParameterValue
)

from ament_index_python.packages import (
    get_package_share_directory
)


def generate_launch_description():

    # ============================================================
    # PACKAGE
    # ============================================================

    package_name = "dobot_e6_description"

    package_share = get_package_share_directory(
        package_name
    )


    # ============================================================
    # LAUNCH ARGUMENTS
    # ============================================================

    use_joint_state_gui_arg = DeclareLaunchArgument(
        "use_joint_state_gui",
        default_value="true",
        description="Enable joint_state_publisher_gui"
    )

    use_joint_state_gui = LaunchConfiguration(
        "use_joint_state_gui"
    )


    controller_type_arg = DeclareLaunchArgument(
        "controller_type",
        default_value="position_control",
        description="Controller type: position_control or velocity_control"
    )

    controller_type = LaunchConfiguration(
        "controller_type"
    )


    # ============================================================
    # XACRO FILE
    # ============================================================

    xacro_file = os.path.join(
        package_share,
        "urdf",
        "robots",
        "dobot_e6.urdf.xacro"
    )


    # ============================================================
    # ROBOT DESCRIPTION
    # ============================================================

    robot_description = ParameterValue(
        Command([
            "xacro ",
            xacro_file,
            " controller_type:=",
            controller_type
        ]),
        value_type=str
    )


    # ============================================================
    # DEBUG CONTROLLER SELECTION
    # ============================================================

    controller_debug = LogInfo(
        msg=[
            "Dobot E6 controller type: ",
            controller_type
        ]
    )


    # ============================================================
    # JOINT STATE PUBLISHER GUI
    # ============================================================

    joint_state_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
        condition=IfCondition(
            use_joint_state_gui
        )
    )


    # ============================================================
    # ROBOT STATE PUBLISHER
    # ============================================================

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True
            }
        ]
    )
    
    # ============================================================
    # RVIZ
    # ============================================================

    rviz_config = os.path.join(
        package_share,
        "rviz",
        "dobot_e6_description.rviz"
    )
    
    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Launch RViz2"
    )

    use_rviz = LaunchConfiguration(
        "use_rviz"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=[
            "-d",
            rviz_config
        ],
        parameters=[
            {
                "use_sim_time": True
            }
        ],
        output="screen",
        condition=IfCondition(
            use_rviz
        )
    )
    
    



    # ============================================================
    # LAUNCH DESCRIPTION
    # ============================================================

    ld = LaunchDescription()

    # Arguments
    ld.add_action(use_joint_state_gui_arg)
    ld.add_action(controller_type_arg)
    ld.add_action(use_rviz_arg)

    # Debug
    ld.add_action(controller_debug)

    # Nodes
    ld.add_action(joint_state_gui)
    ld.add_action(robot_state_publisher)
    ld.add_action(rviz_node)

    return ld
