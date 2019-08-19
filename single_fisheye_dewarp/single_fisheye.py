# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:14:50 2019

@author: HA SEOK YOON
"""

import sys, time
from PIL import Image
import numpy as np
import math

def single_fisheye(PathIn, center, radius, aperture):

    # read fisheye image
    ## shape of 'img' array = N×N×3 (row×col×channel)
    img = np.array(Image.open(PathIn), np.uint8)
    
    
    # error 
    if (img.shape[0] < center[1]):
        print("wrong Y center")
        return
    if (img.shape[1] < center[0]):
        print("wrong X center")
        return
    if(img.shape[0] < center[1] + radius or center[1] - radius < 0):
        print("over Y range")
    if(img.shape[1] < center[0] + radius or center[0] - radius < 0):
        print("over X range")
        
    

    # fisheye → spherical(xyz) → equirect(longitude/latitude)
    #equirect = np.zeros(shape=(radius,int(radius*(aperture/180)), 3, ), dtype=np.uint8)
    equirect = np.zeros(shape=(radius+1,2*radius+1, 3, ), dtype=np.uint8)
    print(equirect.shape)
    print("# of loops: ", img.shape[0]*img.shape[1])
    a = 0
    for i in range(img.shape[0]): # i: y(=v) = row
        for j in range(img.shape[1]): # j: x(=u) = col                                
            r = math.sqrt((j-center[0])**2+(i-center[1])**2)
            if(r <= radius): # inside the fisheye
                
                # fisheye → spherical(xyz)
                ## u axis = x axis / v axis = z axis
                x = j-center[0]
                z = i-center[1]
                
                y = math.sqrt(radius**2-(x**2+z**2))
                
                # spherical(xyz) → equirect(longitude/latitude)
                ## return value of atan2 = [-pi, pi].
                longitude = math.atan2(y, x)
                latitude = math.atan2(z, math.sqrt(x**2+y**2))

                latitude = int((latitude/np.pi+0.5)*radius)
                longitude = int((longitude/np.pi+1)*radius)
                
                equirect[latitude][longitude] = img[i][j]
                a=a+1
                sys.stdout.write("\r" + str(a))

    # save dewarpped image
    return equirect


if __name__ == "__main__":
    start = time.time()
    result = single_fisheye('./test_image/front.jpg', [1550, 1490], 1520, 190)
    end = time.time() - start
    print("single fisheye image: %d sec" %end)
    
    #phi =  (r / radius) * aperture / 2 # degree
    #theta = math.atan2((i-img.shape[0]/2), (j-img.shape[1]/2)) * (180/ math.pi) # degree