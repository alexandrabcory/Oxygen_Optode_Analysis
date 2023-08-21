# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 12:24:16 2023

@author: ACORY
"""

import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import pandas as pd
import Step_1_Crop_Images as step1

###################     STEP 2: Calculate Pixel-Specific O2 Concentrations             ############################################

def makeDfOfO2Concentrations(imageName, csv_calCurveParamsByOptode, resolutionDecreaseFactor, xMin, xMax, yMin, yMax, optodeNumber):
    # Returns a dataframe with the same dimensions as the cropped optode image. 
    # The dataframe is populated by pixel-specific O2 concentration (uM) values.  
    
    # inputs: (1) image file name, 
    #         (2) a csv file with primary identifier = Optode, and accompanying columns are Ksv, alpha, and R0. 
    #         (3) resolution decrease factor (for instance a value of 4 means we divide resolution by 4)
    #         (4-7) the coordinates for the corners of the "good" optode area
    #         (8) the optode number that is pictured (after cropping)
    
    # Read calibration parameters csv file- this shows cal curve parameters by optode
    df_calCurveParams_byOptode=pd.read_csv(csv_calCurveParamsByOptode) ### Getting df of ALL cal curve params (for each optode)
    
    # Retrieve optode-specific calibration parameters.
    # First, select the full row of calibration curve parameters (specific to the optode selected)
    df_calCurveParams=df_calCurveParams_byOptode[df_calCurveParams_byOptode['Optode']==optodeNumber] ### Getting optode-specific cal curve params
    
    # Next, get specific calibration curve parameters from this row. 
    Ksv=float(df_calCurveParams['Ksv'])
    alpha=float(df_calCurveParams['alpha'])
    R0=float(df_calCurveParams['R0'])
    
    # Get red and green channel images
    red = step1.readAndCropImage(imageName, "red", resolutionDecreaseFactor, xMin, xMax, yMin, yMax)
    green=step1.readAndCropImage(imageName, "green", resolutionDecreaseFactor, xMin, xMax, yMin, yMax)
    
    # Count pixels in vertical and horizontal directions
    pixels_vertical=red.shape[0]
    pixels_horiz=red.shape[1]

    # Make a blank dataframe- this will ultimately be filled with O2 concentrations (uM)
    df = pd.DataFrame(np.zeros((pixels_vertical, pixels_horiz)))
    
    # Fill the dataframe with O2 concentration values
    for v in range(0,pixels_vertical):

        for h in range(0,pixels_horiz):
            
            # get the intensity value for red and green (pixel-specific)
            redHere=float(red[v,h])
            greenHere=float(green[v,h])
            
            # Exclusion criteria- we can't calculate (R-G)/G if G = 0
            if greenHere==0:
                df.iloc[v][h]=None
            else:
                
                # Calculate the ratio here
                ratioHere=(redHere-greenHere)/greenHere
                
                # Calculate O2 concentration
                O2 = float((R0-ratioHere)/(Ksv*((ratioHere-R0 * alpha))))
                
                # Add the O2 concentration value to the dataframe
                df.iloc[v][h]=O2

    return df