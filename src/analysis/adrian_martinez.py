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

# Adrian in 1st quarter

#------------- Handle "Split" stats --------------------------------------

# retrieve categories for "split" statistics
split_ctg = []
split_stats = []

# 1. Rank by year
df_split_ranked = pd.DataFrame()
print('ranking each situational stat by year')
for ctg in tqdm.tqdm(split_ctg):
    # rank every stat based on the specific category - year combination
    df_ctg = df_split[df_split['split'] == ctg].copy()
    for stat in split_stats:
        ctg_name = 'rank_' + stat + '_by_year'
        df_ctg[ctg_name] = df_ctg.groupby(['season'])[stat].rank(
                method='first', ascending=False, na_option='bottom')
        
    # add the stats to the master dataframe
    if len(df_split_ranked) == 0:
        df_split_ranked = df_ctg.copy()
    else:
        df_split_ranked = df_split_ranked.append(df_ctg)
df_split_ranked = df_split_ranked.reset_index(drop = True)

#------------- Handle "Situational" stats --------------------------------

# retrieve categories for "situational" statistics
sit_stats = [s for s in list(df_situational.columns) if any(xs in s for xs in ['pass', 'rush'])]
sit_ctg = list(set(df_situational['situation']))

# Adrian in 2nd quarter

# Adrian in 3rd quarter

# Adrian in 4th quarter

# Adrian in 1st/3rd Quarters

# Adrian in 2nd/4th Quarters

# Compare 1st/3rd and 2nd/4th Quarters...is the dropoff normal?

# Adrian in one-score games (8 pts or less)

# Adrian in 15+ score games

# Compare one-score vs 15+ score games...is the dropoff normal?