# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 13:21:06 2023

@author: ACORY
"""
import exifread
import datetime

######################  STEP 3: Retrieves the datetime from an image  #####################

def returnDateTimeFromImageFile(imagePath, daysToAdd, stringOrEpochTime):
    # returns the datetime string for a certain image path
    # inputs: (1) path to the image
    #         (2) the number of days needed to be added to the date (necessary since there  
    #             was a period of time in which the camera's date stamp was off)
    
    # Use the exifread library to extract EXIF metadata from the file
    try:
        with open(imagePath, 'rb') as f:
            tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')
            
        # Extract the creation date and time from the EXIF metadata
        date_str = str(tags['EXIF DateTimeOriginal'])
           
        # Convert the date and time string to a datetime object
        date_obj = datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                
        # Add the specified number of days to the date object
        modified_date_obj = date_obj + datetime.timedelta(days=daysToAdd)
        
        if stringOrEpochTime == 'string':
            
            # Convert the datetime stamp to a string in the format Y-m-d H-M-S
            modified_formatted_date_str = modified_date_obj.strftime('%Y-%m-%d %H-%M-%S')
        
            return modified_formatted_date_str
        
        elif stringOrEpochTime == 'epochTime': 
            
            # Convert the modified datetime object to epoch time
            modified_epoch_time = int(modified_date_obj.timestamp())
            
            return modified_epoch_time


    except Exception as e:
        
        # Skip the image and print the error message
        return f"Skipping image '{imagePath}': {str(e)}"