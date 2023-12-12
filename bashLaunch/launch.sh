#! /usr/bin/env bash

source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

echo "Launch Application"

roslaunch astrochef start.launch
