cmake_minimum_required(VERSION 3.0.2)
project(bot_navigation)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  std_srvs
  tf
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES bot_navigation
#  CATKIN_DEPENDS geometry_msgs nav_msgs roscpp rospy sensor_msgs std_msgs std_srvs tf
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

install(DIRECTORY launch param
 DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)