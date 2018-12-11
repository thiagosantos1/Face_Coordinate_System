#!/usr/bin/env python3
# chmod u+x
# -*- coding: utf-8 -*-   

import random as rnd
import sys
import numpy as np
from convolution_manual import *
import cv2

def read_image(img_path):
  try:
    img = np.array(imageio.imread(img_path), dtype=np.uint8)
  except:
    print("Img " + str(img_path) + " do not exist")
    sys.exit(1)

  return img

def get_next(visited):
  for i in range(len(visited)):
    for j in range(len(visited[i])):
      if visited[i][j] == False:
        return [i,j]

  return []

def get_nbrs(visited, s):
  y,x = s[0],s[1]

  n,s,w,e = [],[],[],[]

  if y > 0 :
    n = [y-1, x]
  if x >0:
    w = [y,x-1]
  if y < len(visited) -1:
    s = [y+1, x]
  if x < len(visited[0]) -1:
    e = [y, x+1]

  return [n,s,w,e]

def BFS(visited,min_y_, min_x_):
  
  stg_cpt = [] # save min and max x,y for each component
  while True:
  
    s = get_next(visited)
    if len(s) >0:
      queue = [] 
      queue.append(s) 
  
      visited[s[0]][s[1]] = True

      min_y,min_x = len(visited), len(visited[0])
      max_y,max_x = 0,0

      while queue:
        s = queue.pop(0)
        min_y, min_x = min(min_y,s[0]), min(min_x, s[1])
        max_y, max_x = max(max_y,s[0]), max(max_x, s[1])

        nbrs = get_nbrs(visited, s)
        while nbrs:
          nbr = nbrs.pop(0)
          if len(nbr) >0:
            if visited[nbr[0]][nbr[1]] == False:
              queue.append(nbr)
              visited[nbr[0]][nbr[1]] = True
      stg_cpt.append([min_y + min_y_ , min_x + min_x_ ,max_y + min_y_, max_x + min_x_])

    else:
      break

  return stg_cpt


def eye_finder(img):
  width,height = get_width_height(img)

  # define trashhold
  min_x,max_x = int(width * 0.16),int(width * 0.86)
  min_y,max_y = int(0.2 * height),int(0.65 * height)

  num_p_x = max_x-min_x
  num_p_y = max_y-min_y

  cp_img = img[min_y:max_y, min_x:max_x]
  save_img(cp_img, "center_img.png")

  white_pixels = np.zeros((num_p_y, num_p_x ), dtype=int) # if pixes is available for DFS
  white_pixels = img[min_y:max_y, min_x:max_x] == 255

  visited = white_pixels == False


  return BFS(visited,min_y, min_x)

if __name__ == "__main__":

  np.set_printoptions(threshold=np.nan,linewidth=200)
  img_file = "Dataset/PNG/faces_114.png" # Dataset/PNG/faces_614.png 
  tar1 = 20
  tar2 = 50 

  if len(sys.argv) >= 4:
    img_file = sys.argv[1]
    tar1 = int(sys.argv[2])
    tar2 = int(sys.argv[3])

  elif len(sys.argv) == 2:
    img_file = sys.argv[1]

  img_RGB = read_image(img_file)

  img_grey = cv2.cvtColor(img_RGB, cv2.COLOR_BGR2GRAY)


  w,h = get_width_height(img_grey)

  for i in range(len(img_grey)):
    for j in range(len(img_grey[i])):
      if img_grey[i][j] < tar1 or img_grey[i][j] > tar2:
        img_grey[i][j] = 0
      else:
        img_grey[i][j] = 255

  stg_cpt = eye_finder(img_grey)
  
  for cpt in stg_cpt:
    img_RGB = cv2.rectangle(img_RGB, (cpt[1]-8,cpt[0]-8), (cpt[3]+8,cpt[2]+8), (255,0,100),2)

  save_img(img_grey, "img.png")
  save_img(img_RGB, "out.png")

  display_img(img_RGB)



