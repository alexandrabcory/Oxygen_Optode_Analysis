# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 13:54:37 2023

@author: ACORY
"""
import os
import pandas as pd
import Step_1_Crop_Images as c
import Step_4_Make_Heat_Map as step4
import Step_5_Make_Histogram as step5
import Step_6_Make_O2_Csvs as step6

###### STEP 7: PRODUCE OUTPUT FOR FOLDER OF IMAGES    ########################

def generateAllOutputByFolder(inputFolderPath, outputFolderPath_1, outputFolderPath_2, csv_calCurveParamsByOptode, resolutionDecreaseFactor, bins, optodeNumber, daysToAdd, maxO2ToPlot, site):
    # for every file in the folder, this function generates (1) an O2 heat map; (2) an O2 histogram; 
    # (3) two csvs of pixel-specific O2 concentrations- one named by epoch time and one named by human-readable timestamp
    
    # inputs: (1) inputFolderPath - stores raw image files
    #         (2) outputFolderPath_1- stores output images (histograms and heat maps)
    #         (3) outputFolderPath_2- stores csv files of pixel-specific O2 concentration
    #         (4) csv_calCurveParamsByOptode
    #         (5) resolutionDecreaseFactor
    #         (6) bins
    #         (7) optodeNumber
    #         (8) daysToAdd
    #         (9) maxO2ToPlot
    #         (10) site
    
    # Get the first first in the folder
    first_cr2_file = next((f for f in os.listdir(inputFolderPath) if f.endswith('.CR2')), None)
    
    ### Get a dataframe of optode-specific measurements
    df = pd.read_csv(csv_calCurveParamsByOptode)
    left_fractionTrimmed = df.loc[df['Optode'] == optodeNumber, 'left_fractionTrimmed'].values[0]
    right_fractionTrimmed = df.loc[df['Optode'] == optodeNumber, 'right_fractionTrimmed'].values[0]
    bottom_fractionTrimmed = df.loc[df['Optode'] == optodeNumber, 'bottom_fractionTrimmed'].values[0]
    top_fractionTrimmed = df.loc[df['Optode'] == optodeNumber, 'top_fractionTrimmed'].values[0]
    xMin, xMax, yMin, yMax = c.guiToCropImage(inputFolderPath + "/" + first_cr2_file, left_fractionTrimmed, right_fractionTrimmed, bottom_fractionTrimmed, top_fractionTrimmed)
    
   # Initialize file counters
    fileCount = 0
    fileNumber = 0

    # Count the number of .CR2 files
    for filename in os.listdir(inputFolderPath):
        if filename.endswith('.CR2'):
            fileCount += 1

    # Process the .CR2 files
    for filename in os.listdir(inputFolderPath):
        if filename.endswith('.CR2'):
            fileNumber += 1
            
            # Get the filepath
            filePath = os.path.join(inputFolderPath, filename)
            
            # Generate the heat map (step 3), histogram (step 5), and O2 concentration csvs (step 6)
            step4.plotRaster(filePath, outputFolderPath_1, csv_calCurveParamsByOptode, resolutionDecreaseFactor, xMin, xMax, yMin, yMax, optodeNumber, maxO2ToPlot, daysToAdd)
            step5.createAndSaveHistogramAndRaster(filePath, outputFolderPath_1, csv_calCurveParamsByOptode, resolutionDecreaseFactor, bins, optodeNumber, xMin, xMax, yMin, yMax, daysToAdd, maxO2ToPlot)
            step6.saveO2ConcToCSVs(filePath, outputFolderPath_2, csv_calCurveParamsByOptode, resolutionDecreaseFactor, optodeNumber, xMin, xMax, yMin, yMax, daysToAdd, site)
            
            print(f"Finished {fileNumber} of {fileCount}")

    return "done"
