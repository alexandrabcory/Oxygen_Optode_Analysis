# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 13:47:31 2023

@author: ACORY
"""

################    STEP 6: Make Two CSV Files of Pixel-Specific O2 Concentration (same dimensions as the image)  #####################
################    .................one of the csv files is in epoch time and one is human-readable time

import Step_2_Calculate_Oxygen as step2
import Step_3_Retrieve_DateTime_From_CR2 as step3
import pandas as pd


def saveO2ConcToCSVs(filePath, outputFolderPath_2, csv_calCurveParamsByOptode, resolutionDecreaseFactor, optodeNumber, xMin, xMax, yMin, yMax, daysToAdd, site):
    # returns csv of pixel-specific O2 concentration values (in uM)
    # inputs: (1) imageName, 
    #         (2) inputFolderPath
    #         (3) outputFolderPath_2
    #         (4) csv_calCurveParamsByOptode- optode-specific dataframe showing cal curve parameters (Ksv, alpha, and R0)
    #         (5) resolutionDecreaseFactor (for instance a value of 4 means we divide resolution by 4)
    #         (6) optodeNumber
    #         (7-10) xMin, xMax, yMin, yMax:  coordinates of the outer edges of the "good" optode region
    #         (11) days to add to original date stamp- default is 0
    #         (12) site- three options: "Wetland", "Transition", "Upland"
    
    # Get a dataframe of all O2 concentrations (this has the dimensions of the image)
    df = step2.makeDfOfO2Concentrations(filePath, csv_calCurveParamsByOptode, resolutionDecreaseFactor, xMin, xMax, yMin, yMax, optodeNumber)
    
    # Flatten the array into a list
    O2Concentrations = df.values.flatten().tolist()
    
    # Exclude null vals
    O2Concentrations_screened = [x for x in O2Concentrations if str(x) != 'nan']
    
    # Exclude negative values and values that are over 1,000
    O2Concentrations_screened = [x for x in O2Concentrations_screened if x > 0 and x <= 1000]
    
    # Make a dataframe with only one column for output
    outputDf = pd.DataFrame({'O2Conc': O2Concentrations_screened})
    
    # Retrieve the timestamp (in epoch time) so that we can save the file with this timestamp
    epochTime = step3.returnDateTimeFromImageFile(filePath, daysToAdd, 'epochTime')
    
    # Make two csvs; one labeled by epoch time; one labeled by human-readable timestamp
    outputCsvFilePath1 = outputFolderPath_2 + "/" + str(epochTime) + ".csv"
    dateTime_formatted = step3.returnDateTimeFromImageFile(filePath, daysToAdd, 'string')
    outputCsvFilePath2 = outputFolderPath_2 + "/" + site + "_" + dateTime_formatted + ".csv"
    
    # Save file to csv
    outputDf.to_csv(outputCsvFilePath1)
    outputDf.to_csv(outputCsvFilePath2)
    
    return