#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 14:41:30 2021

@author: reideej1

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
from scrape_CFBStats import scrapeCFBStats
from aggregate_CFBStats_by_team import aggregate_data_by_team
from aggregate_CFBStats_by_category import aggregate_data_by_category

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

# # Set the project working directory
# path_project = pathlib.Path(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis')
# os.chdir(path_project)

# # scrape data for the most recent season
# scrapeCFBStats(path_project, 2021)

# # aggregate data across all teams
aggregate_data_by_team(path_project)
    
# aggregate data for all player stats
# aggregate_data_by_category(path_project)