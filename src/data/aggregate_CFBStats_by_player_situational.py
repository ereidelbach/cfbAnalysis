#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:36:24 2021

@author: reideej1

:DESCRIPTION:
    Rolls up situational statistics for individual player stats contained in 
    CFBStats/teamXXX/individual folders.
    
    Totals will be generated for each player on a yearly and a career basis.

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import glob
import numpy as np
import os  
import pandas as pd
import pathlib
import tqdm

from itertools import groupby   # used for grouping similar substrings

#==============================================================================
# Reference Variable Declaration
#==============================================================================

#==============================================================================
# Function Definitions
#==============================================================================
def directoryCheck(team_name):
    '''
    Purpose: Run a check of the /data/raw/CFBStats/ folder to see if a folder
        exists for the specified team and category. If it doesn't, create it.
        
    Input:
        (1) team_name (string): Name of the school being scraped
    
    Output:
        - NONE
    '''
    # Check for the team folder
    pathlib.Path('data/raw/CFBStats/'+team_name).mkdir(parents=True, exist_ok=True)
    
    # Checking for required sub-folders
    for category in ['games', 'players', 'records', 
                     'rosters', 'schedules', 'situations', 'splits']:
        pathlib.Path('data/raw/CFBStats/', team_name, category).mkdir(
                parents=True, exist_ok=True)

