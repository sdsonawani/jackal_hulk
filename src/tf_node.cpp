#include<ros/ros.h>

#include<sensor_msgs/Imu.h>
#include<nav_msgs/Odometry.h>
#include <tf/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>

class odometry{

public:

odometry(){
sub_odom = _n.subscribe("jackal_velocity_controller/odom",1000,&odometry::callbackOdom,this);
}


void spin(){
ros::Rate loop(20);
while(ros::ok()){
odometry_pub();
loop.sleep();
}
}

void odometry_pub( ){
nav_msgs::Odometry odom;
geometry_msgs::TransformStamped odom_trans;
odom_trans.header.stamp = ros::Time::now();
odom_trans.header.frame_id = "jackal_velocity_controller/odom";
odom_trans.child_frame_id =  "base_link";
odom_trans.transform.translation.x = pose_x;
odom_trans.transform.translation.y = pose_y;
odom_trans.transform.translation.z = pose_z;
ROS_INFO("X : [%f] and Y : [%f]distance travelled [%f]", pose_x, pose_y, pose_z);
odom_trans.transform.rotation.x = orient_x;//(orient_x); //+ orientZed_x)/2;
odom_trans.transform.rotation.y = orient_y;//(orient_y);// + orientZed_y)/2;
odom_trans.transform.rotation.z = orient_z;//(orient_z);// + orientZed_z)/2;
odom_trans.transform.rotation.w = orient_w;//(orient_w);// + orientZed_w)/2;
odom_broadcaster.sendTransform(odom_trans);
ros::spinOnce();
}




void callbackOdom(const nav_msgs::Odometry::ConstPtr &msg){
pose_x = msg->pose.pose.position.x;
pose_y = msg->pose.pose.position.y;
pose_z = msg->pose.pose.position.z;
orient_x = msg->pose.pose.orientation.x;
orient_y = msg->pose.pose.orientation.y;
orient_z = msg->pose.pose.orientation.z;
orient_w = msg->pose.pose.orientation.w;
}

private:
double pose_x, pose_y,pose_z;
double orient_x, orient_y, orient_z, orient_w;
ros::NodeHandle _n;
ros::Publisher pub; 
ros::Subscriber sub_odom;
tf::TransformBroadcaster odom_broadcaster;
};

int main(int argc, char **argv)
{
ros::init(argc, argv, "tranform_odom");
odometry obj;
obj.spin();
//ros::spin();
return 0;
}
