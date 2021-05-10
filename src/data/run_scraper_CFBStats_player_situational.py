#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:34:43 2021
@author: reideej1
"""
 
#==============================================================================
# Package Import
#==============================================================================
import os  
import pandas as pd
import pathlib
import scrape_CFBStats
import time

#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
# path_dir = pathlib.Path('C:\Users\reideej1\Projects\a_Personal')
# os.chdir(path_dir)

#--- Step 1. Scrape the stats for each team's players (creating CSV files along the way)
dict_teams = scrape_CFBStats.scrapeTeamNames()
list_teams = list(dict_teams.keys())
for team_name in list_teams:
    print(f'#----- Starting Situational Stats for {team_name} -----#')
    scrape_CFBStats.scrapePlayerSituational(team_name)
    time.sleep(10)
# for team_name in list_teams[list_teams.index('Oregon State'):]:
    
#--- Step 2. Create career stats for individual players ----------------------#
dir_data = r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\raw\CFBStats'
dir_schools = os.listdir(dir_data)

# iterate over every school's data and compile results for players
for school in dir_schools:
    path_school = pathlib.Path(dir_data, school, 'individual')
    
    #--- Step 2.A. Retrieve .csv files for the given school ------------------#
    files_players = os.listdir(path_school)
    
    #--- Step 2.B. Find unique players in directory --------------------------# 
    players = list(set([f.split('_QB_')[1].split('_')[0] for f in files_players]))
    
    # iterate over every player in the team directory
    for player in players:
        player_files = [f for f in files_players if player in f]
        #--- Step 2.C. Aggregate Passing Stats -------------------------------#
        #----- Handle Passing Situational
        paths_pass_sit = [f for f in player_files if 'passing_situational' in f]
        list_pass_sit = []
        for path_pass_sit in paths_pass_sit:
            list_pass_sit.append(pd.read_csv(path_school.joinpath(path_pass_sit)))

        #----- Handle Passing Splits 
        paths_pass_split = [f for f in player_files if 'passing_split' in f] 
        list_pass_split = []
        for path_pass_split in paths_pass_split:
            list_pass_split.append(pd.read_csv(path_school.joinpath(path_pass_split)))
    
        #--- Step 2.D. Aggregate Rushing Stats -------------------------------# 
        #----- Handle Rushing Situational
        paths_rush_sit = [f for f in player_files if 'rushing_situational' in f]
        list_rush_sit = []
        for path_rush_sit in paths_rush_sit:
            list_rush_sit.append(pd.read_csv(path_school.joinpath(path_rush_sit)))
            
        #----- Handle Rushing Splits        
        paths_rush_split = [f for f in player_files if 'rushing_split' in f] 
        list_rush_split = []
        for path_rush_split in paths_rush_split:
            list_rush_split.append(pd.read_csv(path_school.joinpath(path_rush_split)))

        #--- Step 2.E. Merge Situational and Split Files for Each Year -------# 
        
        #--- Step 2.F. Merge Passing and Rushing Files for Each Year ---------# 
        
        #--- Step 2.G. Merge All Years Together into a Career File -----------#
        
#--- Step 3. Analyze stats across all of college football --------------------#