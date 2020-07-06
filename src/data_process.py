import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import time

print("Environment Ready")

pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_device_from_file("/home/shubham/Documents/centerpoint.bag")
profile = pipe.start(cfg)
colorizer = rs.colorizer()
data_dir = "../tmp2/"
# 1156, 2240,3302
for i in range(0,3307):
    frameset = pipe.wait_for_frames(timeout_ms=35)

    # Aligning depth map with respect to color image
    align = rs.align(rs.stream.color)
    frameset = align.process(frameset)
    # Update color and depth frames:
    color = np.asanyarray(frameset.get_color_frame().get_data())
    aligned_depth_frame = frameset.get_depth_frame()
    colorized_depth = np.asarray(colorizer.colorize(aligned_depth_frame).get_data())

    cv2.imwrite(data_dir+"color/color_frame{0:06}.jpg".format(i),color)
    np.save(data_dir+"depth/depth_frame{0:06}".format(i),np.asanyarray(aligned_depth_frame.get_data()))
    cv2.imwrite(data_dir+"depth_jpg/visdepth_frame{0:06}.jpg".format(i),colorized_depth)
    print("Saved frame:{0:06}".format(i))
   

pipe.stop()

# for x in range(500):
#     pipe.wait_for_frames()


# # Store next frameset for later processing:
# frameset = pipe.wait_for_frames()
# color_frame = frameset.get_color_frame()
# depth_frame = frameset.get_depth_frame()

# # Cleanup:

# pipe.stop()
# print("Frames Captured")


# color = np.asanyarray(color_frame.get_data())
# plt.rcParams["axes.grid"] = False
# plt.rcParams['figure.figsize'] = [12, 6]
# plt.imshow(color)



# colorizer = rs.colorizer()
# colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())
# plt.imshow(colorized_depth)



# # Create alignment primitive with color as its target stream:
# align = rs.align(rs.stream.color)
# frameset = align.process(frameset)

# # Update color and depth frames:
# aligned_depth_frame = frameset.get_depth_frame()
# colorized_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())

# # Show the two frames together:
# images = np.hstack((color, colorized_depth))
# plt.imshow(images)
# plt.show()
