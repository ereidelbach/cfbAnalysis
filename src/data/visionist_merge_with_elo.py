#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 10:58:42 2019

@author: ejreidelbach

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import glob
import json
import os  
import pandas as pd
import pathlib
import tqdm
import urllib.request 

#==============================================================================
# Reference Variable Declaration
#==============================================================================
list_nfl = ['ari',
 'atl',
 'bal',
 'buf',
 'car',
 'chi',
 'cin',
 'cle',
 'dal',
 'den',
 'det',
 'gb',
 'hou',
 'ind',
 'jax',
 'kc',
 'lac',
 'lar',
 'mia',
 'min',
 'ne',
 'no',
 'nyg',
 'nyj',
 'oak',
 'phi',
 'pit',
 'sea',
 'sf',
 'tb',
 'ten',
 'wsh']

#==============================================================================
# Function Definitions
#==============================================================================
def combinePositionalData():
    '''
    Purpose: Combine positional data together such that there is a master file
               for all offensive and defensive players

    Inputs
    ------
        NONE
            
    Outputs
    -------
        NONE
    '''    
    # Read in every `_all.csv` positional file
    list_files = glob.glob('positionData/*' + '/player_info_*' + '_all.csv')    
    
    # Ingest the files into two dataframes: one for offense and one for defense
    list_dataframes_off = []
    list_dataframes_def = []
    for csv in list_files:
        df_file = pd.read_csv(csv)
        if 'DEF' in csv:
            list_dataframes_def.append(df_file)
        else:
            list_dataframes_off.append(df_file)
    
    # Complete all steps for both the offensive and the defensive dataframe    
    for type_stats in ['offense', 'defense']:
        df = pd.DataFrame()
        if type_stats == 'offense':
            df = pd.concat(list_dataframes_off, sort = True)
        else:
            df = pd.concat(list_dataframes_def, sort = True)
    
        # Standardize the picture URLs
        df['pictureSchool'] = df['pictureSchool'].astype(str)
        df['pictureSchool'] = df['pictureSchool'].apply(
                lambda x: renameSchoolPictureURL(x))
        
        # Read in existing school_picture data with the URL as the key
        dict_pictures_school = createSchoolPictureDict('url')
        
        # Create a `school_pic` variable using the picture keys
        df['school_pic'] = df['pictureSchool'].apply(
                lambda x: dict_pictures_school[x] if (
                        x in dict_pictures_school.keys()) else '')
            
        # If a school has an NFL picture, remove it
        def removeNFL(url):
            for team in list_nfl:
                if team in url:
                    return ''
            return url
        df['pictureSchool'] = df['pictureSchool'].apply(
                lambda x: removeNFL(x))
        
        # Isolate the schools that are not missing school picture URLs but
        #   are missing entries for school_pic
        df_missing = df[df['pictureSchool'] != '']
        df_missing = df_missing[df_missing['school_pic'] == '']
        print('# of players missing schools: ' + str(len(df_missing)))
              
        # Use the value deriveded from `pictureSchool` to fill in `school`
        # Handle missing values first (i.e. missing value for `school`)
        df['school'] = df.apply(
                lambda row: row['school_pic'] if pd.isna(row['school']) 
                else row['school'], axis=1)
        df.drop(columns = ['school_pic'], inplace=True)
        
        # Read in existing school_picture data with the URL as the key
        dict_pictures_school_names = createSchoolPictureDict()
        
        # Fill in missing values for `pictureSchool`
        def fillPictures(school):
            if school != '':
                return dict_pictures_school_names[school]
            else:
                return ''
        df['pictureSchool'] = df.apply(lambda row: fillPictures(row['school']) 
        if row['pictureSchool'] == '' else row['pictureSchool'], axis = 1)
        
        # Fill missing values with ''
        df = df.fillna('')
        
        # Standardize birthday values by removing included ages
        df['birthday'] = df['birthday'].apply(lambda x: str(x).split(' ')[0])
        
        # Export the newly created dataframes to files in the `Merged` folder
        df.to_csv('positionData/Merged/players_' + type_stats + '.csv', 
                  index = False)

