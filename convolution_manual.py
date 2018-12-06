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
import numpy as np
from math import ceil
import imageio 
import scipy.misc

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

  pass