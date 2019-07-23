(Index)
# Dewarp Fisheye Image.

## Fisheye Image has Distortion
<img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Car_Fisheye.jpg/294px-Car_Fisheye.jpg"  width="40%"> <img src="Theory_img/dewarp/car_dewarp.jpg"  width="40%">


Fisheye Image always has some distortions and it is severe in the circular edge region. 

The original fisheye image is circular shape but, we want to dewarp it into rectangular and blend two fisheye images to equirectangular.

The goal of this document is understand how to convert fisheye image to dewarpped image.


<center><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Barrel_distortion.svg/150px-Barrel_distortion.svg.png"  width="30%"></center> 


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
fisheye image is a kind of sphere's projection image. So, from fisheye image we can imagine a sphere which has fisheye image as a surface.

<center><img src="Theory_img/dewarp/fisheye2spherical.jpg" width="60%"></center

The projection between fisheye and sphere is shown below. 

<center><img src="Theory_img/dewarp/fisheye2sphere_eq.jpg"  width="60%"></center>

### spherical(xyz) → longitude/latitude
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Equirectangular_projection_SW.jpg/600px-Equirectangular_projection_SW.jpg"  width="60%"><br>
In this time, transfer the pixel in the spehre to longitude/latitude coordinate, like world map.

<img src="Theory_img/dewarp/sphere.jpg"  width="40%"><br>

<img src="Theory_img/dewarp/equirect_map.jpg"  width="40%"><br>

<img src="Theory_img/dewarp/sphere2equirect.jpg">

But, if you construct your code in this way, there's must be some **black dot areas** that cannot fullly match to fisheye image to longitude/latitude map.  

Because, **it's impossible to make a squre which has equal-area with a circle.** (cf. it is also applied in discret world)

<img src="Theory_img/dewarp/forward_dewarp.jpg">

## longitude/latitude → spherical → fisheye

## Lens Infromation



## references
- [Wiki - Image Distortion](https://en.wikipedia.org/wiki/Distortion_(optics))  
- [A Practical Distortion Correcting Method from Fisheye
Image to Perspective Projection Image](https://www.semanticscholar.org/paper/A-practical-distortion-correcting-method-from-image-Wang-Liang/3dff7f526f6910e6b104f72f404ef0ebd88bcd7f)  
- [paulbourke](http://paulbourke.net/dome/fish2/)
- [Drawing Equirectangular VR Panoramas with Ruler, Compass, and Protractor](https://www.researchgate.net/publication/324314917_Drawing_Equirectangular_VR_Panoramas_with_Ruler_Compass_and_Protractor)
