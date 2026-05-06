cmake_minimum_required(VERSION 3.0.2)
project(bot_bringup)

find_package(catkin REQUIRED COMPONENTS
  diagnostic_msgs
  nav_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  tf
  bot_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES bot_bringup
  # CATKIN_DEPENDS diagnostic_msgs nav_msgs roscpp rospy sensor_msgs std_msgs tf bot_msgs
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

install(DIRECTORY launch core_launch src DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

file(GLOB SRC_DIR
	"src/*.py"
)

install(PROGRAMS
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS
	${SRC_DIR}
	src/bot_core.py

 	DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
