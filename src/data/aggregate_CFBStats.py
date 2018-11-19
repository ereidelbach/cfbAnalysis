#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:55:09 2018

@author: ejreidelbach

:DESCRIPTION:

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
# Function Definitions / Reference Variable Declaration
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
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
dir_path = pathlib.Path('/home/ejreidelbach/Projects/')
#os.chdir(r'/home/ejreidelbach/Projects')

def aggregateRosters():
    '''
    Purpose: Ingest roster information for all teams and combine into one 
        massive roster file
        
    Input:
        - NONE
        
    Output
        - NONE
    '''
    # Set the directory where the files are located
    dir_path = pathlib.Path('data/raw/CFBStats')
    
    # Find every folder in the Data directory
    list_files_rosters = list(dir_path.rglob('rosters.csv'))
    
    df_master = pd.DataFrame()
    # Iterate over every folder and compile all roster into df_master
    for file in list_files_rosters:
        df = pd.read_csv(file)
        df['school'] = str(file).split('CFBStats/')[1].split('/rosters.csv')[0]
        df_master = df_master.append(df)
        print('Done with: ' +str(file))
    df_master = df_master.reset_index()                 # Reset Index
    df_master.drop(['index'], axis=1, inplace=True)     # Drop Old Index
    df_master.to_csv(pathlib.Path('data/interim').joinpath(pathlib.Path(
                    'merged_rosters.csv')), index=False) # Export to CSV    
    
    
def combineFiles():
    
    # Add dataframe to master dataframe
    df_master = df_master.append(df_year)
    df_master = df_master.reset_index()                # Reset Index
    df_master.drop(['index'], axis=1, inplace=True)    # Drop Old Index

def cleanRoster(roster):
    '''
    Purpose: Clean up errors in a team's roster. Such errors include missing 
        values (e.g. roster numbers, position, hometown, etc.).  In addition,
        create the redshirt variables: redshirt_yr (boolean indicator if a 
        specific year is a player's redshirt year) and redshirted (boolean
        indicator if a player redshirted in their career)
        
    Input:
        - roster (DataFrame): Table containing a team's roster information
        
    Output:
        - roster_clean (DataFrame): Table with missing values filled in and
            redshirt variables included
    '''
