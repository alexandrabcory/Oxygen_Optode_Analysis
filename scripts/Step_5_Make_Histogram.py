# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 13:27:55 2023

@author: ACORY
"""
import Step_2_Calculate_Oxygen as step2
import Step_3_Retrieve_DateTime_From_CR2 as step3
import matplotlib.pyplot as plt
import os

def createAndSaveHistogramAndRaster(filePath, outputFolderPath_1, csv_calCurveParamsByOptode, resolutionDecreaseFactor, bins, optodeNumber, xMin, xMax, yMin, yMax, daysToAdd, maxO2ToPlot):
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
    
    
    # First, precprocess the data by (1) getting a dataframe of O2 concentrations across space (each cell represents a pixel-specific O2 Conc.),
    #                                (2)  flattening that dataframe into a list of values
    df = step2.makeDfOfO2Concentrations(filePath, csv_calCurveParamsByOptode, resolutionDecreaseFactor, xMin, xMax, yMin, yMax, optodeNumber)
    O2Concentrations = df.values.flatten().tolist()
    
    # Exclude null vals
    O2Concentrations_screened = [x for x in O2Concentrations if str(x) != 'nan']
    
    # Exclude negative values and values that are over the max desired threshold
    O2Concentrations_screened = [x for x in O2Concentrations_screened if x > 0 and x <= maxO2ToPlot]

    # Create a new figure and axis before plotting the histogram
    fig, ax = plt.subplots()

    # Make a histogram
    freq, bins, patches = plt.hist(O2Concentrations_screened, bins=bins, density=True, color='green', alpha=0.5)

    # Clean up the figure 
    plt.tick_params(axis='both', which='major', labelsize=14)
    
    # Set x and y labels for the plot
    # The x label is "O2 (uM)" < where 2 is subscription and u is a micro symbol
    plt.xlabel("Dissolved O\u2082 (\u00B5M)", fontsize=16)
    plt.ylabel('Microsite Frequency', fontsize=16)
    
    # Set axis limits
    plt.xlim(0, maxO2ToPlot)
    max_y = max(freq)
    plt.ylim(0, 1.1 * max_y)
    
    # Set figure size and adjust subplot
    fig.set_size_inches(6, 4)
    plt.subplots_adjust(bottom=0.15, top=0.9, left=0.18, right=0.9)
    
    # Format the datetime so that it can be used as a component for the histogram filename (which we're about to save)
    dateTime_formatted = step3.returnDateTimeFromImageFile(filePath, daysToAdd, 'string')
    histogramTitle = 'histTo' + str(maxO2ToPlot) + "_" + dateTime_formatted + ".jpg"
    histogramFilePath = os.path.join(outputFolderPath_1, histogramTitle)
    
    # Save the figure
    plt.savefig(histogramFilePath)
    plt.close()

    return