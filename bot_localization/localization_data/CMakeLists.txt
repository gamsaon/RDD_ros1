cmake_minimum_required(VERSION 3.0.2)
project(localization_data)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  tf
  tf2_ros
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES localization_data
#  CATKIN_DEPENDS geometry_msgs nav_msgs roscpp rospy sensor_msgs std_msgs tf tf2_ros
#  DEPENDS system_lib
)


include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

INCLUDE_DIRECTORIES(/usr/local/lib)
LINK_DIRECTORIES(/usr/local/lib)

## Add rviz_click_to_2d node
add_executable(rviz_click_to_2d src/rviz_click_to_2d.cpp)
target_link_libraries(rviz_click_to_2d ${catkin_LIBRARIES})

## Add ekf_odom_pub node
add_executable(ekf_odom_pub src/ekf_odom_pub.cpp)
target_link_libraries(ekf_odom_pub ${catkin_LIBRARIES})