def roll_up_by_team(path_team):
    '''
    Purpose: Process the individual stats for each team's players. For example,
        there are currently situational and splits stats for every QB a team 
        has had for each year they played. This script will merge the yearly,
        stat-specific .csv files such that each player simply has a file called
        team_QB_playername_year.csv.
        
    Inputs   
    ------
        path_team : pathlib Path
            file path of team directory
            
    Outputs
    -------
        none
    '''
    # grab a list of all files in the directory
    path_files = os.listdir(path_team)
    
    # extract team name
    player_team = path_files[0].split('_')[0]
    
    # create a list of variables that are consistent across table types
    list_col_default_sit = ['situation', 'season', 'team', 'name', 'name_first',
                            'name_last', 'class', 'position', 'height', 'weight',
                            'home_town', 'home_state']
    list_col_default_split = ['split', 'season', 'team', 'name', 'name_first',
                              'name_last', 'class', 'position', 'height', 'weight',
                              'home_town', 'home_state']
    
    # create dataframes for storing all player stats for a team
    df_sit_team = pd.DataFrame()
    df_split_team = pd.DataFrame()    
    
    # group stats by player
    for player_files in tqdm.tqdm([list(playerIdx) for j, playerIdx in groupby(
        path_files, lambda a: a.split('QB_')[1].split('_')[0])]):
    
        # process PASSING situational stats
        df_sit_pass = pd.DataFrame()
        for file_sit_pass in [x for x in player_files if 'passing_situational.csv' in x]:
            df_sit_pass = df_sit_pass.append(pd.read_csv(path_team.joinpath(file_sit_pass)))
        df_sit_pass.columns = ['pass_' + x if x not in list_col_default_sit else x for x in df_sit_pass.columns]
            
        # process RUSHING situational stats
        df_sit_rush = pd.DataFrame()
        for file_sit_rush in [x for x in player_files if 'rushing_situational.csv' in x]:
            df_sit_rush = df_sit_rush.append(pd.read_csv(path_team.joinpath(file_sit_rush)))
        df_sit_rush.columns = ['rush_' + x if x not in list_col_default_sit else x for x in df_sit_rush.columns]
            
        # process PASSING split stats
        df_split_pass = pd.DataFrame()
        for file_split_pass in [x for x in player_files if 'passing_split.csv' in x]:
            df_split_pass = df_split_pass.append(pd.read_csv(path_team.joinpath(file_split_pass)))
        df_split_pass.columns = ['pass_' + x if x not in list_col_default_split else x for x in df_split_pass.columns]
            
        # process RUSHING split stats
        df_split_rush = pd.DataFrame()
        for file_split_rush in [x for x in player_files if 'rushing_split.csv' in x]:
            df_split_rush = df_split_rush.append(pd.read_csv(path_team.joinpath(file_split_rush)))
        df_split_rush.columns = ['rush_' + x if x not in list_col_default_split else x for x in df_split_rush.columns]
            
        # merge SITUATIONAL stats together
        #--- handle empty dataframes by creating NaNs for all variables
        if len(df_sit_pass) == 0:
            df_sit_pass = create_empty_stat_dataframe('sit_pass')
            df_sit = pd.merge(df_sit_rush, df_sit_pass, how = 'left', on = 'situation')
        elif len(df_sit_rush) == 0:
            df_sit_rush = create_empty_stat_dataframe('sit_rush')
            df_sit = pd.merge(df_sit_pass, df_sit_rush, how = 'left', on = 'situation')
        else:
            df_sit = pd.merge(df_sit_pass, df_sit_rush, how = 'inner', on = list_col_default_sit) 
            df_sit = df_sit[['season', 'team', 'position', 'name_last', 'name_first', 
                             'name', 'class', 'situation', 'pass_g', 'pass_att', 
                             'pass_comp', 'pass_pct.', 'pass_yards', 'pass_td', 
                             'pass_int', 'pass_rating', 'pass_long', 'pass_1st', 
                             'pass_15+', 'pass_25+', 'rush_g', 'rush_att', 
                             'rush_yards', 'rush_avg.', 'rush_td', 'rush_long', 
                             'rush_1st', 'rush_10+', 'rush_20+', 
                             'height', 'weight', 'home_town', 'home_state']]
        
        # merge SPLIT stats together
        #--- handle empty dataframes by creating NaNs for all variables
        if len(df_split_pass) == 0:
            df_split_pass = create_empty_stat_dataframe('split_pass')
            df_split = pd.merge(df_split_rush, df_split_pass, how = 'left', on = 'split')
        elif len(df_split_rush) == 0:
            df_split_rush = create_empty_stat_dataframe('split_rush')
            df_split = pd.merge(df_split_pass, df_split_rush, how = 'left', on = 'split')
        else:
            df_split = pd.merge(df_split_pass, df_split_rush, how = 'inner', on = list_col_default_split) 
            df_split = df_split[['season', 'team', 'position', 'name_last', 'name_first', 
                             'name', 'class', 'split', 'pass_g', 'pass_att', 
                             'pass_comp', 'pass_pct.', 'pass_yards', 'pass_td', 
                             'pass_int', 'pass_att/g', 'pass_yards/g', 
                             'pass_yards/att', 'pass_rating', 
                             'rush_g', 'rush_att', 'rush_yards', 'rush_avg.', 
                             'rush_td', 'rush_att/g', 'rush_yards/g', 
                             'height', 'weight', 'home_town', 'home_state']]

        # create career totals for each player
        df_sit, df_split = create_player_career_stats(df_sit, df_split)
        
        # add player stats to team dataframe
        if len(df_sit_team) == 0:
            df_sit_team = df_sit
        else:
            df_sit_team = df_sit_team.append(df_sit)
            
        if len(df_split_team) == 0:
            df_split_team = df_split
        else:
            df_split_team = df_split_team.append(df_split)    
            
    # save SITUATIONAL team file to disk
    fname_sit = f'{player_team}_situational.csv'
    outdir_sit = pathlib.Path('data/processed/CFBStats/individual/situational')
    if not os.path.exists(outdir_sit):
        os.mkdir(outdir_sit)
    df_sit_team.to_csv(outdir_sit.joinpath(fname_sit), index = False)
        
    # save SPLIT team file to disk
    fname_split = f'{player_team}_split.csv'
    outdir_split = pathlib.Path('data/processed/CFBStats/individual/split')
    if not os.path.exists(outdir_split):
        os.mkdir(outdir_split)
    df_split_team.to_csv(outdir_split.joinpath(fname_split), index = False)    
    
    print(f'Done with: {player_team}')
    
    return

