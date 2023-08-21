# -*- coding: utf-8 -*-
"""
Created on Mon May  1 14:26:47 2023

@author: ACORY
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import rawpy
import numpy as np
import cv2

def guiToCropImage(filepath, left_fractionTrimmed, right_fractionTrimmed, bottom_fractionTrimmed, top_fractionTrimmed):
    # Displays a GUI showing the raw image; allows the user to define the edges of the cropped region; returns a cropped image
    # Inputs: (1) filepath to the image in question
    #         (2-5): fractions to implement further cropping by. Using the right_fractionTrimmed as an example, the calculation is:
    #                rightFractionTrimmed = (distance to crop by*)/(distance from the left to right edges of the image)
    #                * this distance traverse the right-to-left direction. A value of zero indicates that the right edge remains the same. 
    #                 .. a distance of >0 indicates that the image will be cropped inwards from the right edge. 
    #         These values (2-5) were determined by inspecting the optodes and ascertaining where the bounds of the "good" optode
    #         region is. The "good" optode region is the region in which the adherence between the optode and the surface of the incubator
    #         is optimal.

    # Read the image
    raw = rawpy.imread(filepath)
    rgb = raw.postprocess()
         
    
    # Extract all three color channels
    allThreeChannels = rgb[:,:,0:3]

    if allThreeChannels is None:
        print("Error: failed to read image file")
        return

    # Check if image dimensions are valid
    if allThreeChannels.shape[0] <= 0 or allThreeChannels.shape[1] <= 0:
        print("Error: invalid image dimensions")
        return

    # Display the image using matplotlib
    plt.imshow(allThreeChannels)
    plt.axis('off')
    plt.show()

    # Allow user to select ROI using plt.ginput()
    pts = plt.ginput(2)
    if len(pts) < 1:
        print("Error: no points selected")
        return
    
    # By calculating the minimum and maximum x and y values of selected points, we can define the outer bounds of the 
    # regoin of interest (roi)
    roi_x1, roi_y1 = np.floor(np.min(pts, axis=0)).astype(int)
    roi_x2, roi_y2 = np.floor(np.max(pts, axis=0)).astype(int)
    
    # Perform an additional cropping step (described at the top of this function) and obtain the final coordinates
    x1, x2, y1, y2 = zoomInByPredeterminedPercentages(roi_x1, roi_x2, roi_y1, roi_y2, left_fractionTrimmed, right_fractionTrimmed, bottom_fractionTrimmed, top_fractionTrimmed)

    plt.close()
    
    return x1, x2, y1, y2

def zoomInByPredeterminedPercentages(x1, x2, y1, y2, left_fractionTrimmed, right_fractionTrimmed, bottom_fractionTrimmed, top_fractionTrimmed): 
    # Zooms into x and y coordinates using pre-determined fraction values. These fraction values, described at the top of "GuiToCropImage", 
    # allow us to crop the image to the "good" optode region (described at the top of "GuiToCropImages")
    
    # Calculate the width and height of the cropped image
    width = abs(x2-x1)
    height = abs(y2-y1)
    
    # Return updated coordinates for cropping using the fraction values provided by the user
    x1_adj = int(x1 + (width*left_fractionTrimmed))
    x2_adj = int(x2- (width*right_fractionTrimmed))
    y1_adj = int(y1 + (height*top_fractionTrimmed))
    y2_adj = int(y2 - (height*bottom_fractionTrimmed))
    
    return x1_adj, x2_adj, y1_adj, y2_adj

def readAndCropImage(imageName, redOrGreen, resolutionDecreaseFactor, xMin, xMax, yMin, yMax): 
    ### reads an image, decreases resolution (if prompted), and crops it. Image returned is either red or green channel. 
    ### Inputs are:
        ###  (1) imageName (cr2 file), 
        ###  (2) red or green, 
        ###  (3) resolution decrease factor (where 4 means you divide resolution by 4)
        ###  (4-7): min and max coordinates for x and y dimension (for cropping)
    
    # Open the raw image file
    raw = rawpy.imread(imageName)
    
    # Get width and height of image, then get new width and height resulting from decreased resolution
    width, height = raw.raw_image.shape[1], raw.raw_image.shape[0]
    newWidth, newHeight = int(width/resolutionDecreaseFactor), int(height/resolutionDecreaseFactor)
    
    # Post-process the raw image to get an RGB image
    rgb = raw.postprocess()
    
    # Scale the image based on image resolution shift
    scaled_image = cv2.resize(rgb, (newWidth, newHeight))
    
    # Extract the red or green channel data
    if redOrGreen=="red":
        specific_channel = scaled_image[:,:,0]
    elif redOrGreen=="green":
        specific_channel = scaled_image[:,:,1]

    # Specify crop coordinates
    x1, x2 = int(xMin/resolutionDecreaseFactor), int(xMax/resolutionDecreaseFactor)
    y1, y2 = int(yMin/resolutionDecreaseFactor), int(yMax/resolutionDecreaseFactor)
    
    # Crop the image
    crop = specific_channel[y1:y2, x1:x2]
    
    return crop

