import os, sys, time
import numpy as np
from PIL import Image
import math
from matplotlib import pyplot as plt

def Equirect_Rotation(src, rotation):
    if(int(src.shape[0]*2/src.shape[1])!=1):
        print("Source Image is not Equirectangular Image...")
        print(src.shape[0], src.shape[1])
        return
    
    # Get Rotation Matrix
    rotation = np.array(rotation, dtype=float)
    rotation = np.radians(rotation)

    Rx = np.array([[1, 0, 0], [0, math.cos(rotation[0]), -math.sin(rotation[0])], \
        [0, math.sin(rotation[0]), math.cos(rotation[0])]])
    Ry = np.array([[math.cos(rotation[1]), 0, math.sin(rotation[1])],\
        [0, 1, 0], [-math.sin(rotation[1]), 0, math.cos(rotation[1])]])
    Rz = np.array([[math.cos(rotation[2]), -math.sin(rotation[2]), 0], \
        [math.sin(rotation[2]), math.cos(rotation[2]), 0], [0, 0, 1]])
    R = np.matmul(np.matmul(Rx, Ry), Rz)

    # Get output image 
    out = np.zeros_like(src)
    longi = list()
    lati = list()
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            # convert to radian unit
            lat2 = (0.5 - i/src.shape[0])*math.pi #(-π/2, +π/2)
            lon2 = 2*(j/src.shape[1] - 0.5)*math.pi #(-π, +π)
            
            # spherical coordinate
            x2 = math.cos(lat2)*math.cos(lon2)
            y2 = math.cos(lat2)*math.sin(lon2)
            z2 = math.sin(lat2)
            xyz2 = np.array([x2, y2, z2]).reshape(3, 1)
            #print(xyz2)

            # original spherical coordinate
            xyz = np.matmul(np.transpose(R), xyz2)
            x, y, z = np.split(xyz, 3)

            lat = math.pi/2 - math.acos(z)
            lon = math.atan2(y, x)

            ### return value
            # acos => [0, π]
            # atan2 => (-π/2, +π/2)
            
            # convert to degree unit and fit in the img size
            j2 = int(src.shape[1]*(lon/(2*math.pi)+0.5))%src.shape[1]
            i2 = int(src.shape[0]*(0.5-(lat/math.pi)))%src.shape[0]

            out[i][j] = src[i2][j2]

    return out


if __name__ == "__main__":
    start = time.time()
    src = np.array(Image.open(sys.argv[1]))
    result = Equirect_Rotation(src, (sys.argv[2], sys.argv[3], sys.argv[4]))
    print(time.time()-start)
    Image.fromarray(result).save(sys.argv[5])

# python equirect_rotation.py scr_img X Y Z out_img