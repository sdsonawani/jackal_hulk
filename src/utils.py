import os
import cv2
import numpy as np
from tqdm import tqdm
import random
# import matplotlib.pyplot as plt
import pandas as pd
import json
import tensorflow as tf
import keras.backend as K


path = "small_space_dataset"
max_depth = 10.0

def load_data(data_set_path=path):
    max_depth_ = 0
    # print("Checking what the path : {}".format(data_set_path))
    if os.path.isdir(os.path.join(data_set_path,"train")) and os.path.isdir(os.path.join(data_set_path,"test")):
        print("Using pre splitted data!!!")
        train_x = os.path.join(data_set_path,"train/color")
        train_y = os.path.join(data_set_path,"train/depth")

        test_x = os.path.join(data_set_path,"test/color")
        test_y = os.path.join(data_set_path,"test/depth")

        train_x_files = sorted([files for files in os.listdir(train_x)])
        train_y_files = sorted([files for files in os.listdir(train_y)])
        
        test_x_files = sorted([files for files in os.listdir(test_x)])
        test_y_files = sorted([files for files in os.listdir(test_y)])


        data_train_x = []
        data_train_y = []
        data_test_x = []
        data_test_y = []
        print("loading train data")
        for imgs in tqdm(train_x_files):
            image = cv2.imread(os.path.join(train_x,imgs))
            data_train_x.append(image) 
        
        for depth in tqdm(train_y_files):
            d_image = np.load(os.path.join(train_y,depth))
            d_image /= max_depth
            d_image = d_image[...,np.newaxis]
            data_train_y.append(d_image)
        
        print("loading test data")
        for imgs in tqdm(test_x_files):
            image = cv2.imread(os.path.join(test_x,imgs))
            data_test_x.append(image) 
        
        for depth in tqdm(test_y_files):
            d_image = np.load(os.path.join(test_y,depth))
            d_image /= max_depth
            d_image = d_image[...,np.newaxis]
            data_test_y.append(d_image)
        
        data_train_x = np.asarray(data_train_x)
        data_train_y = np.asarray(data_train_y)
        data_test_x  = np.asarray(data_test_x)
        data_test_y  = np.asarray(data_test_y)

        print(data_train_x.shape)
        print(data_train_y.shape)
        print(data_test_x.shape)
        print(data_test_y.shape)

        return data_train_x,data_train_y,data_test_x,data_test_y
    
    else:
        print("Using complete data!!!")
        # train_x = os.path.join(data_set_path,"/color")
        # train_y = os.path.join(data_set_path,"/depth")
        
        train_x = data_set_path+"/color/"
        train_y = data_set_path+"/depth/"



        train_x_files = sorted([files for files in os.listdir(train_x)])
        train_y_files = sorted([files for files in os.listdir(train_y)])

        data_train_x = []
        data_train_y = []

        print("Waiting while loading data")
        for imgs in tqdm(train_x_files):
            image = cv2.imread(os.path.join(train_x,imgs))
            data_train_x.append(image) 
        
        for depth in tqdm(train_y_files):
            d_image = np.load(os.path.join(train_y,depth))/1000.0
            max_depth_ += np.max(d_image)
            # max_depth 
            # d_image /= max_depth
            d_image = d_image[...,np.newaxis]
            data_train_y.append(d_image)

        data_train_x = np.asarray(data_train_x)

        max_depth_ = max_depth_ / data_train_x.shape[0]
        print("\n\n\n Average Max Depth {}\n\n\n".format(max_depth_))
        data_train_y = np.asarray(data_train_y)/max_depth_

        return data_train_x,data_train_y,None,None,max_depth_
# load_data()