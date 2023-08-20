# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 13:27:55 2023

@author: ACORY
"""
import numpy as np
from scipy.stats import lognorm
import Step_2_Calculate_Oxygen as step2
import Step_3_Retrieve_DateTime_From_CR2 as step3
import matplotlib.pyplot as plt
import os

# Create a probability distribution function; this will be fit on top of the histogram
def modelLognormalDistribution(data, size=1000):
    # Returns x and y values for a log-normal distribution; these values are meant to fit the data plotted in a histogram
    # inputs: (1) data= the O2 concentration (pixel-specific) data
    #         (2) the number of modeled data points to generate per axis (x and y)
    min_value = np.min(data)
    max_value = np.max(data)
    
    params = lognorm.fit(data)

    # Generate x and y values for log-normal distribution
    x = np.linspace(min_value, max_value, size)
    y = lognorm.pdf(x, *params)
    
    return x, y

def createAndSaveHistogramAndRaster(imageName, inputFolderPath, outputFolderPath_1, csv_calCurveParamsByOptode, resolutionDecreaseFactor, bins, optodeNumber, xMin, xMax, yMin, yMax, daysToAdd, maxO2ToPlot):
    # saves a histogram image of O2 concentration distribution
    # inputs: (1) image name
    #         (2) input folder path- where the raw image is stored
    #         (3) the output folder path- where the histogram will be stored
    #         (4) csv_calCurveParamsByOptode
    #         (5) resolutionDecreaseFactor (for instance a value of 4 means we divide resolution by 4)
    #         (6) bins for the histogram
    #         (7)  optode number
    #         (8-11) xMin, xMax, yMin, yMax:  coordinates of the outer edges of the "good" optode region
    #         (12) days to add to original date stamp- default is 0
    #         (13) max O2 value to plot- in uM 
    
    # get coordinates for cropping
    filePath = inputFolderPath + '/' + imageName
    
    # precprocess the data by (1) getting a dataframe of O2 concentrations across space (each cell represents a pixel-specific O2 Conc.),
    #                     and (2) flattening that dataframe into a list of values
    df = step2.makeDfOfO2Concentrations(filePath, csv_calCurveParamsByOptode, resolutionDecreaseFactor, xMin, xMax, yMin, yMax, optodeNumber)
    O2Concentrations = df.values.flatten().tolist()
    
    # exclude null vals
    O2Concentrations_screened = [x for x in O2Concentrations if str(x) != 'nan']
    
    # exclude negative values and values that are over the max desired threshold
    O2Concentrations_screened = [x for x in O2Concentrations_screened if x > 0 and x <= maxO2ToPlot]

    # Create a new figure and axis before plotting the histogram
    fig, ax = plt.subplots()

    # make a histogram
    freq, bins, patches = plt.hist(O2Concentrations_screened, bins=bins, density=True, color='green', alpha=0.5)

    # plot modeled values
    x_modeled, y_modeled = modelLognormalDistribution(O2Concentrations_screened, size=1000)

    # clean up the figure 
    plt.tick_params(axis='both', which='major', labelsize=14)
    
    # set x and y labels
    # the x label is "O2 (uM)" < where 2 is subscription and u is a micro symbol
    plt.xlabel("Dissolved O\u2082 (\u00B5M)", fontsize=16)
    plt.ylabel('Microsite Frequency', fontsize=16)
    
    # set axis limits
    plt.xlim(0, maxO2ToPlot)
    max_y = max(freq)
    plt.ylim(0, 1.1 * max_y)
    
    # set figure size and adjust subplot
    fig.set_size_inches(6, 4)
    plt.subplots_adjust(bottom=0.15, top=0.9, left=0.18, right=0.9)
    
    # format the datetime so that it can be used as a component of the histogram filename. 
    dateTime_formatted = step3.returnDateTimeFromImageFile(filePath, daysToAdd, 'string')
    histogramTitle = 'histTo' + str(maxO2ToPlot) + "_" + dateTime_formatted + ".jpg"
    histogramFilePath = os.path.join(outputFolderPath_1, histogramTitle)
    
    # save the figure
    plt.savefig(histogramFilePath)
    plt.close()

    return