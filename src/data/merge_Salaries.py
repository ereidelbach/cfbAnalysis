#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 13:56:10 2017

@author: ejreidelbach

:DESCRIPTION:
    - Merges multiple years of Coaching Salary Data from USA Today's Website 
        into single files for all years

:REQUIRES:
    - Refer to `Package Import` section below for required packages
   
:TODO:
    - NONE
    
"""
#==============================================================================
# Package Import
#==============================================================================
import math
import os
import pandas as pd
import pathlib

#==============================================================================
# Function Definitions
#==============================================================================
def directoryCheck():
    '''
    Purpose: Run a check of the /data/interim/Salary/ folder to see if such a 
        folder exists. If it doesn't, create it.
        
    Input:
        - NONE
    
    Outpu:
        - NONE
    '''
    # Check for the team folder
    pathlib.Path('data/interim/Salary/').mkdir(parents=True, exist_ok=True)
    
def mergeColumns(row):
    if math.isnan(row['year_x']):
        return row['year_y']
    else:
        return row['year_x']
    
def renameColumns(df):
    list_new_names = []
    for name in list(df.columns):
        if name == 'coach_name':
            name = 'coach'
        elif name == 'school_name':
            name = 'school'
        name = name.strip()
        list_new_names.append(name)
    df.columns = list_new_names
    return df
    
#==============================================================================
# Working Code
#==============================================================================
    
# Set the project working directory
path_project = pathlib.Path(__file__).resolve().parents[2]
#path_project = pathlib.Path('/home/ejreidelbach/Projects/cfbAnalysis')
os.chdir(path_project)

# Ensure the data/interim/Salary folder exists
directoryCheck()

#------------------------------------------------------------------------------
# Football Head Coach Salaries
#------------------------------------------------------------------------------
# Coach Info
df2017 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','coach_info_fb_head_2017.csv'))
df2018 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','coach_info_fb_head_2018.csv'))
df2017 = renameColumns(df2017)
df2018 = renameColumns(df2018)
dfAll = df2017.append(df2018)
dfAll.to_csv(path_project.joinpath(
        'data/interim/Salary','head_info_all.csv'), index = False)

# Current Info
df2017 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','current_head_2017.csv'))
df2018 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','current_head_2018.csv'))
df2017 = renameColumns(df2017)
df2018 = renameColumns(df2018)
dfAll = df2017.append(df2018, sort=False)
dfAll.to_csv(path_project.joinpath(
        'data/interim/Salary','head_teams_all.csv'), index = False)

# History Info
df2017 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','salary_fb_head_team_hist_2017.csv'))
df2018 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','salary_fb_head_team_hist_2018.csv'))
df2017 = renameColumns(df2017)
df2018 = renameColumns(df2018)
dfAll = pd.merge(df2017, df2018, how='outer', 
                 on = ['coach', 'last_year_bonus', 'max_bonus', 'other_pay', 
                       'school', 'school_pay', 'total_pay', 'conference'])
dfAll['year'] = dfAll.apply(lambda row: mergeColumns(row), axis = 1)
dfAll = dfAll.drop(['year_x', 'year_y'], axis=1)
dfAll['conference'] = dfAll['conference'].apply(lambda x: x.strip())
dfAll.drop_duplicates(inplace=True)
dfAll = dfAll.sort_values(by=['coach'])
dfAll.to_csv(path_project.joinpath(
        'data/interim/Salary','head_hist_all.csv'), index = False)

#------------------------------------------------------------------------------
# Football Assistant Coach Salaries
#------------------------------------------------------------------------------
# Coach Info
df2017 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','coach_info_fb_asst_2017.csv'))
df2018 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','coach_info_fb_asst_2018.csv'))
df2017 = df2017.drop(['career_record', 'school_record'], axis=1)
df2018 = df2018.drop(['career_record', 'school_record'], axis=1)
dfAll = df2017.append(df2018)
dfAll.to_csv(path_project.joinpath(
        'data/interim/Salary','asst_info_all.csv'), index = False)

# Current Info
df2017 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','current_asst_2017.csv'))
df2018 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','current_asst_2018.csv'))
dfAll = df2017.append(df2018)
dfAll.to_csv(path_project.joinpath(
        'data/interim/Salary','asst_teams_all.csv'), index = False)

# History Info
df2017 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','salary_fb_asst_hist_2017.csv'))
df2018 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','salary_fb_asst_hist_2018.csv'))
dfAll = pd.merge(df2017, df2018, how='outer', 
                 on = ['coach', 'last_year_bonus', 'max_bonus', 'other_pay', 
                       'position', 'school_name', 'school_pay', 'total_pay',])
dfAll['year'] = dfAll.apply(lambda row: mergeColumns(row), axis = 1)
dfAll = dfAll.drop(['year_x', 'year_y'], axis=1)
dfAll.drop_duplicates(inplace=True)
dfAll = dfAll.sort_values(by=['coach'])
dfAll.to_csv(path_project.joinpath(
        'data/interim/Salary','asst_hist_all.csv'), index = False)

#------------------------------------------------------------------------------
# Football Strength Coach Salaries
#------------------------------------------------------------------------------
# Coach Info
df2017 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','current_strength_2017.csv'))
df2018 = pd.read_csv(path_project.joinpath(
        'data/raw/Salary','current_strength_2018.csv'))
dfAll = df2017.append(df2018)
dfAll.to_csv(path_project.joinpath(
        'data/interim/Salary','strength_teams_all.csv'), index = False)
