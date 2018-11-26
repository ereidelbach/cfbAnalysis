#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:55:09 2018

@author: ejreidelbach

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import os  
import pandas as pd
import pathlib
import tqdm

#==============================================================================
# Reference Variable Declaration
#============================================================================== 
#list_stats_defense = ['rushing', 'passing', 'receiving',]
#list_stats_offense = []
list_stats_special = ['punt_returns', 'kickoff_returns', 'punting', 'kickoffs',
                      'place_kicking',]

#==============================================================================
# Function Definitions
#==============================================================================   
def identifyRawDataPaths(path_project):
    '''
    Purpose: In their raw format, statistics are broken out into individual 
        files for each category, for every available year. This function
        loops over every stat folder, for each team, in `data/raw/CFBStats`
        and creates a dictionary to store a record of statistical folders that 
        exist and file paths for every statistic for every year for every team    
        
    Input:
        (1) path_project (pathlib Path): Project directory file path containing
                the project's files
        
    Output:
        (1) dict_stat_files (dictionary): All paths for each team's statistics
                for every stat/year combo
        (2) list_stat_folders (list): All stat categories
    '''
    # Set the path to the raw data folder
    path_data_raw = path_project.joinpath(pathlib.Path('data/raw/CFBStats'))
    
    # Create a dictionary for storing folder paths for every stat/year combo
    dict_stat_files = {}
    
    # Identify the team folders
    list_path_team = [f for f in path_data_raw.iterdir() if f.is_dir()]
    list_path_team.sort()
    
    # Identify the types of statistical category/folders
    list_stat_folders = [x for x in list_path_team[0].iterdir() if x.is_dir()]
    list_stat_folders = [str(x).split('/')[-1] for x in list_stat_folders]
    list_stat_folders.sort()
    
    # Loop over every team's folders
    for path_team in list_path_team:
        
        # Identify all statistical files on record for the team
        list_team_files = list(path_team.glob('**/*.csv'))
        list_team_files.sort()
        
        # Iterate over every file, identify the type of statistic, identify the
        #   year, and add the file to the correct portion of the dictionary
        for path_stat in list_team_files:
            category = str(path_stat).split('/')[-2]
            year = str(path_stat).split('/')[-1].split('.csv')[0].split('_')[-1]
            
            # Check to make sure there is an actual statistic (not just '2014')
            if len(str(path_stat).split('/')[-1]) > 8:
                statistic = '_'.join(str(path_stat).split('/')[-1].split(
                        '.csv')[0].split('_')[:-1])
            else:
                statistic = category
            
            # Check if the key exists for the specified stat/year combo 
            #   If it does, append the value to the existing list
            #   If not, create the list as a value for the new key
            if category + '/' + statistic + '_' + year in dict_stat_files:
                key_list = dict_stat_files[str(category + '/' + 
                                    statistic + '_' + year)]
                key_list.append(path_stat)
                dict_stat_files[str(category + '/' + 
                                    statistic + '_' + year)] = key_list
            else:
                temp_list = []
                temp_list.append(path_stat)
                dict_stat_files[str(category + '/' + 
                                    statistic + '_' + year)] = temp_list

    return dict_stat_files, list_stat_folders

def directoryCheck(list_stat_folders):
    '''
    Purpose: Run a check of the /data/interim/CFBStats/ folder to see if a 
        'ALL' folder exists for holding all combined team statistics, and their
        respective subfolders. If a folder is missing, create it.
        
    Input:
        (1) list_stat_folders (list): Contains a listing of all statistical
                categories that exist in the data
    
    Output:
        - NONE
    '''
    # Check for the 'ALL' data folder 
    pathlib.Path('data/interim/CFBStats/' + 'ALL').mkdir(
            parents=True, exist_ok=True)
    # Iterate over every statistical sub-folder in the 'ALL' data folder
    for category in list_stat_folders:
        # Check for required sub-folders
        pathlib.Path('data/interim/CFBStats/ALL', category).mkdir(
                parents=True, exist_ok=True)
    
def combineYears(path_project, dict_stat_files):
    '''
    Purpose: In their raw format, statistics are broken out into individual 
        files for each category, for every available year. This function
        loops over every stat folder, for each team, and merges these yearly
        files together so that there is one aggregate .csv file for each
        category which can then be placed in the 'ALL' folder.
        
    Input:
        (1) dict_stat_files (dictionary): All paths for each team's statistics
                for every stat/year combo
        
    Output:
        (1) (.csv file) A single .csv file for each statistical category 
                containing data for that stat/year combo
    '''    
    # Loop over every stat/year combo and retrieve the associated list of paths
    for stat_name_year, list_paths in tqdm.tqdm(dict_stat_files.items()):
        
        # Create a master dataframe for storing all the stat/year data
        df_stat_year = pd.DataFrame()
        
        # Iterate over every path available for the stat/year combo
        for path_file in list_paths:
        
            # Retrieve data from the specified path
            df_team = pd.read_csv(path_file)
            
            # Add the team name to the dataframe
            df_team['team'] = str(path_file).split('CFBStats/')[1].split('/')[0]
            
            # If the master dataframe is empty, set it to equal this dataframe
            if len(df_stat_year) ==  0:
                df_stat_year = df_team.copy()
            else:
                df_stat_year = df_stat_year.append(df_team)

        df_stat_year.reset_index(inplace=True, drop=True)                
        df_stat_year.to_csv(path_project.joinpath(pathlib.Path(
                'data/interim/CFBStats/ALL', stat_name_year + '.csv')), 
                index = False)
            
def mergeStatsGame(year, folder, statistic):
    '''
    Purpose: Combine all statistics that are derived from the `Game Logs`
        portion of the CFBStats website into one file.  These files contain the
        `_game_` tag in their name.
    
    Input:
        (1) year (string): Year for which data is being merged (i.e. `2018`)
        (2) folder (string): Name of the statistical cagegory / subfolder
        (2) statistic (string): Name of the statistic being merged
        
    Output:
        (1) (.csv file) 1 .csv file for each statistical category containing
            data for all years for all teams
    '''  
    # Create DataFrame for storing data for all years
    df_all = pd.DataFrame()

    # Aggregate all yearly files that exist for the category  
    for path_file in list_path_files:
        
        # Import Year's worth of data
        df_year = pd.read_csv(path_file)
        
        # Append the yearly data to the aggregate DataFrame
        df_all = df_all.append(df_year)   
    
    # Sort the DataFrame by season
    df_all = df_all.sort_values(by = ['season'])
    
    # Reset the index to account for multiple DataFrames
    df_all = df_all.reset_index()
    
    # Drop the old index
    df_all.drop(['index'], axis=1, inplace=True)
    
    # Create the output path for the new .csv file
    output_path = pathlib.Path(str(path_category).replace('raw','interim'))
    
    # Export the CSV to the same folder in `data/interim`
    df_all.to_csv(output_path.joinpath(name_category + '.csv'), index = False)
    
def mergeStatsSituational():
    pass

def mergeStatsSplit():
    pass

#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
path_project = pathlib.Path(__file__).resolve().parents[2]
os.chdir(path_project)

# Identify Raw Data file paths and Statistical Categories
dict_paths_raw_data, list_stat_folders = identifyRawDataPaths(path_project)

# Verify the required folder structure in `data/interim/CFBStats/ALL` exists
directoryCheck(list_stat_folders)

# Combine yearly statistics into one file per statistical category
combineYears(path_project, dict_paths_raw_data)

# Create a master roster list of all players in the database
#aggregateRosters(path_project)