def createSchoolPictureDict(key = 'school'):
    '''
    Purpose: Create a dictionary with team names as keys and pic_urls as values

    Inputs
    ------
        style : string
            Indicates which variable should serve as the key in the dictionary
                - 'school' indicates the school name should be the key
                - 'url' indicates the url should be the key
            
    Outputs
    -------
        dict_pictures : dictionary
            Keys are school names and values are URLs of the team logo
    '''    
    # ingest the school names and URLs from a flat file    
    df_pictures = pd.read_csv('positionData/school_pictures.csv')

    # School is the key
    if key == 'school':
        df_pictures.set_index('school', drop=True, inplace=True)
        dict_pictures = df_pictures.to_dict('index')
        for key, value in dict_pictures.items():
            dict_pictures[key] = value['urlSchool']
    # URL is the key
    elif key == 'url':
        df_pictures.set_index('urlSchool', drop=True, inplace=True)
        dict_pictures = df_pictures.to_dict('index')
        for key, value in dict_pictures.items():
            dict_pictures[key] = value['school']        
    
    return dict_pictures

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
#    dict_url = dict_pos_small.copy()
    # Check to see if the desired folder exists and create it if it doesn't
    pathlib.Path('pictures/',folder_name).mkdir(parents=True, exist_ok=True)
            
    # Check what files exist in the specified folder
    list_files = glob.glob('pictures/' + folder_name + '/*') 
    list_files = [x.split('/')[-1:][0].split('.')[0] for x in list_files]
    
    # Download all the images at the associated URLs
    for name, url in tqdm.tqdm(dict_url.items()):
        # only download files we don't have
        if name not in list_files:
            # if a url exists, retrieve the file
            if url != '':
                try:
                    urllib.request.urlretrieve(url, 'pictures/' + folder_name + '/' 
                                               + name + '.jpg')
                except:
                    pass
    
def mergeWithELO(position, category):
    '''
    Purpose: Merge all player-specific information for a position group 
        contained in multiple batch-specific files into one cohesive file

    Inputs
    ------
        position : string
            Position group for which data exists and must be merged
            (options are 'DEF', 'QB', RB', and 'WR')
        category : string
            Category of positional data beinged merge (i.e. offense or defense)
    
    Outputs
    -------
        df_merge : Pandas DataFrame containing all information for a specified
            position group (OUTPUT TO DISK -- `player_info_POS_merged.csv`)
    '''      
    
    # read in the ELO data
    df_elo = pd.read_csv('positionData/Merged/elo_' + position + '.csv')
    
    # standardize school names for ELO data
    df_elo = renameSchool(df_elo, 'School')
    
    # read in the position data for all offensive or defensive players
    df_pos = pd.read_csv('positionData/Merged/players_' + category + '.csv',
                         parse_dates = ['birthday'])

    # merge the ELO data with ESPN player info data
    df_merge = pd.merge(df_elo, df_pos, how='left', 
                        left_on = ['Player', 'School'], 
                        right_on = ['nameFull', 'school'], 
                        indicator=True)
    
    # flags players that have duplicate entries for their unique ID's
    df_merge['duplicated'] = df_merge['unique_id'].duplicated(keep = False)
    print(str(df_merge['duplicated'].value_counts()[1]) + 
          ' duplicated players exist that need to be fixed in the ' + position
          + ' file.')
    
    # remove ages from birthdays
    df_merge['birthday'] = pd.to_datetime(df_merge['birthday'].apply(
            lambda x: str(x).split(' (')[0])).dt.date

    # format birthdays as a data object
    df_merge['birthday'] = pd.to_datetime(df_merge['birthday'].apply(
            lambda x: str(x).split(' (')[0])).dt.date

    # drop any rows that do not possess a last name [not useful player data]
    df_merge = df_merge[df_merge['unique_id'].apply(
            lambda x: len(str(x).split('-'))) > 2]
    
    # fill in the missing values for first names
    df_merge['nameFirst'] = df_merge['nameFirst'].astype(str)
    df_merge['nameFirst'] = df_merge.apply(lambda row: 
        row['Player'].split(' ')[0] if pd.isna(
                row['nameFirst']) else row['nameFirst'], axis=1)
        
    # fill in the missing values for last names
    df_merge['nameLast'] = df_merge.apply(lambda row: 
        row['Player'].split(' ')[1] if pd.isna(
                row['nameLast']) else row['nameLast'], axis=1)
        
    # delete the 'nameFull' column
    df_merge.drop(columns=['nameFull'], inplace = True)
    
    return df_merge

