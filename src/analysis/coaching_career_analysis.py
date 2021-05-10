#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:46:57 2020

@author: reideej1

:DESCRIPTION: Evaluate coaching data for the last 50 years of college football
    - the goal is to determine how coaches who struggle in their first 3 years
        fare over time at the same program

:REQUIRES: scrape_sports_reference.py located in: cfbAnalysis\src\data
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import datetime
import glob
import os  
import pandas as pd
import pathlib
import tqdm

from src.data.scrape_sports_reference import *

#==============================================================================
# Reference Variable Declaration
#==============================================================================

#==============================================================================
# Function Definitions
#==============================================================================
def create_coach_dataframe(df_schools):
    '''
    Purpose: Given historic school data, create a dataframe of coaches and
        their performance data on a year-by-year basis

    Inputs   
    ------
        df_schools : Pandas DataFrame
            Contains year-by-year results for each school (with coaches' names)
            
    Outputs
    -------
        df_coaches : Pandas DataFrame
            A dataframe containing all historic season data from a coaching perspective
    '''
    # Create a dictionary that assigns each school to its current conference
    df_conf = df_schools.groupby(['School', 'Conf']).head(1).groupby('School').head(1).reset_index(drop = True)
    df_conf = df_conf[['School', 'Conf']]
    df_conf['Power5'] = df_conf.apply(lambda row: True if row['Conf'] in [
        'SEC', 'Pac-12', 'Big 12', 'ACC', 'Big Ten'] else False, axis = 1)
    df_conf = df_conf.set_index('School')
    dict_conf = df_conf.to_dict(orient = 'index')
    
    # Create a coaching dataframe by iterating over every year for every school
    list_coaches = []
    for index, row in df_schools.iterrows():
        # handle every coach that coached that season
        for coach in row['Coach(es)'].split(','):
            dict_coach_year = {}
            dict_coach_year['coach'] = coach.split(' (')[0].strip()
            dict_coach_year['year'] = row['Year']
            dict_coach_year['school'] = row['School']
            dict_coach_year['ranking_pre'] = row['AP Pre']
            dict_coach_year['ranking_high'] = row['AP High']
            dict_coach_year['ranking_post'] = row['AP Post']
            dict_coach_year['ranked_pre'] = not pd.isna(row['AP Pre'])
            dict_coach_year['ranked_post'] = not pd.isna(row['AP Post'])
            dict_coach_year['ranked_top_10'] = row['AP Post'] <= 10
            dict_coach_year['ranked_top_5'] = row['AP Post'] <= 5
            # handle bowl games
            if pd.isna(row['Bowl']):
                dict_coach_year['bowl'] = False
                dict_coach_year['bowl_name'] = ''
                dict_coach_year['bowl_win'] = False
            else:
                dict_coach_year['bowl'] = True
                dict_coach_year['bowl_name'] = row['Bowl'].split('-')[0]
                if '-' in row['Bowl']:
                    if row['Bowl'].split('-')[1] == 'W':
                        dict_coach_year['bowl_win'] = True       
            # handle wins and losses
            if len(coach.split('(')[1].split('-')) > 2:
                dict_coach_year['W'] = coach.split('(')[1].split('-')[0]
                dict_coach_year['L'] = coach.split('(')[1].split('-')[1].strip(')')
                dict_coach_year['T'] = coach.split('(')[1].split('-')[2].strip(')')
            else:
                dict_coach_year['W'] = coach.split('(')[1].split('-')[0]
                dict_coach_year['L'] = coach.split('(')[1].split('-')[1].strip(')')
            # assign conference information
            dict_coach_year['conf'] = dict_conf[row['School']]['Conf']
            dict_coach_year['power5'] = dict_conf[row['School']]['Power5']
            list_coaches.append(dict_coach_year)
            
    # Convert list to DataFrame
    df_coaches = pd.DataFrame(list_coaches)
    
    # Convert all Tie Nans to 0
    df_coaches['T'] = df_coaches['T'].fillna(0)
    
    # Identify all unique coaches in the dataframe
    list_coaches = list(df_coaches['coach'].unique())
    
    # Cast Win and Loss columns to ints
    df_coaches['W'] = df_coaches['W'].astype('int')
    df_coaches['L'] = df_coaches['L'].astype('int')
    df_coaches['T'] = df_coaches['T'].astype('int')
    
    # Add a column for games coached in the season
    df_coaches['GP'] = df_coaches.apply(lambda row: row['W'] + row['L'] + row['T'], axis = 1)
    
    return df_coaches