def create_empty_stat_dataframe(df_type):
    '''
    Purpose: Create a placeholder "situational" or "split" stats dataframe 
        that can be used as a stand-in if a player is lacking stats for a 
        specific year (i.e. no rushing stats for freshman year, but QB has
        passing stats)
        
    Inputs   
    ------
        df_type : string
            specifies which type of dataframe to make:
                - "sit_pass"
                - "sit_rush"
                - "split_pass"
                - "split_rush"
            
    Outputs
    -------
        df_empty: pandas DataFrame
            stats dataframe with all values initialized to NaN for all categories
    '''
    list_situations = ['1st Half', '2nd Half/OT', '1st Quarter', '2nd Quarter',
                       '3rd Quarter', '4th Quarter', 'Overtime', '1st Down',
                       '2nd Down', '3rd Down', '3rd Down, 1-3 To Go', 
                       '3rd Down, 4-6 To Go', '3rd Down, 7-9 To Go', 
                       '3rd Down, 10+ To Go', '4th Down', 'Own 1 To 20 Yd Ln',
                       'Own 21 To 39 Yd Ln', 'Own 40 To Opp 40 Yd Ln', 
                       'Opp 39 To 21 Yd Ln', 'Opp 20 To 1 Yd Ln (RZ)',
                       'Winning By 15+ Pts', 'Winning By 8-14 Pts',
                       'Winning By 1-7 Pts', 'Tied', 'Losing By 1-7 Pts',
                       'Losing By 8-14 Pts', 'Losing By 15+ Pts']
    list_sit_pass = ['pass_g', 'pass_att', 'pass_comp', 'pass_pct.', 'pass_yards', 
                     'pass_td', 'pass_int', 'pass_rating', 'pass_long', 'pass_1st', 
                     'pass_15+', 'pass_25+']
    list_sit_rush = ['rush_g', 'rush_att', 'rush_yards', 'rush_avg.', 'rush_td',
                     'rush_long', 'rush_1st', 'rush_10+', 'rush_20+']
    
    list_split = ['All Games', 'at Home', 'on Road/Neutral Site', 'in Wins',
                  'in Losses', 'vs. Conference', 'vs. Non-Conference',
                  'vs. Ranked (AP)', 'vs. Unranked (AP)', 'vs. FBS (I-A)',
                  'vs. FCS (I-AA)', 'vs. FBS Winning', 'vs. FBS Non-Winning',
                  'vs. BCS AQ', 'vs. BCS non-AQ', 'in August/September',
                  'in October', 'in November', 'in December/January']
    list_split_pass = ['pass_g', 'pass_att', 'pass_comp', 'pass_pct.', 
                       'pass_yards', 'pass_td', 'pass_int', 'pass_att/g', 
                       'pass_yards/g', 'pass_yards/att', 'pass_rating']
    list_split_rush = ['rush_g', 'rush_att', 'rush_yards', 'rush_avg.', 
                       'rush_td', 'rush_att/g', 'rush_yards/g']
    
    df_empty = pd.DataFrame()
    # Handle SITUATIONAL - PASSING
    if df_type == "sit_pass":
        nrow = len(list_situations)
        ncol = len(list_sit_pass)
        df_empty = pd.DataFrame(np.zeros([nrow, ncol])*np.nan, columns=list_sit_pass)
        df_empty['situation'] = list_situations
    # Handle SITUATIONAL - RUSHING
    elif df_type == "sit_rush":
        nrow = len(list_situations)
        ncol = len(list_sit_rush)
        df_empty = pd.DataFrame(np.zeros([nrow, ncol])*np.nan, columns=list_sit_rush)
        df_empty['situation'] = list_situations        
    # Handle SPLIT - PASSING
    elif df_type == "split_pass":
        nrow = len(list_split)
        ncol = len(list_split_pass)
        df_empty = pd.DataFrame(np.zeros([nrow, ncol])*np.nan, columns=list_split_pass)
        df_empty['split'] = list_split
    # Handle SPLIT - PASSING
    elif df_type == "split_rush":
        nrow = len(list_split)
        ncol = len(list_split_rush)
        df_empty = pd.DataFrame(np.zeros([nrow, ncol])*np.nan, columns=list_split_rush)
        df_empty['split'] = list_split    
    else:
        print("Error detected. Wrong stats type presented to 'create_empty_stat_dataframe'")
        return
    
    return df_empty
          
