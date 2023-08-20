                  Introduction

Oxygen optodes are colorimetric tools for obtaining spatially and temporally-resolved 
O2 concentration across a 2-dimensional surface. Optodes are generally thin, rectangular, surfaces that have been coated in a dye that, when exposed to blue LED light, fluoresces two visible colors: red and green. The amount of red fluoresence is inversely proportional to O2 concentration, while the amount of green fluoresence is constant across a range of O2 concentrations. We can thus generate calibration curves by examining the relationship between average O2 concentration vs. average ratio of (red green)/green. The calibration curves should be produced (in another script) prior to running this code. 

We use oxygen optodes to study the heterogeneity of O2 concentration across a vertical transect of incubated soil cores. For every two-minute interval, a new raw image file, showcasing three soil cores with adjoined fluorescing optodes, is created.

The goals of this code are to:
(1)	accept a folder full of raw image files (CR2)
(2)	crop each image so that only one oxygen optodes is in the frame  
(3)	 calculate O2 concentration for every pixel in the cropped image
(4)	generate a heat map of O2 concentration 
(5)	generate a histogram of O2 distribution
(6)	 a csv file containing pixel-specific O2 concentrations.This is used as an input to the DAMM-GHG model (separate script). 

                  Folder Structure

Prior to running this code, set up the following folder structure: 

a source folder, including: 
- main.py
- Step_1_Crop_Images.py
- Step_2_Calculate_Oxygen.py
- Step_3_Retrieve_DateTime_From_CR2.py
- Step_4_Make_Heat_Map.py
- Step_5_Make_Histogram.py
- Step_6_Make_O2_Csvs.py
- Step_7_Produce_Output_For_Folder.py
- CalCurveParams_AndCropParams_byOptode.csv

an input folder containing:
- a series of raw images (CR2)
- each image showcases three soil cores, each with an adjoined O2 optode (that should be visibly fluorescent.)

a site-specific folder to hold all output. Title options include:
- Wetland
- Transition
- Upland

The first of two output folders, located within the Site-Specific Folder (Wetland/Transition/Upland). This one stores:
- Histograms*
- heat maps*

The second of two output folders, located within the Site-Specific Folder (Wetland/Transition/Upland). This one stores:
- CSVs of pixel-specific O2 concentrations (uM)**

*For every original raw image, one of these files are produced.
** These CSV files have the same dimensions as the raw image (in pixels). 

