                  Introduction

Oxygen optodes are colorimetric tools for obtaining spatially and temporally-resolved 
O2 concentration across a 2-dimensional surface. Optodes are generally thin, rectangular, surfaces that have been coated in a dye that, when exposed to blue LED light, fluoresces two visible colors: red and green. The amount of red fluoresence is inversely proportional to O2 concentration, while the amount of green fluoresence is constant across a range of O2 concentrations. We can thus generate calibration curves by examining the relationship between average O2 concentration vs. average ratio of (red green)/green. The calibration curves should be produced (in another script) prior to running this code. 

We use oxygen optodes to study the heterogeneity of O2 concentration across a vertical transect of incubated soil cores. For every two-minute interval, a new raw image file, showcasing three soil cores with adjoined fluorescing optodes, is created.

The goals of this code are to:
- accept a folder full of raw image files (CR2)
- crop each image so that only one oxygen optodes is in the frame
-  calculate O2 concentration for every pixel in the cropped image
-  generate a heat map of O2 concentration
-  generate a histogram of O2 distribution
-  generate a csv file containing pixel-specific O2 concentrations.This is used as an input to the DAMM-GHG model (separate script). 

                  Folder Structure

All scripts are located in the folder 'Scripts'. All executions are performed in 'main.py' file.

Prior to running the code, set create the following folders (which match the folder structure here on Git): 

..a Scripts folder, including: 
- main.py
- Step_1_Crop_Images.py
- Step_2_Calculate_Oxygen.py
- Step_3_Retrieve_DateTime_From_CR2.py
- Step_4_Make_Heat_Map.py
- Step_5_Make_Histogram.py
- Step_6_Make_O2_Csvs.py
- Step_7_Produce_Output_For_Folder.py
  
..an input folder, containing:
- CalCurveParams_AndCropParams_byOptode.csv
- rawImages folder, which contains a series of raw images (CR2 files)

..an output folder containing three site-specific folders:
- Wetland
- Transition
- Upland

..two subfolders in each of the site-specific folders (above):
- CsvsOfOxygen -- populated by csv files of pixel-specific O2 concentrations (uM)
- HistogramsAndHeatMaps -- shows distribution of O2 concentration (uM)

