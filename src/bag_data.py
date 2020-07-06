import rosbag 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
import cv2
import sys
import os
import time

path2bag = sys.argv[1]
path2data = sys.argv[2]

bag  =  rosbag.Bag(path2bag)
stamp_color = 1155
stamp_depth = 1155

bridge = CvBridge()

for topic,msg,t in bag.read_messages(["/device_0/sensor_1/Color_0/image/data", "/device_0/sensor_0/Depth_0/image/data"]):
   
    if topic == "/device_0/sensor_1/Color_0/image/data":
        color_image = bridge.imgmsg_to_cv2(msg,desired_encoding='rgb8')
        cv2.imwrite(path2data+"/color/color_frame{0:06}.jpg".format(stamp_color),color_image)
        print("saved color image frame: {0:06}".format(stamp_color))
        stamp_color += 1
    
    elif topic == "/device_0/sensor_0/Depth_0/image/data":
        depth_image = bridge.imgmsg_to_cv2(msg,desired_encoding='mono16')
        np.save(path2data+"/depth/depth_frame{0:06}".format(stamp_depth),np.asarray(depth_image))
        cv_depth_copy = np.copy(depth_image)
        cv2.normalize(cv_depth_copy,cv_depth_copy,0,65536,cv2.NORM_MINMAX,cv2.CV_16UC1)  
        # cv2.imwrite(path2data+"/depth_jpg/visdepth_frame{0:06}.jpg".format(stamp_depth),cv_depth_copy)
        plt.imsave(path2data+"/depth_jpg/visdepth_frame{0:06}.jpg".format(stamp_depth),cv_depth_copy,cmap="plasma")
        print("saved depth image frame: {0:06} \n".format(stamp_depth))
        stamp_depth += 1
    
    if stamp_color == 2240 and stamp_depth == 2240:
        break
    