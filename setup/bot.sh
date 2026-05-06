#!/bin/bash
# Launched by /etc/systemd/system/bot.service

# source
source /opt/ros/noetic/setup.bash
source /home/sokim/catkin_ws/devel_isolated/setup.bash

# export
export ROS_DB_PATH='/home/sokim/ROS_DB'
export ROS_PACKAGE_PATH=/opt/ros/noetic/share:/home/sokim/catkin_ws/src
# export ROS_HOME=$HOME/.ros
export ROS_HOME=${ROS_HOME:=$(echo ~sokim)/.ros}
export HOME=${HOME:=$(echo ~sokim)}
# export ROS_LOG_DIR=/tmp
export BOT_BRINGUP=$(rospack find bot_bringup)

# launch
roslaunch $BOT_BRINGUP/launch/start.launch