#!/usr/bin/env python3
# chmod u+x
# -*- coding: utf-8 -*-  

"""
Author: Thiago Santos

In in this file we have built a code to run a convolution with a giving/default filter/weight in a list of images. 
With the results, we can then run the code idx3_format.py to format all to idx3.

convert 1.png -compress none x.ppm

"""

import matplotlib.pyplot as plt
#from scipy import misc
import numpy as np
from math import ceil
import random
import imageio 
import sys
from math import ceil
import scipy.misc
import os

def read_RGB_image(img_path):
  RGB_Imgs = []
  try:
    #img = np.array(imageio.imread(img_path), dtype=np.uint8)
    with open(img_path, "r") as fp:
      fp.readline()
      w_h = fp.readline().strip().split()
      width, height = int(w_h[0]), int(w_h[1])
      pixes = np.zeros((height,width*3), dtype=int)
      RGB_Imgs = np.zeros((3,height,width), dtype=int)
      fp.readline()
      to_save = []
      h=0
      for line in fp:
        values = [int(i) for i in line.split()] 
        if len(values) == width *3:
          pixes[h] = np.array(values)
          h+=1
        elif len(values) >= 0:
          to_save += values
          if len(to_save) == width *3:
            pixes[h] = np.array(to_save)
            h+=1
            to_save = []

      RGB_Imgs[0] = pixes[ : , ::3]
      RGB_Imgs[1] = pixes[ : , 1::3]
      RGB_Imgs[2] = pixes[ : , 2::3]

  except Exception as e:
    print("Img " + str(img_path) + " do not exist")
    print(e)
    sys.exit(1)

  return RGB_Imgs

def display_img(img):
  # Plot the input
  plt.subplot(223)
  plt.imshow(img, cmap=plt.cm.gray)
  plt.axis('off')
  plt.show()



def save_img(img, path_to='dataset/out.pgm'):
  imageio.imwrite(path_to, img[:, :])

def get_width_height(img):
  return [len(img[0]), len(img)]


def convolutional(img, width,height, filter_conv=[[0,-1,0], [-1,4,-1], [0,-1,0]], h_stride=1, v_tride=1, paddings=0, out_half_size=False):

  fw = len(filter_conv[0])
  fh = len(filter_conv)

  w_out = ceil( ( (width - fw + (2*paddings)) // h_stride) + 1)
  h_out = ceil( ( (height - fh + (2*paddings)) // v_tride) + 1)

  output_img_conv = np.zeros((h_out,w_out),dtype=np.uint8)

  index_h = index_w = 0
  sum_dot = 0
  # for all "smalls" filters going trough the image
  for line_height in range(0,h_out,h_stride):
    for line_weidth in range(0,w_out,v_tride):
      sum_dot = 0
      # inside of the small part part image
      # use these indexes for the filter
      for pixel_height in range(fh):
        for pixel_weight in range(fw):
          sum_dot += filter_conv[pixel_height][pixel_weight] * img[line_height+pixel_height][line_weidth+pixel_weight]

      # ReLu the pixel, and make sure it goes just till 255, cause we are working with chromatic pics
      sum_dot = max(0,min(sum_dot,255))

      output_img_conv[line_height][line_weidth] = sum_dot

  # return half of the size
  if out_half_size:
    return  scipy.misc.imresize(np.pad(output_img_conv, (1,1), 'constant', constant_values=(0, 0)), (height//2, width//2))
  
  return np.pad(output_img_conv, (1,1), 'constant', constant_values=(0, 0))


if __name__ == '__main__':

  img_file = "Dataset/x.ppm"
  RGB_Imgs = read_RGB_image(img_file)
  R_Img,G_Img,B_Img = RGB_Imgs[0], RGB_Imgs[1], RGB_Imgs[2]
  width,height = get_width_height(R_Img)
  # display_img(R_Img)
  # display_img(G_Img)
  # display_img(B_Img)
  #img = convolutional(img,width,height)
  R_Conv_Img = convolutional(R_Img,width,height)
  G_Conv_Img = convolutional(G_Img,width,height)
  B_Conv_Img = convolutional(B_Img,width,height)

  display_img(R_Img)
  display_img(R_Conv_Img)

  display_img(G_Img)
  display_img(G_Conv_Img)

  display_img(B_Img)
  display_img(B_Conv_Img)
