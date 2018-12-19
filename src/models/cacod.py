#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 11:05:27 2018

@author: ejreidelbach

:DESCRIPTION:
    Conference-Adjsuted Combined Offensive-Defensive (CACOD) metric
        - http://volleymetrics.blogspot.com/2012/11/ranking-64-ncaa-womens-teams-on.html
        
    Inspired by:
        - https://hailvarsity.com/s/5775/hot-reads-score-another-one-for-simple-ranking-systems

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import os  
import pandas as pd
import pathlib

#==============================================================================
# Reference Variable Declaration
#==============================================================================
dict_conf_factors = {
        'Big 10':,1.25,
        'SEC':1.3
        'Pac 12':1.0,
        'Big 12':1.0,
        'AAC':,
        'ACC':,
        'CUSA':,
        'Ind':,
        'MAC':,
        'MWC':,
        'Sun Belt:',
        }

#==============================================================================
# Function Definitions 
#==============================================================================
def function_name(var1, var2, var3):
    '''
    Purpose: Stuff goes here

    Input:   
        (1) var1 (type): description
        (2) var2 (type): description
        (3) var3 (type): description
    
    Output: 
        (1) output1 (type): description
    '''

def points_per_play(df):
    '''
    Purpose:  Calculate a team's points per play on offense and defense
    
    Input:
        (1) df (Pandas DataFrame): A DataFrame containing game-level statistics
                for all teams across multiple season
    
    Output:
        (1) pts_per_play_off (float): points scored on offense per play run
        (2) pts_per_play_off (float): points given up on defense per play
    '''

    
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
#path_project = pathlib.Path(__file__).resolve().parents[2]
#os.chdir(path_project)

# Set the project working directory
path_dir = pathlib.Path('/home/ejreidelbach/Projects/cfbAnalysis')
os.chdir(path_dir)

#------------------------------------------------------------------------------
# Offense
#------------------------------------------------------------------------------
df_off = pd.read_csv(path_dir.joinpath('data/interim/CFBStats/ALL/merged_final',
                                       'game_offense_all.csv'))
df_off_pts = df_off.groupby(['team','season'])['pts_for','play_num'].sum()
df_off_pts['pts_play_off'] = df_off_pts.apply(lambda x: x['pts_for']/x['play_num'], axis=1)
df_off_pts['team'] = df_off_pts.apply(lambda x: x.name[0], axis=1)
df_off_pts['season'] = df_off_pts.apply(lambda x: x.name[1], axis=1)
df_off_pts.rename({'play_num':'plays_for'}, axis=1, inplace=True)
df_off_pts = df_off_pts.reset_index(drop=True)

#------------------------------------------------------------------------------
# Defense
#------------------------------------------------------------------------------
df_def = pd.read_csv(path_dir.joinpath('data/interim/CFBStats/ALL/merged_final',
                                       'game_defense_all.csv'))
df_def_pts = df_def.groupby(['team','season'])['pts_against','play_num'].sum()
df_def_pts['pts_play_def'] = df_def_pts.apply(lambda x: x['pts_against']/x['play_num'], axis=1)
df_def_pts['team'] = df_def_pts.apply(lambda x: x.name[0], axis=1)
df_def_pts['season'] = df_def_pts.apply(lambda x: x.name[1], axis=1)
df_def_pts.rename({'play_num':'plays_against'}, axis=1, inplace=True)
df_def_pts = df_def_pts.reset_index(drop=True)

df_teams = pd.merge(df_off_pts, df_def_pts, on=['team', 'season'])
df_teams['pts_diff'] = df_teams.apply(lambda x: x['pts_play_off'] - x['pts_play_def'], axis=1)

for year in list(range(2009,2019)):
    df_year = df_teams[df_teams['season'] == year]
    var_name = 'rank_diff_' + str(year)
    # pts diff ranking
    df_year[var_name] = df_year['pts_diff'].rank(method='first', ascending=False)
    # pts off ranking
    var_name = 'rank_off_' + str(year)
    df_year[var_name] = df_year['pts_play_off'].rank(method='first', ascending=False)
    # pts def ranking
    var_name = 'rank_def_' + str(year)
    df_year[var_name] = df_year['pts_play_def'].rank(method='first')
    df_year = df_year[['team'
                       ,'season'
                       ,'rank_diff_'+str(year)
                       ,'pts_diff'
                       ,'rank_off_'+str(year)
                       ,'pts_play_off'
                       ,'pts_for'
                       ,'plays_for'
                       ,'rank_def_'+str(year)
                       ,'pts_play_def'
                       ,'pts_against'
                       ,'plays_against']]