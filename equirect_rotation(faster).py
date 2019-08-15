import os, sys, time
import numpy as np
from PIL import Image
import math

def Rot_Matrix(rotation, unit='degree'):
    rotation = np.array(rotation, dtype=float)

    if(unit=='degree'):
        # input's unit of cos, sin function is radian
        rotation = np.deg2rad(rotation)
    elif(unit!='rad'):
        print("ParameterError: "+unit+"is wrong unit!")
        return
    Rx = np.array([[1, 0, 0], [0, math.cos(rotation[0]), -math.sin(rotation[0])], \
        [0, math.sin(rotation[0]), math.cos(rotation[0])]])
    Ry = np.array([[math.cos(rotation[1]), 0, math.sin(rotation[1])],\
        [0, 1, 0], [-math.sin(rotation[1]), 0, math.cos(rotation[1])]])
    Rz = np.array([[math.cos(rotation[2]), -math.sin(rotation[2]), 0], \
        [math.sin(rotation[2]), math.cos(rotation[2]), 0], [0, 0, 1]])
    R = np.matmul(np.matmul(Rx, Ry), Rz)
    return R

def Pixel2LonLat(equirect):
    # LongLat - shape = (N, 2N, (Long, Lat)) 
    Lon = np.array([2*(x/8-0.5)*math.pi for x in range(8)])
    Lat = np.array([(0.5-y/4)*math.pi for y in range(4)])
        
    Lon = np.tile(Lon, (4, 1))
    Lat = np.tile(Lat.reshape(4, 1), (8))

    LonLat = np.dstack((Lon, Lat))
    return LonLat

def LonLat2Sphere(LonLat):
    x = np.cos(LonLat[:, :, 1])*np.cos(LonLat[:, :, 0])
    y = np.cos(LonLat[:, :, 1])*np.sin(LonLat[:, :, 0])
    z = np.sin(LonLat[:, :, 1])

    xyz = np.dstack((x, y, z))
    return xyz

def Sphere2LonLat(xyz):
    Lon = math.pi/2 - np.arccos(xyz[:, :, 2])
    Lat = np.arctan(xyz[:, :, 1], xyz[:, :, 0])

    LonLat = np.dstack((Lon, Lat))
    return LonLat

def LonLat2Pixel(LonLat, width, height):
    j = int(width*(LonLat[:, :, 0]/(2*math.pi)+0.5))%width
    i = int(height*(0.5-(LonLat[:, :, 1]/math.pi)))%height
    
    ij = np.dstack((i, j))
    return ij


def Rot_Equirect(src, rotation):
    if(int(src.shape[0]*2/src.shape[1])!=1):
        print("Source Image is not Equirectangular Image...")
        print(src.shape[0], src.shape[1])
        return
    
    R = Rot_Matrix(rotation)

    out = np.zeros_like(src)
    out_LonLat = Pixel2LonLat(out)
    out_xyz = LonLat2Sphere(out_LonLat)

    src_xyz = np.matmul(np.transpose(R), out_xyz[:, :]) #여기가 문제
    src_LonLat = Sphere2LonLat(src_xyz)
    src_Pixel = LonLat2Pixel(src_LonLat)

    for i in range(src.shape[0]):
        for j in range(src.shape[1]):
            pixel = src_Pixel[i][j]
            out[i][j]=src[pixel[1]][pixel[0]]

    return out


if __name__ == "__main__":
    start = time.time()
    src = np.array(Image.open(sys.argv[1]))
    out = Rot_Equirect(src, (sys.argv[2], sys.argv[3], sys.argv[4]))
    print(time.time()-start)
    Image.fromarray(out).save(sys.argv[5])

