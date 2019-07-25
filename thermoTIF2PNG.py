# -*- coding: utf-8 -*-
"""
thermoTIF2PNG.py
25.07.2019
Landon Halloran (www.ljsh.ca)
github.com/lhalloran

Simple script to do a batch conversion of TIFF files from a thermal 
camera (e.g. SenseFly ThermoMap) to PNG files. Useful for rapid 
analysis of thermal data before more stitching, radiometric, etc. 

The script can also do a global normalisation of values.

This should work for other non-thermal imagery applications too,
as long as the input is a greyscale TIFF. A small modification would
adapt the script to other input/output formats too...

Options: 
- colour map 
  (see https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html)
- normalisation of max/min values based on individual files OR 
  on max/min across all files
"""
# import the good stuff...
import matplotlib.image as mplimg
import matplotlib.pyplot as plt
import numpy as np
import os
import skimage.io

#### USER DEFINES THESE ####
foldername = 'example_input/' # folder with tiff files (and only tiff files!)
colourmap = 'coolwarm' # a colo(u)rmap of your choosing (e.g.,  'hot', 'coolwarm', 'viridis', 'gray')
globalrange = True # normalise to max/min accross all files?
############################

# get names of all files in folder
files = []
for file in sorted(os.listdir(foldername)):
    files.append(file)

# create 'png' subdirectory if non-existant
if not os.path.exists(foldername+'png'):
    os.makedirs(foldername+'png')

# determine global min and max values
if globalrange:
    globmin=1E8 # init values
    globmax=-1E6
    filemax=''
    filemin=''
    print('thermoTIF2PNG.py determining maximum and minimum values across all files...')
    for filenow in files:
        img = skimage.io.imread(foldername+filenow, plugin='tifffile')
        img_arr = np.array(img)
        if np.max(img_arr)>globmax:
            globmax=np.max(img_arr)
            filemax=filenow
        if np.min(img_arr)<globmin:
            globmin=np.min(img_arr)
            filemin=filenow
    print('thermoTIF2PNG.py found global max of ' + str(globmax) + ' in file ' + filemax)
    print('                   and global min of ' + str(globmin) + ' in file ' + filemin + '.')
    print('################################################################################')
    
# export images to PNG files
for filenow in files:
    print('thermoTIF2PNG.py processing '+filenow+' ...')
    img = skimage.io.imread(foldername+filenow, plugin='tifffile')
    #plt.imshow(img) # uncomment this line to display the images as they are processing
    img_arr = np.array(img)
    if globalrange:
        mplimg.imsave(foldername+'png/'+filenow+'.png',img_arr,cmap=colourmap,vmin=globmin,vmax=globmax)
    else:
        mplimg.imsave(foldername+'png/'+filenow+'.png',img_arr,cmap=colourmap)