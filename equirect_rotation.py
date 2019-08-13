import os, sys, time
import numpy as np
from PIL import Image
import math

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
    R = Rx*Ry*Rz

    # Get output image 
    out = np.zeros_like(src)

    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            lat2 = i/src.shape[0]*math.pi
            lon2 = (j/src.shape[1] - 0.5)*math.pi
            x2 = math.cos(lat2)*math.cos(lon2)
            y2 = math.cos(lat2)*math.sin(lon2)
            z2 = math.sin(lat2)

            xyz2 = np.array([x2, y2, z2]).reshape(3, 1)
            #print(xyz2)
            xyz = np.matmul(np.transpose(R), xyz2)
           # print(xyz)

            x, y, z = np.split(xyz, 3)
            if(x!=x2):
                print("x2 not equal", xyz, xyz2)
            if(y!=y2):
                print("y2 not equal", xyz, xyz2)
            if(z!=z2):
                print("z2 not equal", xyz, xyz2)
            lat = math.atan2(z, math.sqrt(x**2+y**2))   
            lon = math.atan2(y, x)
         #   print(lat, lon)
            lat=int((lat/math.pi+0.25)*src.shape[0])%src.shape[0]
            lon=int((lon/math.pi+0.5)*src.shape[1])%src.shape[1]
            if(i>200 and j/20==0 and i!=lat):
                print("out", i, j)
                print("src", lat, lon, "\n")
         #   print("lat", lat, "long",lon)  
          #  print("i", i,  "j", j)
            try:
                out[i][j] = src[lat][lon]
            except:
                print("out", i, j)
                print("scr", lat, lon, "\n")

    print(out.shape)
    return out


if __name__ == "__main__":
    start = time.time()
    src = np.array(Image.open(sys.argv[1]))
    result = Equirect_Rotation(src, (sys.argv[2], sys.argv[3], sys.argv[4]))
    print(time.time()-start)
    #print("out", result[200][300], result[800][800])
    Image.fromarray(result).save(sys.argv[5])

# python equirect_rotation.py scr_img X Y Z out_img