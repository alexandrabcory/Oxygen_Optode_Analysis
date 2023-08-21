# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 10:39:26 2023

@author: ACORY
"""

#############       CHANGE THESE THINGS           ##########################################################################
# Define the site. Three options: (1) Wetland, (2) Transition, (3) Upland (see Folder Structure- above)
site = "Upland" 

# Now, define the folders. See the above cell- "Folder Structure"- for more details. 
# Define the input folder path. 
inputFolderPath_1=r"C:\Users\ACORY\Documents\Optodes\OWC\Exp1_Demonstration\inputFiles\rawImages" 
inputFolderPath_2=r"C:\Users\ACORY\Documents\Optodes\OWC\Exp1_Demonstration\inputFiles"

# Define the first output folder path
outputFolderPath_1 = r"C:\Users\ACORY\Documents\Optodes\OWC\Exp1_Demonstration\outputFiles\Upland\HistogramsAndHeatMaps" 

# Define the second output folder path
outputFolderPath_2 = r"C:\Users\ACORY\Documents\Optodes\OWC\Exp1_Demonstration\outputFiles\Upland\CsvsOfOxygen" #This is where you store csvs of pixel-specific O2 concentration 

# Define the optode number for the incubator you'll be analyzing. 
# There are three optodes pictured per frame, but we'll be cropping the image to showcase just one.  
optodeNumber = 10

# Define the number of bins we want to use for our histograms. 
bins=100 

# Define the resolution decrease factor. We take this value and divide the initial number of pixels by that number to produce
# an adjusted number of pixels.  
# Reducing image resolution was recommended by collaborators because it reduces noise imposed by light scattering.
resolutionDecreaseFactor=5                                                     

# Define the number of days we need to add to each date stamp. Values >0 are only necessary if the camera incorrectly recorded the date. 
daysToAdd= 0

# Define the maximum value of O2 that you wish to plot (unit: uM)
maxO2ToPlot = 1000



##############    EXECUTE THE FUNCTION         ########################################################################
# import the script that contains 'generateAllOutputByFolder'- the main function we're calling
import Step_7_Produce_Output_For_Folder as step7

# define csv of calibration curve parameters by optode - these were determined previously
csv_parametersForCalibrationAndCropping_ByOptode = inputFolderPath_2+ '/' 'CalCurveParams_AndCropParams_byOptode.csv'

# generate all three outputs relating to O2 concentration-- (1) heat map (2) histogram (3) csv

# Retrieving the path to the csv input file
print(step7.generateAllOutputByFolder(inputFolderPath_1, outputFolderPath_1, outputFolderPath_2, csv_parametersForCalibrationAndCropping_ByOptode, resolutionDecreaseFactor, bins, optodeNumber, daysToAdd, maxO2ToPlot, site))