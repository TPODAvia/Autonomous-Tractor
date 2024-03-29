cmake_minimum_required(VERSION 3.5)
project(main_pkg)
# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
# Include Cpp "include" directory
include_directories(include)
# Create Cpp executable
add_executable(cpp_executable src/cpp_node.cpp)
ament_target_dependencies(cpp_executable rclcpp geometry_msgs)

add_executable(save_filter_gps src/save_filter_gps.cpp)
ament_target_dependencies(save_filter_gps rclcpp sensor_msgs cv_bridge)

# Install Cpp executables
install(TARGETS
  cpp_executable
  save_filter_gps
  DESTINATION lib/${PROJECT_NAME}
)
# Install Python modules
ament_python_install_package(${PROJECT_NAME})
# Install Python executables
install(PROGRAMS
  scripts/control_node.py
  scripts/fake_gps.py
  scripts/real_gps.py
  scripts/web.py
  scripts/fake_odom.py
  scripts/imu_quat.py
  scripts/odom_quat.py
  scripts/mpu9250_node.py
  scripts/fake_map.py
  scripts/fake_scan.py
  scripts/transform.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
ament_package()