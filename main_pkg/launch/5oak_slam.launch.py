import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LoadComposableNodes, Node
from launch_ros.descriptions import ComposableNode
from launch.actions import TimerAction

def launch_setup(context, *args, **kwargs):
    name = LaunchConfiguration('name').perform(context)
    depthai_prefix = get_package_share_directory("depthai_ros_driver")
    
    params_file= LaunchConfiguration("params_file")
    parameters = [
        {
            "frame_id": name,
            "subscribe_rgb": True,
            "subscribe_depth": True,
            "subscribe_odom_info": True,
            "approx_sync": True,
            "Rtabmap/DetectionRate": "3.5",
            "subscribe_rgbd": True
        }
    ]

    remappings = [
        # ("rgb/image", name+"/rgb/image_raw"),
        # ("rgb/camera_info", name+"/rgb/camera_info"),
        # ("depth/image", name+"/stereo/image_raw"),
    ]

    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("main_pkg"), 'launch', '0rgbd_pcl.launch.py')),
            launch_arguments={"name": name,
                              "params_file": params_file}.items()),
 
        LoadComposableNodes(
            target_container=name+"_container",
            composable_node_descriptions=[
                ComposableNode(
                    package='rtabmap_odom',
                    plugin='rtabmap_odom::RGBDOdometry',
                    name='rgbd_odometry',
                    parameters=parameters,
                    remappings=remappings,
                ),
            ],
        ),

        LoadComposableNodes(
            target_container=name+"_container",
            composable_node_descriptions=[
                ComposableNode(
                    package='rtabmap_slam',
                    plugin='rtabmap_slam::CoreWrapper',
                    name='rtabmap',
                    parameters=parameters,
                    remappings=remappings,
                ),
            ],
        ),

        Node(
            package="rtabmap_viz",
            executable="rtabmap_viz",
            output="screen",
            parameters=parameters,
            remappings=remappings,
        ),
    ]


def generate_launch_description():
    depthai_prefix = get_package_share_directory("depthai_ros_driver")
    config_dir = os.path.join(get_package_share_directory('main_pkg'), 'launch')
    declared_arguments = [
        DeclareLaunchArgument("name", default_value="oak"),
        DeclareLaunchArgument("params_file", default_value=os.path.join(depthai_prefix, 'config', 'rgbd.yaml')),
        DeclareLaunchArgument("rectify_rgb", default_value="True"),
        DeclareLaunchArgument("rviz", default_value="False"),
    ]

    use_rviz = LaunchConfiguration('rviz')
    bringup_dir = get_package_share_directory('nav2_bringup')
    rviz_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(bringup_dir, "launch", 'rviz_launch.py')),
        condition=IfCondition(use_rviz)
    )

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup), TimerAction(period=15.0, actions=[rviz_cmd])]
    )