from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    rviz_config=get_package_share_directory('bot_rslidar')+'/rviz/rviz2.rviz'
    return LaunchDescription([
        Node(
            package='bot_rslidar',
            executable='bot_rslidar_node',
            name='bot_rslidar_node',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d',rviz_config]
        )
    ])
