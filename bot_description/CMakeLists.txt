cmake_minimum_required(VERSION 3.0.2)
project(bot_description)

find_package(catkin REQUIRED COMPONENTS
  urdf
  xacro
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES bot_description
#  CATKIN_DEPENDS urdf xacro
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(DIRECTORY urdf DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
