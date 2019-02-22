#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:14:12 2019

@author: ejreidelbach

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import json
import os  
import pandas as pd
import pathlib
import tqdm
import urllib.request 

#==============================================================================
# Reference Variable Declaration
#==============================================================================

#==============================================================================
# Function Definitions
#==============================================================================
def downloadPictures(dict_url, folder_name):
    '''
    Purpose: Download pictures via the provided url for the image
    
    Inputs   
    ------
        dict_url : dictionary of URLs
            dictionary in which the name of the image is the key and the
            associated value is the URL of the image
        folder_name : string
            name of the folder in which downloaded images should be stored
            
    Outputs
    -------
        files are saved to a folder named after the input dictionary
    '''
    # Check to see if the desired folder exists and create it if it doesn't
    pathlib.Path('pictures/',folder_name).mkdir(parents=True, exist_ok=True)
    
    # Download all the images at the associated URLs
    for name, url in tqdm.tqdm(dict_url.items()):
        if not pd.isna(url):
            urllib.request.urlretrieve(url, 'pictures/' + folder_name + '/' 
                                       + name + '.jpg')
    
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
path_dir = pathlib.Path('/home/ejreidelbach/Projects/draft-gem/src/static')
os.chdir(path_dir)

#------------------------------------------------------------------------------
# Download Pictures of Schools
#------------------------------------------------------------------------------
# Ingest the listing of schools and their associated pictures
df_pics_school = pd.read_csv('positionData/school_pictures.csv')
df_pics_school.set_index('school', drop=True, inplace=True)

# Convert the dataframe to a dictionary
dict_pics_school = df_pics_school.to_dict('index')
for key, value in dict_pics_school.items():
    dict_pics_school[key] = value['urlSchool']
    
# Download the pictures
downloadPictures(dict_pics_school, 'School')

#------------------------------------------------------------------------------
# Download Pictures of Quarterbacks
#------------------------------------------------------------------------------
# Ingest the Quarterback data
df_pics_qb = pd.read_csv('positionData/QB/pos_QB_final.csv')

# Rename the `pictureSchool` and `picturePlayer` variables to include URL
df_pics_qb.rename(columns = {'picturePlayer':'picturePlayerURL',
                             'pictureSchool':'pictureSchoolURL'}, inplace=True)
    
# Create the `pictureSchoolPath` and `picturePlayerPath` variables to map
#   the file location of the associated images (i.e. /positionData/pictures/..)
df_pics_qb['picturePlayerPath'] = df_pics_qb.apply(
        lambda row: '/positionData/pictures/QB/' + row['unique_id'] + '.png' 
        if not pd.isnull(row['picturePlayerURL']) else '', axis = 1)
df_pics_qb['pictureSchoolPath'] = df_pics_qb['School'].apply(
        lambda x: '/positionData/pictures/School/' + x + '.png')

# Convert the dataframe to a dictionary
dict_pics_qb = df_pics_qb.to_dict('index')

# Write the updated data (with paths to pictures vice URLs) to a .csv file
#   ('pos_POSITION_final_pics.csv')
df_pics_qb.to_csv('positionData/QB/pos_QB_final_pics.csv', index = False)

# Write the updated data (with paths to pictures vice URLs) to a .json file 
#   ('pos_POSITION_final_pics.json')
with open('positionData/QB/pos_QB_final_pics.json', 'wt') as out:
    json.dump(dict_pics_qb, out, sort_keys=True)
    
# Minimize the QB Dictionary for the purposes of picture scraping
dict_pics_qb_small = {}
for key, value in dict_pics_qb.items():
    dict_pics_qb_small[dict_pics_qb[key]['unique_id']] = value['picturePlayerURL']

# Download the pictures
downloadPictures(dict_pics_qb_small, 'QB')
