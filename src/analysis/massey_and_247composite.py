#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 15:43:37 2021

@author: reideej1

:DESCRIPTION: Analyze the difference between 247 Composite Recruiting Rankings
    and Massey Ratings

:REQUIRES:
    - Refer to Package Import Section for required packages/libraries
   
:TODO:
    -None
"""
 
#==============================================================================
# Package Import
#==============================================================================
import numpy as np
import os  
import pandas as pd
import pathlib

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

# load team data for all available years (Massey and 247 Composite)
df_massey = pd.read_csv(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\processed\Massey\massey_ALL.csv')
df_247 = pd.read_csv(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\processed\Recruiting\247Composite\247composite_ALL.csv')

# merge data to create one cohesive data set
df = pd.merge(df_massey, df_247, how = 'left', on = ['Team', 'Year', 'Conference', 'Power5'])

# subset data to years 2000+ because recruiting data only goes back to then
df = df[df['Year'] >= 2000]
df = df.reset_index(drop = True)
df = df.drop('Recruit_Pts', axis = 1)

# sort dataframe by team and year
df = df.sort_values(by = ['Team', 'Year'])
df = df.reset_index(drop = True)

# calculate rolling 4 year average for 247 Composite Rankings        
df['Rank_247Comp_4_yr_avg'] = df.groupby(['Team'])['Rank_247Comp'].transform(
    lambda x: x.rolling(4).median())

# calculate difference between overall Massey Rank and rolling 4 yr 247 Composite Avg.
df['massey_vs_247comp'] = df.apply(lambda row: row['Rank_247Comp_4_yr_avg'] - row['Rank_Overall']
                                   if ~pd.isna(row['Rank_247Comp_4_yr_avg']) else np.nan, axis = 1)

# subset data to 2004 (first year with a full 4 years of recruiting data)
df = df[df['Year'] >= 2004]

# plot all teams
df_p5 = df[df['Power5'] == True]
df_p5.plot.line(x = 'Year', y = 'massey_vs_247comp')

# plot power 5
df_neb = df[df['Team'] == 'Nebraska']
df_neb.plot.line(x = 'Year', y = 'massey_vs_247comp')
df_neb.plot.line(x = 'Year', y = ['Rank_247Comp_4_yr_avg', 'Rank_Overall'])

# plot by conference