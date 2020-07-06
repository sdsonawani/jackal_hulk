import cv2
import numpy as np
import sys
import time

print("path number and hz")
path = "/home/local/ASURITE/sdsonawa/catkin_ws/src/intel/src/tmp"
# sys.argv[1
number  = int(sys.argv[1])
hz = float(sys.argv[2])
img = []
# out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(*"MJPG"), hz, (480,1920))
for i in range(100,number):
    time.sleep(0.2)
    color = cv2.imread(path+"/color/color_{0:06}.jpg".format(i))
    depth = cv2.imread(path+"/depth/depth_{0:06}.jpg".format(i))
    # print(color.shape)
    # print(type(depth))
    print("adding video frame {0:06}".format(i))
    image = np.hstack((color,depth))
    print(image.shape)
    cv2.imshow("test",image)
    img.append(image)
    cv2.waitKey(2)
    # out.write(image)

out =  cv2.VideoWriter('Blender.avi',cv2.VideoWriter_fourcc(*"MJPG"), hz, (480,1920))

for i in range(len(img)):
    print("adding frame")
    out.write(img[i])


out.release
