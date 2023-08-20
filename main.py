# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 10:39:26 2023

@author: ACORY
"""

#################      Introduction          #################################################################################

# Oxygen optodes are colorimetric tools for obtaining spatially and temporally-resolved 
# O2 concentration across a 2-dimensional surface. Optodes are generally thin, rectangular, surfaces that have been 
# coated in a dye that, when exposed to blue LED light, fluoresces two visible colors: red and green. The amount of 
#red fluoresence is inversely proportional to O2 concentration, while the amount of green fluoresence is constant 
#across a range of O2 concentrations. We can thus generate calibration curves by examining the relationship between 
#average O2 concentration vs. average ratio of (red green)/green. The calibration curves should be produced 
#(in another script) prior to running this code. 

# We use oxygen optodes to study the heterogeneity of O2 concentration across a vertical transect of incubated soil 
#cores. For every two-minute interval, a new raw image file, showcasing three soil cores with adjoined fluorescing 
#optodes, is created.

# The goals of this code are to:
#    (1) accept a folder full of raw image files (CR2), 
#    (2) crop each image so that only one oxygen optodes is in the frame, 
#    (3) calculate O2 concentration for every pixel in the cropped image
#    (4) generate a heat map of O2 concentration 
#    (5) generate a histogram of O2 distribution
#    (6) generate a csv file containing pixel-specific O2 concentrations.This is used as an input to the 
#        DAMM-GHG model (separate script). 

################     Folder Structure          ########################################################################

# Prior to running this code, set up the following folder structure: 
   
#    (1) a source folder, including:
#        (i) this script
#        (ii) A csv file titled 'CalCurveParams_AndCropParams_byOptode'
   
#    (2) an input folder containing a series of raw images (CR2). 
#        Each image should showcase three soil cores, each with an adjoined O2 optode (that should be visibly
#        fluorescent. 
   
#    (2) two output folders. Both of these should be located within a folder titled by Site (options = Wetland or              Transition or Upland.) In this folder, there should be two folders, for:
   
#        (i) storing histograms and heat maps
#        (ii) storing csv files of pixel-specific O2 concentration. 



#############       CHANGE THESE THINGS           ##########################################################################
# Define the site. Three options: (1) Wetland, (2) Transition, (3) Upland (see Folder Structure- above)
site = "Transition" 

# Now, define the folders. See the above cell- "Folder Structure"- for more details. 
# Define the input folder path. 
inputFolderPath=r"C:\Users\ACORY\Documents\Optodes\OWC\Exp1_Demonstration\All_Images\sample" 

# Define the first output folder path
outputFolderPath_1 = r"C:\Users\ACORY\Documents\Optodes\OWC\Exp1_Demonstration\Transition\HistogramsAndHeatMaps" 

# Define the second output folder path
outputFolderPath_2 = r"C:\Users\ACORY\Documents\Optodes\OWC\Exp1_Demonstration\Transition\CsvsOfOxygen" #This is where you store csvs of pixel-specific O2 concentration 

# Define the optode number for the incubator you'll be analyzing. 
# There are three optodes pictured per frame, but we'll be cropping the image to showcase just one.  
optodeNumber = 5 

# Define the number of bins we want to use for our histograms. 
bins=100 

# Define the resolution decrease factor. We take this value and divide the initial number of pixels by that number to produce
# an adjusted number of pixels.  
# Reducing image resolution was recommended by collaborators because it reduces noise imposed by light scattering.
resolutionDecreaseFactor=5                                                     

# Define the number of days we need to add to each date stamp. Values >0 are only necessary if the camera incorrectly recorded the date. 
daysToAdd= 0

# Define the 
maxO2ToPlot = 1000



##############    EXECUTE THE FUNCTION         ########################################################################
# import the script that contains 'generateAllOutputByFolder'- the main function we're calling
import Step_7_Produce_Output_For_Folder as step7

# define csv of calibration curve parameters by optode - these were determined previously
csv_parametersForCalibrationAndCropping_ByOptode='CalCurveParams_AndCropParams_byOptode.csv'

# generate all three outputs relating to O2 concentration-- (1) heat map (2) histogram (3) csv
print(step7.generateAllOutputByFolder(inputFolderPath, outputFolderPath_1, outputFolderPath_2, csv_parametersForCalibrationAndCropping_ByOptode, resolutionDecreaseFactor, bins, optodeNumber, daysToAdd, maxO2ToPlot, site))