# Dewarp Fisheye Image.
[한국판(KOR)]()

[TOC]

## Fisheye Image has Distortion
<img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Car_Fisheye.jpg/294px-Car_Fisheye.jpg"  width="40%"> <img src="Theory_img/dewarp/car_dewarp.jpg"  width="40%">


**Fisheye Image** always has some distortions and it is severe in the circular edge region. 

The original fisheye image is circular shape but, we want to dewarp it into rectangular and blend two fisheye images to equirectangular.

The goal of this document is to understand how to convert fisheye image to dewarpped image.


<center><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Barrel_distortion.svg/150px-Barrel_distortion.svg.png"  width="30%"></center><br>

cf) dewarpped fisheye image  has **Barrel distortion**.

## Fisheye Image dewarp
When dewarp the fisheye image, we use three coordinate systems.
- **fisheye image** - (u, v) or (x', y')
- **spherecial** - (x, y, z)
- **longitude/latitude** - (x'', y'')

And there are two ways to generate dewarpped fisheye image.  
(1) fisheye → spherical → longitude/latitude  
(2) longitude/latitude → spherical → fisheye

(Let's think in the unit coordinate system first, and later we'll adapt it to the practical use.)

## fisheye → spherical → longitude/latitude

### fisheye(uv) → spherical(xyz)
fisheye image is a kind of **sphere's projection image**. So, from fisheye image we can imagine a sphere which has fisheye image as a surface.

<center><img src="Theory_img/dewarp/fisheye2spherical.jpg" width="60%"></center><br>

The projection between fisheye and sphere is shown below. 

<center><img src="Theory_img/dewarp/fisheye2sphere_eq.jpg"  width="55%"></center><br>

### spherical(xyz) → longitude/latitude(x''y'')
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Equirectangular_projection_SW.jpg/600px-Equirectangular_projection_SW.jpg"  width="55%"><br>
In this time, transfer the pixel in the spehre to longitude/latitude coordinate, like world map.

<img src="Theory_img/dewarp/spherical2equirect.jpg"  width="70%"><br>

<img src="Theory_img/dewarp/sphere2equirect.jpg" width="55%">

But, if you write your code in this way, there's must be some **black dot areas** that doesn't match from the fisheye image.  

<img src="Theory_img/dewarp/forward_dewarp.jpg" width="50%">

The reason is **it's impossible to make a square which has equal-area with a circle.** (cf. it is also applied in discrete world)

Due to the problem of the above method, this time, we will try the inverse way.

## longitude/latitude → spherical → fisheye

### longitude/latitdue(x''y'') → spherical(xyz)
<img src="Theory_img/dewarp/equirect2spherical.jpg" width="60%"><br>
<img src="Theory_img/dewarp/equirect2spherical_eq.jpg" width="55%"><br>
(**R**, raidus of the sphere is 'one' if it is an unit sphere.)

### spherical(xyz) → fisheye(uv)
<img src="Theory_img/dewarp/spherical2fisheye.jpg" width="60%"><br>
(aperture's unit is **radian**.(Because `atan2` function returns radian.))

In this way, there's no unmatched pixel in the long/lat image.  
<img src="Theory_img/dewarp/car_dewarp.jpg"  width="80%">

## Lens Information
Before we process our fisheye image, we necessarily know the Lens information.

- Center of Lens
- Radius
- Aperture


## references
- [Wiki - Image Distortion](https://en.wikipedia.org/wiki/Distortion_(optics))  
- [A Practical Distortion Correcting Method from Fisheye
Image to Perspective Projection Image](https://www.semanticscholar.org/paper/A-practical-distortion-correcting-method-from-image-Wang-Liang/3dff7f526f6910e6b104f72f404ef0ebd88bcd7f)  
- [paulbourke](http://paulbourke.net/dome/fish2/)
- [Drawing Equirectangular VR Panoramas with Ruler, Compass, and Protractor](https://www.researchgate.net/publication/324314917_Drawing_Equirectangular_VR_Panoramas_with_Ruler_Compass_and_Protractor)