def renameSchool(df, name_var):
    '''
    Purpose: Rename a school/university to a standard name as specified in 
        the file `school_abbreviations.csv`

    Inputs
    ------
        df : Pandas Dataframe
            DataFrame containing a school-name variable for which the names
            need to be standardized
        name_var : string
            Name of the variable which is to be renamed/standardized
    
    Outputs
    -------
        list(row)[0] : string
            Standardized version of the school's name based on the first value
            in the row in the file `school_abbreviations.csv`
    '''  
    # read in school name information
    df_school_names = pd.read_csv(path_dir.joinpath(
            'positionData/school_abbreviations.csv'))    
     
    # convert the dataframe to a dictionary such that the keys are the
    #   optional spelling of each school and the value is the standardized
    #   name of the school
    dict_school_names = {}
    
    for index, row in df_school_names.iterrows():
        # isolate the alternative name columns
        names = row[[x for x in row.index if 'Name' in x]]
        # convert the row to a list that doesn't include NaN values
        list_names = [x for x in names.values.tolist() if str(x) != 'nan']
        # add the nickname to the team names as an alternative name
        nickname = row['Nickname']
        list_names_nicknames = list_names.copy()
        for name in list_names:
            list_names_nicknames.append(name + ' ' + nickname)
        # extract the standardized team name
        name_standardized = row['Team']
        # add the standardized name
        list_names_nicknames.append(name_standardized)
        # add the nickname to the standardized name
        list_names_nicknames.append(name_standardized + ' ' + nickname)
        # for every alternative spelling of the team, set the value to be
        #   the standardized name
        for name_alternate in list_names_nicknames:
            dict_school_names[name_alternate] = name_standardized
            
    df[name_var] = df[name_var].apply(
            lambda x: dict_school_names[x] if str(x) != 'nan' else '')
        
    return df    

def renameSchoolPictureURL(url):
    '''
    Purpose: Standardize a school's picture URL to point to the 500 pixel
                version rather than the scraped 250 pixel version

    Inputs
    ------
        url : string
            URL that points to a school's logo
    
    Outputs
    -------
        url_new : string
            Standardized version of the URL that points to the 500 pixel version
    '''      
    # handle teams with missing URLs
    if url == 'nan':
        return ''
    # handle non-standard teams
    elif '500/' not in url:
        return url
    else:
        team_id = url.split('.png')[0].split('500/')[1]
        url_new = 'https://a.espncdn.com/i/teamlogos/ncaa/500/' + team_id + '.png'
        return url_new

def scrapePictures(df_merge, position):
    '''
    Purpose: Clean up picture URL variables, drop variables that are no longer
            needed, then scrape images for both players and schools before
            outputting a JSON and CSV version of each file to disk

    Inputs
    ------
        df_merge : Pandas Dataframe
            DataFrame containing a school-name variable for which the names
            need to be standardized
        position : string
            Position group for which data exists and must be merged
            (options are 'DEF', 'QB', RB', and 'WR')
    
    Outputs
    -------
        url_new : string
            Standardized version of the URL that points to the 500 pxl version
    '''    
    # Rename the `pictureSchool` & `picturePlayer` variables to include URL
    df_merge.rename(
            columns = {'picturePlayer':'picturePlayerURL',
                       'pictureSchool':'pictureSchoolURL'}, inplace=True)

    # Drop the 'school' variables as they are no longer needed
    df_merge.drop(columns = ['school'], inplace = True)
    
    # Fill in missing values of 'pictureSchoolURL' based on 'School' names
    dict_school_urls = createSchoolPictureDict()
    list_urls = []
    for index, row in df_merge.iterrows():
        if ((pd.isna(row['pictureSchoolURL'])) and (row['School'] != '')):
            list_urls.append(dict_school_urls[row['School']])
        else:
            list_urls.append(row['pictureSchoolURL'])
    df_merge['pictureSchoolURL'] = list_urls
            
    # Create the `pictureSchoolPath` & `picturePlayerPath` variables to map
    #   the file location of the associated images 
    #   (i.e. /positionData/pictures/..)
    df_merge['picturePlayerPath'] = df_merge.apply(
            lambda row: ('/pictures/' + position + 
                         '/' + row['unique_id'] + '.png') 
            if not pd.isnull(row['picturePlayerURL']) else '', axis = 1)
    df_merge['pictureSchoolPath'] = df_merge['School'].apply(
            lambda x: '/pictures/School/' + x + '.png')
   
    # fill in missing values with blanks rather than float NaNs
    df_merge = df_merge.fillna('')

    # Convert the date object 'birthday' to its string equivalent
    df_merge['birthday'] = df_merge['birthday'].apply(lambda x: x.__str__())
    
    # output to csv
    df_merge.to_csv('positionData/Merged/pos_' + position + '.csv', 
                    index=False)
    
    # Convert the dataframe to a dictionary
    dict_pos = df_merge.to_dict('index')    
    
    # Write updated data (with paths to pictures vice URLs) to a .json file 
    #   ('pos_POSITION_final_pics.json')
    with open('positionData/Merged/pos_' + position + '.json', 'wt') as out:
        json.dump(dict_pos, out, sort_keys=True)
     
    # Minimize the dictionary for the purposes of picture scraping
    dict_pos_small = {}
    for key, value in dict_pos.items():
        dict_pos_small[dict_pos[key]['unique_id']] = value[
                'picturePlayerURL']
    
    dict_schools_small = {}
    for key, value in dict_pos.items():
        dict_schools_small[dict_pos[key]['School']] = value[
                'pictureSchoolURL']
    
    # Download the pictures for the players
    downloadPictures(dict_pos_small, position)
    
    # Download the pictures for the schools
    downloadPictures(dict_schools_small, 'School')
    
