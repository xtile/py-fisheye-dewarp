(Index)
# Dewarp Fisheye Image.

## Fisheye Image has Distortion
![sample_distortion](https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Car_Fisheye.jpg/294px-Car_Fisheye.jpg)
![car_dewarp](Theory_img/dewarp/car_dewarp.jpg)  
Fisheye Image always has some distortions and it is severe in the circular edge region. 

The original fisheye image is circular shape but, we want to dewarp it into rectangular and blend two fisheye images to equirectangular.

The goal of this document is understand how to convert fisheye image to dewarpped image.

![barrel](https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Barrel_distortion.svg/150px-Barrel_distortion.svg.png)

cf) dewarpped fisheye image  has **Barrel distortion**.

## Fisheye Image dewarp
When dewarp the fisheye image, we use three coordinate system.
- **fisheye image** - (u, v) or (x', y')
- **spherecial** - (x, y, z)
- **longitude/latitude** - (x'', y'')

There are two way to generate dewarpped fisheye image.  
(1) fisheye → spherical → longitude/latitude
(2) longitude/latidue → spherical → fisheye

(Let's think in the unit coordinate system first, and later we'll adjust it to the practical use.)

## fisheye → spherical → longitude/latitude

### fisheye(uv) → spherical(xyz)
fisheye image is a kind of part of sphere's projection. So, from fisheye image we can imagine a sphere which has fisheye image as a surface.

![fisheye2spherical](Theory_img/dewarp/fisheye2spherical.jpg)  
The projection between fisheye and sphere is shown below. 

![fisheye2sphere_eq](Theory/Theory_img/ewarp/fisheye2sphere_eq.jpg)

### spherical(xyz) → longitude/latitude
![world map](https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Equirectangular_projection_SW.jpg/600px-Equirectangular_projection_SW.jpg)  
In this time, transfer the pixel in the spehre to longitude/latitude coordinate, like world map.

![sphere](Theory_img/dewarp/sphere.jpg) {: width="80" height="80"}  
![equirect_coord](Theory_img/dewarp/equirect_map.jpg)




## longitude/latitude → spherical → fisheye

## Lens Infromation



## references
- [Wiki - Image Distortion](https://en.wikipedia.org/wiki/Distortion_(optics))  
- [A Practical Distortion Correcting Method from Fisheye
Image to Perspective Projection Image](https://www.semanticscholar.org/paper/A-practical-distortion-correcting-method-from-image-Wang-Liang/3dff7f526f6910e6b104f72f404ef0ebd88bcd7f)  
- [paulbourke](http://paulbourke.net/dome/fish2/)
- [Drawing Equirectangular VR Panoramas with Ruler, Compass, and Protractor](https://www.researchgate.net/publication/324314917_Drawing_Equirectangular_VR_Panoramas_with_Ruler_Compass_and_Protractor)