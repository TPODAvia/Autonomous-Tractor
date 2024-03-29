import os
 
from launch import LaunchDescription
from launch_ros.actions import Node
from launch import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from ament_index_python.packages import get_package_share_directory
def generate_launch_description():
    
    kalman_launch_path = PythonLaunchDescriptionSource([get_package_share_directory('my_package'), '/launch/0kalman.launch.py']) 
    
    return LaunchDescription([
        Node(
            package='orbslam3_ros2',
            executable='mono',
            name='orbslam3_ros2',
            output='screen',
        ),
        # Get the path to the launch file
        IncludeLaunchDescription(kalman_launch_path),

    ])