#==============================================================================
# Working Code
#==============================================================================
# Set the project working directory
path_dir = pathlib.Path('/home/ejreidelbach/Projects/draft-gem/src/static/')
os.chdir(path_dir)

#------------------------------------------------------------------------------
# Step 1. Merge positional data into 2 files:  Offensive and Defense
#------------------------------------------------------------------------------
combinePositionalData()

#------------------------------------------------------------------------------
# Step 2. Merge positional data with ELO data
#------------------------------------------------------------------------------
for position in ['QB', 'RB', 'WR', 'DEF']:
    if position == 'DEF':
        df_merge = mergeWithELO(position, 'defense')
    else:
        df_merge = mergeWithELO(position, 'offense')
      
    df_merge = df_merge.reset_index(drop = True)
    # drop wrong matches from dataframes (determined by manual inspection)
    if position == 'QB':
        df_merge = df_merge.drop(df_merge.index[[276, 927]])
    elif position == 'RB':  
        df_merge = df_merge.drop(df_merge.index[[476, 721, 
                                                 725, 763, 
                                                 809, 860, 
                                                 1003, 1004,
                                                 1300, 1307,
                                                 1308, 1425, 
                                                 1465, 1700,
                                                 1845, 2703,
                                                 3098]])
    elif position == 'WR':
        df_merge = df_merge.drop(df_merge.index[[817, 1012,
                                                 1145, 1772,
                                                 1773, 2076,
                                                 2188, 2420,
                                                 2528, 2816,
                                                 2894, 4200,
                                                 4420, 4444,
                                                 4546, 4573]])
    elif position == 'DEF':
        df_merge = df_merge.drop(df_merge.index[[1884, 2104,
                                                 2329, 3090,
                                                 3638, 3822,
                                                 3836, 4119, 
                                                 4625, 4626,
                                                 5154, 5319, 
                                                 5320, 5321,
                                                 5534, 5535,
                                                 5539, 5541,
                                                 5545, 5566,
                                                 6302, 6364,
                                                 6417, 7574,
                                                 7777, 8133,
                                                 8765, 8883,
                                                 8962, 9349,
                                                 11591, 11977, 
                                                 12303, 13361]])
    try:
        df_merge['duplicated'] = df_merge['unique_id'].duplicated(keep = False)
        print('After pruning mis-matches, there are ' 
              + str(df_merge['duplicated'].value_counts()[1])
              + ' duplicates remaining')
    except:
        print('No duplicates found')
    
    # drop `_merge` and `duplicated` columns as they are no longer needed
    df_merge.drop(columns = ['_merge', 'duplicated'], inplace = True)

    #--------------------------------------------------------------------------
    # Step 3. Scrape pictures for players/teams and output finalized pos. data
    #--------------------------------------------------------------------------
    scrapePictures(df_merge, position)