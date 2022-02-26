#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 14:15:13 2021

@author: reideej1

:DESCRIPTION: Analyze the situational and split statistics for Adrian Martinez
    during his career at Nebraska

:REQUIRES: N/A
   
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

# read in data from .csv files
df_split = pd.read_csv(path_dir.joinpath('data', 'processed', 'CFBStats', 'individual', 
                                         'all_years_split_with_team_info.csv'))
df_situational = pd.read_csv(path_dir.joinpath('data', 'processed', 'CFBStats', 'individual', 
                                         'all_years_situational_with_team_info.csv'))

# determine the appropriate cutoffs for minimum pass attempts/games played
df_situational_all = df_situational[df_situational['situation'] == 'All Plays'].copy()
# Required:  
#   ---- played in 50% of the team's games
df_situational_all['%_games_played'] = df_situational_all['pass_g'] / (
    df_situational_all['team_w'] + df_situational_all['team_l'] + df_situational_all['team_t'])
#   ---- attempted 20 or more passing attempts per game == OR == 
#   ---- attempted 100 or more passes on the season
df_situational_all['pass_att_game'] = df_situational_all['pass_att'] / df_situational_all['pass_g']
df_situational_all = df_situational_all[(df_situational_all['%_games_played'] >= .50) &
                                        ((df_situational_all['pass_att_game'] > 20) & 
                                         (df_situational_all['pass_att'] >= 100))].reset_index(drop = True)
#   ---- find the unique players based on team and season
df_situational_all = df_situational_all[['team', 'season', 'name']]
#   ---- merge the original data back to make the desired subset
df_situational_subset = pd.merge(df_situational_all, df_situational, how = 'left', 
                  on = ['team', 'season', 'name'])

# determine the appropriate cutoffs for minimum pass attempts/games played
df_split_all = df_split[df_split['split'] == 'All Games'].copy()
# Required:  
#   ---- played in 50% of the team's games
df_split_all['%_games_played'] = df_split_all['pass_g'] / (
    df_split_all['team_w'] + df_split_all['team_l'] + df_split_all['team_t'])
#   ---- attempted 20 or more passing attempts per game == OR == 
#   ---- attempted 100 or more passes on the season
df_split_all['pass_att_game'] = df_split_all['pass_att'] / df_split_all['pass_g']
df_split_all = df_split_all[(df_split_all['%_games_played'] >= .40) &
                            ((df_split_all['pass_att_game'] > 20) & 
                             (df_split_all['pass_att'] >= 100))].reset_index(drop = True)
#   ---- find the unique players based on team and season
df_split_all = df_split_all[['team', 'season', 'name']]
#   ---- merge the original data back to make the desired subset
df_split_subset = pd.merge(df_split_all, df_split, how = 'left', 
                  on = ['team', 'season', 'name'])

#------------- Handle "Split" stats --------------------------------------

# # retrieve categories for "split" statistics
# split_ctg = []
# split_stats = []

# # 1. Rank by year
# df_split_ranked = pd.DataFrame()
# print('ranking each situational stat by year')
# for ctg in tqdm.tqdm(split_ctg):
#     # rank every stat based on the specific category - year combination
#     df_ctg = df_split[df_split['split'] == ctg].copy()
#     for stat in split_stats:
#         ctg_name = 'rank_' + stat + '_by_year'
#         df_ctg[ctg_name] = df_ctg.groupby(['season'])[stat].rank(
#                 method='first', ascending=False, na_option='bottom')
        
#     # add the stats to the master dataframe
#     if len(df_split_ranked) == 0:
#         df_split_ranked = df_ctg.copy()
#     else:
#         df_split_ranked = df_split_ranked.append(df_ctg)
# df_split_ranked = df_split_ranked.reset_index(drop = True)

# #------------- Handle "Situational" stats --------------------------------

# # retrieve categories for "situational" statistics
# sit_stats = [s for s in list(df_situational.columns) if any(xs in s for xs in ['pass', 'rush'])]
# sit_ctg = list(set(df_situational['situation']))

#=============== Make stats for all situations =================================
#--- % of games played
df_situational_subset['%_games_played'] = df_situational_subset['pass_g'] / (
    df_situational_subset['team_w'] + df_situational_subset['team_l'] + df_situational_subset['team_t'])