def create_player_career_stats(df_sit, df_split):
    '''
    Purpose: Given a player's statistics broken out by year (both situational
        and split), calculate the player's career numbers across all categories.
        
    Inputs   
    ------
        df_sit : pandas DataFrame
            contains the pilot's situational stats for all available years
        df_split : pandas DataFrame
            contains the pilot's split stats for all available 
            
    Outputs
    -------
        df_sit_career : pandas DataFrame
            the player's situational stats updated with career totals
        df_split_career : pandas DataFrame
            the player's split stats updated with career totals
    '''
    list_cols_unchanged = ['team', 'position', 'name_last', 'name_first', 'name', 
                           'height', 'weight', 'home_town', 'home_state']
    
    #----- Process SITUATIONAL Stats
    # group all situational stats by statistical category 
    groups_sit = df_sit.groupby(['situation'])
    
    df_sit_career = df_sit.copy(deep = True)
    # iterate over every category and "sum" up one by one
    for grp in groups_sit:
            career_sit = grp[1].sum()   
            for col in list_cols_unchanged:
                career_sit[col] = grp[1].iloc[-1][col]
                career_sit['season'] = np.nan
                career_sit['class'] = 'Career'
                career_sit['situation'] = grp[0]
            # add category to player's career list
            df_sit_career = df_sit_career.append(career_sit, ignore_index = True)

    # fix career situational stats for the player
    #--- 1. Pass Rating
    ''' NCAA passer rating is calculated by: 
        ((8.4 x Passing Yards) + (330 x Touchdown Passes) + 
         (100 x Number of Completions) – (200 x Interceptions)) 
        ÷ Passing Attempts
        
        Sourced from: https://captaincalculator.com/sports/football/ncaa-passer-rating-calculator/
        '''
    df_sit_career['pass_rating'] = (((8.4 * df_sit_career['pass_yards']) + 
                                      (330 * df_sit_career['pass_td']) + 
                                      (100 * df_sit_career['pass_comp']) - 
                                      (200 * df_sit_career['pass_int'])) /
                                      df_sit_career['pass_att'])  
    
    #--- 2. Pass Completion %
    df_sit_career['pass_pct.'] = df_sit_career['pass_comp']/df_sit_career['pass_att']
    
    #--- 3. Rush Avg (Yds/Att.)
    df_sit_career['rush_avg.'] = df_sit_career['rush_yards']/df_sit_career['rush_att']
                        
    #----- Process SPLIT Stats
    # group all split stats by statistical category 
    groups_split = df_split.groupby(['split'])
    
    df_split_career = df_split.copy(deep = True)
    # iterate over every category and "sum" up one by one
    for grp in groups_split:
            career_split = grp[1].sum()   
            for col in list_cols_unchanged:
                career_split[col] = grp[1].iloc[-1][col]
                career_split['season'] = np.nan
                career_split['class'] = 'Career'
                career_split['split'] = grp[0]
            # add category to player's career list
            df_split_career = df_split_career.append(career_split, ignore_index = True)

    # fix career situational stats for the player
    #--- 1. Pass Rating
    ''' NCAA passer rating is calculated by: 
        ((8.4 x Passing Yards) + (330 x Touchdown Passes) + 
         (100 x Number of Completions) – (200 x Interceptions)) 
        ÷ Passing Attempts
        
        Sourced from: https://captaincalculator.com/sports/football/ncaa-passer-rating-calculator/
        '''
    df_split_career['pass_rating'] = (((8.4 * df_split_career['pass_yards']) + 
                                      (330 * df_split_career['pass_td']) + 
                                      (100 * df_split_career['pass_comp']) - 
                                      (200 * df_split_career['pass_int'])) / 
                                      df_split_career['pass_att'])
    
    #--- 2. Pass Completion %
    df_split_career['pass_pct.'] = (df_split_career['pass_comp']/
                                    df_split_career['pass_att'])
    
    #--- 3. Pass Att/Game
    df_split_career['pass_att/g'] = (df_split_career['pass_att']/
                                    df_split_career['pass_g'])
    
    #--- 4. Pass Yards/Game
    df_split_career['pass_yards/g'] = (df_split_career['pass_yards']/
                                   df_split_career['pass_g'])
    
    #--- 5. Rush Avg (Yds/Att.)
    df_split_career['rush_avg.'] = (df_split_career['rush_yards']/
                                    df_split_career['rush_att'])
    
    #--- 6. Rush Att/Game
    df_split_career['rush_att/g'] = (df_split_career['rush_att']/
                                    df_split_career['rush_g'])
    
    #--- 7. Rush Yards/Game
    df_split_career['rush_yards/g'] = (df_split_career['rush_yards']/
                                    df_split_career['rush_g'])
            
    return df_sit_career, df_split_career

