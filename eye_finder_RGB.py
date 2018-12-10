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

# function to get how many of its closest K neigbors are white.
def dfs_intesity(avlb_pixel, img, i,j, min_y, min_x):
  h = min_y + i
  w = min_x + j
  avlb_pixel[i][j] = 0

  for nbr in [i-1, i+1]:
    if avlb_pixel[nbr][j] ==1:
      if img[h][w] ==255:
        sum_wt +=1
        dfs_intesity(avlb_pixel, img, nbr,j, min_y, min_x)
      else:
        return sum_wt
      


  for nbr in [j-1, j+1]:
    if avlb_pixel[i][nbr] ==1:
      dfs_intesity(avlb_pixel, img, i,nbr, min_y, min_x)


def eye_finder(R_img, G_img, B_img):
  width,height = get_width_height(R_img)
  R_G = np.absolute(R_img - G_img ) 
  R_B = np.absolute(R_img - B_img )
  G_B = np.absolute(G_img - B_img ) 

  # define trashhold
  min_x,max_x = int(width * 0.13),int(width * 0.88)
  min_y,max_y = int(0.2 * height),int(0.65 * height)
  #display_img(R_G)
  #display_img(R_B)
  #display_img(G_B)
  num_p_x = max_x-min_x
  num_p_y = max_y-min_y
  avlb_pixel = np.ones((num_p_y, num_p_x ), dtype=int) # if pixes is available for DFS
  for i in range(num_p_y):
    for j in range(num_p_x):
      if avlb_pixel[i][j] ==1:
        intesity =  dfs_intesity(avlb_pixel,G_B,i,j, min_y, min_x)
        if intesity > 0: # means the area searched has some white pixes(may be an eye) 
          pass

  #wh     = np.argpartition(white_intensity, num_wh)



if __name__ == '__main__':

  img_file = "Dataset/faces_10.ppm"
  if len(sys.argv) >= 2:
    img_file = sys.argv[1]
    
  RGB_Imgs = read_RGB_image(img_file)
  R_img,G_img,B_img =  RGB_Imgs[0][:][:].transpose(), RGB_Imgs[1][:][:].transpose(), RGB_Imgs[2][:][:].transpose()

  eye_finder(R_img,G_img,B_img)