def add_coach_metadata(df_stint):
    '''
    Purpose: Iterate over a coach's historic data and tabulate totals on a 
        year-by-year basis

    Inputs   
    ------
        df_stint : Pandas DataFrame
            Contains year-by-year results for a coach
            ** Note: This is continuous years only. Breaks in coaching stints
                        are treated as separate coaching histories **
            
    Outputs
    -------
        df_coach : Pandas DataFrame
            Coaching data with updated year-by-year totals
    '''
    df_coach = df_stint.copy()
    #   1. Year # at school
    df_coach['season'] = list(range(1,len(df_coach)+1))
    
    #   2. Cumulative games coached at school (on a year-by-year basis)
    df_coach['cum_GP'] = df_coach['GP'].cumsum(axis = 0)
    
    #   3. Cumulative wins at school (on a year-by-year basis)
    df_coach['cum_W'] = df_coach['W'].cumsum(axis = 0)
    
    #   4. Cumulative losses at school (on a year-by-year basis)
    df_coach['cum_L'] = df_coach['L'].cumsum(axis = 0)
    
    #   5. Cumulative ties at school (on a year-by-year basis)
    df_coach['cum_T'] = df_coach['T'].cumsum(axis = 0)
    
    #   6. Cumulative Win Pct at school (on a year-by-year basis)
    if len(df_coach) == 1:
        if int(df_coach['cum_GP']) == 0:
            df_coach['cum_win_pct'] = 0
        else:
            df_coach['cum_win_pct'] = df_coach.apply(lambda row: row['cum_W'] / row['cum_GP'], axis = 1)
    else:
        df_coach['cum_win_pct'] = df_coach.apply(lambda row: row['cum_W'] / row['cum_GP'], axis = 1)
    
    #   7. Total bowl games at school
    df_coach['total_bowl'] = df_coach['bowl'].sum(axis = 0)
    
    #   8. Total bowl wins at school
    df_coach['total_bowl_win'] = df_coach['bowl_win'].sum(axis = 0)
    
    #   9. Total AP Preseason rankings
    df_coach['total_ranked_pre'] = df_coach['ranked_pre'].sum(axis = 0)
    
    #   10. Total AP Postseason rankings
    df_coach['total_ranked_post'] = df_coach['ranked_post'].sum(axis = 0)
    
    #   11. Total Top 10 finishes
    df_coach['total_top_10'] = df_coach['ranked_top_10'].sum(axis = 0)
    
    #   12. Total Top 5 finishes
    df_coach['total_top_5'] = df_coach['ranked_top_5'].sum(axis = 0)
    
    #   13. Total Seasons Coached at School
    df_coach['total_seasons'] = df_coach.iloc[len(df_coach)-1]['season'] 
    
    #   14. Total Games Coached at School
    df_coach['total_games'] = df_coach.iloc[len(df_coach)-1]['cum_GP']
    
    #   15. Total Wins at School
    df_coach['total_wins'] = df_coach.iloc[len(df_coach)-1]['cum_W']
    
    #   16. Total Losses at School
    df_coach['total_losses'] = df_coach.iloc[len(df_coach)-1]['cum_L']
    
    #   17. Total Win Pct at School
    df_coach['total_win_pct'] = df_coach.iloc[len(df_coach)-1]['cum_win_pct']
    
    return df_coach

def calculate_year_by_year(df_coaches):
    '''
    Purpose: Given the data for coaches in a historical perspective, iterate
        through their coaching stints and calculate year-by-year totals in an 
        effor to understand their progress over time

    Inputs   
    ------
        df_coaches : Pandas DataFrame
            A dataframe containing all historic season data from a coaching perspective
            
    Outputs
    -------
        df_yr_by_yr : Pandas DataFrame
            Coaching data with updated year-by-year totals separated by stints
                at schools in each coach's career
    '''
    # make an empty dataframe for storing new coach info
    df_yr_by_yr = pd.DataFrame()
    
    # Coach-by-coach --> Year by year, determine the following:
    gps = df_coaches.groupby(['coach', 'school'])
    for combo, df_coach in tqdm.tqdm(gps):
        # sort the dataframe by earliest year to latest
        df_coach = df_coach.sort_values(by = 'year')
        
        # look for gaps in years
        num_stints = 1
        list_stint_end = []
        list_years = list(df_coach['year'])
        for num_ele in list(range(0,len(list_years))):
            if (num_ele == 0):
                pass
            else:
                if list_years[num_ele] - list_years[num_ele-1] > 1:
                    # print(f"Gap detected for coach: {df_coach.iloc[0]['coach']}")
                    # print(f"  -- Gap between {list_years[num_ele]} and {list_years[num_ele-1]}")
                    list_stint_end.append(list_years[num_ele-1])
                    num_stints = num_stints + 1
                    
        # handle coaches with multiple stints
        if num_stints >= 2:
            for stint_count in list(range(0,num_stints)):
                # split the coaches data into stints
                if stint_count == 0:
                    year_stint_end = list_stint_end[stint_count]
                    df_stint = df_coach[df_coach['year'] <= year_stint_end]
                elif stint_count < num_stints-1:
                    year_stint_end = list_stint_end[stint_count]
                    year_stint_end_prev = list_stint_end[stint_count-1]
                    df_stint = df_coach[df_coach['year'] <= year_stint_end]
                    df_stint = df_stint[df_stint['year'] > year_stint_end_prev]
                else:
                    year_stint_end_prev = list_stint_end[stint_count-1]
                    df_stint = df_coach[df_coach['year'] > year_stint_end_prev]
                # process the data on a year by year basis
                df_stint = add_coach_metadata(df_stint)
                # Add coach dataframe to overall dataframe
                if len(df_yr_by_yr) == 0:
                    df_yr_by_yr = df_stint.copy()
                else:
                    df_yr_by_yr = df_yr_by_yr.append(df_stint)            
        else:
            # process the data on a year by year basis
            df_coach = add_coach_metadata(df_coach)
            # Add coach dataframe to overall dataframe
            if len(df_yr_by_yr) == 0:
                df_yr_by_yr = df_coach.copy()
            else:
                df_yr_by_yr = df_yr_by_yr.append(df_coach)
            
    # reset dataframe index
    df_yr_by_yr = df_yr_by_yr.reset_index(drop = True)
    
    return df_yr_by_yr

