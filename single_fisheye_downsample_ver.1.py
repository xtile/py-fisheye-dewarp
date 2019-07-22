import sys, time
from PIL import Image
import numpy as np
import math

# IF input image has too high resolution,
# it is better to downsample the input
# before fisheye image dewarpping.

def downsampling(PathIn, ratio):
    #source Image load
    src = np.array(Image.open(PathIn), np.uint8)

    # result ndarray generate
    out = np.zeros((int(src.shape[0]*ratio), int(src.shape[1]*ratio), 3, ), dtype = np.uint8)

    # downsampling
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i][j] = src[int(i/ratio)][int(j/ratio)]

    # Save result    
    return out

def single_fisheye_DownSample(PathIn, center, radius, aperture):

    # read fisheye image
    ## shape of 'img' array = N×N×3 (row×col×channel)
    img = np.array(Image.open(PathIn), np.uint8)
    
    # Down Sampling
    ratio = 0.5
    
    # result ndarray generate
    out = np.zeros((int(img.shape[0]*ratio), int(img.shape[1]*ratio), 3, ), dtype = np.uint8)

    # downsampling
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i][j] = img[int(i/ratio)][int(j/ratio)]
    center[0]=int(center[0]*ratio)
    center[1]=int(center[1]*ratio)
    radius = int(radius*ratio)
    
    # error 
    if (img.shape[0] < center[1]):
        print("wrong Y center")
    if (img.shape[1] < center[0]):
        print("wrong X center")
    if(img.shape[0] < center[1] + radius or center[1] - radius < 0):
        print("over Y range")
    if(img.shape[1] < center[0] + radius or center[0] - radius < 0):
        print("over X range")
        
    
    print(out.shape)
    

    # fisheye → spherical(xyz) → equirect(longitude/latitude)
    #equirect = np.zeros(shape=(radius,int(radius*(aperture/180)), 3, ), dtype=np.uint8)
    equirect = np.zeros(shape=(radius+1,2*radius+1, 3, ), dtype=np.uint8)
    print(equirect.shape)
    print("# of loops: ", out.shape[0]*out.shape[1])
    a = 0
    for i in range(out.shape[0]): # i: y(=v) = row
        for j in range(out.shape[1]): # j: x(=u) = col                                
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
                
                equirect[latitude][longitude] = out[i][j]
                a=a+1
                sys.stdout.write("\r" + str(a))

    # save dewarpped image
    return equirect


if __name__ == "__main__":
    start = time.time()
    result = single_fisheye_DownSample('./test_image/front.jpg', [1550, 1490], 1520, 190)
    end = time.time() - start
    print("single fisheye image: %d sec" %end)
    
    #phi =  (r / radius) * aperture / 2 # degree
    #theta = math.atan2((i-img.shape[0]/2), (j-img.shape[1]/2)) * (180/ math.pi) # degree