#--- avg. # of passes per game for the situation
df_situational_subset['pass_att_game'] = df_situational_subset['pass_att'] / df_situational_subset['pass_g']
#--- Yards per Completion
df_situational_subset['pass_yards_per_comp'] = df_situational_subset['pass_yards'] / df_situational_subset['pass_comp']
#--- Attempts per TD
df_situational_subset['pass_att_per_td'] = df_situational_subset['pass_att'] / df_situational_subset['pass_td']
#--- Attempts per INT
df_situational_subset['pass_att_per_int'] = df_situational_subset['pass_att'] / df_situational_subset['pass_int']
#--- TD per INT (TD/INT ratio)
df_situational_subset['pass_td_per_int'] = df_situational_subset['pass_td'] / df_situational_subset['pass_int']
#--- Yards per TD
df_situational_subset['pass_yards_per_td'] = df_situational_subset['pass_yards'] / df_situational_subset['pass_td']
#--- Yards per INT
df_situational_subset['pass_yards_per_int'] = df_situational_subset['pass_yards'] / df_situational_subset['pass_int']


# Required:  (minimum 14 Att/G, 75% of school games played)
df_qbs = df_situational_subset[(df_situational_subset['%_games_played'] >= 0.75) &
                               (df_situational_subset['pass_att_game'] >= 14)]
df_qbs = df_qbs[['team', 'season', 'name']]
df_qbs = pd.merge(df_qbs, df_situational_subset, how ='left', on = ['team', 'season', 'name'])
                                               

# # Required:  
# #   ---- played in 50% of the team's games
# #   ---- averaged 5 or more passing attempts in the quarter
# df_quarter = df_quarter[(df_quarter['%_games_played'] >= .50) & (
#     df_quarter['pass_att'] > 5)].reset_index(drop = True)

# sort columns for QBs DataFrame
df_qbs = df_qbs[[
    'team', 'season', 'conf', 'Power5', 'position', 'name', 'name_last', 'name_first',
    'class', 'situation', 'pass_g', 'pass_att', 'pass_comp', 'pass_pct.',
    'pass_yards', 'pass_td', 'pass_int', 'pass_rating', 'pass_long',
    'pass_1st', 'pass_15+', 'pass_25+', 
    'pass_att_game', 'pass_yards_per_comp', 'pass_att_per_td', 'pass_att_per_int',
    'pass_td_per_int', 'pass_yards_per_td', 'pass_yards_per_int', 
    'rush_g', 'rush_att', 'rush_yards',
    'rush_avg.', 'rush_td', 'rush_long', 'rush_1st', 'rush_10+', 'rush_20+',
    'team_w', 'team_l', 'team_t', 'team_pct', 'coach', 'bowl', '%_games_played',
    'height', 'weight', 'home_town', 'home_state']]

#=============== Rank all stats by situation ==================================
df_qbs_updated = pd.DataFrame()
for situation in tqdm.tqdm(list(set(df_qbs['situation']))):
    df_situation = df_qbs[df_qbs['situation'] == situation].copy()
    for stat in ['pass_att', 'pass_comp', 'pass_pct.',
        'pass_yards', 'pass_td', 'pass_int', 'pass_rating', 'pass_long',
        'pass_1st', 'pass_15+', 'pass_25+', 
        'pass_att_game', 'pass_yards_per_comp', 'pass_att_per_td', 'pass_att_per_int',
        'pass_td_per_int', 'pass_yards_per_td', 'pass_yards_per_int', 
        'rush_g', 'rush_att', 'rush_yards',
        'rush_avg.', 'rush_td', 'rush_long', 'rush_1st', 'rush_10+', 'rush_20+',]:
        for stat_type in ['_year', '_alltime']:
            new_stat_name = stat + '_rank' + stat_type
            if stat_type == '_year':
                df_situation[new_stat_name] = df_situation.groupby(by = ['season'])[stat].rank(method = 'dense', ascending = False, na_option = 'bottom')
            elif stat_type == '_alltime':
                df_situation[new_stat_name] = df_situation[stat].rank(method = 'dense', ascending = False, na_option = 'bottom')
    
    if len(df_qbs_updated) == 0:
        df_qbs_updated = df_situation
    else:
        df_qbs_updated = df_qbs_updated.append(df_situation)
df_qbs_updated.to_csv('stats.csv', index = False)

#=============== Analyze Adrian's Performance =================================
# Adrian in 1st quarter

# Adrian in 2nd quarter

# Adrian in 3rd quarter

# Adrian in 4th quarter

# Adrian in 1st/3rd Quarters

# Adrian in 2nd/4th Quarters

# Compare 1st/3rd and 2nd/4th Quarters...is the dropoff normal?

# Adrian in 1st Half (1st and 2nd Quarters)

# Adrian in 2nd Half (3rd and 4th Quarters)

# Compare 1st/3rd and 2nd/4th Quarters...is the dropoff normal?

# Adrian in one-score games (8 pts or less)

# Adrian in 15+ score games

# Compare one-score vs 15+ score games...is the dropoff normal?