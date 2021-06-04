#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 15:34:59 2021

@author: reideej1

:DESCRIPTION:
    - Post-process 247 composite recruiting data for NCAA College Football
    - data manually acquired from: https://collegefootballdata.com/exporter/recruiting/teams?year=1999

:REQUIRES:
    - Refer to `Package Import` section below for required packages
   
:TODO:
    - NONE
"""
 
#==============================================================================
# Package Import
#==============================================================================
import os  
import pandas as pd
import pathlib
import requests
import tqdm
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

#==============================================================================
# Function Definitions / Reference Variable Declaration
#==============================================================================
def renameSchool(df_year, name_var):
    '''
    Purpose: Rename a school/university to a standard name as specified in 
        the file `school_abbreviations.csv`

    Inputs
    ------
        df_year : Pandas Dataframe
            DataFrame containing massey ratings for a specific year
        name_var : string
            Name of the variable which is to be renamed/standardized
    
    Outputs
    -------
        df_year : Pandas DataFrame
            Standardized version of the massey ratings  with "standardized"
            school names to ensure compatability across all datasets
    '''  
    # read in school name information
    df_school_names = pd.read_csv(
        pathlib.Path('data/raw/school abbreviations and pictures.csv'))
     
    # convert the dataframe to a dictionary such that the keys are the
    #   optional spelling of each school and the value is the standardized
    #   name of the school
    dict_school_names = {}
    
    for index, row in df_school_names.iterrows():
        # isolate the alternative name columns
        names = row[[x for x in row.index if 'Name' in x]]
        # convert the row to a list that doesn't include NaN values
        list_names = [x for x in names.values.tolist() if str(x) != 'nan']
        # add the nickname to the team names as an alternative name
        nickname = row['Nickname']
        list_names_nicknames = list_names.copy()
        for name in list_names:
            list_names_nicknames.append(name + ' ' + nickname)
        # extract the standardized team name
        name_standardized = row['Team']
        # add the standardized name
        list_names_nicknames.append(name_standardized)
        # add the nickname to the standardized name
        list_names_nicknames.append(name_standardized + ' ' + nickname)
        # for every alternative spelling of the team, set the value to be
        #   the standardized name
        for name_alternate in list_names_nicknames:
            dict_school_names[name_alternate] = name_standardized
            
    df_year[name_var] = df_year[name_var].apply(
        lambda x: dict_school_names[x] if str(x) != 'nan' else '')
        
    return df_year   

def insertConferenceData(df_year):
    '''
    Purpose: Insert a school's conference and Power 5 status into the dataframe

    Inputs
    ------
        df_year : Pandas Dataframe
            DataFrame containing massey ratings for a specific year
    
    Outputs
    -------
        list(row)[0] : string
            Standardized version of the school's name based on the first value
            in the row in the file `school_abbreviations.csv`
    '''  
    # read in school name information
    df_school_names = pd.read_csv(
        pathlib.Path('data/raw/school abbreviations and pictures.csv'))
     
    # make a look-up dictionary for conferences and power 5 status
    dict_lookup = {}
    for index, row in df_school_names.iterrows():
        dict_lookup[row['Team']] = {'conference' : row['ConferenceAbbrev'],
                                    'power5' : row['Power5']}
    
    # for each team, add the conference and power5 status
    df_year['Conference'] = df_year['Team'].apply(
        lambda x: dict_lookup[x]['conference'] if str(x) != 'nan' else '')
    df_year['Power5'] = df_year['Team'].apply(
        lambda x: dict_lookup[x]['power5'] if str(x) != 'nan' else '')
    
    return df_year

def processYear(scrape_year):
    '''
    Purpose: Given a year, clean up the .csv generated for that year
    
    Input:
        (1) scrape_year (int): year for which to scrape data
    
    Output:
        (1) (.csv file) A processed .csv file for the given year
            Files are output to /data/raw/Massey/ 
    '''    
    # read in data for the given year
    df_year = pd.read_csv(pathlib.Path('data/raw/Recruiting/247Composite').joinpath(
        '247composite_' + str(scrape_year) + '.csv'))
    
    # clean up column names
    df_year.columns = ['Year', 'Rank_247Comp', 'Team', 'Recruit_Pts']
    
    # standardize team names
    df_year = renameSchool(df_year, 'Team')
    
    # add a column for conference and power 5 status
    df_year = insertConferenceData(df_year)
       
    # export the cleaned/processed Pandas DataFrame to a .csv
    df_year.to_csv(pathlib.Path('data/processed/Recruiting/247Composite').joinpath(
        '247composite_' + str(scrape_year) + '.csv'), index = False)

def createSummaryFile():
    '''
    Purpose: Combine 247 Composite rankings for all available years into one file
    
    Input:
        None
    
    Output:
        (1) (.csv file) A processed .csv file for the given year
            Files are output to /data/raw/Massey/ 
    '''    
    # get a list of all .csv files available for Massey ratings
    filenames = os.listdir(pathlib.Path('data/processed/Recruiting/247Composite'))
    list_files = [fname for fname in filenames if fname.endswith('.csv')]
    
    # merge data together
    df_all = pd.DataFrame()
    for file_path in list_files:
        if len(df_all) == 0:
            df_all = pd.read_csv(pathlib.Path(
                'data/processed/Recruiting/247Composite').joinpath(file_path))
        else:
            df_all = df_all.append(pd.read_csv(
                pathlib.Path('data/processed/Recruiting/247Composite').joinpath(file_path)))
    
    # rename IND (FBS) to IND
    df_all['Conference'] = df_all['Conference'].apply(lambda x: 'IND' if x == 'IND (FBS)' else x)
    
    # export the "master" file to a .csv
    df_all.to_csv(pathlib.Path('data/processed/Recruiting/247Composite').joinpath(
        '247composite_ALL.csv'), index = False)
    
    return

def process247CompositeRatings(path_project, scrape_year='all'):
    '''
    Purpose: Scrape 247 Composite Rankings NCAA College Football. 
        Rankings are output to individual .cvs files for every year.  
    
    Input:
        (1) path_project (pathlib Path): Directory file path of the project
        (2) scrape_year (int): year for which to scrape data
        
    Output:
        None
    '''            
    # post-process ratings data for all available years
    for year in tqdm.tqdm(list(range(2000,2021))):
        processYear(year)    
        
    # create one file for all available years
    createSummaryFile()

process247CompositeRatings(os.path.abspath(os.curdir))