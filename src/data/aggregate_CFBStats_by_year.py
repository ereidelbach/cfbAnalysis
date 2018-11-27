#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:55:09 2018

@author: ejreidelbach

:DESCRIPTION:
    - Reads in all team data contained within `data/interim/CFBStats/', combines
        it so that info for every team is condensed down to one file for per
        category and writes the the new file to `data/interim/CFBStats/ALL`

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
list_stats_special = ['punt_returns', 'kickoff_returns', 'punting', 'kickoffs',
                      'place_kicking',]

# a list of variables present in all game-log related stat files
list_vars_game = ['date', 'opponent', 'opp_rank', 'home_away', 'result', 
                  'pts_for', 'pts_against', 'pts_diff', 'surface',
                  'month', 'day', 'year', 'day_of_week', 'season', 'team']
list_vars_split = ['split', 'season', 'team']
list_vars_situational = ['situation', 'g', 'season', 'team']

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
    # Check for the 'ALL' data folder and create it if not present
    pathlib.Path('data/interim/CFBStats/' + 'ALL').mkdir(
            parents=True, exist_ok=True)
    # Iterate over every statistical sub-folder in the 'ALL' data folder
    for category in list_stat_folders:
        # Check for required sub-folders and create them if not present
        pathlib.Path('data/interim/CFBStats/ALL', category).mkdir(
                parents=True, exist_ok=True)
    # Check for the 'merged' folder and create it if not present
    pathlib.Path('data/interim/CFBStats/ALL', 'merged').mkdir(
            parents=True, exist_ok=True)
    # Check for every statistical sub-folder in the `merged` folder and
    #   create it if not present
    for category in list_stat_folders:
        # Check for the recquired sub-folder and create it if not present
        pathlib.Path('data/interim/CFBStats/ALL/merged', category).mkdir(
                parents=True, exist_ok=True)        
    # Check for the `merged_final` folder and create it if not present
    pathlib.Path('data/interim/CFBStats/ALL', 'merged_final').mkdir(
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
        df_stat_year.to_csv(path_project.joinpath(
                'data/interim/CFBStats/ALL', stat_name_year + '.csv'), 
                index = False)
            
def mergeStatsGame(path_project):
    '''
    Purpose: Combine all statistics that are derived from the `Game Logs`
        portion of the CFBStats website into one file.  These files contain the
        `_game_` tag in their name and are located in the `games` subfolder.
    
    Input:
        (1) path_project (pathlib Path): Project directory file path containing
                the project's files
        
    Output:
        (1) (.csv file) A .csv file for offense, defense and special team 
                game log statistics
    '''  
    # Set the Game Logs path project
    path_dir = path_project.joinpath('data/interim/CFBStats/ALL/games')
    
    # Identify all statistical files on record for the team
    list_game_files = list(path_dir.glob('**/*.csv'))
    list_game_files.sort()
    
    # Identify all years that exist in the data
    list_temp = [str(x).split('games/')[1] for x in list_game_files]
    list_years = list(set([x.split('.csv')[0].split(
            '_')[-1] for x in list_temp]))
    list_years.sort()
        
    # Iterate over every year
    for year in tqdm.tqdm(list_years):
        
        # Create DataFrame for storing data all three category types
        df_def = pd.DataFrame()     # defense
        df_off = pd.DataFrame()     # offense
        df_spc = pd.DataFrame()     # special teams        
        
        # Find all the files that belong to the given year
        list_files_year = [x for x in list_game_files if year in str(x)]
        # Aggregate all files for the given year that exist for each category  
        for path_file in list_files_year:
            
            # Import the file
            df_year = pd.read_csv(path_file)            
            
            # Determine the stat category (and remove `_year` from the end)
            category = str(path_file).split('games/')[1].split('.csv')[0][:-5]
            
            # Determine the category prefix
            cat_prefix = '_'.join([x for x in category.split('_') if x not in [
                    'offense', 'defense', 'team', 'opponent','game']])
            
            # Find the columns that are unique to the file
            list_cols = [x not in list_vars_game for x in list(df_year.columns)]
            list_cols = list(set(list(df_year.columns)) - set(list_vars_game))
            
            # remove spaces and '.' from variable names
            list_cols_prefix = [x.replace(' ','_').replace('.','') for x in list_cols]
            list_cols_prefix = [cat_prefix + '_' + x for x in list_cols_prefix]
            
            dict_renamed_cols = dict(zip(list_cols, list_cols_prefix))
            df_year = df_year.rename(columns=dict_renamed_cols)
            
            # Check to see what category the file belongs to
            # Ignore `all_purpose` yards
            if 'all_purpose' in category:
                continue
            # Special Teams-related files
            elif any(x in category for x in list_stats_special):
                if len(df_spc) == 0:
                    df_spc = df_year
                else:
                    df_spc = df_spc.merge(df_year, on=list_vars_game)
            # Offensive-related files
            elif 'offense' in category or 'team' in category:
                if len(df_off) == 0:
                    df_off = df_year
                else:
                    df_off = df_off.merge(df_year, on=list_vars_game)
            # Defensive-related files
            elif 'defense' in category \
                or 'opponent' in category \
                or 'fumble_returns' in category \
                or 'interceptions' in category \
                or 'sacks' in category \
                or 'tackles' in category:
                if len(df_def) == 0:
                    df_def = df_year
                else:
                    df_def = df_def.merge(df_year, on=list_vars_game)
            # Add turnover stats to offense and defense
            elif 'turnover' in category:
                df_off = df_off.merge(df_year, on=list_vars_game)
                df_def = df_def.merge(df_year, on=list_vars_game)
            # Check for any missed files
            else:
                print(category.split('games/')[1])
    
        # Export all merged dataframes to a CSV file for that year
        df_def.to_csv(path_dir.parent.joinpath('merged/game_defense_' + year 
                                               + '.csv'), index = False)
        df_off.to_csv(path_dir.parent.joinpath('merged/game_offense_' + year 
                                        + '.csv'), index = False)
        df_spc.to_csv(path_dir.parent.joinpath('merged/game_special_' + year 
                                        + '.csv'), index = False)

def mergeStatsSituational(path_project):
    '''
    Purpose: Combine all statistics that are derived from the `Situational 
        Stats` portion of the CFBStats website into one file.  These files 
        contain the `_situational_` tag in their name and are located in the 
        `situations` subfolder.
    
    Input:
        (1) path_project (pathlib Path): Project directory file path containing
                the project's files
        
    Output:
        (1) (.csv file) A .csv file for offense, defense and special team 
                game log statistics
    '''  
    # Set the Game Logs path project
    path_dir = path_project.joinpath('data/interim/CFBStats/ALL/situations')
    
    # Identify all statistical files on record for the team
    list_files = list(path_dir.glob('**/*.csv'))
    list_files.sort()

    # Identify all years that exist in the data
    list_temp = [str(x).split('situational')[1] for x in list_files]
    list_years = list(set([x.split('.csv')[0].split(
            '_')[-1] for x in list_temp]))
    list_years.sort()

    # Iterate over every year
    for year in tqdm.tqdm(list_years):
        # Create DataFrame for storing data all three category types
        df_def = pd.DataFrame()     # defense
        df_off = pd.DataFrame()     # offense
        
        # Find all the files that belong to the given year
        list_files_year = [x for x in list_files if year in str(x)]
        # Aggregate all files for the given year that exist for each category  
        for path_file in list_files_year:
            
            # Import the file
            df_year = pd.read_csv(path_file)            
            
            # Determine the stat category (and remove `_year` from the end)
            filename = str(path_file).split('situations/')[1]
            if 'passing' in filename:
                category = 'pass'
            elif 'rushing' in filename:
                category = 'rush'
            else:
                print('Error: Did not properly categorize file!')
            
            # Find the columns that are unique to the file
            list_cols_old = list(set(list(df_year.columns)) - set(
                    list_vars_situational))
            
            # remove spaces and '.' from variable names
            list_cols_new = [x.replace(' ','_').replace(
                    '.','') for x in list_cols_old]
            list_cols_new = [category + '_' + x for x in list_cols_new]
            
            dict_renamed_cols = dict(zip(list_cols_old, list_cols_new))
            df_year = df_year.rename(columns=dict_renamed_cols)

            # Check to see what category the file belongs to
            # Offensive-related files
            if 'offense' in filename:
                if len(df_off) == 0:
                    df_off = df_year
                else:
                    df_off = df_off.merge(df_year, on=list_vars_situational)
            # Defensive-related files
            elif 'defense' in filename:
                if len(df_def) == 0:
                    df_def = df_year
                else:
                    df_def = df_def.merge(df_year, on=list_vars_situational)
            # Check for any missed files
            else:
                print('Error: Did not properly merge file: ' + filename)
    
        # Export all merged dataframes to a CSV file for that year
        df_def.to_csv(path_dir.parent.joinpath(
                'merged/situations/situational_defense_' 
                + year + '.csv'), index = False)
        df_off.to_csv(path_dir.parent.joinpath(
                'merged/situations/situational_offense_' 
                + year + '.csv'), index = False)            

def mergeStatsSplit(path_project):
    '''
    Purpose: Combine all statistics that are derived from the `Split Stats`
        portion of the CFBStats website into one file.  These files contain the
        `_split_` tag in their name and are located in the `splits` subfolder.
    
    Input:
        (1) path_project (pathlib Path): Project directory file path containing
                the project's files
        
    Output:
        (1) (.csv file) A .csv file for offense, defense and special team 
                game log statistics
    '''  
    # Set the Game Logs path project
    path_dir = path_project.joinpath('data/interim/CFBStats/ALL/splits')

    # Export all merged dataframes to a CSV file for that year
    df_def.to_csv(path_dir.parent.joinpath('merged/split_defense_' 
                                           + year + '.csv'), index = False)

def mergeStatsPlayers(path_project):
    '''
    Purpose: Combine all statistics that are derived from the `Players`
        portion of the CFBStats website into one file.  These files contain the
        `_player_` tag in their name and are located in the `players` subfolder.
    
    Input:
        (1) path_project (pathlib Path): Project directory file path containing
                the project's files
        
    Output:
        (1) (.csv file) A .csv file for offense, defense and special team 
                game log statistics
    '''  

def combineStatsIntoOne(path_folder):
    '''
    Purpose: Combine all `merged` statistics into one file for each statistical
        grouping such that all years are contained within one file
    
    Input:
        (1) path_folder (pathlib Path): Directory file path containing
                the project's files for all years
        
    Output:
        (1) (.csv file) A single .csv file that contains data for all years
    '''         
    # Find every folder in the Data directory
    list_files = list(path_folder.glob('*.csv'))
    list_files.sort()
    
    # Determine the statistical categories to be combined
    list_file_categories = list(set(['_'.join(
            str(x).split('/')[-1].split('_')[:-1]) for x in list_files]))
    
    # Set the output folder
    path_output = pathlib.Path(str(
            path_folder).split('ALL')[0], 'ALL', 'merged_final')
    
    # Iterate over all the statistical categories for which files exist
    for file_category in tqdm.tqdm(list_file_categories):

        # Create a dataframe for holding all roster information
        df_all = pd.DataFrame()

        # Iterate over every folder and compile all roster into df_all
        for file in [x for x in list_files if file_category in str(x)]:
            df = pd.read_csv(file)
            df_all = df_all.append(df)
        
        # Resest the DataFrame Index
        df_all = df_all.reset_index()
        # Drop the old DataFrame Index
        df_all.drop(['index'], axis=1, inplace=True)
        # Remove all spaces from column names and replace with a '_'
        df_all.columns = [x.replace(' ','_') for x in list(df_all.columns)]
        # Export to a CSV File
        df_all.to_csv(path_output.joinpath(file_category + '_all.csv'),
                      index=False)  

#==============================================================================
#--- Working Code
#==============================================================================

# Set the project working directory
path_project = pathlib.Path(__file__).resolve().parents[2]
os.chdir(path_project)

#------------------------------------------------------------------------------
# Identify Raw Data file paths and Statistical Categories
dict_paths_raw_data, list_stat_folders = identifyRawDataPaths(path_project)

# Verify the required folder structure in `data/interim/CFBStats/ALL` exists
directoryCheck(list_stat_folders)


#------------------------------------------------------------------------------
# Combine yearly statistics into one file per statistical category
combineYears(path_project, dict_paths_raw_data)


#------------------------------------------------------------------------------
# Merge all statistics files such that there are combined versions for every
#   year (e.g. game_defense_2009.csv)

# Game Logs
mergeStatsGame(path_project)

# Situational Stats
mergeStatsSituational(path_project)

# Split Stats
mergeStatsSplit(path_project)

# Player Stats
mergeStatsPlayers(path_project)


#------------------------------------------------------------------------------
# Combine all `merged` files such that there is one file for all years
#------------------------------------------------------------------------------
# Games
combineStatsIntoOne(path_project.joinpath(
        'data/interim/CFBStats/ALL/merged/games'))

# Players
combineStatsIntoOne(path_project.joinpath(
        'data/interim/CFBStats/ALL/merged/players'))

# Situations
combineStatsIntoOne(path_project.joinpath(
        'data/interim/CFBStats/ALL/merged/situations'))

# Splits
combineStatsIntoOne(path_project.joinpath(
        'data/interim/CFBStats/ALL/merged/splits'))

# Records
combineStatsIntoOne(path_project.joinpath(
        'data/interim/CFBStats/ALL/records'))

# Rosters
combineStatsIntoOne(path_project.joinpath(
        'data/interim/CFBStats/ALL/rosters'))

# Schedules
combineStatsIntoOne(path_project.joinpath(
        'data/interim/CFBStats/ALL/schedules'))

# Create a master roster list of all players in the database
#aggregateRosters(path_project)
