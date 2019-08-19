# py-fisheye-dewarp

## requirement
- python 3

- numpy
- scipy
- opencv


## description
convert fisheye image to dewarpped image

## Detail Distctiption & Theory
[https://github.com/BlueHorn07/py-fisheye-dewarp/wiki](https://github.com/BlueHorn07/py-fisheye-dewarp/wiki)


## Codes
### single_fisheye.py
dewarp one single fisheye image.

### sinlge_fisheye_downsample.py
dewarp one single fisheye image with down-sampling.

### equirect_rotation.py
rotate an equirectagnular image.
**efficiency** - 1024 x 512 image => 1.8 sec (intel Core i7)

### equirect_rotation(slow).py
rotate an equirectangular image.  
**efficiency** - 1024 x 512 image => 9~10 sec (intel Core i7)