#==============================================================================
# Working Code
#==============================================================================
# Set the project working directory
path_dir = pathlib.Path(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis')
os.chdir(path_dir)

# Load team history data
df_schools = scrapeCfbSchoolsAllYears()

# Load week-by-week records for all schools
df_results = scrapeCfbResultsAllYears()

# Create week-by-week records for all coaches

# Create timestamp for filename 
ts = datetime.date.fromtimestamp(time.time())
df_schools.to_csv(rf'data\raw\Team History\team_history_{ts}.csv', index = False)

# Ingest the most recent team history file
df_schools = pd.read_csv(max(glob.iglob(r'data\raw\Team History\team_history*.csv'), key=os.path.getmtime))

# Create a dataframe of coaching information given school info
df_coaches = create_coach_dataframe(df_schools)

# Using historic coaching data, create a new dataframe that calculates
#   year-over-year totals for each coach
df_coaches = calculate_year_by_year(df_coaches)

# Save coaching data to disk
ts = datetime.date.fromtimestamp(time.time())
df_coaches.to_csv(rf'data\raw\Coaches\coaching_history_{ts}.csv', index = False)

#------------------------------------------------------------------------------
# Start of Scott Frost Analysis
#------------------------------------------------------------------------------
# Ingest the most recent coaching history file
df_coaches = pd.read_csv(max(glob.iglob(r'data\raw\Coaches\coaching_history*.csv'), key=os.path.getmtime))

# Subset the data to coaches in their 3rd year with more
df_yr_3 = df_coaches[df_coaches['season'] == 3]

# Isolate Scott Frost's Winning %
sf_win_pct = float(df_yr_3[df_yr_3['coach'] == 'Scott Frost']['cum_win_pct'])
# Isolate Scott Frost's Games Played
sf_gp = int(df_yr_3[df_yr_3['coach'] == 'Scott Frost']['cum_GP'])

# Subset the data to coaches have coached at least the same number of games as Scott
df_yr_3 = df_yr_3[df_yr_3['cum_GP'] >= sf_gp]

# Save coaches with 3 or more years of tenure to disk
ts = datetime.date.fromtimestamp(time.time())
df_yr_3.to_csv(rf'data\raw\Coaches\coaching_history_year_3_{ts}.csv', index = False)

# Subset the data to coaches with a winning percentage the same as or worse than Scott
df_bad = df_yr_3[df_yr_3['cum_win_pct'] < sf_win_pct]

# Save coaches who are as bad as Scott (or worse) to disk
ts = datetime.date.fromtimestamp(time.time())
df_bad.to_csv(rf'data\raw\Coaches\coaching_history_bad_{ts}.csv', index = False)

pd.DataFrame.mean(df_bad['total_win_pct'])
pd.DataFrame.mean(df_bad['total_seasons'])

#------------------------------------------------------------------------------
# Visualize Results
#------------------------------------------------------------------------------
import plotly.graph_objects as go
import plotly.express as px

# data
label = ['Coaching Tenures Since 1970','Year 3, 29+ Games Coached','Did Not Last',
         'Win % >= 40.6','Win % < 40.6', '.500 record or better', 'Worse than .500 record', 'Multiple 10 Top AP Seasons']
source = [0, 0 ,1, 1, 4, 4, 5]
target = [1, 2, 3, 4, 5, 6, 7]
value = [835, 362, 523, 312, 26, 286, 6]
# data to dict, dict to sankey
link = dict(source = source, target = target, value = value)
node = dict(label = label, pad=50, thickness=5)
data = go.Sankey(link = link, node=node)
# plot
fig = go.Figure(data)
fig.show()