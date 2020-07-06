import rospy
from sensor_msgs.msg import Image, CameraInfo
import cv2
from dd import get_dd
# from loss import depth_loss_function
from cv_bridge import CvBridge
import tensorflow as tf
import tensorboard
import numpy as np
import matplotlib.pyplot as plt


class RUN():
    def __init__(self):
        rospy.init_node("testingDepth",anonymous=True)
        self.model  = get_dd()
        self.model.load_weights('realsense_dd.h5')
        self.rgbImage = Image()
        rospy.Subscriber('/camera/color/image_raw',Image,callback=self.rgbImagecallback)
        rospy.Subscriber('/camera/color/camera_info',CameraInfo,callback=self.cameraInfocallback)
        rospy.Subscriber('/camera/aligned_depth_to_color/image_raw',Image,callback=self.depthImagecallback)

        self.pub_depth = rospy.Publisher('/camera/predicted_depth',Image)
        self.pub_newrgb = rospy.Publisher('/rgb_image',Image)
        self.pub_camera = rospy.Publisher('/camera_info',CameraInfo)
        self.depth_image = Image()
        self.bridge = CvBridge()
        self.camera_info = CameraInfo()
        self.flag = False
        # rospy.Subscriber('/camera/color/image_raw',Image,callback=self.rgbImagecallback)
    
    def cameraInfocallback(self,msg):
        self.camera_info = msg

    def rgbImagecallback(self,msg):
        if msg.data:
            self.flag=True
        self.rgbImage = msg
    def depthImagecallback(self,msg):
        self.depth_image = msg
    
    def publish_data(self, stamp):
        self.rgbImage.header.stamp = rospy.Time.now()
        rgb_cv =  self.bridge.imgmsg_to_cv2(self.rgbImage,desired_encoding='rgb8')
        # color = np.copy(rgb_cv)
        # depth_cv = self.bridge.imgmsg_to_cv2(self.depth_image,desired_encoding='16UC1')
        # depth_cv = depth_cv

        # depth_cv = depth_cv.astype(np.uint8)
        # depth_cv = cv2.applyColorMap(depth_cv,cv2.COLORMAP_JET)

        rgb_cv = rgb_cv[np.newaxis,:]
        predicted_depth =  self.model.predict(rgb_cv)
        predicted_depth = predicted_depth[0,:,:,0]*10000.0
        predicted_depth = predicted_depth.astype(np.uint16)


        ros_depth = self.bridge.cv2_to_imgmsg(predicted_depth,encoding='16UC1')
        ros_depth.header.stamp=self.rgbImage.header.stamp
        ros_depth.header.frame_id =  "camera_color_optical_frame"
        # plt.imshow(predicted_depth,cmap='plasma')
        # plt.show()
        # print(np.max(predicted_depth))
        # predicted_depth = predicted_depth/1000.0
        # predicted_depth = predicted_depth.astype(np.uint8)
        # predicted_depth = cv2.applyColorMap(predicted_depth,cv2.COLORMAP_JET)
        # print("max distances true depth {}, predicted depth {}".format(np.max(depth_cv),np.max(predicted_depth)))
        # image = np.hstack((depth_cv,predicted_depth))
        # plt.imsave("tmp/depth/depth_{0:06}.jpg".format(stamp),image,cmap='plasma')
        # plt.imsave("tmp/color/color_{0:06}.jpg".format(stamp),color)
        # cv2.imshow("test",image)
        self.pub_camera.publish(self.camera_info)
        self.pub_depth.publish(ros_depth)
        self.pub_newrgb.publish(self.rgbImage)
        # cv2.waitKey(2)



if __name__ == "__main__":
    run  = RUN()
    rate = rospy.Rate(30)
    stamp = 0
    while not rospy.is_shutdown():
        try:
            if run.flag:
                run.publish_data(stamp)
                print("predicting depth")
            else: 
                print("waiting for topic!!")
            rate.sleep()
            stamp +=1
        except KeyboardInterrupt:
            print("Shutting down ")