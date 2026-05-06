cmake_minimum_required(VERSION 3.0.2)
project(bot_teleop)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES bot_teleop
   CATKIN_DEPENDS geometry_msgs rospy std_msgs
#  DEPENDS system_lib
)

## Build ##
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)


## Install ##
catkin_install_python(PROGRAMS
  scripts/teleop_key.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch scripts
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