def create_master_file(path_project):
    '''
    Purpose: Loop through all team files and make a unique file that includes
        all player data across all years/careers
        
    Input:
        - NONE
    
    Output:
        - NONE
    '''
    #------------- Handle "Split" stats --------------------------------------
    # grab a list of all files in the directory for "split" stats
    path_split = pathlib.Path(os.path.abspath(os.curdir), 
                              'data', 'processed', 'CFBStats', 'individual', 'split')
    files_split = os.listdir(path_split)
    
    # merge all files into a single file
    df_split_all = pd.DataFrame()
    for fname_split in files_split:
        if len(df_split_all) == 0:
            df_split_all = pd.read_csv(path_split.joinpath(fname_split))
        else:
            df_split_all = df_split_all.append(pd.read_csv(path_split.joinpath(fname_split)))
    
    # write csv to disk
    out_fname_split = pathlib.Path(os.path.abspath(os.curdir), 
                              'data', 'processed', 'CFBStats', 'individual', 'all_years_split.csv')
    df_split_all.to_csv(out_fname_split, index = False)    

    #------------- Handle "Situational" stats --------------------------------
    # grab a list of all files in the directory for "situational" stats
    path_situational = pathlib.Path(os.path.abspath(os.curdir), 
                              'data', 'processed', 'CFBStats', 'individual', 'situational')
    files_situational = os.listdir(path_situational)

    # merge all files into a single file
    df_situational_all = pd.DataFrame()
    for fname_situational in files_situational:
        if len(df_situational_all) == 0:
            df_situational_all = pd.read_csv(path_situational.joinpath(fname_situational))
        else:
            df_situational_all = df_situational_all.append(pd.read_csv(path_situational.joinpath(fname_situational)))  
    
    # write csv to disk
    out_fname_sit = pathlib.Path(os.path.abspath(os.curdir), 
                              'data', 'processed', 'CFBStats', 'individual', 'all_years_situational.csv')
    df_situational_all.to_csv(out_fname_sit, index = False)     
    
    return

