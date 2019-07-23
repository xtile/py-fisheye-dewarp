
import sys, time
from PIL import Image
import numpy as np
import math

def single_fisheye(PathIn, center, radius, aperture, out_pixel):
     # read fisheye image
    ## shape of 'img' array = N×N×3 (row×col×channel)
    img = np.array(Image.open(PathIn), np.uint8)
    print(img.shape)

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

    equirect = np.zeros(shape=(out_pixel,2*out_pixel, 3, ), dtype=np.uint8)
    print(equirect.shape)

    for i in range(equirect.shape[0]):
        for j in range(equirect.shape[1]):
            x = radius * math.cos((i/out_pixel-0.5)*np.pi) * math.cos((j/out_pixel-1)*np.pi)
            y = radius * math.cos((i/out_pixel-0.5)*np.pi) * math.sin((j/out_pixel-1)*np.pi)
            z = radius * math.sin((i/out_pixel-0.5)*np.pi)

            r = 2*math.atan2(math.sqrt(x**2+z**2), y)/np.pi*180/aperture*radius
            #r = 2*math.atan2(math.sqrt(x**2+z**2), y)/aperture
            theta = math.atan2(z, x)
            #theta = math.atan2(z, x)

            ###
            u = r*math.cos(theta) + center[0]
            v = r*math.sin(theta) + center[1]
            #print(r, theta, int(u), int(v))
            try:
                equirect[i][j]=img[int(v)][int(u)]
            except:
                equirect[i][j]=[0, 0, 0]
                #print("other side")

    return equirect


if __name__ == "__main__":
    start = time.time()
    #result = single_fisheye('./Theory/Theory_img/1024px_Car_Fisheye.jpg', [1550, 1490], 1520, 190, 400)
    result = single_fisheye('./Theory/Theory_img/1024px_Car_Fisheye.jpg', [513, 497], 483, 190, 400)
    end = time.time() - start
    print("single fisheye image: %d sec" %end)


    Image.fromarray(result).save("./car.jpg")
