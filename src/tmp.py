import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cv2
import cmapy

i=1000
color_path         = '/home/shubham/catkin_ws/src/intel/tmp/color/color_frame{0:06}.jpg'.format(i)
org_depth_path     = '/home/shubham/catkin_ws/src/intel/tmp/depth/depth_frame{0:06}.npy'.format(i)
filled_depth_path  = '/home/shubham/catkin_ws/src/intel/tmp/filled_depth/filled_depth_frame{0:06}.npy'.format(i)

color              = cv2.imread(color_path)
org_depth          = np.load(org_depth_path)
filled_depth       = np.load(filled_depth_path)

print(np.max(filled_depth))

fig, ax = plt.subplots(1,3)
ax[0].imshow(color)
ax[1].imshow(org_depth,cmap='plasma')
ax[2].imshow(filled_depth,cmap='plasma')
plt.show()