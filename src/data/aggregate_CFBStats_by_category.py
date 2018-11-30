#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:55:09 2018

@author: ejreidelbach

:DESCRIPTION:
    - Reads in all team data contained within `data/interim/CFBStats/', 
        combines it so that info for every team is condensed down to one file 
        for per category and writes the the new file to 
        `data/interim/CFBStats/ALL/merged_final`

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import builtins
import pandas as pd
import pathlib
import tqdm
from rename_variables_CFBStats import renameVariables

#==============================================================================
# Reference Variable Declaration
#============================================================================== 
list_stats_special = ['punt_returns', 'kickoff_returns', 'punting', 'kickoffs',
                      'place_kicking',]

# a list of variables present in all game-log related stat files
list_vars_game = ['date', 'opponent', 'opp_rank', 'home_away', 'result', 
                  'pts_for', 'pts_against', 'pts_diff', 'surface',
                  'month', 'day', 'year', 'day_of_week', 'season', 'team']
list_vars_split = ['g', 'split', 'season', 'team']
list_vars_situational = ['situation', 'season', 'team']
list_vars_player = ['name', 'yr', 'pos', 'g', 'season', 'team']

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
        df_spc_def = pd.DataFrame() # special teams (defense)
        df_spc_off = pd.DataFrame() # special teams (offense)      
        
        # Find all the files that belong to the given year
        list_files_year = [x for x in list_game_files if year in str(x)]
        # Aggregate all files for the given year that exist for each category  
        for path_file in list_files_year:
            
            # Import the file
            df_year = pd.read_csv(path_file)
           
            # Determine the stat category (and remove `_year` from the end)
            category = str(path_file).split('games/')[1].split('.csv')[0][:-5]
            
            # Determine the stat sub-category by slicing on `_`
            #   Note:  This method won't work for all variables and requires 
            #   special handling for the following variables:
            #   fumble_returns, interceptions, misc._defense, sacks, 
            #   tackles_for_loss, tackles, turnover_margin
            if builtins.any(category.split('_')[0] in x for x in 
                            ['fumble_returns', 'interceptions', 'misc._defense', 
                             'sacks', 'tackles_for_loss', 'tackles',
                             'turnover_margin']):
                sub_category = '_'.join(category.split('_')[:-1])
            else:
                sub_category = '_'.join(category.split('_')[:-2])
            
            # Rename the variables in the year DataFrame to match their category
            df_year = renameVariables(df_year, sub_category)
            
            # Check to see what category the file belongs to
            # Special Teams-related files
            if any(x in category for x in list_stats_special):
                # Special Teams Defense-related files
                if 'defense' in category or 'opponent' in category:
                    if len(df_spc_def) == 0:
                        df_spc_def = df_year
                    else:
                        df_spc_def = df_spc_def.merge(
                                df_year, on=list_vars_game)
                # Special Teams Offense-related files
                elif 'offense' in category or 'team' in category:
                    if len(df_spc_off) == 0:
                        df_spc_off = df_year
                    else:
                        df_spc_off = df_spc_off.merge(
                                df_year, on=list_vars_game)
            # Offensive-related files
            elif (('offense' in category and 'defense' not in category) 
                    or 'team' in category):
                if 'all_purpose' not in category:    # ignore all_purpose yards
                    if len(df_off) == 0:
                        df_off = df_year
                    else:
                        # remove duplicate columns: rush_yds & pass_yds
                        if 'total_offense' in category:
                            list_cols_keep = list(set(list(df_year.columns)) 
                                            - set(['rush_yds', 'pass_yds']))
                            df_year = df_year[list_cols_keep]
                        df_off = df_off.merge(df_year, on=list_vars_game)
            # Defensive-related files
            elif 'defense' in category \
                or 'opponent' in category \
                or 'fumble_returns' in category \
                or 'interceptions' in category \
                or 'sacks' in category \
                or 'tackles' in category:
                if 'all_purpose' not in category:   # ignore all_purpose yards
                    if len(df_def) == 0:
                        df_def = df_year
                    else:
                        # remove duplicate columns: rush_yds & pass_yds
                        if 'total_offense' in category:
                            list_cols_keep = list(set(list(df_year.columns)) 
                                            - set(['rush_yds', 'pass_yds']))
                            df_year = df_year[list_cols_keep]                        
                        df_def = df_def.merge(df_year, on=list_vars_game)
            # Add turnover stats to offense and defense
            elif 'turnover' in category:
                df_off = df_off.merge(df_year, on=list_vars_game)
                df_def = df_def.merge(df_year, on=list_vars_game)
            # Check for any missed files
            else:
                print(category)
    
        # Export all merged dataframes to a CSV file for that year
        df_def.to_csv(path_dir.parent.joinpath('merged/games/game_defense_' 
                                               + year + '.csv'), index = False)
        df_off.to_csv(path_dir.parent.joinpath('merged/games/game_offense_' 
                                               + year + '.csv'), index = False)
        df_spc_def.to_csv(path_dir.parent.joinpath(
                'merged/games/game_special_defense_' 
                + year + '.csv'), index = False)
        df_spc_off.to_csv(path_dir.parent.joinpath(
                'merged/games/game_special_offense_' 
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
    # Set the Game Logs path project
    path_dir = path_project.joinpath('data/interim/CFBStats/ALL/players')

    # Identify all statistical files on record for the team
    list_files = list(path_dir.glob('**/*.csv'))
    list_files.sort()

    # Identify all years that exist in the data
    list_temp = [str(x).split('players/')[1] for x in list_files]
    list_years = list(set([x.split('.csv')[0].split(
            '_')[-1] for x in list_temp]))
    list_years.sort()

    # Iterate over every year
    for year in tqdm.tqdm(list_years):
        # Create DataFrame for storing data all three category types
        df_def = pd.DataFrame()         # defense
        df_off = pd.DataFrame()         # offense
        df_spc_ret  = pd.DataFrame()    # special teams (punt/kick returns)
        df_spc_kick = pd.DataFrame()    # special teams (place kicking/punting)
        
        # Find all the files that belong to the given year
        list_files_year = [x for x in list_files if year in str(x)]
        # Aggregate all files for the given year that exist for each category  
        for path_file in list_files_year:
            
            # Import the file
            df_year = pd.read_csv(path_file)
           
            # Determine the stat category (and remove `_year` from the end)
            category = str(path_file).split('players/')[1].split('.csv')[0][:-5]
            
            # Determine the stat sub-category
            sub_category = category.split('_player')[0]
            
            # Rename the variables in the year DataFrame to match their category
            df_year = renameVariables(df_year, sub_category)
            
            # Check to see what category the file belongs to
            # Special Teams-related files
            if any(x in category for x in list_stats_special):
                # Handle Return Stats
                if 'returns' in category:
                    if len(df_spc_ret) == 0:
                        df_spc_ret = df_year
                    else:
                        df_spc_ret = df_spc_ret.merge(
                                df_year, how='outer', on=list_vars_player)
                # Handle Kicking/Punting related stats
                else:
                    if len(df_spc_kick) == 0:
                        df_spc_kick = df_year
                    else:
                        df_spc_kick = df_spc_kick.merge(
                                df_year, how='outer', on=list_vars_player)
            # Offensive-related files
            elif 'running' in category \
                or 'passing' in category \
                or 'receiving' in category \
                or 'rushing' in category \
                or 'scoring' in category \
                or 'offense' in category:
                if 'all_purpose' not in category:    # ignore all_purpose yards
                    if len(df_off) == 0:
                        df_off = df_year
                    else:
                        # remove duplicate columns: rush_yds & pass_yds
                        if 'total_offense' in category:
                            list_cols_keep = list(set(list(df_year.columns)) 
                                            - set(['rush_yds', 'pass_yds']))
                            df_year = df_year[list_cols_keep]
                        df_off = df_off.merge(df_year, how='outer', 
                                              on=list_vars_player)
            # Defensive-related files
            elif 'defense' in category \
                or 'fumble' in category \
                or 'interceptions' in category \
                or 'sacks' in category \
                or 'tackles' in category:
                if 'all_purpose' not in category:   # ignore all_purpose yards
                    if len(df_def) == 0:
                        df_def = df_year
                    else:
                        # remove duplicate columns: rush_yds & pass_yds
                        if 'total_offense' in category:
                            list_cols_keep = list(set(list(df_year.columns)) 
                                            - set(['rush_yds', 'pass_yds']))
                            df_year = df_year[list_cols_keep]
                        df_def = df_def.merge(df_year, how='outer', 
                                              on=list_vars_player)
            # Add turnover stats to offense and defense
            elif 'turnover' in category:
                df_off = df_off.merge(df_year, how='outer', on=list_vars_player)
                df_def = df_def.merge(df_year, how='outer', on=list_vars_player)
            # Check for any missed files
            else:
                print(category)
    
        # Export all merged dataframes to a CSV file for that year
        df_def.to_csv(path_dir.parent.joinpath('merged/players/players_defense_' 
                                               + year + '.csv'), index = False)
        df_off.to_csv(path_dir.parent.joinpath('merged/players/players_offense_' 
                                               + year + '.csv'), index = False)
        df_spc_ret.to_csv(path_dir.parent.joinpath(
                'merged/players/players_special_return_' 
                + year + '.csv'), index = False)
        df_spc_kick.to_csv(path_dir.parent.joinpath(
                'merged/players/players_special_kicking_' 
                + year + '.csv'), index = False)
        
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

    # Identify all statistical files on record for the team
    list_files = list(path_dir.glob('**/*.csv'))
    list_files.sort()

    # Identify all years that exist in the data
    list_temp = [str(x).split('splits/')[1] for x in list_files]
    list_years = list(set([x.split('.csv')[0].split(
            '_')[-1] for x in list_temp]))
    list_years.sort()

    # Iterate over every year
    for year in tqdm.tqdm(list_years):
        # Create DataFrame for storing data all three category types
        df_def = pd.DataFrame()     # defense
        df_off = pd.DataFrame()     # offense
        df_spc_def = pd.DataFrame() # special teams (defense)
        df_spc_off = pd.DataFrame() # special teams (offense)
        
        # Find all the files that belong to the given year
        list_files_year = [x for x in list_files if year in str(x)]
        # Aggregate all files for the given year that exist for each category  
        for path_file in list_files_year:
            
            # Import the file
            df_year = pd.read_csv(path_file)
           
            # Determine the stat category (and remove `_year` from the end)
            category = str(path_file).split('splits/')[1].split('.csv')[0][:-5]
            
            # Determine the stat sub-category by slicing on `_`
            #   Note:  This method won't work for all variables and requires 
            #   special handling for the following variables:
            #   fumble_returns, interceptions, misc._defense, sacks, 
            #   tackles_for_loss, tackles, turnover_margin
            if builtins.any(category.split('_')[0] in x for x in 
                            ['fumble_returns', 'interceptions', 'misc._defense', 
                             'sacks', 'tackles_for_loss', 'tackles',
                             'turnover_margin']):
                sub_category = '_'.join(category.split('_')[:-1])
            else:
                sub_category = '_'.join(category.split('_')[:-2])
            
            # Rename the variables in the year DataFrame to match their category
            df_year = renameVariables(df_year, sub_category)
            
            # Check to see what category the file belongs to
            # Special Teams-related files
            if any(x in category for x in list_stats_special):
                # Special Teams Defense-related files
                if 'defense' in category or 'opponent' in category:
                    if len(df_spc_def) == 0:
                        df_spc_def = df_year
                    else:
                        df_spc_def = df_spc_def.merge(
                                df_year, on=list_vars_split)
                # Special Teams Offense-related files
                elif 'offense' in category or 'team' in category:
                    if len(df_spc_off) == 0:
                        df_spc_off = df_year
                    else:
                        df_spc_off = df_spc_off.merge(
                                df_year, on=list_vars_split)
            # Offensive-related files
            elif (('offense' in category and 'defense' not in category) 
                    or 'team' in category):
                if 'all_purpose' not in category:    # ignore all_purpose yards
                    if len(df_off) == 0:
                        df_off = df_year
                    else:
                        # remove duplicate columns: rush_yds & pass_yds
                        if 'total_offense' in category:
                            list_cols_keep = list(set(list(df_year.columns)) 
                                            - set(['rush_yds', 'pass_yds']))
                            df_year = df_year[list_cols_keep]
                        df_off = df_off.merge(df_year, on=list_vars_split)
            # Defensive-related files
            elif 'defense' in category \
                or 'opponent' in category \
                or 'fumble_returns' in category \
                or 'interceptions' in category \
                or 'sacks' in category \
                or 'tackles' in category:
                if 'all_purpose' not in category:   # ignore all_purpose yards
                    if len(df_def) == 0:
                        df_def = df_year
                    else:
                        # remove duplicate columns: rush_yds & pass_yds
                        if 'total_offense' in category:
                            list_cols_keep = list(set(list(df_year.columns)) 
                                            - set(['rush_yds', 'pass_yds']))
                            df_year = df_year[list_cols_keep]
                        df_def = df_def.merge(df_year, on=list_vars_split)
            # Add turnover stats to offense and defense
            elif 'turnover' in category:
                df_off = df_off.merge(df_year, on=list_vars_split)
                df_def = df_def.merge(df_year, on=list_vars_split)
            # Check for any missed files
            else:
                print(category)
    
        # Export all merged dataframes to a CSV file for that year
        df_def.to_csv(path_dir.parent.joinpath('merged/splits/split_defense_' 
                                               + year + '.csv'), index = False)
        df_off.to_csv(path_dir.parent.joinpath('merged/splits/split_offense_' 
                                               + year + '.csv'), index = False)
        df_spc_def.to_csv(path_dir.parent.joinpath(
                'merged/splits/split_special_defense_' 
                + year + '.csv'), index = False)
        df_spc_off.to_csv(path_dir.parent.joinpath(
                'merged/splits/split_special_offense_' 
                + year + '.csv'), index = False)
        
def combineStatsIntoOne(path_folder):
    '''
    Purpose: Combine all `merged` statistics into one file for each statistical
        grouping such that all years are contained within one file
    
    Input:
        (1) path_folder (pathlib Path): Directory file path containing
                the project's files for all years
        
    Output:
        (1) (.csv file) A single .csv file per category that contains 
                all sub-category data belonging to that category for all years
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
            df_all = df_all.append(df, sort=False)
        
        # Resest the DataFrame Index
        df_all = df_all.reset_index()
        # Drop the old DataFrame Index
        df_all.drop(['index'], axis=1, inplace=True)
        # Remove all spaces from column names and replace with a '_'
        df_all.columns = [x.replace(' ','_') for x in list(df_all.columns)]
        # Export to a CSV File
        df_all.to_csv(path_output.joinpath(file_category + '_all.csv'),
                      index=False)  

def aggregate_data_by_category(path_project):
    '''
    Purpose: Aggregate all statistical data into 17 distinct .csv files 
        such that all years for each statistic are grouped together in one 
        file per category.  These files are located in /data/interim/ALL/
        merged_files
    
    Input:
        (1) path_project (pathlib Path): Directory file path of the project
        
    Output:
        (1) (.csv file) A single .csv file that contains data for all years
    '''    
    #--------------------------------------------------------------------------
    # Step 1: Identify the data file paths and verify the desired folder
    #           structure exists in the data/interim/ folder.
    #--------------------------------------------------------------------------
    
    # Identify Raw Data file paths and Statistical Categories
    dict_paths_raw_data, list_stat_folders = identifyRawDataPaths(path_project)
    
    # Verify the required folder structure in `data/interim/CFBStats/ALL` exists
    directoryCheck(list_stat_folders)

    #--------------------------------------------------------------------------
    # Step 2: Combine yearly statistics into one file per statistical 
    #           sub_category.  Examples of sub_categories include: 
    #           'passing_offense_game', 'rushing_offense_game', 
    #           'receiving_offense_game'.  Thus, all team files (e.g. 
    #           'passing_offense_game_Air_Force_2009', etc.) are grouped into
    #           one file called 'passing_offense_game_ALL_2009'. Files are 
    #           organized by team and category and are placed in the
    #           /data/interim/CFBStats/ folder.
    #--------------------------------------------------------------------------
    combineYears(path_project, dict_paths_raw_data)

    #--------------------------------------------------------------------------
    # Step 3: Combine sub_category data such that the files created in Step 2
    #           are aggregated based on the broader category they belong to.  
    #           For example, all offensive files ('passing_offense_game_ALL_2009', 
    #           'rushing_offense_game__ALL_2009', etc.) would be grouped into
    #           one single file for the year called 'game_offense_2009'. Files
    #           are organized by category and placed in the 
    #           /data/interim/CFBStats/ALL/merged folder.
    #--------------------------------------------------------------------------
    # Game Logs
    mergeStatsGame(path_project)
    
    # Situational Stats
    mergeStatsSituational(path_project)
    
    # Split Stats
    mergeStatsSplit(path_project)  
    
    # Player Stats
    mergeStatsPlayers(path_project)

    #--------------------------------------------------------------------------
    # Step 4: Combine category data created in Step 3 such that data from all 
    #           years is grouped together in one file.  For example, 
    #           'game_offfense_2009', 'game_offense_2010', 'game_offense_2011', 
    #           are combined together into 'game_offense' and output to the
    #           /data/interim/CFBStats/ALL/merged_final folder.
    #--------------------------------------------------------------------------

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