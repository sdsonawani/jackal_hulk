#!/usr/bin/env python
import os
import sys
import PyKDL as KDL
import kdl_parser_py.urdf
import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from gazebo_msgs.srv import GetModelState
from std_srvs.srv import Empty
 
class kdl:
    def __init__(self):
        # self.pose_sub = rospy.Subscriber("irl_truss_pose",PoseStamped,self.poseCallback)
        # self.gt_sub = rospy.Subscriber("irl_truss_pose",PoseStamped,self.gposeCallback)
        self.joint_sub = rospy.Subscriber("joint_states",JointState,self.jointstateCallback)
        # self.trussState = rospy.Service("gazebo/get_model_state",GetModelState,self.getModelstate)
        self.joint1_pub =rospy.Publisher("jackal_hulk/hulk_controller/joint6_position_controller/command",Float64,queue_size = 10)
        self.joint2_pub =rospy.Publisher("jackal_hulk/hulk_controller/joint7_position_controller/command",Float64,queue_size = 10)
        self.joint3_pub =rospy.Publisher("jackal_hulk/hulk_controller/joint8_position_controller/command",Float64,queue_size = 10)
        self.joint4_pub =rospy.Publisher("jackal_hulk/hulk_controller/joint9_position_controller/command",Float64,queue_size = 10)
        self.joint5_pub =rospy.Publisher("jackal_hulk/hulk_controller/joint10_position_controller/command",Float64,queue_size = 10)
        self.joint6_pub =rospy.Publisher("jackal_hulk/hulk_controller/joint11_position_controller/command",Float64,queue_size = 10)
    
        
    # def poseCallback(self, msg):
    #     self.truss_pose = PoseStamped()
    #     self.truss_pose.pose.position = msg.pose.position
    #     # print(self.truss_pose.pose.position)

    # def gposeCallback(self,msg):
    #     self.g_pose = PoseStamped()
    #     self.g_pose.pose.position = msg.pose.position

    def jointstateCallback(self,msg):
        joint_state = JointState()
        joint_state.position  = msg.position
        # print(joint_state.position[0])
        self.joints = np.ones((1,6))
        for i in range(6):
            self.joints[0,i] = joint_state.position[i+3]
        # print(self.joints[0,2])


    def state_output(self,var):
        state = Float64()
        state.data = var
        return state.data


    def ikSolve(self):        
        
        hulk_kdl_tree = kdl_parser_py.urdf.treeFromFile("/home/local/ASURITE/sdsonawa/catkin_ws/src/jackal/urdf/robot.urdf")[1]
        hulk_transform = hulk_kdl_tree.getChain("base_link","fake_end_effector_link")
        print("Finding Transform Between base_link and end_effector_link")
        kdl_fk = KDL.ChainFkSolverPos_recursive(hulk_transform)
        kdl_ik = KDL.ChainIkSolverPos_LMA(hulk_transform)
        kdl_input = KDL.JntArray(6)
        kdl_init = KDL.JntArray(6)
        for i in range(5):
            kdl_init[i] = self.joints[0,i]
        kdl_output = KDL.Frame()
        
        ########################################
        ## offset below provide static transformation between link_0 and camera_link
        x_offset = 0.334
        y_offset = 0.16
        z_offset = 0.59 -0.35
        ########################################
        initial = True
        # if (initial):
        # kdl_output.p[0] = 0 + x_offset
        # kdl_output.p[1] = -2 + y_offset
        # kdl_output.p[2] = 0 + z_offset
                # initial = False

        # kdl_output.p[0] = self.truss_pose.pose.position.z + x_offset
        # kdl_output.p[1] = -self.truss_pose.pose.position.x - y_offset
        # kdl_output.p[2] =  z_offset  - self.truss_pose.pose.position.y 

        kdl_output.p[0] = 0.3 
        kdl_output.p[1] = 0.3
        kdl_output.p[2] = 0.0
       
        
        
        
        t_0 = rospy.get_time()
        kdl_ik.CartToJnt(kdl_init, kdl_output, kdl_input)
        t_1 = rospy.get_time()
        delta = t_1 - t_0
        print(kdl_input[0])
        print(kdl_input[1])
        print(kdl_input[2])
        print(kdl_input[3])
        print(kdl_input[4])


        self.joint1_pub.publish(self.state_output(kdl_input[0]))
        self.joint2_pub.publish(self.state_output(kdl_input[1]))
        self.joint3_pub.publish(self.state_output(kdl_input[2]))
        self.joint4_pub.publish(self.state_output(kdl_input[3]))
        self.joint5_pub.publish(self.state_output(kdl_input[4]))
        self.joint6_pub.publish(self.state_output(kdl_input[5]))
        # print("Publishing Ik Solution on Joints ROS Topics")
        # print("Ik Solution found in [%f] Seconds", delta)

        




def Main(args):
    object = kdl()
    rospy.init_node("hulk_manipulation",anonymous=True)
    rate = rospy.Rate(10)
    # rospy.wait_for_service('/gazebo/reset_world')
    # reset_world = rospy.ServiceProxy('/gazebo/reset_world',Empty)
    while not rospy.is_shutdown():
        try:
            object.ikSolve()
            # print(object.getModelstate())

        except KeyboardInterrupt:
            print("Shutting the node down")
        # reset_world()
        rate.sleep()


    
    
if __name__ == '__main__':
    Main(sys.argv)
    