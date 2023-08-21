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

import pandas as pd

def guiToCropImage(imageName, left_fractionTrimmed, right_fractionTrimmed, bottom_fractionTrimmed, top_fractionTrimmed):
    # read image
    raw = rawpy.imread(imageName)
    rgb = raw.postprocess()
         
    
    # extract all three color channels
    allThreeChannels = rgb[:,:,0:3]
    #redChannel = rgb[:,:,2]

    if allThreeChannels is None:
        print("Error: failed to read image file")
        return

    # check if image dimensions are valid
    if allThreeChannels.shape[0] <= 0 or allThreeChannels.shape[1] <= 0:
        print("Error: invalid image dimensions")
        return

    # display the image using matplotlib
    plt.imshow(allThreeChannels)
    plt.axis('off')
    plt.show()

    # allow user to select ROI using plt.ginput()
    pts = plt.ginput(2)
    if len(pts) < 1:
        print("Error: no points selected")
        return
    roi_x1, roi_y1 = np.floor(np.min(pts, axis=0)).astype(int)
    roi_x2, roi_y2 = np.floor(np.max(pts, axis=0)).astype(int)

    x1, x2, y1, y2 = zoomInByPredeterminedPercentages(roi_x1, roi_x2, roi_y1, roi_y2, left_fractionTrimmed, right_fractionTrimmed, bottom_fractionTrimmed, top_fractionTrimmed)
    # # crop selected roi from image
    plt.close()
    
    roi_cropped = allThreeChannels[y1:y2, x1:x2]
    #red_cropped = redChannel[y1:y2, x1:x2]

    # # show cropped image
    #plt.imshow(red_cropped)
    #plt.axis('off')
    #plt.show()
    #plt.close()
    # # save cropped image as JPEG
    #cv2.imwrite("mediumO2.jpeg", cv2.cvtColor(roi_cropped, cv2.COLOR_BGR2RGB))
    #cv2.imwrite("original.jpeg", cv2.cvtColor(allThreeChannels, cv2.COLOR_BGR2RGB))
    # close all windows
    #plt.close('all')
    #return roi_x1, roi_x2, roi_y1, roi_y2
    return x1, x2, y1, y2

def zoomInByPredeterminedPercentages(x1, x2, y1, y2, left_fractionTrimmed, right_fractionTrimmed, bottom_fractionTrimmed, top_fractionTrimmed): 
    width = abs(x2-x1)
    height = abs(y2-y1)
    x1_adj = int(x1 + (width*left_fractionTrimmed))
    x2_adj = int(x2- (width*right_fractionTrimmed))
    y1_adj = int(y1 + (height*top_fractionTrimmed))
    y2_adj = int(y2 - (height*bottom_fractionTrimmed))
    
    return x1_adj, x2_adj, y1_adj, y2_adj
    #return croppedImage[y1_adj:y2_adj, x1_adj:x2_adj]
def readAndCropImage(imageName, redOrGreen, resolutionDecreaseFactor, xMin, xMax, yMin, yMax): 
    ### reads an image, decreases resolution (if prompted), and crops it. Image returned is either red or green channel. 
    ### Inputs are:
        ###  (1) imageName (cr2 file), 
        ###  (2) red or green, 
        ###  (3) resolution decrease factor (where 4 means you divide resolution by 4)
        ###  (4-7): min and max coordinates for x and y dimension (for cropping)
    
    #       Open the raw image file
    
    raw = rawpy.imread(imageName)
    
    ###     get width and height of image, then get new width and height resulting from decreased resolution
    width, height = raw.raw_image.shape[1], raw.raw_image.shape[0]
    newWidth, newHeight = int(width/resolutionDecreaseFactor), int(height/resolutionDecreaseFactor)
    
    ###     get a dataframe for the image file
    rgb = raw.postprocess()
    
    ###     scale the image based on image resolution shift
    scaled_image = cv2.resize(rgb, (newWidth, newHeight))
    
    ###      Extract the red or green channel data
    if redOrGreen=="red":
        specific_channel = scaled_image[:,:,0]
    elif redOrGreen=="green":
        specific_channel = scaled_image[:,:,1]

    ###     Specify crop coordinates
    x1, x2 = int(xMin/resolutionDecreaseFactor), int(xMax/resolutionDecreaseFactor)
    y1, y2 = int(yMin/resolutionDecreaseFactor), int(yMax/resolutionDecreaseFactor)
    
    
    ###     Crop the image
    crop = specific_channel[y1:y2, x1:x2]
    
    #crop = zoomInByPredeterminedPercentages(crop, 0.3, 0.2, 0.1, 0.6)

    ###      Display and return the cropped image
    # redOrGreen=="red":
        
    #     plt.imshow(crop, cmap='Reds') ## The "reds"argument indicates that intensity will be displayed using a red color bar
    # elif redOrGreen=="green":
    #     plt.imshow(crop, cmap='Greens')
    
    #plt.show()
    return crop

