import os, sys, time
import numpy as np
from PIL import Image
import math

def rotation(src, rotation):
    out = np.empty_like(src)

    height = out.shape[0]
    width = out.shape[1]

    # Get rotation matrix
    Rot = get_rotation_matrix(rotation, 'degree')

    for i in range(height):
        for j in range(width):
            lon1, lat1 = rotate_pixel((i, j), Rot, height, width)
            out[i][j] = src[lon1][lat1]
    return out

def get_rotation_matrix(rotation, unit='degree'):
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
    return Rx*Ry*Rz

def rotate_pixel(xy, rot_mat, width, height):
    #lat2 = math.pi*xy[0]/height
    lat2 = math.pi*xy[0]/height
    #lon2 = 2*math.pi*xy[1]/width
    lon2 = 2*math.pi*(xy[1]/width-0.5)
    x2 = math.sin(lat2)*math.cos(lon2)
    y2 = math.sin(lat2)*math.sin(lon2)
    z2 = math.cos(lat2)
    xyz = np.matmul(rot_mat, [x2, y2, z2])
    lon1 = math.acos(xyz[2])
    lat1 = math.atan2(xyz[1], xyz[0])
    if(lat1 < 0 ):
        lat1 += math.pi*2
    
    lon1 = height*lon1/math.pi
    lat1 = width*lat1/(2*math.pi)

    return np.array(lon1, lat1)




if __name__ == "__main__":
    start = time.time()
    img = np.array(Image.open(sys.argv[1]))
    result = rotation(img, (sys.argv[2], sys.argv[3], sys.argv[4]))
    print(time.time()-start)
    print("out", result[200][300], result[800][800])
    Image.fromarray(result).save(sys.argv[5])

# python equirect_rotation2.py scr_img X Y Z out_img
