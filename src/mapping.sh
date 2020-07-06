roslaunch rtabmap_ros rtabmap.launch \
    rtabmap_args:="--delete_db_on_start" \
    depth_topic:=/camera/predicted_depth \
    rgb_topic:=/rgb_image \
    camera_info_topic:=/camera_info \
    approx_sync:=true\
    visual_odometry:=false\
    odom_topic:="/odometry/filtered "
