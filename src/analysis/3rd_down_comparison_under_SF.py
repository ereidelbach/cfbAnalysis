#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 21:45:27 2021

@author: Eric

:DESCRIPTION:

:REQUIRES:
    - Refer to Package Import section for all required packages
  
:TODO:
    - TBD
"""
 
#==============================================================================
# Package Import
#==============================================================================
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
path_proj = pathlib.Path(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis')
os.chdir(path_proj)
path_data = path_proj.joinpath('data', 'interim', 'CFBStats', 'ALL', 'situations')
list_fpaths = [str(x) for x in path_data.glob('*_offense_*.csv')]

df_passing = pd.DataFrame()
df_rushing = pd.DataFrame()

for fpath in tqdm.tqdm(list_fpaths):
    if 'passing' in fpath:
        df_passing = df_passing.append(pd.read_csv(fpath), sort = False)
    elif 'rushing' in fpath:
        df_rushing = df_rushing.append(pd.read_csv(fpath), sort = False)
        
# reduce data to the years of interest (2018-2020)
df_passing = df_passing[df_passing['season'].isin([2018, 2019, 2020])]
df_rushing = df_rushing[df_rushing['season'].isin([2018, 2019, 2020])]
        
# reduce data to the stats we care about (total plays + 3rd downs)
df_passing = df_passing[df_passing['situation'].str.contains('(3rd Down)', regex = True)]
df_rushing = df_rushing[df_rushing['situation'].str.contains('(3rd Down)', regex = True)]
df_rushing = df_rushing.drop_duplicates()
        
# # eliminate teams that haven't played at least 6 games in a season
# df_passing_remove = df_passing[(df_passing['situation'] == 'All Plays') & (df_passing['g'] < 6)]
# df_passing_remove = df_passing_remove[['season', 'team']]
# df_passing = df_passing[~(df_passing['team'].isin(list(set(df_passing_remove.team))) & 
#                           (df_passing['season'].isin(list(set(df_passing_remove.season)))))]
# df_passing = df_passing.reset_index(drop = True)

# df_rushing_remove = df_rushing[(df_rushing['situation'] == 'All Plays') & (df_rushing['g'] < 6)]
# df_rushing_remove = df_rushing_remove[['season', 'team']]
# df_rushing = df_rushing[~(df_rushing['team'].isin(list(set(df_rushing_remove.team))) & 
#                           (df_rushing['season'].isin(list(set(df_rushing_remove.season)))))]
# df_rushing = df_rushing.reset_index(drop = True)

# combine stats into one table
df_passing = df_passing.drop(columns = ['rating', '15+', '25+', 'long'])
df_passing.columns = ['situation', 'g_pass', 'att_pass', 'comp_pass', 'comp_pct_pass', 
                      'yards_pass', 'td_pass', 'int', '1st_pass', 'season', 'team']
df_rushing = df_rushing.drop(columns = ['10+', '20+', 'long'])
df_rushing.columns = ['situation', 'g_run', 'att_run', 'yards_run', 
                      'avg_run', 'td_run', '1st_run', 'season', 'team']
df_stats = pd.merge(df_passing, df_rushing, how = 'left', on=['situation', 'season', 'team'])

# engineer some new features/variables
df_stats['att_total']   = df_stats['att_pass'] + df_stats['att_run']            # 3rd Down Attempts
df_stats['1st_total']   = df_stats['1st_pass'] + df_stats['1st_run']            # 1st Downs (3rd Down Conversions)

df_stats['%_pass']      = (df_stats['att_pass'] / df_stats['att_total'])*100    # 3rd Down Attempts as a Rush
df_stats['%_run']       = (df_stats['att_run'] / df_stats['att_total'])*100     # 3rd Down Attempts as a Pass

df_stats['conv_%']      = (df_stats['1st_total'] / df_stats['att_total'])*100   # 3rd Down Conversion %
df_stats['conv_%_pass'] = (df_stats['1st_pass'] / df_stats['att_total'])*100       # 3rd Down Pass Conversion %
df_stats['conv_%_run']  = (df_stats['1st_run'] / df_stats['att_total'])*100        # 3rd Down Rush Conversion %

df_stats['yards_att_pass']  = df_stats['yards_pass']/df_stats['att_pass']       # Avg. Yards Per Pass Att.
df_stats['yards_comp_pass'] = df_stats['yards_pass']/df_stats['comp_pass']      # Avg. Yards Per Pass Comp.

df_stats['yards_total']     = df_stats['yards_pass'] + df_stats['yards_run']    # Total Yards Gained
df_stats['yards_att_total'] = df_stats['yards_total'] / df_stats['att_total']   # Total Yards per Attempt

df_stats['g']           = max([int(x) for x in df_stats['g_pass']], [int(x) for x in df_stats['g_run']])  # Total Games

# Determine % of each situation (as a percentage of total 3rd down attempts)
list_situation_pct = []
df_stat_groups = df_stats.groupby(['season', 'team'])
for group_name, df_group in df_stat_groups:
    total_attempts = 0
    for row_index, row in df_group.iterrows():
        if row['situation'] == '3rd Down':
            list_situation_pct.append(np.nan)
            total_attempts = row['att_total']
        else:
            list_situation_pct.append((row['att_total']/total_attempts) * 100)
df_stats['situation_%'] = list_situation_pct

# rename some variables
df_stats = df_stats.rename({'avg_run':'yards_att_run'}, axis = 1)

# round all decimals to 1 decimal place
df_stats = df_stats.round(1)

#-----------------------------------------------------------------------------#
# CREATE TOTAL COLUMNS
#-----------------------------------------------------------------------------#
df_stat_groups = df_stats.groupby(['team'])
# iterate over every school
for group_name, df_group in df_stat_groups:
    # iterate over every situation
    total_attempts = 0
    for situation in list(df_group.situation.unique()):
        df_situation = df_group[df_group['situation'] == situation]
        # sum all stats
        df_situation_sum = df_situation.sum()
        # clean up variables as required
        df_situation_sum['situation']       = df_situation['situation'].iloc[0]
        df_situation_sum['team']            = df_situation['team'].iloc[0]
        df_situation_sum['season']          = 'ALL'
        df_situation_sum['comp_pct_pass']   = round(float(df_situation_sum['comp_pass'] / df_situation_sum['att_pass'])*100,1)
        df_situation_sum['yards_att_run']   = round(float(df_situation_sum['yards_run'] / df_situation_sum['att_run']),1)
        df_situation_sum['%_pass']          = round(float(df_situation_sum['att_pass'] / df_situation_sum['att_total'])*100,1)
        df_situation_sum['%_run']           = round(float(df_situation_sum['att_run'] / df_situation_sum['att_total'])*100,1)
        df_situation_sum['conv_%']          = round(float(df_situation_sum['1st_total'] / df_situation_sum['att_total'])*100,1)
        df_situation_sum['conv_%_pass']     = round(float(df_situation_sum['1st_pass'] / df_situation_sum['att_total'])*100,1)
        df_situation_sum['conv_%_run']      = round(float(df_situation_sum['1st_run'] / df_situation_sum['att_total'])*100,1)
        df_situation_sum['yards_att_pass']  = round(float(df_situation_sum['yards_pass'] / df_situation_sum['att_pass']),1)
        df_situation_sum['yards_comp_pass'] = round(float(df_situation_sum['yards_pass'] / df_situation_sum['comp_pass']),1)
        df_situation_sum['yards_att_total'] = round(float(df_situation_sum['yards_total'] / df_situation_sum['att_total']),1)
        if df_situation_sum['situation'] == '3rd Down':
            df_situation_sum['situation_%'] = np.nan
            total_attempts = df_situation_sum['att_total']
        else:
            df_situation_sum['situation_%'] = round(float(df_situation_sum['att_total'] / total_attempts)*100,1)
        df_situation_sum = df_situation_sum.to_frame().transpose()
        # add situation to the overall dataframe
        df_stats = df_stats.append(df_situation_sum)

# # Clean up columns
# df_stats['comp_pct_pass']   = round(float(df_stats['comp_pass']   / df_stats['att_pass'])*100,1)
# df_stats['yards_att_run']   = round(float(df_stats['yards_run']   / df_stats['att_run']),1)
# df_stats['%_pass']          = round(float(df_stats['att_pass']    / df_stats['att_total'])*100,1)
# df_stats['%_run']           = round(float(df_stats['att_run']     / df_stats['att_total'])*100,1)
# df_stats['conv_%']          = round(float(df_stats['1st_total']   / df_stats['att_total'])*100,1)
# df_stats['conv_%_pass']     = round(float(df_stats['1st_pass']    / df_stats['att_total'])*100,1)
# df_stats['conv_%_run']      = round(float(df_stats['1st_run']     / df_stats['att_total'])*100,1)
# df_stats['yards_att_pass']  = round(float(df_stats['yards_pass']  / df_stats['att_pass']),1)
# df_stats['yards_comp_pass'] = round(float(df_stats['yards_pass']  / df_stats['comp_pass']),1)
# df_stats['yards_att_total'] = round(float(df_stats['yards_total'] / df_stats['att_total']),1)
        
# ensure all columns are numeric (where applicable)
df_stats = df_stats.apply(pd.to_numeric, errors = 'ignore')

#-----------------------------------------------------------------------------#
# RANK VARIABLES
#-----------------------------------------------------------------------------#
rank_vars = ['situation_%', '%_pass', '%_run', 'conv_%', 'conv_%_pass', 'conv_%_run',
             'att_total','att_pass', 'att_run', '1st_total', 
             'yards_att_total', 'yards_comp_pass', 'yards_att_pass', 'yards_att_run', 
             'comp_pct_pass', '1st_pass', '1st_run']
for var in rank_vars:
    df_stats[var + '_rank'] = df_stats.groupby(['situation', 'season'])[var].rank('min', ascending = False)
    
# Reorder columns
df_stats = df_stats[['season', 'team', 'g', 'situation', 'situation_%', 
                     'situation_%_rank', '%_pass', '%_pass_rank', 
                     '%_run', '%_run_rank', 'conv_%', 'conv_%_rank', 'conv_%_pass', 
                     'conv_%_pass_rank', 'conv_%_run', 'conv_%_run_rank',   
                     'att_total', 'att_total_rank', 'att_pass', 'att_pass_rank',
                     'att_run', 'att_run_rank', 
                     '1st_total', '1st_total_rank',
                     'yards_total', 'yards_att_total', 'yards_att_total_rank', 
                     'g_pass', 'yards_pass', 'att_pass', 'att_pass_rank',
                     'comp_pass', 'comp_pct_pass', 'comp_pct_pass_rank', 'yards_att_pass',
                     'yards_att_pass_rank', 'yards_comp_pass', 
                     'yards_comp_pass_rank', '1st_pass', '1st_pass_rank', 
                     'td_pass', 'int', 
                     'g_run', 'yards_run', 'att_run', 'att_run_rank', 
                     'yards_att_run', 'yards_att_run_rank', 
                     'td_run', '1st_run', '1st_run_rank']]
df_stats.to_csv(r'C:\Users\reideej1\Desktop\3rd_down_all_years.csv', index = False)