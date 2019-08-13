import os, sys, time
import numpy as np
from PIL import Image
import math

def rotation(src, rotation):
    rotation = np.array(rotation, dtype=int)
    rotation = np.radians(rotation)
    Rx = np.array([[1, 0, 0], [0, math.cos(rotation[0]), -math.sin(rotation[0])], \
        [0, math.sin(rotation[0]), math.cos(rotation[0])]])
    Ry = np.array([[math.cos(rotation[1]), 0, math.sin(rotation[1])],\
        [0, 1, 0], [-math.sin(rotation[1]), 0, math.cos(rotation[1])]])
    Rz = np.array([[math.cos(rotation[2]), -math.sin(rotation[2]), 0], \
        [math.sin(rotation[2]), math.cos(rotation[2]), 0], [0, 0, 1]])
    R = Rx*Ry*Rz

    out = np.zeros_like(src)
    if(src.shape[0]*2!=src.shape[1]):
        print("Source Image is not Equirectangular Image...")
        return
    print(src.shape)
    k=0

    log = (()/src.shape[1]-1.0)*math.pi
    lat = (0.5 - i/src.shape[0])*math.pi
    LongLat = np.array()


    for i in range(src.shape[0]):
        for j in range(src.shape[1]):
            #print()
            lon = (j/src.shape[1] - 1.0)*math.pi
            lat = (0.5 - i/src.shape[0])*math.pi
            x = math.cos(lat)*math.cos(lon)
            y = math.cos(lat)*math.sin(lon)
            z = math.sin(lat)
            #print(lat, lon)

            xyz = np.array([x, y, z]).reshape(3, 1)
            #print(xyz)
            xyz2 = np.matmul(R, xyz)
            #print(xyz2)
            x2, y2, z2 = np.split(xyz2, 3)
            lon2 = math.atan2(y2, x2)
            lat2 = math.asin(z2/1)
            lon2=int((lon2/math.pi+1.0)*src.shape[1])
            lat2=int((0.5 - lat2/math.pi)*src.shape[0])
            
            #print("lat2", lat2, "long2",lon2)  
            #print("i", i,  "j", j)
            #try: 
            out[lat2][lon2] = src[i][j]
            """except :
                if lon2 == src.shape[1] :
                     out[lat2][lon2-1]=src[i][j]
                     k=k+1
                else :
                    print("EROO!")
                    return"""
    print("k", k)
    print(out.shape)
    return out


if __name__ == "__main__":
    start = time.time()
    src = np.array(Image.open(sys.argv[1]))
    out = rotation(src, (sys.argv[2], sys.argv[3], sys.argv[4]))
    print(time.time()-start)
    Image.fromarray(out).save(sys.argv[5])

