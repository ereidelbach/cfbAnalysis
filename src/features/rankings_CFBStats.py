#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 11:15:56 2018

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
    
def createRankingVariable():
    # National Ranking
    
    # Conference Ranking
    
    # Division Ranking
    
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
path_project = pathlib.Path('/home/ejreidelbach/Projects/cfbAnalysis')
os.chdir(path_project)

# Grab data for the Nebraska Cornhuskers
df = pd.read_csv(pathlib.Path('data/interim/CFBStats/Nebraska/situations' + 
                              '/passing_offense_situational.csv'))