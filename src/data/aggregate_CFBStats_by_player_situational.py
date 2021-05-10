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
import os  
import pandas as pd
import pathlib

from itertools import groupby   # used for grouping similar substrings

#==============================================================================
# Reference Variable Declaration
#==============================================================================

#==============================================================================
# Function Definitions
#==============================================================================
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
    
    # group stats by player
    for player_files in [list(playerIdx) for j, playerIdx in groupby(
        path_files, lambda a: a.split('QB_')[1].split('_')[0])]:
    
        # process PASSING situational stats
        df_sit_pass = pd.DataFrame()
        for file_sit_pass in [x for x in player_files if 'passing_situational.csv' in x]:
            df_sit_pass = df_sit_pass.append(pd.read_csv(path_team.joinpath(file_sit_pass)))
            
        # process RUSHING situational stats
        df_sit_rush = pandas.DataFrame()
        for file_sit_rush in [x for x in player_files if 'rushing_situational.csv' in x]:
            
        # process PASSING split stats
        df_split_pass = pandas.DataFrame()
        for file_split_pass in [x for x in player_files if 'passing_split.csv' in x]:
            
        # process RUSHING split stats
        df_split_rush = pandas.DataFrame()
        for file_split_rush in [x for x in player_files if 'rushing_split.csv' in x]:
            
        # merge all stats together

def aggregate_stats():
    # set folder path for CFB Stats
    path_project = pathlib.Path(os.path.abspath(os.curdir), 'data', 'raw', 'CFBStats')
    
    # retrieve the listing of all team folders in the directory
    list_teams = os.listdir(path_project)
    
    # roll up stats by year for each player on a team
    for team in list_teams:
        # create team directory path
        path_team = path_project.joinpath(team, 'individual')
        
        # roll up stats
        roll_up_team_by_year(path_team)
    
    
#==============================================================================
# Working Code
#==============================================================================

# # Set the project working directory
# path_dir = pathlib.Path('C:\Users\reideej1\Projects')
# os.chdir(path_dir)

# aggregate stats for all players
aggregate_stats()