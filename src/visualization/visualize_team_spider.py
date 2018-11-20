#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 11:24:47 2018

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
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

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
path_project = pathlib.Path('/home/ejreidelbach/Projects/cfbAnalysis')
os.chdir(path_project)

# Attempt to visualize the Nebraska Cornhuskers
df = pd.read_csv(pathlib.Path('data/interim/CFBStats/Nebraska/situations' + 
                              '/passing_offense_situational.csv'))