def cropAutomatically(imageName, resolutionDecreaseFactor):
    ### reads an image, decreases resolution (if prompted), creates a binary image of pixels that are brighter than certain threshold, then crops it. 
    ### Inputs are:
    ###  (1) imageName (cr2 file), 
    ###  (2) red or green< Determines if we want to filter by red or green when cropping
    ###  (3) resolution decrease factor (where 4 means you divide resolution by 4)

    # Open the raw image file
    raw = rawpy.imread(imageName)

    ### Get width and height of image, then get new width and height resulting from decreased resolution
    ### Getting shape of the image
    width, height = raw.raw_image.shape[1], raw.raw_image.shape[0]
    newWidth, newHeight = int(width/resolutionDecreaseFactor), int(height/resolutionDecreaseFactor)

    ### Get a dataframe for the image file
    rgb = raw.postprocess()

    ### Scale the image based on image resolution shift
    scaled_image = cv2.resize(rgb, (newWidth, newHeight))

    ### Extract the red or green channel data
    red_channel = scaled_image[:,:,0]
    green_channel = scaled_image[:,:,1]
    
    
    ### Convert image into binary image, where something registers as a 1 if above certain threshold for the specific channel and 0 otherwise
    _, thresholded_image = cv2.threshold(green_channel, 0, 250, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    ### Counting pixels in vertical and horizontal directions
    pixels_vertical=thresholded_image.shape[0]
    pixels_horiz=thresholded_image.shape[1]

    ### Getting a list of all ratios
    greens=[]
    for v in range(0,pixels_vertical):
        for h in range(0,pixels_horiz):
            greenHere=green_channel[v,h]
            redHere=red_channel[v,h]
            greens.append(greenHere)
            #if greenHere!=0:
             #   ratioHere=float(redHere-greenHere)/float(greenHere)
              #  ratios.append(ratioHere)
    
    ### Calculating the 95th percentile value of ratios
    dfHere=pd.DataFrame(greens)
    percentile99_ratios=float(dfHere.quantile(0.99))
    
    ### Getting vertical and horizontal positions of ratios that fall above the 95th percentile
    verticalPositionsAboveThreshold=[]
    horizontalPositionsAboveThreshold=[]
    for v in range(0,pixels_vertical):
        
        for h in range(0,pixels_horiz):
            greenHere=green_channel[v,h]
            redHere=red_channel[v,h]
            if greenHere>=percentile99_ratios:
                verticalPositionsAboveThreshold.append(v)
                horizontalPositionsAboveThreshold.append(h)
            # if greenHere!=0:
            #     ratioHere=float(redHere-greenHere)/float(greenHere)
            #     if ratioHere>=percentile95_ratios:
            #         verticalPositionsAboveThreshold.append(v)
            #         horizontalPositionsAboveThreshold.append(h)
    
    ### Making a histogram of all ratios
    plt.hist(greens, bins=1000, density=False)
    plt.savefig("histogramOfGreens")

    xMin=np.min(horizontalPositionsAboveThreshold)     
    xMax=np.max(horizontalPositionsAboveThreshold)            
    yMin=np.min(verticalPositionsAboveThreshold)     
    yMax=np.max(verticalPositionsAboveThreshold)  


    ### Define xMin, xMax, yMin, and yMax for outer rectangle--> this will be the outermost points in which the values are 1s
    #xMin, yMin = 0, 0
    #xMax, yMax = thresholded_image.shape[1], thresholded_image.shape[0]

    ### Define xMin, xMax, yMin, and yMax for inner rectangle
    # You can implement your own method to determine the coordinates of the inner rectangle

    ### Specify crop coordinates
    x1, x2 = int(xMin/resolutionDecreaseFactor), int(xMax/resolutionDecreaseFactor)
    y1, y2 = int(yMin/resolutionDecreaseFactor), int(yMax/resolutionDecreaseFactor)

    ### Crop the image
    cropped_image = scaled_image[y1:y2, x1:x2]
    
    # save cropped image as JPEG
    cv2.imwrite("crop.jpeg", cv2.cvtColor(cropped_image))

    
    return xMin, xMax, yMin, yMax

imageName = "IMG_1065.cr2"
folderPath = r"C:/Users/ACORY/Documents/Optodes/Calibration/20230508"


left_fractionTrimmed = 0.32
right_fractionTrimmed = 0.22
bottom_fractionTrimmed = 0.17
top_fractionTrimmed = 0.52
#print(guiToCropImage(folderPath + "/" + imageName, left_fractionTrimmed, right_fractionTrimmed, bottom_fractionTrimmed, top_fractionTrimmed))