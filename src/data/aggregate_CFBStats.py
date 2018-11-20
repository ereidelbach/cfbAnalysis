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
# Function Definitions / Reference Variable Declaration
#==============================================================================   
def identifyRawData(path_project):
    '''
    Purpose: In their raw format, statistics are broken out into individual 
        files for each category, for every available year. This function
        loops over every stat folder, for each team, in `data/raw/CFBStats`
        and create a dictionary to store a record of folders that exist 
        for each team       
        
    Input:
        (1) path_project (pathlib Path): Project directory file path containing
                the project's files
        
    Output:
        (1) dict_paths_all (dictionary): Contains a listing of all subfolders
                and paths for each team on file
    '''
    # Set the path to the raw data folder
    path_data_raw = path_project.joinpath(pathlib.Path('data/raw/CFBStats'))
    
    # Create a dictionary for storing all folder paths for each team
    dict_paths_all = {}
    
    # Identify the team folders
    list_path_team = [f for f in path_data_raw.iterdir() if f.is_dir()]
    list_path_team.sort()
    
    # Loop over every team's folders
    for path_team in list_path_team:
        # Create a dictionary for storing each team's folder paths
        dict_paths_team = {}
        
        # Identify every category subfolder the team has
        list_path_subfolder = [x for x in path_team.iterdir() if x.is_dir()]
        list_path_subfolder.sort()
        
        # Loop over every subfolder and add it to the team's dictionary
        for path_subfolder in list_path_subfolder:
            dict_paths_team[str(path_subfolder).split('/')[-1]] = path_subfolder
            
        # Add the team's subfolder to the master dictionary
        dict_paths_all[str(path_team).split('/')[-1]] = dict_paths_team
        
    return dict_paths_all

def directoryCheck(dict_paths_all):
    '''
    Purpose: Run a check of the /data/interim/CFBStats/ folder to see if a 
        folder exists for every team, and its respective subfolders. If 
        a folder is missing, create it.
        
    Input:
        (1) dict_paths_all (dictionary): Contains a listing of all subfolders
                and paths for each team on file
    
    Output:
        - NONE
    '''
    # Iterate over every team
    for team_name, dict_team in dict_paths_all.items():
        # Check for the team folder
        pathlib.Path('data/interim/CFBStats/' + team_name).mkdir(
                parents=True, exist_ok=True)
        # Iterate over every sub-folder the team possesses
        for category, category_path in dict_team.items():
            # Check for required sub-folders
            pathlib.Path('data/interim/CFBStats/', team_name, category).mkdir(
                    parents=True, exist_ok=True)  
    
def combineYears(path_project, dict_paths_all):
    '''
    Purpose: In their raw format, statistics are broken out into individual 
        files for each category, for every available year. This function
        loops over every stat folder, for each team, and merges these yearly
        files together so that there is one aggregate .csv file for each
        category.
        
    Input:
        (1) path_project (pathlib Path): Project directory file path containing
                the project's files
        (2) dict_paths_all (dictionary): Contains a listing of all subfolders
                and paths for each team on file
        
    Output:
        (1) (.csv file) 1 .csv file for each statistical category containing
                data for all years
    '''    
    # Loop over every team's folders
    for team_name, dict_team in dict_paths_all.items():
        
        # Loop over every category subfolder the team has
        for category, category_path in tqdm.tqdm(dict_team.items()):
            
            # Identify every statistical category that is stored in the folder
            list_path_files = list(category_path.glob('*.csv'))
            
            # Records, Rosters and Schedules do not have sub-categories
            if category in ['records', 'rosters', 'schedules']:
            
                # Write the DataFrame to a .csv file
                writeAggregateStatsToFile(list_path_files, 
                                          category_path, category)
                
            # Account for the other folders with multiple categores in one
            else:
                # Identify all unique sub-category names within the folder
                list_sub_categories = list(set(['_'.join(str(x).split(
                        '/')[-1].split('_')[:-1]) for x in list_path_files]))
    
                # Iterate over each sub-category 
                for sub_category in list_sub_categories:

                    # Identify the sub-category files
                    list_sub_path_files = list(
                            category_path.glob(sub_category + '*.csv'))

                    # Aggregate the data for the sub-category and save it .csv
                    writeAggregateStatsToFile(list_sub_path_files, 
                                              category_path, sub_category)
        
        print('Done with: ' + team_name)
            
def writeAggregateStatsToFile(list_path_files, path_category, name_category):
    '''
    Purpose: Write a Pandas DataFrame (df_all) containing statistical 
        information for all years within a category to a .csv file in the
        `data/interim/CFBStats/path_category` folder
    
    Input:
        (1) list_path_files (list): List of file path's for every yearly
                statistic .csv file in a the category folder
        (2) path_category (pathlib Path): Category directory file path 
                containing the project's files
        (3) name_category (string): Name of the statistical category
                for which historical values have been aggregated
    Output:
        (1) (.csv file) 1 .csv file for each statistical category containing
            data for all years
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

def cleanRoster(roster):
    '''
    Purpose: Clean up errors in a team's roster. Such errors include missing 
        values (e.g. roster numbers, position, hometown, etc.).  In addition,
        create the redshirt variables: redshirt_yr (boolean indicator if a 
        specific year is a player's redshirt year) and redshirted (boolean
        indicator if a player redshirted in their career)
        
    Input:
        (1) roster (DataFrame): Table containing a team's roster information
        
    Output:
        (1) roster_clean (DataFrame): Table with missing values filled in and
            redshirt variables included
    '''

def aggregateRosters(path_project):
    '''
    Purpose: Ingest roster information for all teams and combine into one 
        massive roster file
        
    Input:
        (1) path_project (pathlib Path): Project directory file path containing
                the project's files
        
    Output
        (1) (.csv file) .csv file containing all players in the database
                `merged_rosters.csv`
    '''
    # Set the directory where the files are located
    path_data_interim = path_project.joinpath(pathlib.Path(
            'data/interim/CFBStats'))
    
    # Find every folder in the Data directory
    list_files_rosters = list(path_data_interim.glob('*/rosters/*.csv'))
    list_files_rosters.sort()
    
    # Create a dataframe for holding all roster information
    df_master = pd.DataFrame()
    
    # Iterate over every folder and compile all roster into df_master
    for file in list_files_rosters:
        df = pd.read_csv(file)
        df['school'] = str(file).split('CFBStats/')[1].split('/rosters.csv')[0]
        df_master = df_master.append(df)
        print('Done with: ' +str(file).split('/rosters')[0].split('/')[-1])
        
    # Resest the DataFrame Index
    df_master = df_master.reset_index()
    # Drop the old DataFrame Index
    df_master.drop(['index'], axis=1, inplace=True)
    # Export to a CSV File
    df_master.to_csv(path_data_interim.joinpath(pathlib.Path(
                    'merged_rosters.csv')), index=False)  

#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
path_project = pathlib.Path(__file__).resolve().parents[2]
os.chdir(path_project)

# Identify Raw Data
dict_paths_raw_data = identifyRawData(path_project)

# Verify the required folder structure in `data/interim/CFBStats/` exists
directoryCheck(dict_paths_raw_data)

# Combine yearly statistics into one file per statistical category
combineYears(path_project, dict_paths_raw_data)

# Create a master roster list of all players in the database
#aggregateRosters(path_project)