#!/usr/bin/env python3
# chmod u+x
# -*- coding: utf-8 -*-  

"""
Author: Thiago Santos

In in this file we have built a code to run a convolution with a giving/default filter/weight in a list of images. 
With the results, we can then run the code idx3_format.py to format all to idx3.

convert 1.png -compress none x.ppm

"""
import numpy as np
import random
import sys
import os
from convolution_manual import *

def read_RGB_image(img_path):
  RGB_Imgs = []
  try:
    img = []
    with open(img_path, "r") as fp:
      fp.readline()
      w_h = fp.readline().strip().split()
      width, height = int(w_h[0]), int(w_h[1])
      fp.readline()
      img = np.array([int(x) for x in fp.read().strip().split()]).reshape(height, width, 3).astype(np.uint8)
      img = img.transpose()
  except Exception as e:
    print("Img " + str(img_path) + " do not exist")
    print(e)
    sys.exit(1)

  return img

def eye_finder(R_img, G_img, B_img):
  width,height = get_width_height(R_img)
  R_Conv_Img = convolutional(R_img,width,height)
  G_Conv_Img = convolutional(G_img,width,height)
  B_Conv_Img = convolutional(B_img,width,height)

  display_img( np.absolute(R_img - G_img ) )
  display_img( np.absolute(R_img - B_img ) )
  display_img( np.absolute(G_img - B_img ) )
  display_img( np.absolute(R_img - G_img - B_img ) )

  display_img( np.absolute(R_Conv_Img - G_Conv_Img ) )
  display_img( np.absolute(R_Conv_Img - B_Conv_Img ) )
  display_img( np.absolute(G_Conv_Img - B_Conv_Img ) )
  display_img( np.absolute(R_Conv_Img - G_Conv_Img - B_Conv_Img ) )

if __name__ == '__main__':

  img_file = "Dataset/x.ppm"
  if len(sys.argv) >= 2:
    img_file = sys.argv[1]
    
  RGB_Imgs = read_RGB_image(img_file)
  R_img,G_img,B_img =  RGB_Imgs[0][:][:].transpose(), RGB_Imgs[1][:][:].transpose(), RGB_Imgs[2][:][:].transpose()

  eye_finder(R_img,G_img,B_img)

