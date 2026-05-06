cmake_minimum_required(VERSION 3.0.2)
project(bot_msgs)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  message_generation
  nav_msgs
  sensor_msgs
  std_msgs
)

add_service_files(
  FILES
  SaveMap.srv
)

generate_messages(
	DEPENDENCIES actionlib actionlib_msgs nav_msgs sensor_msgs std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES bot_msgs
#  CATKIN_DEPENDS actionlib actionlib_msgs message_generation nav_msgs sensor_msgs std_msgs
#  DEPENDS system_lib
)

