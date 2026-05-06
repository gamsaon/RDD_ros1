cmake_minimum_required(VERSION 3.0.2)
project(bot_slam)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  sensor_msgs
  std_msgs
  tf
)

catkin_package(
  # INCLUDE_DIRS include
  # LIBRARIES bot_slam
  CATKIN_DEPENDS roscpp rospy sensor_msgs std_msgs tf
  # DEPENDS system_lib
)

include_directories(
  # include
  ${catkin_INCLUDE_DIRS}
)

install(DIRECTORY launch src DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

file(GLOB SRC_DIR
	"src/*.py"
)

install(PROGRAMS
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS
	${SRC_DIR}

 	DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)