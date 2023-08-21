# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 12:50:28 2023

@author: ACORY
"""

import Step_2_Calculate_Oxygen as step2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import Step_3_Retrieve_DateTime_From_CR2 as step3 


#############              STEP 4: GENERATE HEAT MAP OF O2 CONCENTRATION          ############################################

    
def plotRaster(imageName, inputFolderPath, outputFolderPath, csv_calCurveParamsByOptode, resolutionDecreaseFactor, xMin, xMax, yMin, yMax, optodeNumber, maxO2Val, daysToAdd):
    # returns a heatmap of O2 concentration
    # inputs: (1) image name
    #         (2) input folder path
    #         (3) output folder path-- the heat map is saved here
    #         (4) csv of calibration curve parameters by optode
    #         (5) the resolution decrease factor (for instance a value of 4 means we divide resolution by 4)
    #         (6-9) coordinates of the outer edges of the "good" optode region
    #         (10) optode number- this is an integer value
    #         (11) maximum O2 value for the heat map scale
    #         (12) days to add; default 0; this is necessary just because some image files have incorrect date stamps,
    #             which necessitate adding one extra day to the originally-stored datetime stamp
    
    # get the file path for the image file
    filePath=inputFolderPath + '/' + imageName
    
    # get a dataframe of O2 concentrations across space 
    df = step2. makeDfOfO2Concentrations(filePath, csv_calCurveParamsByOptode, resolutionDecreaseFactor, xMin, xMax, yMin, yMax, optodeNumber)
    
    # convert the dataframe to an array to and clip the array to the desired range
    array = df.values
    array = np.clip(array, 0, maxO2Val) 
    
    # get the height and width of the dataframe/array
    ht, width = array.shape[0], array.shape[1]
    
    #get the ratio of height to width- this is useful for scaling
    ratio_htToWidth = ht / width
    
    # compress figure to be shorter. This is useful because it's difficult to see such a thin image 
    ratioToUseForFigure = ratio_htToWidth * 0.4
    
    # make the architecture of the plot
    fig, ax = plt.subplots(figsize=(2, 2*ratioToUseForFigure))
    
    # define the color scheme 
    cmap = colors.LinearSegmentedColormap.from_list('custom', [(0, 'white'), (1, 'red')])
    cmap.set_over('red')
    cmap.set_under('green')
    
    # show the image 
    im = ax.imshow(array, cmap=cmap, interpolation='nearest', aspect='equal', vmin=0, vmax=maxO2Val)

    # Remove x and y tick marks and tick labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    
    # add a y axis label: O2 (uM)< where the 2 is subscript and the u is a micro symbol
    cbar.ax.set_ylabel("O\u2082 (\u00B5M)", rotation=-90, va="bottom", fontsize = 16)
    cbar.ax.tick_params(labelsize=14)
    
    # make room for the colorbar
    fig.subplots_adjust(right=0.65)
    
    # get the date time in a formatted way so that it can be part of the file title
    dateTime_formatted = step3.returnDateTimeFromImageFile(filePath, daysToAdd, 'string')
    outputFileName = "\mapTo" + str(maxO2Val) + "_" + dateTime_formatted + ".jpg"
    outputFilePath = outputFolderPath + outputFileName
    
    # adjust the figure to enable a "tight layout" < this prevents text from overlapping 
    # or running off the page
    plt.tight_layout()
    
    # save and close the figure
    plt.savefig(outputFilePath)
    plt.close()
    
    return array, fig, ax
