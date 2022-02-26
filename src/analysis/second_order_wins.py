#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:43:46 2021

@author: reideej1

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import datetime
import glob
import numpy as np
import os  
import pandas as pd
import pathlib
import tqdm

#==============================================================================
# Reference Variable Declaration
#==============================================================================

#==============================================================================
# Function Definitions
#==============================================================================
def function_name(var1, var2):
    '''
    Purpose: Stuff goes here

    Inputs   
    ------
        var1 : type
            description
        var2 : type
            description
            
    Outputs
    -------
        var1 : type
            description
        var2 : type
            description
    '''
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
path_dir = pathlib.Path(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis')
os.chdir(path_dir)

#------------------------------------------------------------------------------
#- 2021 Season
#------------------------------------------------------------------------------
# read in 2021 data
df = pd.read_csv(r'data\raw\CollegeFootballData\2021_season_game_summaries.csv', 
                 encoding = "ISO-8859-1")
df['home_team'] = df['home_team'].replace('San José State', 'San Jose State')
df['away_team'] = df['away_team'].replace('San José State', 'San Jose State')
df['home_team'] = df['home_team'].replace('San JosÃ© State', 'San Jose State')
df['away_team'] = df['away_team'].replace('San JosÃ© State', 'San Jose State')

# identify FBS teams
list_teams = list(df[~pd.isna(df['home_conference']) & ~pd.isna(df['away_conference'])].home_team.unique())
list_teams.sort()

today = datetime.datetime.now()

# calculate each team's post-game win probability and total record
list_team_data = []
for team in list_teams:
    # subset to team games
    df_team = df[(df['home_team'] == team) | (df['away_team'] == team)]
    
    # calculate team's win-loss record & post-game win probabilities
    wins   = 0
    losses = 0
    pg_win = 0
    elo    = 0
    for index, row in tqdm.tqdm(df_team.iterrows()):
        if today > datetime.datetime.fromisoformat(row['start_date'][:-1]):
            if row['home_team'] == team:
                pg_win = np.nansum([row['home_post_win_prob'], pg_win])
                if ~pd.isna(row['home_postgame_elo']):
                    elo = row['home_postgame_elo']
                if row['home_points'] > row['away_points']:
                    wins = wins + 1
                else:
                    losses = losses + 1
            else:
                pg_win = np.nansum([row['away_post_win_prob'], pg_win])
                if ~pd.isna(row['away_postgame_elo']):
                    elo = row['away_postgame_elo']
                if row['away_points'] > row['home_points']:
                    wins = wins + 1
                else:
                    losses = losses + 1
                
    elo    = round(elo, 2)
    pg_win = round(pg_win, 2)
    win_diff = wins - pg_win
    list_team_data.append([team, wins, losses, pg_win, win_diff, elo])
    
df_final = pd.DataFrame(list_team_data, columns = [
    'Team', 'Wins', 'Losses', '2nd Order Wins', 'Win Diff.', 'Elo'])

df_final['Rank_2nd_order'] = df_final['Elo'].rank(ascending = False, method = 'min')
df_final['Rank_Elo'] = df_final['Elo'].rank(ascending = False, method = 'min')
df_final[df_final['Team'] == 'Nebraska']

#------------------------------------------------------------------------------
#- 2000 to 2021 Season
#------------------------------------------------------------------------------
# read in data for all years
list_files = glob.glob(r'data\raw\CollegeFootballData\results*.csv')               

df_all = pd.DataFrame()
for file in list_files:        
    df_all = df_all.append(pd.read_csv(file, encoding = "ISO-8859-1"))
df_all['home_team'] = df_all['home_team'].replace('San JosÃ© State', 'San Jose State')
df_all['away_team'] = df_all['away_team'].replace('San JosÃ© State', 'San Jose State')
df_all = df_all[['season', 'week', 'season_type', 'start_date', 'conference_game', 'home_team',
                 'home_conference', 'home_points', 'home_post_win_prob', 'home_postgame_elo',
                 'away_team', 'away_conference', 'away_points', 'away_post_win_prob',
                 'away_postgame_elo']]
# post-game win probability data only goes back to 2010
df_all = df_all[df_all['season'] >= 2010]

# identify FBS teams
list_teams_all = list(df_all[~pd.isna(df_all['home_conference']) & ~pd.isna(df_all['away_conference'])].home_team.unique())
list_teams_all.sort()

today = datetime.datetime.now()

# calculate each team's post-game win probability and total record
list_team_data = []
for year in tqdm.tqdm(range(2000,2021+1)):
    for team in list_teams_all:
        df_year = df_all[df_all['season'] == year]
        # subset to team games
        df_team = df_year[(df_year['home_team'] == team) | (df_year['away_team'] == team)]
        
        # calculate team's win-loss record & post-game win probabilities
        wins   = 0
        losses = 0
        pg_win = 0
        elo    = 0
        for index, row in df_team.iterrows():
            if today > datetime.datetime.fromisoformat(row['start_date'][:-1]):
                if row['home_team'] == team:
                    pg_win = np.nansum([row['home_post_win_prob'], pg_win])
                    if ~pd.isna(row['home_postgame_elo']):
                        elo = row['home_postgame_elo']
                    if row['home_points'] > row['away_points']:
                        wins = wins + 1
                    else:
                        losses = losses + 1
                else:
                    pg_win = np.nansum([row['away_post_win_prob'], pg_win])
                    if ~pd.isna(row['away_postgame_elo']):
                        elo = row['away_postgame_elo']
                    if row['away_points'] > row['home_points']:
                        wins = wins + 1
                    else:
                        losses = losses + 1
                    
        elo    = round(elo, 2)
        pg_win = round(pg_win, 2)
        win_diff = wins - pg_win
        list_team_data.append([year, team, wins, losses, pg_win, win_diff, elo])
    
df_final = pd.DataFrame(list_team_data, columns = [
    'Season', 'Team', 'Wins', 'Losses', '2nd Order Wins', 'Win Diff.', 'Elo'])

df_final['Rank_2nd_order'] = df_final['Elo'].rank(ascending = False, method = 'min')
df_final['Rank_Elo'] = df_final['Elo'].rank(ascending = False, method = 'min')

df_final[df_final['Team'] == 'Nebraska']