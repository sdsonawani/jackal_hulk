import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2
import os
import sys
import rosbag
from matplotlib import cm
import matplotlib.pyplot as plt

path_to_data_dir = "/home/shubham/rosbags/data"
path_to_rosbag = ""

class Data:
    def __init__(self,path=path_to_data_dir):
        '''
        Read rostopics and save as jpg for color and 
        npy as depth values
        '''
        rospy.init_node("data",anonymous=True)
        # temp_sub  = rospy.Subscriber("/camera/aligned_depth_to_color/image_raw",Image,callback=self.tmpImageCallback)
        # depth_sub = rospy.Subscriber("/device_0/sensor_0/Depth_0/image/data",Image,callback=self.depthImageCallback)
        # color_sub = rospy.Subscriber("/device_0/sensor_1/Color_0/image/data",Image,callback=self.colorImageCallback)
        depth_sub = rospy.Subscriber("/camera/aligned_depth_to_color/image_raw",Image,callback=self.depthImageCallback)
        color_sub = rospy.Subscriber("/camera/color/image_raw",Image,callback=self.colorImageCallback)

        # pose_sub  = rospy.Subscriber("/projected_truss_pose",PoseStamped,callback=self.poseCallback)
        
        self.path        = path
        self.color_image = Image()
        self.depth_image = Image()
        self.tmp_image   = Image()
        # self.pose        = PoseStamped()
        self.bridge      = CvBridge()
        self.flag        = False

    def tmpImageCallback(self,msg):
        if msg.data:
            self.flag = True
        else: 
            print("No data recieved")
        self.tmp_image = msg
        
    def save_tmp(self,stamp):
        tmp_cv = self.bridge.imgmsg_to_cv2(self.tmp_image,desired_encoding='16UC1')
        np.save(self.path+"/tmp_frame{0:06}".format(stamp),tmp_cv)
        

    def ros_init(self):
        rospy.spin()

    def colorImageCallback(self,color):
        if(color.data == None):
            raise ValueError("No data recieved. Check color image topic name!!\n")
        else:
            # print("Recieved Color Image!!\n")
            # pass
            self.flag = True
        self.color_image = self.bridge.imgmsg_to_cv2(color,desired_encoding="rgb8")

        # Testing Msgs
        # print(color.encoding)
        # bridge = CvBridge()
        # cv_raw_color = bridge.imgmsg_to_cv2(self.color_image,desired_encoding="rgb8")
        # cv2.imshow("image",cv_raw_color)
        # cv2.waitKey(3)
              

    def depthImageCallback(self,depth):       
        if (depth.data == None):
            raise ValueError("No data recieved. Check depth image topic name!!\n")
        else:
            # print("Recieved Depth Image !!\n")
            pass
            
        self.depth_image = self.bridge.imgmsg_to_cv2(depth,desired_encoding="16UC1")

        # Testing Msgs 
        # print(depth.encoding)
        # bridge = CvBridge()
        # cv_raw_depth = bridge.imgmsg_to_cv2(self.depth_image,desired_encoding="16UC1")
        # cv2.normalize(cv_raw_depth,cv_raw_depth,0,65536,cv2.NORM_MINMAX,cv2.CV_16UC1)  
        # cv2.imshow("depth",cv_raw_depth)
        # cv2.waitKey(3)

    

    def poseCallback(self,data):
        self.pose = data
          

    def save_data(self,stamp):
        # trans = np.array([[self.pose.pose.position.x,
        #                    self.pose.pose.position.y,
        #                    self.pose.pose.position.z]])

        # quat = np.array([[self.pose.pose.orientation.w,
        #                   self.pose.pose.orientation.x,
        #                   self.pose.pose.orientation.y,
        #                   self.pose.pose.orientation.z]])
        
        # object_pose = np.concatenate((trans,quat),axis=1)        
        # cv_depth_copy = np.copy(self.depth_image)
        # cv2.normalize(cv_depth_copy,cv_depth_copy,0,65536,cv2.NORM_MINMAX,cv2.CV_16UC1)  
        
        # cv_color = np.asarray(cv_raw_color)
        # cv_depth = np.asarray(cv_raw_depth)

        # Saving all the data
        cv2.imwrite(self.path+"/color/color_frame{0:06}.jpg".format(stamp),self.color_image)
        np.save(self.path+"/depth/depth_frame{0:06}".format(stamp),np.asarray(self.depth_image))
        # np.savetxt(self.path+"/pose/pose_frame{0:06}.txt".format(stamp),object_pose)
        plt.imsave(self.path+"/depth_jpg/visdepth_frame{0:06}.jpg".format(stamp),np.asarray(self.depth_image),cmap='plasma')
        # cv2.imshow("Image window", cv_depth_copy)
        # cv2.waitKey(3)


if __name__ == "__main__":
    path = sys.argv[1]
    data = Data(path=path)   
    rate = rospy.Rate(30)
    stamp = 0
    try:
        while not rospy.is_shutdown():
            rate.sleep()
            if (data.flag):
                data.save_data(stamp)
                # data.save_tmp(stamp)
                print("saved image: frame{0:06}".format(stamp))
                stamp += 1
            else: 
                print("Waiting for topics !")
    except KeyboardInterrupt:
        print("\nfinished saving data!!")