def calculate_rankings():
    '''
    Purpose: Loop through the master file for 'situational' and 'split' stats
        to calculate ranking across a variety of categories within a given year
            - by conference
            - by year
            - by power5 status
        
    Input:
        - NONE
    
    Output:
        - NONE
    '''
    path_indiv = pathlib.Path(os.path.abspath(os.curdir), 'data', 'processed', 'CFBStats', 'individual')  

    # import team stats to integrate with individual stats
    path_team = pathlib.Path(os.path.abspath(os.curdir), 'data', 'processed', 'CFBStats', 'team')
    files = path_team.glob('*.csv')
    latest = max(files, key=lambda f: f.stat().st_mtime)
    df_teams = pd.read_csv(latest)

    # A. Add conference to each player row

    # B. Add Power 5 status to each player row

    # C. Add # of wins to each player row (for the season)

    # D. Add # of losses to each player row (for the season)

    # E. Add bowl status to each player row (for the season)     

    #------------- Handle "Split" stats --------------------------------------
    df_split = pd.read_csv(path_indiv.joinpath('all_years_split.csv'))
    
    # retrieve categories for "split" statistics
    split_stats = [s for s in list(df_split.columns) if any(xs in s for xs in ['pass', 'rush'])]
    split_ctg = list(set(df_split['split']))
    
    # 1. Rank by year
    df_split_ranked = pd.DataFrame()
    print('ranking each situational stat by year')
    for ctg in tqdm.tqdm(split_ctg):
        # rank every stat based on the specific category - year combination
        df_ctg = df_split[df_split['split'] == ctg].copy()
        for stat in split_stats:
            ctg_name = 'rank_' + stat
            df_ctg[ctg_name] = df_ctg.groupby(['season'])[stat].rank(
                    method='first', ascending=False, na_option='bottom')
            
        # add the stats to the master dataframe
        if len(df_split_ranked) == 0:
            df_split_ranked = df_ctg.copy()
        else:
            df_split_ranked = df_split_ranked.append(df_ctg)
            
            
    # 2. Rank by year and by conference
    
    # 3. Rank by year and by Power5 status
    
    # 4. Rank all time
    
    # 5. Rank all time and by conference
    
    # 6. Rank all time and by Power5 status
      
    # write csv to disk
    df_split.to_csv(path_indiv.joinpath('all_years_split_ranked.csv'), index = False)    

    #------------- Handle "Situational" stats --------------------------------
    df_situational = pd.read_csv(path_indiv.joinpath('all_years_situational.csv'))
    
    # retrieve categories for "situational" statistics
    sit_stats = [s for s in list(df_situational.columns) if any(xs in s for xs in ['pass', 'rush'])]
    sit_ctg = list(set(df_situational['situation']))
    
    # 1. Rank by year
    
    # 2. Rank by year and by conference
    
    # 3. Rank by year and by Power5 status
    
    # 4. Rank all time
    
    # 5. Rank all time and by conference
    
    # 6. Rank all time and by Power5 status
      
    # write csv to disk
    df_situational.to_csv(path_indiv.joinpath('all_years_situational_ranked.csv'), index = False)    
    
def aggregate_stats():
    '''
    Purpose: Kickoff the process of merging all files for individual players
        into comprehensive files that include all files for a team (including
        player career stats) as well as stats broken out by year and a cohesive
        file containing data for all players from all years
        
    Input:
        - NONE
    
    Output:
        - NONE
    '''
    # set folder path for CFB Stats
    path_project = pathlib.Path(os.path.abspath(os.curdir), 'data', 'raw', 'CFBStats')
    
    # retrieve the listing of all team folders in the directory
    list_teams = os.listdir(path_project)
    
    # roll up stats by year for each player on a team
    for team in tqdm.tqdm(list_teams):
        # create team directory path
        path_team = path_project.joinpath(team, 'individual')
        
        # roll up stats
        roll_up_by_team(path_team)
        
    # create files for each year across all teams
    create_master_file(pathlib.Path(os.path.abspath(os.curdir), 'data', 'processed' 'CFBStats', 'individual'))
    
    # rank each statistic by various categories
    calculate_rankings(path_project)
                         
#==============================================================================
# Working Code
#==============================================================================

# # Set the project working directory
# path_dir = pathlib.Path('C:\Users\reideej1\Projects')
# os.chdir(path_dir)

# aggregate stats for all players
aggregate_stats()