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
import numpy as np
import pandas as pd
import pathlib
import time
import tqdm

from src.data.scrape_sports_reference import *

#==============================================================================
# Reference Variable Declaration
#==============================================================================

#==============================================================================
# Function Definitions
#==============================================================================
def renameSchool(df, name_var):
<<<<<<< HEAD
=======
    '''
    Purpose: Rename a school/university to a standard name as specified in 
        the file `school_abbreviations.csv`

    Inputs
    ------
        df : Pandas Dataframe
            DataFrame containing a school-name variable for which the names
            need to be standardized
        name_var : string
            Name of the variable which is to be renamed/standardized
    
    Outputs
    -------
        list(row)[0] : string
            Standardized version of the school's name based on the first value
            in the row in the file `school_abbreviations.csv`
    '''  
    # read in school name information
    df_school_names = pd.read_csv(r'references\names_pictures_ncaa.csv')
     
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
            
    # df[name_var] = df[name_var].apply(
    #         lambda x: dict_school_names[x] if str(x) != 'nan' else '')
    df[name_var] = df[name_var].apply(
            lambda x: rename_school_helper(x, dict_school_names))
        
    return df   

def rename_school_helper(name_school, dict_school_names):
    try:
        if str(name_school) != 'nan':
            return dict_school_names[name_school]
        else:
            return ''
    except:
        print(f'School not found in school abbreviations .csv file: {name_school} ')
        return name_school
    
def create_coach_dataframe(df_schools):
>>>>>>> 55366a4305b3f99adab491b38426258b0a28e62f
    '''
    Purpose: Rename a school/university to a standard name as specified in 
        the file `school_abbreviations.csv`

    Inputs
    ------
        df : Pandas Dataframe
            DataFrame containing a school-name variable for which the names
            need to be standardized
        name_var : string
            Name of the variable which is to be renamed/standardized
    
    Outputs
    -------
        list(row)[0] : string
            Standardized version of the school's name based on the first value
            in the row in the file `school_abbreviations.csv`
    '''  
    # read in school name information
    df_school_names = pd.read_csv(r'references\names_pictures_ncaa.csv')
     
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
            
    # df[name_var] = df[name_var].apply(
    #         lambda x: dict_school_names[x] if str(x) != 'nan' else '')
    df[name_var] = df[name_var].apply(
            lambda x: rename_school_helper(x, dict_school_names))
        
    return df   

def rename_school_helper(name_school, dict_school_names):
    try:
        if str(name_school) != 'nan':
            return dict_school_names[name_school]
        else:
            return ''
    except:
        print(f'School not found in school abbreviations .csv file: {name_school} ')
        return name_school
    
# def create_coach_dataframe(df_schools):
#     '''
#     Purpose: Given historic school data, create a dataframe of coaches and
#         their performance data on a year-by-year basis

#     Inputs   
#     ------
#         df_schools : Pandas DataFrame
#             Contains year-by-year results for each school (with coaches' names)
            
#     Outputs
#     -------
#         df_coaches : Pandas DataFrame
#             A dataframe containing all historic season data from a coaching perspective
#     '''
#     # Create a dictionary that assigns each school to its current conference
#     df_conf = df_schools.groupby(['School', 'Conf']).head(1).groupby('School').head(1).reset_index(drop = True)
#     df_conf = df_conf[['School', 'Conf']]
#     df_conf['Power5'] = df_conf.apply(lambda row: True if row['Conf'] in [
#         'SEC', 'Pac-12', 'Big 12', 'ACC', 'Big Ten'] else False, axis = 1)
#     df_conf = df_conf.set_index('School')
#     dict_conf = df_conf.to_dict(orient = 'index')
    
#     # Create a coaching dataframe by iterating over every year for every school
#     list_coaches = []
#     for index, row in df_schools.iterrows():
#         # handle every coach that coached that season
#         for coach in row['Coach(es)'].split(', '):
#             dict_coach_year = {}
#             dict_coach_year['coach'] = coach.split(' (')[0].strip()
#             dict_coach_year['year'] = row['Year']
#             dict_coach_year['school'] = row['School']
#             dict_coach_year['ranking_pre'] = row['AP_Pre']
#             dict_coach_year['ranking_high'] = row['AP_High']
#             dict_coach_year['ranking_post'] = row['AP_Post']
#             dict_coach_year['ranked_pre'] = not pd.isna(row['AP_Pre'])
#             dict_coach_year['ranked_post'] = not pd.isna(row['AP_Post'])
#             try:
#                 dict_coach_year['ranked_top_10'] = row['AP_Post'] <= 10
#             except:
#                 print(row['AP_Post'])                    
#             dict_coach_year['ranked_top_5'] = row['AP_Post'] <= 5
#             # handle bowl games
#             if pd.isna(row['Bowl']):
#                 dict_coach_year['bowl'] = False
#                 dict_coach_year['bowl_name'] = ''
#                 dict_coach_year['bowl_win'] = False
#             else:
#                 dict_coach_year['bowl'] = True
#                 dict_coach_year['bowl_name'] = row['Bowl'].split('-')[0]
#                 if '-' in str(row['Bowl']):
#                     try:
#                         if row['Bowl'].split('-')[1] == 'W':
#                             dict_coach_year['bowl_win'] = True       
#                     except:
#                         print(row['Bowl'])
#             # handle wins and losses
#             if len(coach.split('(')[1].split('-')) > 2:
#                 dict_coach_year['W'] = coach.split('(')[1].split('-')[0]
#                 dict_coach_year['L'] = coach.split('(')[1].split('-')[1].strip(')')
#                 dict_coach_year['T'] = coach.split('(')[1].split('-')[2].strip(')')
#             else:
#                 dict_coach_year['W'] = coach.split('(')[1].split('-')[0]
#                 dict_coach_year['L'] = coach.split('(')[1].split('-')[1].strip(')')
#             # assign conference information
#             dict_coach_year['conf'] = dict_conf[row['School']]['Conf']
#             dict_coach_year['power5'] = dict_conf[row['School']]['Power5']
#             list_coaches.append(dict_coach_year)
            
#     # Convert list to DataFrame
#     df_coaches = pd.DataFrame(list_coaches)
    
#     # Convert all Tie Nans to 0
#     df_coaches['T'] = df_coaches['T'].fillna(0)
    
#     # Identify all unique coaches in the dataframe
#     list_coaches = list(df_coaches['coach'].unique())
    
#     # Cast Win and Loss columns to ints
#     df_coaches['W'] = df_coaches['W'].astype('int')
#     df_coaches['L'] = df_coaches['L'].astype('int')
#     df_coaches['T'] = df_coaches['T'].astype('int')
    
#     # Add a column for games coached in the season
#     df_coaches['GP'] = df_coaches.apply(lambda row: row['W'] + row['L'] + row['T'], axis = 1)
    
#     return df_coaches

# def add_coach_metadata(df_stint):
#     '''
#     Purpose: Iterate over a coach's historic data and tabulate totals on a 
#         year-by-year basis

#     Inputs   
#     ------
#         df_stint : Pandas DataFrame
#             Contains year-by-year results for a coach
#             ** Note: This is continuous years only. Breaks in coaching stints
#                         are treated as separate coaching histories **
            
#     Outputs
#     -------
#         df_coach : Pandas DataFrame
#             Coaching data with updated year-by-year totals
#     '''
#     df_coach = df_stint.copy()
#     #   1. Year # at school
#     df_coach['season'] = list(range(1,len(df_coach)+1))
    
#     #   2. Cumulative games coached at school (on a year-by-year basis)
#     df_coach['cum_GP'] = df_coach['GP'].cumsum(axis = 0)
    
#     #   3. Cumulative wins at school (on a year-by-year basis)
#     df_coach['cum_W'] = df_coach['W'].cumsum(axis = 0)
    
#     #   4. Cumulative losses at school (on a year-by-year basis)
#     df_coach['cum_L'] = df_coach['L'].cumsum(axis = 0)
    
#     #   5. Cumulative ties at school (on a year-by-year basis)
#     df_coach['cum_T'] = df_coach['T'].cumsum(axis = 0)
    
#     #   6. Cumulative Win Pct at school (on a year-by-year basis)
#     if len(df_coach) == 1:
#         if int(df_coach['cum_GP']) == 0:
#             df_coach['cum_win_pct'] = 0
#         else:
#             df_coach['cum_win_pct'] = df_coach.apply(lambda row: row['cum_W'] / row['cum_GP'] if row['cum_GP'] != 0 else 0, axis = 1)
#     else:
#         df_coach['cum_win_pct'] = df_coach.apply(lambda row: row['cum_W'] / row['cum_GP'] if row['cum_GP'] != 0 else 0, axis = 1)
    
#     #   7. Total bowl games at school
#     df_coach['total_bowl'] = df_coach['bowl'].sum(axis = 0)
    
#     #   8. Total bowl wins at school
#     df_coach['total_bowl_win'] = df_coach['bowl_win'].sum(axis = 0)
    
#     #   9. Total AP Preseason rankings
#     df_coach['total_ranked_pre'] = df_coach['ranked_pre'].sum(axis = 0)
    
#     #   10. Total AP Postseason rankings
#     df_coach['total_ranked_post'] = df_coach['ranked_post'].sum(axis = 0)
    
#     #   11. Total Top 10 finishes
#     df_coach['total_top_10'] = df_coach['ranked_top_10'].sum(axis = 0)
    
#     #   12. Total Top 5 finishes
#     df_coach['total_top_5'] = df_coach['ranked_top_5'].sum(axis = 0)
    
#     #   13. Total Seasons Coached at School
#     df_coach['total_seasons'] = df_coach.iloc[len(df_coach)-1]['season'] 
    
#     #   14. Total Games Coached at School
#     df_coach['total_games'] = df_coach.iloc[len(df_coach)-1]['cum_GP']
    
#     #   15. Total Wins at School
#     df_coach['total_wins'] = df_coach.iloc[len(df_coach)-1]['cum_W']
    
#     #   16. Total Losses at School
#     df_coach['total_losses'] = df_coach.iloc[len(df_coach)-1]['cum_L']
    
#     #   17. Total Win Pct at School
#     df_coach['total_win_pct'] = df_coach.iloc[len(df_coach)-1]['cum_win_pct']
    
#     return df_coach

# def calculate_year_by_year(df_coaches):
#     '''
#     Purpose: Given the data for coaches in a historical perspective, iterate
#         through their coaching stints and calculate year-by-year totals in an 
#         effor to understand their progress over time

#     Inputs   
#     ------
#         df_coaches : Pandas DataFrame
#             A dataframe containing all historic season data from a coaching perspective
            
#     Outputs
#     -------
#         df_yr_by_yr : Pandas DataFrame
#             Coaching data with updated year-by-year totals separated by stints
#                 at schools in each coach's career
#     '''
#     # make an empty dataframe for storing new coach info
#     df_yr_by_yr = pd.DataFrame()
    
#     # Coach-by-coach --> Year by year, determine the following:
#     gps = df_coaches.groupby(['coach', 'school'])
#     for combo, df_coach in tqdm.tqdm(gps):
#         # sort the dataframe by earliest year to latest
#         df_coach = df_coach.sort_values(by = 'year')
        
#         # look for gaps in years
#         num_stints = 1
#         list_stint_end = []
#         list_years = list(df_coach['year'])
#         for num_ele in list(range(0,len(list_years))):
#             if (num_ele == 0):
#                 pass
#             else:
#                 if list_years[num_ele] - list_years[num_ele-1] > 1:
#                     # print(f"Gap detected for coach: {df_coach.iloc[0]['coach']}")
#                     # print(f"  -- Gap between {list_years[num_ele]} and {list_years[num_ele-1]}")
#                     list_stint_end.append(list_years[num_ele-1])
#                     num_stints = num_stints + 1
                    
#         # handle coaches with multiple stints
#         if num_stints >= 2:
#             for stint_count in list(range(0,num_stints)):
#                 # split the coaches data into stints
#                 if stint_count == 0:
#                     year_stint_end = list_stint_end[stint_count]
#                     df_stint = df_coach[df_coach['year'] <= year_stint_end]
#                 elif stint_count < num_stints-1:
#                     year_stint_end = list_stint_end[stint_count]
#                     year_stint_end_prev = list_stint_end[stint_count-1]
#                     df_stint = df_coach[df_coach['year'] <= year_stint_end]
#                     df_stint = df_stint[df_stint['year'] > year_stint_end_prev]
#                 else:
#                     year_stint_end_prev = list_stint_end[stint_count-1]
#                     df_stint = df_coach[df_coach['year'] > year_stint_end_prev]
#                 # process the data on a year by year basis
#                 df_stint = add_coach_metadata(df_stint)
#                 # Add coach dataframe to overall dataframe
#                 if len(df_yr_by_yr) == 0:
#                     df_yr_by_yr = df_stint.copy()
#                 else:
#                     df_yr_by_yr = df_yr_by_yr.append(df_stint)            
#         else:
#             # process the data on a year by year basis
#             df_coach = add_coach_metadata(df_coach)
#             # Add coach dataframe to overall dataframe
#             if len(df_yr_by_yr) == 0:
#                 df_yr_by_yr = df_coach.copy()
#             else:
#                 df_yr_by_yr = df_yr_by_yr.append(df_coach)
            
#     # reset dataframe index
#     df_yr_by_yr = df_yr_by_yr.reset_index(drop = True)
    
#     return df_yr_by_yr

def create_week_by_week_dataframe(df_all_games, df_schools, games_sf):
    '''
    Purpose: Combine the week-by-week results for each school with the 
        end-of-year school/coach information to create a week-by-week 
        dataframe detailing who coached each team when. This will facilitate
        analysis of coaching tenures.

    Inputs   
    ------
        df_all_games : Pandas DataFrame
            Contains week-by-week results for each school
        df_schools : Pandas DataFrame
            Contains year-by-year results for each school (with coaches' names)
        games_sf : int
            Scott Frost's current number of games
            
    Outputs
    -------
        df_engineered : Pandas DataFrame
            A dataframe containing all historic week-by-week results infused
                with coaches' names
    '''           
    # standardize team names
    df_all_games = renameSchool(df_all_games, 'School')
    df_all_games = renameSchool(df_all_games, 'Opponent')
    df_schools   = renameSchool(df_schools, 'School')
    
    # merge data together
    df_coaches = pd.merge(df_all_games, 
                          df_schools[['School', 'Year', 'Conf', 'Conf_W', 'Conf_L', 
                                      'Conf_T', 'AP_Pre', 'AP_High', 'AP_Post', 
                                      'Coach(es)', 'Bowl']],
                          how = 'left',
                          on = ['School', 'Year'])
    
    # rename columns
    df_coaches = df_coaches.rename(columns = {'Conf_x':'Conf_Opp', 'Conf_y':'Conf'})
    
    # sort dataframe to ensure no issues with groupby
    df_coaches = df_coaches.sort_values(by = ['School', 'Year', 'G'])
    
    # Break out coaches on a week-by-week basis
    list_coaches = []
<<<<<<< HEAD
    table_coaches = pd.DataFrame(columns = ['School', 'Year', 'Coach', 'Games'])
    for school, grp in tqdm.tqdm(df_coaches.groupby(['School', 'Year'])):
        dict_coaches = {}
        # Handle Utah 2003
        if school[0] == 'Utah' and school[1] == 2004:
            dict_coaches['Urban Meyer'] = 12
        # Handle Utah St. 2021
        elif school[0] == 'Utah St.' and school[1] == 2021:
            coach_name = 'Blake Anderson'
            coach_games = grp['G'].count()
            dict_coaches[coach_name] = coach_games
        # Handle USC 2021
        elif school[0] == 'USC' and school[1] == 2021:
            dict_coaches['Clay Helton'] = 2
            dict_coaches['Donte Williams'] = len(grp) - 2
        # handle every coach that coached that season for that team
        else:
            # for every coach a team has, calculate how many games they coached that season
            for coach in grp['Coach(es)'].iloc[0].split(', '):
                coach_name = coach.split(' (')[0]
                coach_record = coach.split(' (')[1].replace(')','')
                # first attempt to account for ties in a coaches' record
                try:
                    coach_games = int(coach_record.split('-')[0]) + int(coach_record.split('-')[1]) + int(coach_record.split('-')[2])
                # otherwise assume they only have wins-losses in their record
                except:
                    coach_games = int(coach_record.split('-')[0]) + int(coach_record.split('-')[1])
                dict_coaches[coach_name] = coach_games
        # add coaches to master list
        num_games = 0
        for coach in dict_coaches.keys():
            list_coaches = list_coaches + ([coach] * dict_coaches[coach])
            table_coaches = table_coaches.append(pd.DataFrame(
                [[school[0], school[1], coach, dict_coaches[coach]]], 
                columns = ['School', 'Year', 'Coach', 'Games']))
            num_games = dict_coaches[coach] + num_games
        if num_games != len(grp):
            print('oops!')
            break
    df_coaches['Coach'] = list_coaches  
    
    # test for any values of "coach" that weren't in the original data
    for index, row in tqdm.tqdm(df_coaches.iterrows()):
        if not pd.isna(row['Coach(es)']):
            if row['Coach'] not in row['Coach(es)']:
                print(f"{row['Coach']} not found in {row['Coach(es)']}")
=======
    for index, row in df_schools.iterrows():
        # handle every coach that coached that season
        for coach in row['Coach(es)'].split(', '):
            dict_coach_year = {}
            dict_coach_year['coach'] = coach.split(' (')[0].strip()
            dict_coach_year['year'] = row['Year']
            dict_coach_year['school'] = row['School']
            dict_coach_year['ranking_pre'] = row['AP_Pre']
            dict_coach_year['ranking_high'] = row['AP_High']
            dict_coach_year['ranking_post'] = row['AP_Post']
            dict_coach_year['ranked_pre'] = not pd.isna(row['AP_Pre'])
            dict_coach_year['ranked_post'] = not pd.isna(row['AP_Post'])
            try:
                dict_coach_year['ranked_top_10'] = row['AP_Post'] <= 10
            except:
                print(row['AP_Post'])                    
            dict_coach_year['ranked_top_5'] = row['AP_Post'] <= 5
            # handle bowl games
            if pd.isna(row['Bowl']):
                dict_coach_year['bowl'] = False
                dict_coach_year['bowl_name'] = ''
                dict_coach_year['bowl_win'] = False
            else:
                dict_coach_year['bowl'] = True
                dict_coach_year['bowl_name'] = row['Bowl'].split('-')[0]
                if '-' in str(row['Bowl']):
                    try:
                        if row['Bowl'].split('-')[1] == 'W':
                            dict_coach_year['bowl_win'] = True       
                    except:
                        print(row['Bowl'])
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
>>>>>>> 55366a4305b3f99adab491b38426258b0a28e62f
    
    # add power5 status to dataframe
    df_school_info = pd.read_csv(r'references\names_pictures_ncaa.csv')
    df_school_info = df_school_info.rename(columns = {'Team':'School'})
    df_coaches = pd.merge(df_coaches, df_school_info[['School', 'Power5']], how = 'left', on = 'School')
    df_school_info = df_school_info.rename(columns = {'School':'Opponent', 'Power5':'Power5_Opp'})
    df_coaches = pd.merge(df_coaches, df_school_info[['Opponent', 'Power5_Opp']], how = 'left', on = 'Opponent')
    
    # rename columns    
    df_coaches = df_coaches.rename(columns = {'G':'Week',
                                              'Year':'Season',
                                              'Opp':'Pts_Opp',
                                              'Cum_W':'W_Sn',
                                              'Cum_L':'L_Sn',
                                              'T':'T_Sn'})
    
    # add opponent's record for the year to the table
    df_team_records = pd.merge(df_coaches[['Season', 'Opponent']], 
                               df_schools[['School', 'Year', 'Overall_Pct', 'Conf_Pct']],
                               left_on = ['Season', 'Opponent'],
                               right_on = ['Year', 'School'])
    df_team_records = df_team_records.drop_duplicates()
    df_team_records = df_team_records[['Season', 'School', 'Overall_Pct', 'Conf_Pct']]
    df_team_records = df_team_records.rename(columns = {'Overall_Pct':'Win_Pct_Opp',
                                                        'Conf_Pct':'Win_Pct_Conf_Opp',
                                                        'School':'Opponent'})
    df_coaches = pd.merge(df_coaches, df_team_records, how = 'left', on = ['Season', 'Opponent'])
    
    # add flag if opponent's overall record was > .500
    df_coaches['Opp_Winning_Record'] = list(df_coaches.apply(
        lambda row: True if row['Win_Pct_Opp'] > .5 else False, axis = 1))
    
    # add flag if opponent's conference record was > .500
    df_coaches['Opp_Conf_Winning_Record'] = list(df_coaches.apply(
        lambda row: True if row['Win_Pct_Conf_Opp'] > .5 else False, axis = 1))
    
    # reorder columns
    df_coaches = df_coaches[['Season', 'Week', 'Date', 'Day', 'Rank', 'School', 
                             'Coach', 'Conf', 'Power5', 'Home_Away', 'Rank_Opp', 'Opponent', 
                             'Conf_Opp', 'Power5_Opp', 'Win_Pct_Opp', 'Opp_Winning_Record',
                             'Win_Pct_Conf_Opp', 'Opp_Conf_Winning_Record', 
                             'Result', 'Pts', 'Pts_Opp', 'W_Sn', 
                             'L_Sn', 'T_Sn', 'Streak', 'AP_Pre', 'AP_High', 'AP_Post', 
                             'Notes', 'Bowl', 'url_boxscore']]
    
    # df_coaches.to_csv(rf'data\processed\Coaches\backup.csv', index = False)
    # df_tenure = df_coaches[(df_coaches['School']=='Charlotte') & (df_coaches['Coach']=='Brad Lambert')]
    
    # Engineer variables for each coach's stint/tenure at a given school=
    df_engineered = pd.DataFrame()
    idx_tenure = 0
    for index, grp in tqdm.tqdm(df_coaches.groupby(['School', 'Coach'])):
        pass
        # Ignore any coaching tenures of 3 games or less
        if len(grp) <= 3:
            continue
        
        if len(df_engineered) == 0:
            [df_engineered, idx_tenure] = add_tenure_features(grp, games_sf, idx_tenure)
        else:
            [df_new, idx_tenure] = add_tenure_features(grp, games_sf, idx_tenure)
            df_engineered = df_engineered.append(df_new)
        
    return df_engineered

def add_tenure_features(df_coach, games_sf, idx_tenure):
    '''
    Purpose: Manage the engineering of features across a coach's tenure at a
        a given school (while also accounting for those coaches who have 
        multiple coaching stints/tenures at the same school)

    Inputs   
    ------
        df_coach : Pandas DataFrame
            Contains data for all seasons a coach has coached at a given school
        games_sf : int
            Scott Frost's current number of games
        idx_tenure : int
            Running counter that serves as a unique index/identifier for each tenure
            - Allows deconfliction of same coach with multiple stops at same school
            
    Outputs
    -------
        df_coach_eng : Pandas DataFrame
            Contains input data with newly engineered features that span the
                whole coaching tenure, not just seasons
    '''  
    # Step 1. Identify if the coach's dataframe has multiple stints 
    #   (i.e. gaps in years between tenures at the same school)
    num_stints = 1
    list_stint_end = []
    list_years = list(df_coach['Season'])
    for num_ele in list(range(0,len(list_years))):
        if (num_ele == 0):
            pass
        else:
            if list_years[num_ele] - list_years[num_ele-1] > 1:
                # print(f"Gap detected for coach: {df_coach.iloc[0]['coach']}")
                # print(f"  -- Gap between {list_years[num_ele]} and {list_years[num_ele-1]}")
                list_stint_end.append(list_years[num_ele-1])
                num_stints = num_stints + 1
                
    # Step 2.A. Handle coaches with multiple stints (i.e. gaps in years)
    if num_stints >= 2:
        df_coach_eng = pd.DataFrame()
        for stint_count in list(range(0,num_stints)):
            # handle the first coaching stint
            if stint_count == 0:
                year_stint_end = list_stint_end[stint_count]
                df_stint = df_coach[df_coach['Season'] <= year_stint_end].copy()
            # handle coaching stints 2 through num_stints - 1
            elif stint_count < num_stints-1:
                year_stint_end = list_stint_end[stint_count]
                year_stint_end_prev = list_stint_end[stint_count-1]
                df_stint = df_coach[df_coach['Season'] <= year_stint_end].copy()
                df_stint = df_stint[df_stint['Season'] > year_stint_end_prev].copy()
            # handle the last coaching stint
            else:
                year_stint_end_prev = list_stint_end[stint_count-1]
                df_stint = df_coach[df_coach['Season'] > year_stint_end_prev].copy()
                
            # skip any tenures less than 4 games
            if len(df_stint) >= 4:
                # assign and increment identifier/counter
                df_stint['Tenure_Index'] = idx_tenure
                idx_tenure = idx_tenure + 1
                # engineer new features and add to coach's tenure dataframe
                if len(df_coach_eng) == 0:
                    df_coach_eng = engineer_stint_features(df_stint, games_sf)
                else:
                    df_coach_eng = df_coach_eng.append(engineer_stint_features(df_stint, games_sf))
            else:
                continue
            # print(f"Coach: {df_stint['Coach'].iloc[0]}, Games: {len(df_stint)}")
    # Step 2.B. Handle coaches with only a single stint at the respective school
    else:
        df_coach['Tenure_Index'] = idx_tenure
        idx_tenure = idx_tenure + 1
        df_coach_eng = engineer_stint_features(df_coach, games_sf)
        
    return [df_coach_eng, idx_tenure]
        
def engineer_stint_features(df_tenure, games_sf):
    '''
    Purpose: Engineer features across a coach's tenure at a given school 

    Inputs   
    ------
        df_tenure : Pandas DataFrame
            Contains data for all seasons in a tenure for a given coach/school combo
        games_sf : int
            Scott Frost's current number of games
            
    Outputs
    -------
        df_tenure : Pandas DataFrame
            Contains input data with newly engineered features 
    '''     
    # df_tenure = df_coaches[(df_coaches['School'] == 'Nebraska') & (df_coaches['Coach'] == 'Scott Frost')].copy()
    # df_tenure = df_coaches[(df_coaches['School'] == 'Nebraska') & (df_coaches['Coach'] == 'Mike Riley')].copy()
    # df_tenure = df_coaches[(df_coaches['School'] == 'Nebraska') & (df_coaches['Coach'] == 'Tom Osborne')].copy()
    
    # remove any seasons where the coach coached 3 games or less
    df_tenure_clean = pd.DataFrame()
    for index, grp in df_tenure.groupby('Season'):
        if len(grp) >= 4:
            if len(df_tenure_clean) == 0:
                df_tenure_clean = grp.copy()
            else:
                df_tenure_clean = df_tenure_clean.append(grp.copy())
    df_tenure = df_tenure_clean.copy()
    
    # Fill NaNs with 0s for 'T_Sn'
    df_tenure['T_Sn'] = df_tenure['T_Sn'].fillna(0)
    
    # 0. Total seasons
    row_counts = list(df_tenure.Season.value_counts(sort = False))
    list_seasons = []
    for idx in range(0,len(row_counts)):
        list_seasons = list_seasons + ([idx+1] * row_counts[idx])
    df_tenure['Sn'] = list_seasons
    
    # 1. Total games
    df_tenure['G'] = list(range(1,len(df_tenure)+1))

    # 2. Total wins
    df_tenure['W'] = df_tenure.Result.eq('W').cumsum()
    
<<<<<<< HEAD
    # 3. Total losses
    df_tenure['L'] = df_tenure.Result.eq('L').cumsum()
    
    # 4. Total ties
    df_tenure['T'] = df_tenure.Result.eq('T').cumsum()
    df_tenure['T'] = df_tenure['T'].fillna(0)
    
    # 5. Win Pct.
    if (len(df_tenure) == 1) and (int(df_tenure['G']) == 0):
            df_tenure['Win_Pct'] = 0
    else:
        df_tenure['Win_Pct'] = df_tenure.apply(
            lambda row: (row['W'] + (row['T']*0.5)) / row['G'] 
            if row['G'] != 0 else 0, axis = 1)
    
    # 6. Create conference win/loss flag
    list_conf_flag = []
    for index, row in df_tenure.iterrows():
         if (row['Result'] == 'W') and (row['Conf'] == row['Conf_Opp']):
             list_conf_flag.append('W')
         elif (row['Result'] == 'L') and (row['Conf'] == row['Conf_Opp']):
             list_conf_flag.append('L') 
         elif (row['Result'] == 'T') and (row['Conf'] == row['Conf_Opp']):
             list_conf_flag.append('T') 
         else:
             list_conf_flag.append('')
    df_tenure['Result_Conf'] = list_conf_flag
    
    # 7. Total conference games
    df_tenure['G_Conf'] = df_tenure.Result_Conf.ne('').cumsum()
             
    # 8. Total conference wins
    df_tenure['W_Conf'] = df_tenure.Result_Conf.eq('W').cumsum()
    
    # 9. Total conference losses
    df_tenure['L_Conf'] = df_tenure.Result_Conf.eq('L').cumsum()
    
    # 10. Total conference ties
    df_tenure['T_Conf'] = df_tenure.Result_Conf.eq('T').cumsum()
    
    # 11. Conference Win Pct.
    df_tenure['Win_Pct_Conf'] = df_tenure.apply(
        lambda row: (row['W_Conf'] + (row['T_Conf']*0.5)) / row['G_Conf'] 
        if row['G_Conf'] != 0 else 0, axis = 1)
    # if (len(df_tenure) == 1) and (int(df_tenure['G_Conf']) == 0):
    #         df_tenure['Win_Pct_Conf'] = 0
    # else:
    #     df_tenure['Win_Pct_Conf'] = df_tenure.apply(lambda row: row['W_Conf'] / row['G_Conf'] 
    #                                            if row['G_Conf'] != 0 else 0, axis = 1)
     
    # 12. Create top 25 opponent win/loss flag
    list_top25_results = []
    for index, row in df_tenure.iterrows():
        if (row['Result'] == 'W') and (~np.isnan(row['Rank_Opp'])):
            list_top25_results.append('W')
        elif (row['Result'] == 'L') and (~np.isnan(row['Rank_Opp'])):
            list_top25_results.append('L')
        elif (row['Result'] == 'T') and (~np.isnan(row['Rank_Opp'])):
            list_top25_results.append('T')
        else:
            list_top25_results.append('')
    df_tenure['Result_Top25_Opp'] = list_top25_results
=======
    #   6. Cumulative Win Pct at school (on a year-by-year basis)
    if len(df_coach) == 1:
        if int(df_coach['cum_GP']) == 0:
            df_coach['cum_win_pct'] = 0
        else:
            df_coach['cum_win_pct'] = df_coach.apply(lambda row: row['cum_W'] / row['cum_GP'] if row['cum_GP'] != 0 else 0, axis = 1)
    else:
        df_coach['cum_win_pct'] = df_coach.apply(lambda row: row['cum_W'] / row['cum_GP'] if row['cum_GP'] != 0 else 0, axis = 1)
>>>>>>> 55366a4305b3f99adab491b38426258b0a28e62f
    
    # 13. Games vs AP Top-25
    df_tenure['G_vs_Rank'] = df_tenure.Result_Top25_Opp.ne('').cumsum()
    
    # 14. Wins vs. AP Top-25
    df_tenure['W_vs_Rank'] = df_tenure.Result_Top25_Opp.eq('W').cumsum()
    
    # 15. Losses vs. AP Top-25
    df_tenure['L_vs_Rank'] = df_tenure.Result_Top25_Opp.eq('L').cumsum()
    
    # 16. Ties vs AP Top-25
    df_tenure['T_vs_Rank'] = df_tenure.Result_Top25_Opp.eq('T').cumsum()
    
    # 17. Win Pct. vs AP Top-25
    df_tenure['Win_Pct_vs_Rank'] = df_tenure.apply(
        lambda row: (row['W_vs_Rank'] + (row['T_vs_Rank'])*0.5) / row['G_vs_Rank']
        if row['G_vs_Rank'] != 0 else 0, axis = 1)
        
    # 18. Total bowl games
    list_bowl_games = list(df_tenure.groupby('Season').tail(1).Bowl)
    list_bowl_games = [0 if pd.isna(x) else 1 for x in list_bowl_games]
    list_bowl_games = list(pd.Series(list_bowl_games).cumsum())
    list_bowl_sn_cnt = []
    for idx in range(0,len(row_counts)):
        list_bowl_sn_cnt = list_bowl_sn_cnt + ([list_bowl_games[idx]] * row_counts[idx])
    df_tenure['Bowl_G'] = list_bowl_sn_cnt
    
    # 19. Create bowl win/loss flag
    list_bowl_results = []
    for index, row in df_tenure.iterrows():
        if (row['Result'] == 'W') and ('Bowl' in str(row['Notes'])):
            list_bowl_results.append('W')
        elif (row['Result'] == 'L') and ('Bowl' in str(row['Notes'])):
            list_bowl_results.append('L')
        elif (row['Result'] == 'T') and ('Bowl' in str(row['Notes'])):
            list_bowl_results.append('T')
        else:
            list_bowl_results.append('')
    df_tenure['Result_Bowl'] = list_bowl_results
    
    # 20. Bowl Wins
    df_tenure['Bowl_W'] = df_tenure.Result_Bowl.eq('W').cumsum()
    
    # 21. Bowl Losses
    df_tenure['Bowl_L'] = df_tenure.Result_Bowl.eq('L').cumsum()
    
    # 22. Bowl Ties
    df_tenure['Bowl_T'] = df_tenure.Result_Bowl.eq('T').cumsum()
    
    # 23. Bowl Win Pct.
    df_tenure['Win_Pct_Bowl'] = df_tenure.apply(
        lambda row: (row['Bowl_W'] + (row['Bowl_T']*0.5))/ row['Bowl_G'] 
        if row['Bowl_G'] != 0 else 0, axis = 1)
    
    # 24. Calculate # of seasons with pre-post season AP Top 25 rankings
    list_AP_Pre_counts     = []
    list_AP_Post_25_counts = []
    list_AP_Post_10_counts = []
    list_AP_Post_5_counts  = []
    list_game_counts = []
    for season, grp in df_tenure.groupby('Season'):
        list_AP_Pre_counts     = list_AP_Pre_counts + [1 if ~np.isnan(grp.AP_Pre.iloc[0]) else 0]
        list_AP_Post_25_counts = list_AP_Post_25_counts + [1 if grp.AP_Post.iloc[0] <= 25 else 0]
        list_AP_Post_10_counts = list_AP_Post_10_counts + [1 if grp.AP_Post.iloc[0] <= 10 else 0]
        list_AP_Post_5_counts  = list_AP_Post_5_counts  + [1 if grp.AP_Post.iloc[0] <= 5  else 0]
        list_game_counts = list_game_counts + [len(grp)]
    series_AP_Pre_counts     = pd.Series(list_AP_Pre_counts).cumsum()
    series_AP_Post_25_counts = pd.Series(list_AP_Post_25_counts).cumsum()
    series_AP_Post_10_counts = pd.Series(list_AP_Post_10_counts).cumsum()
    series_AP_Post_5_counts  = pd.Series(list_AP_Post_5_counts).cumsum()
        
    # 25. Total Years in AP Top-25 (Preaseason)   
    df_tenure['AP_Pre_count'] = sum([[x]*y for x,y in zip(series_AP_Pre_counts, list_game_counts)], [])
    
    # 26. Total Years in AP Top-25 (Postseason)
    df_tenure['AP_Post_25_count'] = sum([[x]*y for x,y in zip(series_AP_Post_25_counts, list_game_counts)], [])
    
    # 27. Total Years in AP Top-10 (Postseason)
    df_tenure['AP_Post_10_count'] = sum([[x]*y for x,y in zip(series_AP_Post_10_counts, list_game_counts)], [])
    
    # 28. Total Years in AP Top-5 (Postseason)
    df_tenure['AP_Post_5_count'] = sum([[x]*y for x,y in zip(series_AP_Post_5_counts, list_game_counts)], [])
    
    # 29. Total Weeks in AP Top-25
    df_tenure['Weeks_Ranked'] = list(pd.Series([1 if ~np.isnan(x) else 0 for x in df_tenure.Rank]).cumsum())
    
    # 30. Weeks Ranked in AP Top-25 Pct.
    df_tenure['Weeks_Ranked_Pct.'] = df_tenure.apply(lambda row: row['Weeks_Ranked'] / row['G'], axis = 1)

    # 31. Season Conference Wins
    list_conf_wins = []
    for season, grp in df_tenure.groupby(['Season']):
        list_conf_wins = list_conf_wins + list(grp.Result_Conf.eq('W').cumsum())
    df_tenure['W_Sn_Conf'] = list_conf_wins
    
    # 32. Season Conference Losses
    list_conf_losses = []
    for season, grp in df_tenure.groupby(['Season']):
        list_conf_losses = list_conf_losses + list(grp.Result_Conf.eq('L').cumsum())
    df_tenure['L_Sn_Conf'] = list_conf_losses
    
    # 33. Season Conference Ties
    list_conf_ties = []
    for season, grp in df_tenure.groupby(['Season']):
        list_conf_ties = list_conf_ties + list(grp.Result_Conf.eq('T').cumsum())
    df_tenure['T_Sn_Conf'] = list_conf_ties
    
    # 34. Season Conference Games
    list_conf_games = []
    for season, grp in df_tenure.groupby(['Season']):
        list_conf_games = list_conf_games + list(grp.Result_Conf.ne('').cumsum())
    df_tenure['G_Sn_Conf'] = list_conf_games
    
    # 35. Season Win Pct. (Ties count as 0.5 wins and 0.5 losses)
    df_tenure['Win_Pct_Sn'] = df_tenure.apply(
        lambda row: (row['W_Sn'] + (row['T_Sn']*0.5)) / (
            row['W_Sn'] + row['L_Sn'] + row['T_Sn']), axis = 1)
    
    # 36. Season Conference Win Pct. (Ties count as 0.5 wins and 0.5 losses)
    df_tenure['Win_Pct_Sn_Conf'] = df_tenure.apply(
        lambda row: (row['W_Sn_Conf'] + (row['T_Sn_Conf']*0.5)) / row['G_Sn_Conf'] 
        if row['G_Sn_Conf'] != 0 else 0, axis = 1)
    
    # 37. Winning Seasons
    list_final_win_pct = list(df_tenure.groupby('Season').tail(1).Win_Pct_Sn)
    list_winning_seasons = [1 if x > .5 else 0 for x in list_final_win_pct]
    list_winning_seasons = list(pd.Series(list_winning_seasons).cumsum())
    list_win_sn_cnt = []
    for idx in range(0,len(row_counts)):
        list_win_sn_cnt = list_win_sn_cnt + ([list_winning_seasons[idx]] * row_counts[idx])
    df_tenure['Winning_Sns'] = list_win_sn_cnt
    
    # 38. Create a flag for win/loss vs Power 5 teams
    list_p5_results = []
    for index, row in df_tenure.iterrows():
        if (row['Result'] == 'W') and (row['Power5_Opp'] == True):
            list_p5_results.append('W')
        elif (row['Result'] == 'L') and (row['Power5_Opp'] == True):
            list_p5_results.append('L')
        elif (row['Result'] == 'T') and (row['Power5_Opp'] == True):
            list_p5_results.append('T')
        else:
            list_p5_results.append('')
    df_tenure['Results_P5'] = list_p5_results
    
    # 39. Games vs. Power 5 teams
    df_tenure['G_P5'] = df_tenure.Results_P5.ne('').cumsum()
    
    # 40. Wins vs. Power 5 teams
    df_tenure['W_P5'] = df_tenure.Results_P5.eq('W').cumsum()
    
    # 41. Losses vs. Power 5 teams
    df_tenure['L_P5'] = df_tenure.Results_P5.eq('L').cumsum()
    
    # 42. Ties vs. Power 5 teams
    df_tenure['T_P5'] = df_tenure.Results_P5.eq('T').cumsum()
    
    # 43. Win Pct. vs Power 5 teams
    df_tenure['Win_Pct_P5'] = df_tenure.apply(
        lambda row: (row['W_P5'] + (row['T_P5']*0.5)) / row['G_P5'] 
        if row['G_P5'] != 0 else 0, axis = 1)
    
    # 44. Create a flag for win/loss vs. teams with > .500 records
    list_winning_results = []
    for index, row in df_tenure.iterrows():
        if (row['Result'] == 'W') and (row['Opp_Winning_Record'] == True):
            list_winning_results.append('W')
        elif (row['Result'] == 'L') and (row['Opp_Winning_Record'] == True):
            list_winning_results.append('L')
        elif (row['Result'] == 'T') and (row['Opp_Winning_Record'] == True):
            list_winning_results.append('T')
        else:
            list_winning_results.append('')
    df_tenure['Results_vs_Winning'] = list_winning_results
    
    # 45. Games vs. teams with winning (> .500) records
    df_tenure['G_vs_Winning'] = df_tenure.Results_vs_Winning.ne('').cumsum()
    
    # 46. Wins vs. teams with winning (> .500) records
    df_tenure['W_vs_Winning'] = df_tenure.Results_vs_Winning.eq('W').cumsum()
    
    # 47. Losses vs. teams with winning (> .500) records
    df_tenure['L_vs_Winning'] = df_tenure.Results_vs_Winning.eq('L').cumsum()
    
    # 48. Ties vs. teams with winning (> .500) records
    df_tenure['T_vs_Winning'] = df_tenure.Results_vs_Winning.eq('T').cumsum()
    
    # 49. Win Pct. vs. teams with winning (> .500 ) records
    df_tenure['Win_Pct_vs_Winning'] = df_tenure.apply(
        lambda row: (row['W_vs_Winning'] + (row['T_vs_Winning']*0.5)) / row['G_vs_Winning'] 
        if row['G_vs_Winning'] != 0 else 0, axis = 1)
    
    # 50. Create a flag for win/loss vs. teams with > .500 records in conference
    list_winning_results_conf = []
    for index, row in df_tenure.iterrows():
        if ((row['Result'] == 'W') and (
                row['Opp_Conf_Winning_Record'] == True)) and (
                    row['Conf'] == row['Conf_Opp']):
                        list_winning_results_conf.append('W')
        elif ((row['Result'] == 'L') and (
                row['Opp_Conf_Winning_Record'] == True)) and (
                    row['Conf'] == row['Conf_Opp']):
                        list_winning_results_conf.append('L')
        elif ((row['Result'] == 'T') and (
                row['Opp_Conf_Winning_Record'] == True)) and (
                    row['Conf'] == row['Conf_Opp']):
                        list_winning_results_conf.append('T')
        else:
            list_winning_results_conf.append('')
    df_tenure['Results_vs_Winning_Conf'] = list_winning_results_conf
    
    # 51. Games vs. teams with winning (> .500) records in conference
    df_tenure['G_vs_Winning_Conf'] = df_tenure.Results_vs_Winning_Conf.ne('').cumsum()
    
    # 52. Wins vs. teams with winning (> .500) records in conference
    df_tenure['W_vs_Winning_Conf'] = df_tenure.Results_vs_Winning_Conf.eq('W').cumsum()
    
    # 53. Losses vs. teams with winning (> .500) records in conference
    df_tenure['L_vs_Winning_Conf'] = df_tenure.Results_vs_Winning_Conf.eq('L').cumsum()
    
    # 54. Ties vs. teams with winning (> .500) records in conference
    df_tenure['T_vs_Winning_Conf'] = df_tenure.Results_vs_Winning_Conf.eq('T').cumsum()
    
    # 55. Win Pct. vs. teams with winning (> .500) records in conference
    df_tenure['Win_Pct_vs_Winning_Conf'] = df_tenure.apply(
        lambda row: (row['W_vs_Winning_Conf'] + (row['T_vs_Winning_Conf']*0.5))/ row['G_vs_Winning_Conf'] 
        if row['G_vs_Winning_Conf'] != 0 else 0, axis = 1)
    
    # test = df_tenure[['Season', 'Week', 'Opponent', 'Win_Pct_Opp', 'Opp_Winning_Record', 'Results_vs_Winning', 'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 'Win_Pct_vs_Winning']]
    # test = df_tenure[['Season', 'Week', 'Opponent', 'Win_Pct_Conf_Opp', 'Opp_Conf_Winning_Record', 
    #                   'Results_vs_Winning_Conf', 'G_vs_Winning_Conf', 
    #                   'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf']]
    
    # 56. Calculate the coach's winning pct at the same number of games as SF's current total
    if len(df_tenure) >= games_sf:
        df_tenure['Win_Pct_at_SF'] = [float(df_tenure[df_tenure['G'] == games_sf]['Win_Pct'])] * len(df_tenure)
    else:
        df_tenure['Win_Pct_at_SF'] = [np.nan] * len(df_tenure)
        
    # 57. Create 'G_Sn' column
    df_tenure['G_Sn'] = list(df_tenure['Week'])
    
    # 58. Reorder columns
    df_tenure = df_tenure[['Season', 'Week', 'Sn', 'Date', 'Day', 'Rank', 'School',
                            'Coach', 'Conf', 'Power5', 'Home_Away', 'Rank_Opp',
                            'Opponent', 'Conf_Opp', 'Power5_Opp', 'Result', 'Pts', 'Pts_Opp', 
                            'Winning_Sns', 'G', 'W', 'L', 'T', 'Streak', 'Win_Pct', 
                            'G_Conf', 'W_Conf', 'L_Conf', 'T_Conf', 'Win_Pct_Conf',
                            'G_P5', 'W_P5', 'L_P5', 'T_P5', 'Win_Pct_P5',
                            'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 'T_vs_Winning', 'Win_Pct_vs_Winning',
                            'G_vs_Winning_Conf', 'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 'T_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf',
                            'G_vs_Rank', 'W_vs_Rank', 'L_vs_Rank', 'T_vs_Rank', 'Win_Pct_vs_Rank', 
                            'G_Sn', 'W_Sn', 'L_Sn', 'T_Sn', 'Win_Pct_Sn', 
                            'G_Sn_Conf', 'W_Sn_Conf', 'L_Sn_Conf', 'T_Sn_Conf', 'Win_Pct_Sn_Conf', 
                            'Bowl_G', 'Bowl_W', 'Bowl_L', 'Bowl_T', 'Win_Pct_Bowl', 
                            'AP_Pre', 'AP_High', 'AP_Post', 
                            'AP_Pre_count', 'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count',
                            'Weeks_Ranked', 'Weeks_Ranked_Pct.',
                            'Win_Pct_at_SF', 'Tenure_Index',
                            'Notes', 'url_boxscore']]
    
    return df_tenure

def extract_all_tenures(df_coach):
    '''
    Purpose: Look through a coach's dataframe and detect/extract multiple 
        tenures for the same coach at the same school

    Inputs   
    ------
        df_coach : Pandas DataFrame
            Contains data for all seasons a coach has coached at a given school
            
    Outputs
    -------
        list_tenures : list of Pandas DataFrames
            Contains all dataframes for a given coach where each dataframe
            represents a seperate tenure for a coach at the same school
    '''  
    # Step 1. Identify if the coach's dataframe has multiple stints 
    #   (i.e. gaps in years between tenures at the same school)
    num_stints = 1
    list_stint_end = []
    list_years = list(df_coach['Season'])
    for num_ele in list(range(0,len(list_years))):
        if (num_ele == 0):
            pass
        else:
            if list_years[num_ele] - list_years[num_ele-1] > 1:
                # print(f"Gap detected for coach: {df_coach.iloc[0]['coach']}")
                # print(f"  -- Gap between {list_years[num_ele]} and {list_years[num_ele-1]}")
                list_stint_end.append(list_years[num_ele-1])
                num_stints = num_stints + 1
                
    # Step 2.A. Handle coaches with multiple stints (i.e. gaps in years)
    if num_stints >= 2:
        list_tenures = []
        for stint_count in list(range(0,num_stints)):
            # handle the first coaching stint
            if stint_count == 0:
                year_stint_end = list_stint_end[stint_count]
                list_tenures.append(df_coach[df_coach['Season'] <= year_stint_end].copy())
            # handle coaching stints 2 through num_stints - 1
            elif stint_count < num_stints-1:
                year_stint_end = list_stint_end[stint_count]
                year_stint_end_prev = list_stint_end[stint_count-1]
                df_stint = df_coach[df_coach['Season'] <= year_stint_end].copy()
                list_tenures.append(df_stint[df_stint['Season'] > year_stint_end_prev].copy())
            # handle the last coaching stint
            else:
                year_stint_end_prev = list_stint_end[stint_count-1]
                list_tenures.append(df_coach[df_coach['Season'] > year_stint_end_prev].copy())
            # print(f"Coach: {df_stint['Coach'].iloc[0]}, Games: {len(df_stint)}")
    # Step 2.B. Handle coaches with only a single stint at the respective school
    else:
        list_tenures = [df_coach]
        
    return list_tenures

def scrape_and_compile_coaching_data(scrape_year):
    # Scrape updated results for most recent season
    scrapeCfbResultsAllYears(scrape_year)
    
    df_games = pd.DataFrame()
    for fname in tqdm.tqdm(list(path_dir.joinpath(
            'data/raw/Team History').glob('records*.csv'))):
        # load file
        df = pd.read_csv(fname)
        # drop rows without scores
        df = df[df['Result'].notna()]
        if '2020' in str(fname):
            list_years = []
            for date in df['Date']:
                if '-' in date:
                    year = int(datetime.datetime.strptime(
                        date, "%d-%b-%y").strftime('%Y'))
                    month = datetime.datetime.strptime(
                        date, "%d-%b-%y").strftime('%b')
                    if month == 'Jan':
                        year = year-1
                else:
                    year    = int(datetime.datetime.strptime(
                        date, '%b %d, %Y').strftime('%Y'))
                    month   = datetime.datetime.strptime(
                        date, '%b %d, %Y').strftime('%b')
                    if month == 'Jan':
                        year = year-1
                list_years.append(year)
            df['Year'] = list_years
            df = df[df['Year'] < 2020]
        # add team to master dataframe
        if len(df_games) == 0:
            df_games = df.copy()
        else:
            df_games = df_games.append(df)
    # add year variable to all-games DataFrame
    list_years = []
    list_dates = []
    for date in df_games['Date']:
        if '-' in date:
            year = int(datetime.datetime.strptime(date, "%d-%b-%y").strftime('%Y'))
            month = datetime.datetime.strptime(date, "%d-%b-%y").strftime('%b')
            if month == 'Jan':
                year = year-1
            date_reformatted = datetime.datetime.strptime(
                date, "%d-%b-%y").strftime("%d-%b-%y")
        else:
            year    = int(datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y'))
            month   = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%b')
            if month == 'Jan':
                year = year-1
            date_reformatted = datetime.datetime.strptime(
                date, '%b %d, %Y').strftime("%d-%b-%y")
        list_years.append(year)
        list_dates.append(date_reformatted)
    df_games['Date'] = list_dates
    df_games['Year'] = list_years
    df_games = df_games.drop(columns = 'Time')
    # remove duplicate games
    df_games = df_games.drop_duplicates()
    # remove 2 exhibition games from New Mexico State's schedule
    df_games = df_games[~df_games.Opponent.isin(
        ['Tarleton State', 'Dixie State'])]
    # reset index
    df_games = df_games.reset_index(drop = True)
    
    # Merge games with historic data
    df_games_history = pd.read_csv(r'data\raw\Team History\ALL_records_1936_to_2020.csv')
    df_games_all = df_games_history.append(df_games)
    df_games_all = df_games_all.sort_values(by = ['School', 'Year', 'G'])
    
    # Create timestamp for filename and save to disk
    ts = datetime.date.fromtimestamp(time.time())
    df_games_all.to_csv(rf'data\raw\Team History\ALL_records_{ts}.csv', index = False)
    
    # Scrape coaching data for all available years (i.e. teams + coaches)
    df_schools = scrapeCfbSchoolsAllYears(scrape_year)
    
    df_schools = df_schools.reset_index(drop = True)
    df_schools = df_schools.apply(pd.to_numeric, errors = 'ignore')
    
    # Create timestamp for the year's data and save to disk
    ts = datetime.date.fromtimestamp(time.time())
    df_schools.to_csv(rf'data\raw\Team History\team_history_fb_{scrape_year}.csv', index = False) 
    
    # fix an error with 2015 UCF
    # row_index = df_schools[(df_schools['School'] == 'UCF') & (
    #     df_schools['Year'] == 2015)].index[0]
    # list_coaches = df_schools['Coach(es)'].copy()
    # list_coaches[row_index] = "George O'Leary (0-8), Danny Barrett (0-4)"
    # df_schools['Coach(es)'] = list_coaches
    
    # Merge newly scraped data with historic data
    df_schools_history = pd.read_csv(r'data\raw\Team History\team_history_fb_1936_to_2000.csv') 
    df_schools_merged = df_schools_history.append(df_schools)
    df_schools_merged = df_schools_merged.sort_values(by = ['School', 'Year'], ascending = [True, False])
    
    # Create timestamp for filename and save to disk
    ts = datetime.date.fromtimestamp(time.time())
    df_schools_merged.to_csv(rf'data\raw\Team History\team_history_fb_{ts}.csv', index = False) 
    
    return
    
<<<<<<< HEAD
=======
    return df_yr_by_yr

def create_week_by_week_dataframe(df_all_games, df_schools, games_sf):
    '''
    Purpose: Combine the week-by-week results for each school with the 
        end-of-year school/coach information to create a week-by-week 
        dataframe detailing who coached each team when. This will facilitate
        analysis of coaching tenures.

    Inputs   
    ------
        df_all_games : Pandas DataFrame
            Contains week-by-week results for each school
        df_schools : Pandas DataFrame
            Contains year-by-year results for each school (with coaches' names)
        games_sf : int
            Scott Frost's current number of games
            
    Outputs
    -------
        df_engineered : Pandas DataFrame
            A dataframe containing all historic week-by-week results infused
                with coaches' names
    '''           
    # standardize team names
    df_all_games = renameSchool(df_all_games, 'School')
    df_all_games = renameSchool(df_all_games, 'Opponent')
    df_schools   = renameSchool(df_schools, 'School')
    
    # merge data together
    df_coaches = pd.merge(df_all_games, 
                          df_schools[['School', 'Year', 'Conf', 'Conf_W', 'Conf_L', 
                                      'Conf_T', 'AP_Pre', 'AP_High', 'AP_Post', 
                                      'Coach(es)', 'Bowl']],
                          how = 'left',
                          on = ['School', 'Year'])
    
    # rename columns
    df_coaches = df_coaches.rename(columns = {'Conf_x':'Conf_Opp', 'Conf_y':'Conf'})
    
    # sort dataframe to ensure no issues with groupby
    df_coaches = df_coaches.sort_values(by = ['School', 'Year', 'G'])
    
    # Break out coaches on a week-by-week basis
    list_coaches = []
    table_coaches = pd.DataFrame(columns = ['School', 'Year', 'Coach', 'Games'])
    for school, grp in tqdm.tqdm(df_coaches.groupby(['School', 'Year'])):
        dict_coaches = {}
        # Handle Utah 2003
        if school[0] == 'Utah' and school[1] == 2004:
            dict_coaches['Urban Meyer'] = 12
        # Handle Utah St. 2021
        elif school[0] == 'Utah St.' and school[1] == 2021:
            coach_name = 'Blake Anderson'
            coach_games = grp['G'].count()
            dict_coaches[coach_name] = coach_games
        # Handle USC 2021
        elif school[0] == 'USC' and school[1] == 2021:
            dict_coaches['Clay Helton'] = 2
            dict_coaches['Donte Williams'] = len(grp) - 2
        # handle every coach that coached that season for that team
        else:
            # for every coach a team has, calculate how many games they coached that season
            for coach in grp['Coach(es)'].iloc[0].split(', '):
                coach_name = coach.split(' (')[0]
                coach_record = coach.split(' (')[1].replace(')','')
                # first attempt to account for ties in a coaches' record
                try:
                    coach_games = int(coach_record.split('-')[0]) + int(coach_record.split('-')[1]) + int(coach_record.split('-')[2])
                # otherwise assume they only have wins-losses in their record
                except:
                    coach_games = int(coach_record.split('-')[0]) + int(coach_record.split('-')[1])
                dict_coaches[coach_name] = coach_games
        # add coaches to master list
        num_games = 0
        for coach in dict_coaches.keys():
            list_coaches = list_coaches + ([coach] * dict_coaches[coach])
            table_coaches = table_coaches.append(pd.DataFrame(
                [[school[0], school[1], coach, dict_coaches[coach]]], 
                columns = ['School', 'Year', 'Coach', 'Games']))
            num_games = dict_coaches[coach] + num_games
        if num_games != len(grp):
            print('oops!')
            break
    df_coaches['Coach'] = list_coaches  
    
    # test for any values of "coach" that weren't in the original data
    for index, row in tqdm.tqdm(df_coaches.iterrows()):
        if not pd.isna(row['Coach(es)']):
            if row['Coach'] not in row['Coach(es)']:
                print(f"{row['Coach']} not found in {row['Coach(es)']}")
    
    # add power5 status to dataframe
    df_school_info = pd.read_csv(r'references\names_pictures_ncaa.csv')
    df_school_info = df_school_info.rename(columns = {'Team':'School'})
    df_coaches = pd.merge(df_coaches, df_school_info[['School', 'Power5']], how = 'left', on = 'School')
    df_school_info = df_school_info.rename(columns = {'School':'Opponent', 'Power5':'Power5_Opp'})
    df_coaches = pd.merge(df_coaches, df_school_info[['Opponent', 'Power5_Opp']], how = 'left', on = 'Opponent')
    
    # rename columns    
    df_coaches = df_coaches.rename(columns = {'G':'Week',
                                              'Year':'Season',
                                              'Opp':'Pts_Opp',
                                              'Cum_W':'W_Sn',
                                              'Cum_L':'L_Sn',
                                              'T':'T_Sn'})
    
    # add opponent's record for the year to the table
    df_team_records = pd.merge(df_coaches[['Season', 'Opponent']], 
                               df_schools[['School', 'Year', 'Overall_Pct', 'Conf_Pct']],
                               left_on = ['Season', 'Opponent'],
                               right_on = ['Year', 'School'])
    df_team_records = df_team_records.drop_duplicates()
    df_team_records = df_team_records[['Season', 'School', 'Overall_Pct', 'Conf_Pct']]
    df_team_records = df_team_records.rename(columns = {'Overall_Pct':'Win_Pct_Opp',
                                                        'Conf_Pct':'Win_Pct_Conf_Opp',
                                                        'School':'Opponent'})
    df_coaches = pd.merge(df_coaches, df_team_records, how = 'left', on = ['Season', 'Opponent'])
    
    # add flag if opponent's overall record was > .500
    df_coaches['Opp_Winning_Record'] = list(df_coaches.apply(
        lambda row: True if row['Win_Pct_Opp'] > .5 else False, axis = 1))
    
    # add flag if opponent's conference record was > .500
    df_coaches['Opp_Conf_Winning_Record'] = list(df_coaches.apply(
        lambda row: True if row['Win_Pct_Conf_Opp'] > .5 else False, axis = 1))
    
    # reorder columns
    df_coaches = df_coaches[['Season', 'Week', 'Date', 'Day', 'Rank', 'School', 
                             'Coach', 'Conf', 'Power5', 'Home_Away', 'Rank_Opp', 'Opponent', 
                             'Conf_Opp', 'Power5_Opp', 'Win_Pct_Opp', 'Opp_Winning_Record',
                             'Win_Pct_Conf_Opp', 'Opp_Conf_Winning_Record', 
                             'Result', 'Pts', 'Pts_Opp', 'W_Sn', 
                             'L_Sn', 'T_Sn', 'AP_Pre', 'AP_High', 'AP_Post', 
                             'Notes', 'Bowl', 'url_boxscore']]
    
    # Engineer variables for each coach's stint/tenure at a given school=
    df_engineered = pd.DataFrame()
    for index, grp in tqdm.tqdm(df_coaches.groupby(['School', 'Coach'])):
        if len(df_engineered) == 0:
            df_engineered = add_tenure_features(grp, games_sf)
        else:
            df_engineered = df_engineered.append(add_tenure_features(grp, games_sf))
        
    return df_engineered

def add_tenure_features(df_coach, games_sf):
    '''
    Purpose: Manage the engineering of features across a coach's tenure at a
        a given school (while also accounting for those coaches who have 
        multiple coaching stints/tenures at the same school)

    Inputs   
    ------
        df_coach : Pandas DataFrame
            Contains data for all seasons a coach has coached at a given school
        games_sf : int
            Scott Frost's current number of games
            
    Outputs
    -------
        df_coach_eng : Pandas DataFrame
            Contains input data with newly engineered features that span the
                whole coaching tenure, not just seasons
    '''  
    # Step 1. Identify if the coach's dataframe has multiple stints 
    #   (i.e. gaps in years between tenures at the same school)
    num_stints = 1
    list_stint_end = []
    list_years = list(df_coach['Season'])
    for num_ele in list(range(0,len(list_years))):
        if (num_ele == 0):
            pass
        else:
            if list_years[num_ele] - list_years[num_ele-1] > 1:
                # print(f"Gap detected for coach: {df_coach.iloc[0]['coach']}")
                # print(f"  -- Gap between {list_years[num_ele]} and {list_years[num_ele-1]}")
                list_stint_end.append(list_years[num_ele-1])
                num_stints = num_stints + 1
                
    # Step 2.A. Handle coaches with multiple stints (i.e. gaps in years)
    if num_stints >= 2:
        df_coach_eng = pd.DataFrame()
        for stint_count in list(range(0,num_stints)):
            # handle the first coaching stint
            if stint_count == 0:
                year_stint_end = list_stint_end[stint_count]
                df_stint = df_coach[df_coach['Season'] <= year_stint_end].copy()
            # handle coaching stints 2 through num_stints - 1
            elif stint_count < num_stints-1:
                year_stint_end = list_stint_end[stint_count]
                year_stint_end_prev = list_stint_end[stint_count-1]
                df_stint = df_coach[df_coach['Season'] <= year_stint_end].copy()
                df_stint = df_stint[df_stint['Season'] > year_stint_end_prev].copy()
            # handle the last coaching stint
            else:
                year_stint_end_prev = list_stint_end[stint_count-1]
                df_stint = df_coach[df_coach['Season'] > year_stint_end_prev].copy()
            # engineer new features and add to coach's tenure dataframe
            if len(df_coach_eng) == 0:
                df_coach_eng = engineer_stint_features(df_stint, games_sf)
            else:
                df_coach_eng = df_coach_eng.append(engineer_stint_features(df_stint, games_sf))
            # print(f"Coach: {df_stint['Coach'].iloc[0]}, Games: {len(df_stint)}")
    # Step 2.B. Handle coaches with only a single stint at the respective school
    else:
        df_coach_eng = engineer_stint_features(df_coach, games_sf)
        
    return df_coach_eng
        
def engineer_stint_features(df_tenure, games_sf):
    '''
    Purpose: Engineer features across a coach's tenure at a given school 

    Inputs   
    ------
        df_tenure : Pandas DataFrame
            Contains data for all seasons in a tenure for a given coach/school combo
        games_sf : int
            Scott Frost's current number of games
            
    Outputs
    -------
        df_tenure : Pandas DataFrame
            Contains input data with newly engineered features 
    '''     
    # df_tenure = df_coaches[(df_coaches['School'] == 'Nebraska') & (df_coaches['Coach'] == 'Scott Frost')].copy()
    # df_tenure = df_coaches[(df_coaches['School'] == 'Nebraska') & (df_coaches['Coach'] == 'Mike Riley')].copy()
    # df_tenure = df_coaches[(df_coaches['School'] == 'Nebraska') & (df_coaches['Coach'] == 'Tom Osborne')].copy()
    
    # 0. Total seasons
    row_counts = list(df_tenure.Season.value_counts())
    list_seasons = []
    for idx in range(0,len(row_counts)):
        list_seasons = list_seasons + ([idx+1] * row_counts[idx])
    df_tenure['Sn'] = list_seasons
    
    # 1. Total games
    df_tenure['G'] = list(range(1,len(df_tenure)+1))

    # 2. Total wins
    df_tenure['W'] = df_tenure.Result.eq('W').cumsum()
    
    # 3. Total losses
    df_tenure['L'] = df_tenure.Result.eq('L').cumsum()
    
    # 4. Total ties
    df_tenure['T'] = df_tenure.Result.eq('T').cumsum()
    df_tenure['T'] = df_tenure['T'].fillna(0)
    
    # 5. Win Pct.
    if (len(df_tenure) == 1) and (int(df_tenure['G']) == 0):
            df_tenure['Win_Pct'] = 0
    else:
        df_tenure['Win_Pct'] = df_tenure.apply(lambda row: row['W'] / row['G'] 
                                               if row['G'] != 0 else 0, axis = 1)
    
    # 6. Create conference win/loss flag
    list_conf_flag = []
    for index, row in df_tenure.iterrows():
         if (row['Result'] == 'W') and (row['Conf'] == row['Conf_Opp']):
             list_conf_flag.append('W')
         elif (row['Result'] == 'L') and (row['Conf'] == row['Conf_Opp']):
             list_conf_flag.append('L') 
         elif (row['Result'] == 'T') and (row['Conf'] == row['Conf_Opp']):
             list_conf_flag.append('T') 
         else:
             list_conf_flag.append('')
    df_tenure['Result_Conf'] = list_conf_flag
    
    # 7. Total conference games
    df_tenure['G_Conf'] = df_tenure.Result_Conf.ne('').cumsum()
             
    # 8. Total conference wins
    df_tenure['W_Conf'] = df_tenure.Result_Conf.eq('W').cumsum()
    
    # 9. Total conference losses
    df_tenure['L_Conf'] = df_tenure.Result_Conf.eq('L').cumsum()
    
    # 10. Total conference ties
    df_tenure['T_Conf'] = df_tenure.Result_Conf.eq('T').cumsum()
    
    # 11. Conference Win Pct.
    df_tenure['Win_Pct_Conf'] = df_tenure.apply(
        lambda row: row['W_Conf'] / row['G_Conf'] if row['G_Conf'] != 0 else 0, axis = 1)
    # if (len(df_tenure) == 1) and (int(df_tenure['G_Conf']) == 0):
    #         df_tenure['Win_Pct_Conf'] = 0
    # else:
    #     df_tenure['Win_Pct_Conf'] = df_tenure.apply(lambda row: row['W_Conf'] / row['G_Conf'] 
    #                                            if row['G_Conf'] != 0 else 0, axis = 1)
     
    # 12. Create top 25 opponent win/loss flag
    list_top25_results = []
    for index, row in df_tenure.iterrows():
        if (row['Result'] == 'W') and (~np.isnan(row['Rank_Opp'])):
            list_top25_results.append('W')
        elif (row['Result'] == 'L') and (~np.isnan(row['Rank_Opp'])):
            list_top25_results.append('L')
        elif (row['Result'] == 'T') and (~np.isnan(row['Rank_Opp'])):
            list_top25_results.append('T')
        else:
            list_top25_results.append('')
    df_tenure['Result_Top25_Opp'] = list_top25_results
    
    # 13. Wins vs. AP Top-25
    df_tenure['W_vs_Rank'] = df_tenure.Result_Top25_Opp.eq('W').cumsum()
    
    # 14. Losses vs. AP Top-25
    df_tenure['L_vs_Rank'] = df_tenure.Result_Top25_Opp.eq('L').cumsum()
    
    # 15. Ties vs AP Top-25
    df_tenure['T_vs_Rank'] = df_tenure.Result_Top25_Opp.eq('T').cumsum()
    
    # 16. Win Pct. vs AP Top-25
    df_tenure['Win_Pct_vs_Rank'] = df_tenure.apply(
        lambda row: row['W_vs_Rank'] / (row['W_vs_Rank'] + row['L_vs_Rank'] + row['T_vs_Rank']) 
        if (row['W_vs_Rank'] + row['L_vs_Rank'] + row['T_vs_Rank']) != 0 else 0, axis = 1)
        
    # 17. Total bowl games
    df_tenure['Bowl_G'] = df_tenure.Notes.str.contains('Bowl').eq(True).cumsum()
    
    # 18. Create bowl win/loss flag
    list_bowl_results = []
    for index, row in df_tenure.iterrows():
        if (row['Result'] == 'W') and ('Bowl' in str(row['Notes'])):
            list_bowl_results.append('W')
        elif (row['Result'] == 'L') and ('Bowl' in str(row['Notes'])):
            list_bowl_results.append('L')
        elif (row['Result'] == 'T') and ('Bowl' in str(row['Notes'])):
            list_bowl_results.append('T')
        else:
            list_bowl_results.append('')
    df_tenure['Result_Bowl'] = list_bowl_results
    
    # 19. Bowl Wins
    df_tenure['Bowl_W'] = df_tenure.Result_Bowl.eq('W').cumsum()
    
    # 20. Bowl Losses
    df_tenure['Bowl_L'] = df_tenure.Result_Bowl.eq('L').cumsum()
    
    # 21. Bowl Ties
    df_tenure['Bowl_T'] = df_tenure.Result_Bowl.eq('T').cumsum()
    
    # 22. Bowl Win Pct.
    df_tenure['Win_Pct_Bowl'] = df_tenure.apply(
        lambda row: row['Bowl_W'] / (row['Bowl_W'] + row['Bowl_L'] + row['Bowl_T']) 
        if (row['Bowl_W'] + row['Bowl_L'] + row['Bowl_T']) != 0 else 0, axis = 1)
    
    # 23. Calculate # of seasons with pre-post season AP Top 25 rankings
    list_AP_Pre_counts     = []
    list_AP_Post_25_counts = []
    list_AP_Post_10_counts = []
    list_AP_Post_5_counts  = []
    list_game_counts = []
    for season, grp in df_tenure.groupby('Season'):
        list_AP_Pre_counts     = list_AP_Pre_counts + [1 if ~np.isnan(grp.AP_Pre.iloc[0]) else 0]
        list_AP_Post_25_counts = list_AP_Post_25_counts + [1 if grp.AP_Post.iloc[0] <= 25 else 0]
        list_AP_Post_10_counts = list_AP_Post_10_counts + [1 if grp.AP_Post.iloc[0] <= 10 else 0]
        list_AP_Post_5_counts  = list_AP_Post_5_counts  + [1 if grp.AP_Post.iloc[0] <= 5  else 0]
        list_game_counts = list_game_counts + [len(grp)]
    series_AP_Pre_counts     = pd.Series(list_AP_Pre_counts).cumsum()
    series_AP_Post_25_counts = pd.Series(list_AP_Post_25_counts).cumsum()
    series_AP_Post_10_counts = pd.Series(list_AP_Post_10_counts).cumsum()
    series_AP_Post_5_counts  = pd.Series(list_AP_Post_5_counts).cumsum()
        
    # 24. Total Years in AP Top-25 (Preaseason)   
    df_tenure['AP_Pre_count'] = sum([[x]*y for x,y in zip(series_AP_Pre_counts, list_game_counts)], [])
    
    # 25. Total Years in AP Top-25 (Postseason)
    df_tenure['AP_Post_25_count'] = sum([[x]*y for x,y in zip(series_AP_Post_25_counts, list_game_counts)], [])
    
    # 26. Total Years in AP Top-10 (Postseason)
    df_tenure['AP_Post_10_count'] = sum([[x]*y for x,y in zip(series_AP_Post_10_counts, list_game_counts)], [])
    
    # 27. Total Years in AP Top-5 (Postseason)
    df_tenure['AP_Post_5_count'] = sum([[x]*y for x,y in zip(series_AP_Post_5_counts, list_game_counts)], [])
    
    # 28. Total Weeks in AP Top-25
    df_tenure['Weeks_Ranked'] = list(pd.Series([1 if ~np.isnan(x) else 0 for x in df_tenure.Rank]).cumsum())
    
    # 29. Weeks Ranked in AP Top-25 Pct.
    df_tenure['Weeks_Ranked_Pct.'] = df_tenure.apply(lambda row: row['Weeks_Ranked'] / row['G'], axis = 1)

    # 30. Season Conference Wins
    list_conf_wins = []
    for season, grp in df_tenure.groupby(['Season']):
        list_conf_wins = list_conf_wins + list(grp.Result_Conf.eq('W').cumsum())
    df_tenure['W_Sn_Conf'] = list_conf_wins
    
    # 31. Season Conference Losses
    list_conf_losses = []
    for season, grp in df_tenure.groupby(['Season']):
        list_conf_losses = list_conf_losses + list(grp.Result_Conf.eq('L').cumsum())
    df_tenure['L_Sn_Conf'] = list_conf_losses
    
    # 31. Season Conference Ties
    list_conf_ties = []
    for season, grp in df_tenure.groupby(['Season']):
        list_conf_ties = list_conf_ties + list(grp.Result_Conf.eq('T').cumsum())
    df_tenure['T_Sn_Conf'] = list_conf_ties
    
    # 32. Season Win Pct.
    df_tenure['Win_Pct_Sn'] = df_tenure.apply(lambda row: row['W_Sn'] / row['Week'], axis = 1)
    
    # 33. Season Conference Win Pct.
    df_tenure['Win_Pct_Sn_Conf'] = df_tenure.apply(
        lambda row: row['W_Sn_Conf'] / (row['W_Sn_Conf'] + row['L_Sn_Conf'] + row['T_Sn_Conf']) 
        if (row['W_Sn_Conf'] + row['L_Sn_Conf'] + row['T_Sn_Conf']) != 0 else 0, axis = 1)
    
    # 34. Winning Seasons
    list_final_win_pct = list(df_tenure.groupby('Season').tail(1).Win_Pct_Sn)
    list_winning_seasons = [1 if x > .5 else 0 for x in list_final_win_pct]
    list_win_sn_cnt = []
    for idx in range(0,len(row_counts)):
        list_win_sn_cnt = list_win_sn_cnt + ([list_winning_seasons[idx]] * row_counts[idx])
    df_tenure['Winning_Sns'] = list_win_sn_cnt
    
    # 35. Create a flag for win/loss vs Power 5 teams
    list_p5_results = []
    for index, row in df_tenure.iterrows():
        if (row['Result'] == 'W') and (row['Power5_Opp'] == True):
            list_p5_results.append('W')
        elif (row['Result'] == 'L') and (row['Power5_Opp'] == True):
            list_p5_results.append('L')
        elif (row['Result'] == 'T') and (row['Power5_Opp'] == True):
            list_p5_results.append('T')
        else:
            list_p5_results.append('')
    df_tenure['Results_P5'] = list_p5_results
    
    # 36. Games vs. Power 5 teams
    df_tenure['G_P5'] = df_tenure.Results_P5.ne('').cumsum()
    
    # 37. Wins vs. Power 5 teams
    df_tenure['W_P5'] = df_tenure.Results_P5.eq('W').cumsum()
    
    # 38. Losses vs. Power 5 teams
    df_tenure['L_P5'] = df_tenure.Results_P5.eq('L').cumsum()
    
    # 39. Ties vs. Power 5 teams
    df_tenure['T_P5'] = df_tenure.Results_P5.eq('T').cumsum()
    
    # 40. Win Pct. vs Power 5 teams
    df_tenure['Win_Pct_P5'] = df_tenure.apply(
        lambda row: row['W_P5'] / row['G_P5'] if row['G_P5'] != 0 else 0, axis = 1)
    
    # 41. Create a flag for win/loss vs. teams with > .500 records
    list_winning_results = []
    for index, row in df_tenure.iterrows():
        if (row['Result'] == 'W') and (row['Opp_Winning_Record'] == True):
            list_winning_results.append('W')
        elif (row['Result'] == 'L') and (row['Opp_Winning_Record'] == True):
            list_winning_results.append('L')
        elif (row['Result'] == 'T') and (row['Opp_Winning_Record'] == True):
            list_winning_results.append('T')
        else:
            list_winning_results.append('')
    df_tenure['Results_vs_Winning'] = list_winning_results
    
    # 42. Games vs. teams with winning (> .500) records
    df_tenure['G_vs_Winning'] = df_tenure.Results_vs_Winning.ne('').cumsum()
    
    # 43. Wins vs. teams with winning (> .500) records
    df_tenure['W_vs_Winning'] = df_tenure.Results_vs_Winning.eq('W').cumsum()
    
    # 44. Losses vs. teams with winning (> .500) records
    df_tenure['L_vs_Winning'] = df_tenure.Results_vs_Winning.eq('L').cumsum()
    
    # 45. Ties vs. teams with winning (> .500) records
    df_tenure['T_vs_Winning'] = df_tenure.Results_vs_Winning.eq('T').cumsum()
    
    # 46. Win Pct. vs. teams with winning (> .500 ) records
    df_tenure['Win_Pct_vs_Winning'] = df_tenure.apply(
        lambda row: row['W_vs_Winning'] / row['G_vs_Winning'] if row['G_vs_Winning'] != 0 else 0, axis = 1)
    
    # 47. Create a flag for win/loss vs. teams with > .500 records in conference
    list_winning_results_conf = []
    for index, row in df_tenure.iterrows():
        if ((row['Result'] == 'W') and (
                row['Opp_Conf_Winning_Record'] == True)) and (
                    row['Conf'] == row['Conf_Opp']):
                        list_winning_results_conf.append('W')
        elif ((row['Result'] == 'L') and (
                row['Opp_Conf_Winning_Record'] == True)) and (
                    row['Conf'] == row['Conf_Opp']):
                        list_winning_results_conf.append('L')
        elif ((row['Result'] == 'T') and (
                row['Opp_Conf_Winning_Record'] == True)) and (
                    row['Conf'] == row['Conf_Opp']):
                        list_winning_results_conf.append('T')
        else:
            list_winning_results_conf.append('')
    df_tenure['Results_vs_Winning_Conf'] = list_winning_results_conf
    
    # 48. Games vs. teams with winning (> .500) records in conference
    df_tenure['G_vs_Winning_Conf'] = df_tenure.Results_vs_Winning_Conf.ne('').cumsum()
    
    # 49. Wins vs. teams with winning (> .500) records in conference
    df_tenure['W_vs_Winning_Conf'] = df_tenure.Results_vs_Winning_Conf.eq('W').cumsum()
    
    # 50. Losses vs. teams with winning (> .500) records in conference
    df_tenure['L_vs_Winning_Conf'] = df_tenure.Results_vs_Winning_Conf.eq('L').cumsum()
    
    # 51. Ties vs. teams with winning (> .500) records in conference
    df_tenure['T_vs_Winning_Conf'] = df_tenure.Results_vs_Winning_Conf.eq('T').cumsum()
    
    # 52. Win Pct. vs. teams with winning (> .500) records in conference
    df_tenure['Win_Pct_vs_Winning_Conf'] = df_tenure.apply(
        lambda row: row['W_vs_Winning_Conf'] / row['G_vs_Winning_Conf'] if row['G_vs_Winning_Conf'] != 0 else 0, axis = 1)
    
    # test = df_tenure[['Season', 'Week', 'Opponent', 'Win_Pct_Opp', 'Opp_Winning_Record', 'Results_vs_Winning', 'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 'Win_Pct_vs_Winning']]
    # test = df_tenure[['Season', 'Week', 'Opponent', 'Win_Pct_Conf_Opp', 'Opp_Conf_Winning_Record', 
    #                   'Results_vs_Winning_Conf', 'G_vs_Winning_Conf', 
    #                   'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf']]
    
    # 53. Calculate the coach's winning pct at the same number of games as SF's current total
    if len(df_tenure) >= games_sf:
        df_tenure['Win_Pct_at_SF'] = [float(df_tenure[df_tenure['G'] == games_sf]['Win_Pct'])] * len(df_tenure)
    else:
        df_tenure['Win_Pct_at_SF'] = [np.nan] * len(df_tenure)
    
    # 54. Reorder columns
    df_tenure = df_tenure[['Season', 'Week', 'Date', 'Day', 'Rank', 'School',
                            'Coach', 'Conf', 'Power5', 'Home_Away', 'Rank_Opp',
                            'Opponent', 'Conf_Opp', 'Power5_Opp', 'Result', 'Pts', 'Pts_Opp', 
                            'Sn', 'G', 'W', 'L', 'T', 'Win_Pct', 
                            'G_Conf', 'W_Conf', 'L_Conf', 'T_Conf', 'Win_Pct_Conf',
                            'G_P5', 'W_P5', 'L_P5', 'T_P5', 'Win_Pct_P5',
                            'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 'T_vs_Winning', 'Win_Pct_vs_Winning',
                            'G_vs_Winning_Conf', 'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 'T_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf',
                            'W_Sn', 'L_Sn', 'T_Sn', 'Win_Pct_Sn', 
                            'W_Sn_Conf', 'L_Sn_Conf', 'T_Sn_Conf', 'Win_Pct_Sn_Conf', 
                            'W_vs_Rank', 'L_vs_Rank', 'T_vs_Rank', 'Win_Pct_vs_Rank', 
                            'Winning_Sns',
                            'Bowl_G', 'Bowl_W', 'Bowl_L', 'Bowl_T', 'Win_Pct_Bowl', 
                            'AP_Pre', 'AP_High', 'AP_Post', 
                            'AP_Pre_count', 'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count',
                            'Weeks_Ranked', 'Weeks_Ranked_Pct.',
                            'Win_Pct_at_SF',
                            'Notes', 'url_boxscore']]
    
    return df_tenure

>>>>>>> 55366a4305b3f99adab491b38426258b0a28e62f
#==============================================================================
# Working Code
#==============================================================================
# Set the project working directory
# path_dir = pathlib.Path(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis')
path_dir = pathlib.Path(os.getcwd())
if 'cfbAnalysis' not in str(path_dir):
    path_dir = path_dir.joinpath('cfbAnalysis')
os.chdir(path_dir)

#------------------------------------------------------------------------------
# Scrape and compile data for individual team games
#------------------------------------------------------------------------------
<<<<<<< HEAD
# AP poll started in 1936

scrape_and_compile_coaching_data(2021)

#------------------------------------------------------------------------------
# Scrape and compile data for coaches across years
#------------------------------------------------------------------------------
# Ingest the most recent game-by-game history file
df_all_games = pd.read_csv(max(glob.iglob(
    r'data\raw\Team History\ALL_records*.csv'), key=os.path.getmtime))

# Ingest the most recent year-by-year history file
df_schools = pd.read_csv(max(glob.iglob(
    r'data\raw\Team History\team_history*.csv'), key=os.path.getmtime))

#------------------------------------------------------------------------------
# Create week-by-week records for all coaches
#------------------------------------------------------------------------------
games_sf = 44
=======
# Scrape updated results for most recent season
scrapeCfbResultsAllYears(2021)
df_all_games = pd.DataFrame()
for fname in tqdm.tqdm(list(path_dir.joinpath('data/raw/Team History').glob('records*.csv'))):
    # load file
    df = pd.read_csv(fname)
    # drop rows without scores
    df = df[df['Result'].notna()]
    if '2020' in str(fname):
        list_years = []
        for date in df['Date']:
            if '-' in date:
                year = int(datetime.datetime.strptime(date, "%d-%b-%y").strftime('%Y'))
                month = datetime.datetime.strptime(date, "%d-%b-%y").strftime('%b')
                if month == 'Jan':
                    year = year-1
            else:
                year    = int(datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y'))
                month   = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%b')
                if month == 'Jan':
                    year = year-1
            list_years.append(year)
        df['Year'] = list_years
        df = df[df['Year'] < 2020]
    # add team to master dataframe
    if len(df_all_games) == 0:
        df_all_games = df.copy()
    else:
        df_all_games = df_all_games.append(df)
# add year variable to all-games DataFrame
list_years = []
list_dates = []
for date in df_all_games['Date']:
    if '-' in date:
        year = int(datetime.datetime.strptime(date, "%d-%b-%y").strftime('%Y'))
        month = datetime.datetime.strptime(date, "%d-%b-%y").strftime('%b')
        if month == 'Jan':
            year = year-1
        date_reformatted = datetime.datetime.strptime(date, "%d-%b-%y").strftime("%d-%b-%y")
    else:
        year    = int(datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y'))
        month   = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%b')
        if month == 'Jan':
            year = year-1
        date_reformatted = datetime.datetime.strptime(date, '%b %d, %Y').strftime("%d-%b-%y")
    list_years.append(year)
    list_dates.append(date_reformatted)
df_all_games['Date'] = list_dates
df_all_games['Year'] = list_years
df_all_games = df_all_games.drop(columns = 'Time')
# remove duplicate games
df_all_games = df_all_games.drop_duplicates()
# remove 2 exhibition games from New Mexico State's schedule
df_all_games = df_all_games[~df_all_games.Opponent.isin(['Tarleton State', 'Dixie State'])]
# reset index
df_all_games = df_all_games.reset_index(drop = True)

# Create timestamp for filename and save to disk
ts = datetime.date.fromtimestamp(time.time())
df_all_games.to_csv(rf'data\raw\Team History\ALL_records_{ts}.csv', index = False)

# # Ingest the most recent team history file
# df_all_games = pd.read_csv(max(glob.iglob(r'data\raw\Team History\ALL_records*.csv'), key=os.path.getmtime))

#------------------------------------------------------------------------------
# Scrape and compile data for coaches across years
#------------------------------------------------------------------------------
# Scrape coaching data for all available years (i.e. teams + coaches)
df_schools = scrapeCfbSchoolsAllYears()
df_schools = df_schools.reset_index(drop = True)
df_schools = df_schools.apply(pd.to_numeric, errors = 'ignore')

# fix an error with 2015 UCF
row_index = df_schools[(df_schools['School'] == 'UCF') & (df_schools['Year'] == 2015)].index[0]
list_coaches = df_schools['Coach(es)'].copy()
list_coaches[row_index] = "George O'Leary (0-8), Danny Barrett (0-4)"
df_schools['Coach(es)'] = list_coaches

# Create timestamp for filename and save to disk
ts = datetime.date.fromtimestamp(time.time())
df_schools.to_csv(rf'data\raw\Team History\team_history_fb_{ts}.csv', index = False)

# # Ingest the most recent team history file
# df_schools = pd.read_csv(max(glob.iglob(r'data\raw\Team History\team_history*.csv'), key=os.path.getmtime))

#------------------------------------------------------------------------------
# Create a dataframe of coaching information given school info
#------------------------------------------------------------------------------
# df_coaches = create_coach_dataframe(df_schools)

#------------------------------------------------------------------------------
# Using historic coaching data, create a new dataframe that calculates
#   year-over-year totals for each coach
#------------------------------------------------------------------------------
# df_coaches = calculate_year_by_year(df_coaches)

#------------------------------------------------------------------------------
# Create week-by-week records for all coaches
#------------------------------------------------------------------------------
games_sf = 40
>>>>>>> 55366a4305b3f99adab491b38426258b0a28e62f
df_coaches = create_week_by_week_dataframe(df_all_games, df_schools, games_sf)

# Save coaching data to disk
ts = datetime.date.fromtimestamp(time.time())
df_coaches.to_csv(rf'data\processed\Coaches\coaching_history_{ts}.csv', index = False)

#------------------------------------------------------------------------------
# Start of Scott Frost Analysis (DO THIS BEFORE ALL OTHER ANALYSIS)
#------------------------------------------------------------------------------
# Ingest the most recent coaching history file
<<<<<<< HEAD
df_coaches = pd.read_csv(max(glob.iglob(
    r'data\processed\Coaches\coaching_history*.csv'), key=os.path.getmtime))
df_coaches = df_coaches.apply(pd.to_numeric, errors = 'ignore')

# Isolate Scott Frost's data
df_sf = df_coaches[(df_coaches['School'] == 'Nebraska') & (
    df_coaches['Coach'] == 'Scott Frost')]

# Isolate Scott Frost's Last Game Coached
sf = df_coaches[(df_coaches['Coach'] == 'Scott Frost') & (
    df_coaches['School'] == 'Nebraska')].iloc[[-1],:]

# Isolate Scott Frost's Games Played
sf_gp = int(sf['G'])

# #------------------------------------------------------------------------------
# # Active FBS Coaches
# #------------------------------------------------------------------------------
# # 1. Isolate active coaches
# df_active = pd.DataFrame()
# df_current = df_coaches[df_coaches['Season'] == 2021]
# for tup, grp in df_current.groupby(['School']):
#     if len(df_active) == 0:
#         df_active = grp.tail(1)
#     else:
#         df_active = df_active.append(grp.tail(1)) 
       
# # 2. Isolate those who have coached as many games as Frost
# df_active = df_active[df_active['Sn'] >= 4]

# # 3. Drop unneeded columns
# # df_active = df_active.drop(columns = ['Week', 'Rank', 'Date', 'Day', 'Home_Away', 
# #                                       'Rank_Opp', 'Opponent',
# #                                       'Conf_Opp', 'Power5_Opp', 'Result',
# #                                       'Pts', 'Pts_Opp','Notes', 'url_boxscore',
# #                                       'T', 'T_Conf', 'T_P5', 'T_vs_Winning',
# #                                       'T_vs_Winning_Conf', 'T_Sn', 'T_Sn_Conf',
# #                                       'T_vs_Rank', 'Bowl_T'])
# df_active = df_active[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
#                      'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning', 
#                      'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 'Winning_Sns', 
#                      'Bowl_G', 'Win_Pct_at_SF',
#                      'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 
#                      'Weeks_Ranked']]

# #------------------------------------------------------------------------------
# # All Time (as many games, or more, as Frost)
# #------------------------------------------------------------------------------
# # 1. Isolate those who have coached as many games as Frost
# df_subset = df_coaches[df_coaches['G'] >= sf_gp]
# df_final = pd.DataFrame()
# for tup, grp in df_subset.groupby(['School', 'Coach']):
#     if len(df_final) == 0:
#         df_final = grp.iloc[[-1],:].copy()
#     else:
#         df_final = df_final.append(grp.iloc[[-1],:])
 
# df_final = pd.DataFrame()
# for tup, grp in df_coaches.groupby(['School', 'Coach']):
#     if len(df_final) == 0:
#         df_final = grp.iloc[[-1],:].copy()
#     else:
#         df_final = df_final.append(grp.iloc[[-1],:])
# df_final['G_vs_Rank'] = df_final['W_vs_Rank'] + df_final['L_vs_Rank'] + df_final['T_vs_Rank']
# df_final = df_final[df_final['G_vs_Rank'] >= 11]
# df_final = df_final[['School', 'Coach', 'Conf', 'Power5', 'Win_Pct_vs_Rank', 
#                      'G_vs_Rank', 'W_vs_Rank', 'L_vs_Rank', 'T_vs_Rank', ]]

# # 2. Drop unneeded columns
# df_final = df_final[['Season', 'School', 'Coach', 'Conf',
#                     'Power5', 'Winning_Sns',  
#                     'Sn', 'G', 'W', 'L', 'Win_Pct',
#                     'G_Conf', 'W_Conf', 'L_Conf', 'Win_Pct_Conf',
#                     'G_P5', 'W_P5', 'L_P5', 'Win_Pct_P5',
#                     'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 
#                     'Win_Pct_vs_Winning',
#                     'G_vs_Winning_Conf', 'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 
#                     'Win_Pct_vs_Winning_Conf',
#                     'W_vs_Rank', 'L_vs_Rank', 'Win_Pct_vs_Rank', 
#                     'W_Sn', 'L_Sn', 'Win_Pct_Sn', 'W_Sn_Conf', 'L_Sn_Conf', 
#                     'Win_Pct_Sn_Conf',
#                     'Bowl_G', 'Bowl_W', 'Bowl_L', 'Win_Pct_Bowl', 'Win_Pct_at_SF',
#                     'AP_Pre_count', 'AP_Post_25_count', 
#                     'AP_Post_10_count', 'AP_Post_5_count',
#                     'Weeks_Ranked', 'Weeks_Ranked_Pct.']]
=======
df_coaches = pd.read_csv(max(glob.iglob(r'data\processed\Coaches\coaching_history*.csv'), key=os.path.getmtime))
df_coaches = df_coaches.apply(pd.to_numeric, errors = 'ignore')

# Isolate Scott Frost's data
df_sf = df_coaches[(df_coaches['School'] == 'Nebraska') & (df_coaches['Coach'] == 'Scott Frost')]

# Isolate Scott Frost's Last Game Coached
sf = df_coaches[(df_coaches['Coach'] == 'Scott Frost') & (df_coaches['School'] == 'Nebraska')].iloc[[-1],:]

# Isolate Scott Frost's Games Played
sf_gp = int(sf['G'])

#------------------------------------------------------------------------------
# Active FBS Coaches
#------------------------------------------------------------------------------
# 1. Isolate active coaches
df_active = pd.DataFrame()
df_current = df_coaches[df_coaches['Season'] == 2021]
for tup, grp in df_current.groupby(['School']):
    if len(df_active) == 0:
        df_active = grp.tail(1)
    else:
        df_active = df_active.append(grp.tail(1))
        
# 2. Isolate those who have coached as many games as Frost
df_active = df_active[df_active['G'] >= sf_gp]

# 3. Drop unneeded columns
df_active = df_active.drop(columns = ['Week', 'Rank', 'Date', 'Day', 'Home_Away', 
                                      'Rank_Opp', 'Opponent',
                                      'Conf_Opp', 'Power5_Opp', 'Result',
                                      'Pts', 'Pts_Opp','Notes', 'url_boxscore',
                                      'T', 'T_Conf', 'T_P5', 'T_vs_Winning',
                                      'T_vs_Winning_Conf', 'T_Sn', 'T_Sn_Conf',
                                      'T_vs_Rank', 'Bowl_T'])

#------------------------------------------------------------------------------
# All Time (as many games, or more, as Frost)
#------------------------------------------------------------------------------
# 1. Isolate those who have coached as many games as Frost
df_subset = df_coaches[df_coaches['G'] >= sf_gp]
df_final = pd.DataFrame()
for tup, grp in df_subset.groupby(['School', 'Coach']):
    if len(df_final) == 0:
        df_final = grp.iloc[[-1],:].copy()
    else:
        df_final = df_final.append(grp.iloc[[-1],:])

# 2. Drop unneeded columns
df_final = df_final[['Season', 'School', 'Coach', 'Conf',
                    'Power5', 
                    'Sn', 'G', 'W', 'L', 'Win_Pct',
                    'G_Conf', 'W_Conf', 'L_Conf', 'Win_Pct_Conf',
                    'G_P5', 'W_P5', 'L_P5', 'Win_Pct_P5',
                    'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 'Win_Pct_vs_Winning',
                    'G_vs_Winning_Conf', 'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf',
                    'W_Sn', 'L_Sn', 'Win_Pct_Sn', 'W_Sn_Conf', 'L_Sn_Conf', 'Win_Pct_Sn_Conf',
                    'W_vs_Rank', 'L_vs_Rank', 'Win_Pct_vs_Rank', 
                    'Winning_Sns', 
                    'Bowl_G', 'Bowl_W', 'Bowl_L', 'Win_Pct_Bowl', 'Win_Pct_at_SF',
                    'AP_Pre_count', 'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count',
                    'Weeks_Ranked', 'Weeks_Ranked_Pct.']]

# 3. Limit coaches to those in the last 20 years
df_final = df_final[df_final['Season'] >= 2001]

# 4. Make a smaller dataframe for ranking/comparisons
df_ranks = df_final[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
                     'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning', 
                     'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 'Winning_Sns', 'Bowl_G', 'Win_Pct_at_SF',
                     'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 'Weeks_Ranked']]

# 5. Create rankings
df_ranks = df_ranks.reset_index(drop = True)
df_ranks['Win_Pct_rank']                = df_ranks['Win_Pct'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_Conf_rank']           = df_ranks['Win_Pct_Conf'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_P5_rank']             = df_ranks['Win_Pct_P5'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_vs_Winning_rank']     = df_ranks['Win_Pct_vs_Winning'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_vs_Winning_Conf_rank'] = df_ranks['Win_Pct_vs_Winning_Conf'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_vs_Rank_rank']        = df_ranks['Win_Pct_vs_Rank'].rank(method = 'min', ascending = False)

# 6. Reorder columns
df_ranks = df_ranks[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
                     'Win_Pct', 'Win_Pct_rank',
                     'Win_Pct_Conf', 'Win_Pct_Conf_rank', 
                     'Win_Pct_P5', 'Win_Pct_P5_rank',
                     'Win_Pct_vs_Winning', 'Win_Pct_vs_Winning_rank',
                     'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf_rank',
                     'Win_Pct_vs_Rank', 'Win_Pct_vs_Rank_rank',
                     'Winning_Sns', 'Bowl_G', 'Win_Pct_at_SF',
                     'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 'Weeks_Ranked']]

oops = df_ranks[df_ranks['Win_Pct_at_SF'] <= float(sf['Win_Pct'])]

#------------------------------------------------------------------------------
# All Time (the exact same number of games as Frost)
#------------------------------------------------------------------------------
# 1. Isolate those who have coached as many games as Frost
df_subset = df_coaches[df_coaches['G'] == sf_gp]
df_final = pd.DataFrame()
for tup, grp in df_subset.groupby(['School', 'Coach']):
    if len(df_final) == 0:
        df_final = df_coaches[(df_coaches['School'] == tup[0]) & (df_coaches['Coach'] == tup[1])].iloc[[-1],:].copy()
    else:
        df_final = df_final.append(df_coaches[(df_coaches['School'] == tup[0]) & (df_coaches['Coach'] == tup[1])].iloc[[-1],:])

# 2. Drop unneeded columns
df_final = df_final[['Season', 'School', 'Coach', 'Conf',
                    'Power5', 
                    'Sn', 'G', 'W', 'L', 'Win_Pct',
                    'G_Conf', 'W_Conf', 'L_Conf', 'Win_Pct_Conf',
                    'G_P5', 'W_P5', 'L_P5', 'Win_Pct_P5',
                    'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 'Win_Pct_vs_Winning',
                    'G_vs_Winning_Conf', 'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf',
                    'W_Sn', 'L_Sn', 'Win_Pct_Sn', 'W_Sn_Conf', 'L_Sn_Conf', 'Win_Pct_Sn_Conf',
                    'W_vs_Rank', 'L_vs_Rank', 'Win_Pct_vs_Rank', 
                    'Winning_Sns', 
                    'Bowl_G', 'Bowl_W', 'Bowl_L', 'Win_Pct_Bowl', 'Win_Pct_at_SF', 
                    'AP_Pre_count', 'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count',
                    'Weeks_Ranked', 'Weeks_Ranked_Pct.']]

# 3. Limit coaches to those in the last 20 years
# df_final = df_final[df_final['Season'] >= 2001]

# 4. Make a smaller dataframe for ranking/comparisons
df_ranks = df_final[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
                     'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning', 
                     'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 'Winning_Sns', 'Bowl_G', 'Win_Pct_at_SF',
                     'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 'Weeks_Ranked']]

# 5. Create rankings
df_ranks = df_ranks.reset_index(drop = True)
df_ranks['Win_Pct_rank']                = df_ranks['Win_Pct'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_Conf_rank']           = df_ranks['Win_Pct_Conf'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_P5_rank']             = df_ranks['Win_Pct_P5'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_vs_Winning_rank']     = df_ranks['Win_Pct_vs_Winning'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_vs_Winning_Conf_rank'] = df_ranks['Win_Pct_vs_Winning_Conf'].rank(method = 'min', ascending = False)
df_ranks['Win_Pct_vs_Rank_rank']        = df_ranks['Win_Pct_vs_Rank'].rank(method = 'min', ascending = False)

# 6. Reorder columns
df_ranks = df_ranks[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
                     'Win_Pct', 'Win_Pct_rank',
                     'Win_Pct_Conf', 'Win_Pct_Conf_rank', 
                     'Win_Pct_P5', 'Win_Pct_P5_rank',
                     'Win_Pct_vs_Winning', 'Win_Pct_vs_Winning_rank',
                     'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf_rank',
                     'Win_Pct_vs_Rank', 'Win_Pct_vs_Rank_rank',
                     'Winning_Sns', 'Bowl_G', 'Win_Pct_at_SF',
                     'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 'Weeks_Ranked']]

oops = df_ranks[df_ranks['Win_Pct'] <= float(sf['Win_Pct'])]

# Subset the data to coaches have coached at least the same number of games as Scott
df_history = df_coaches[df_coaches['G'] >= sf_gp]
df_history = df_history.reset_index(drop = True)

# Create a subset snap-shot to isolate all coaching records to match Scott's timeframe (i.e. Games coached)
df_snapshot = df_coaches[df_coaches['G'] == sf_gp]
df_snapshot = df_snapshot.reset_index(drop = True)

# Isolate Scott Frost's Winning %
sf_win_pct = float(df_yr_4[df_yr_4['coach'] == 'Scott Frost']['cum_win_pct'])

# Subset the data to be only coaches within the last 25 years
df_yr_4 = df_yr_4[df_yr_4['year'] >= 1991]

# # Save coaches with 4 or more years of tenure to disk
# ts = datetime.date.fromtimestamp(time.time())
# df_yr_4.to_csv(rf'data\raw\Coaches\coaching_history_year_3_{ts}.csv', index = False)

# Subset the data to coaches with a winning percentage the same as or worse than Scott
df_bad = df_yr_4[df_yr_4['cum_win_pct'] < sf_win_pct]
>>>>>>> 55366a4305b3f99adab491b38426258b0a28e62f

# # 3. Limit coaches to those in the last 20 years
# df_final = df_final[df_final['Season'] >= 2001]

# # 4. Make a smaller dataframe for ranking/comparisons
# df_ranks = df_final[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
#                      'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning', 
#                      'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 'Winning_Sns', 
#                      'Bowl_G', 'Win_Pct_at_SF',
#                      'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 
#                      'Weeks_Ranked']]

# # 5. Create rankings
# df_ranks = df_ranks.reset_index(drop = True)
# df_ranks['Win_Pct_rank']                = df_ranks['Win_Pct'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_Conf_rank']           = df_ranks['Win_Pct_Conf'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_P5_rank']             = df_ranks['Win_Pct_P5'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_vs_Winning_rank']     = df_ranks['Win_Pct_vs_Winning'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_vs_Winning_Conf_rank'] = df_ranks['Win_Pct_vs_Winning_Conf'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_vs_Rank_rank']        = df_ranks['Win_Pct_vs_Rank'].rank(
#     method = 'min', ascending = False)

# # 6. Reorder columns
# df_ranks = df_ranks[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
#                      'Win_Pct', 'Win_Pct_rank',
#                      'Win_Pct_Conf', 'Win_Pct_Conf_rank', 
#                      'Win_Pct_P5', 'Win_Pct_P5_rank',
#                      'Win_Pct_vs_Winning', 'Win_Pct_vs_Winning_rank',
#                      'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf_rank',
#                      'Win_Pct_vs_Rank', 'Win_Pct_vs_Rank_rank',
#                      'Winning_Sns', 'Bowl_G', 'Win_Pct_at_SF',
#                      'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 
#                      'Weeks_Ranked']]

# oops = df_ranks[df_ranks['Win_Pct_at_SF'] <= float(sf['Win_Pct'])]

# #------------------------------------------------------------------------------
# # All Time (the exact same number of games as Frost)
# #------------------------------------------------------------------------------
# # 1. Isolate those who have coached as many games as Frost
# df_subset = df_coaches[df_coaches['G'] == sf_gp]
# df_final = pd.DataFrame()
# for tup, grp in df_subset.groupby(['School', 'Coach']):
#     if len(df_final) == 0:
#         df_final = df_coaches[(df_coaches['School'] == tup[0]) & (
#             df_coaches['Coach'] == tup[1])].iloc[[-1],:].copy()
#     else:
#         df_final = df_final.append(df_coaches[(df_coaches['School'] == tup[0]) & (
#             df_coaches['Coach'] == tup[1])].iloc[[-1],:])

# # 2. Drop unneeded columns
# df_final = df_final[['Season', 'School', 'Coach', 'Conf',
#                     'Power5', 'Winning_Sns', 
#                     'Sn', 'G', 'W', 'L', 'Win_Pct',
#                     'G_Conf', 'W_Conf', 'L_Conf', 'Win_Pct_Conf',
#                     'G_P5', 'W_P5', 'L_P5', 'Win_Pct_P5',
#                     'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 
#                     'Win_Pct_vs_Winning',
#                     'G_vs_Winning_Conf', 'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 
#                     'Win_Pct_vs_Winning_Conf',
#                     'W_vs_Rank', 'L_vs_Rank', 'Win_Pct_vs_Rank', 
#                     'W_Sn', 'L_Sn', 'Win_Pct_Sn', 'W_Sn_Conf', 'L_Sn_Conf', 
#                     'Win_Pct_Sn_Conf',
#                     'Bowl_G', 'Bowl_W', 'Bowl_L', 'Win_Pct_Bowl', 'Win_Pct_at_SF', 
#                     'AP_Pre_count', 'AP_Post_25_count', 
#                     'AP_Post_10_count', 'AP_Post_5_count',
#                     'Weeks_Ranked', 'Weeks_Ranked_Pct.']]

# # 3. Limit coaches to those in the last 20 years
# # df_final = df_final[df_final['Season'] >= 2001]

# # 4. Make a smaller dataframe for ranking/comparisons
# df_ranks = df_final[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
#                      'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning', 
#                      'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 'Winning_Sns', 
#                      'Bowl_G', 'Win_Pct_at_SF',
#                      'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 
#                      'Weeks_Ranked']]

# # 5. Create rankings
# df_ranks = df_ranks.reset_index(drop = True)
# df_ranks['Win_Pct_rank']                = df_ranks['Win_Pct'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_Conf_rank']           = df_ranks['Win_Pct_Conf'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_P5_rank']             = df_ranks['Win_Pct_P5'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_vs_Winning_rank']     = df_ranks['Win_Pct_vs_Winning'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_vs_Winning_Conf_rank'] = df_ranks['Win_Pct_vs_Winning_Conf'].rank(
#     method = 'min', ascending = False)
# df_ranks['Win_Pct_vs_Rank_rank']        = df_ranks['Win_Pct_vs_Rank'].rank(
#     method = 'min', ascending = False)

# # 6. Reorder columns
# df_ranks = df_ranks[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Sn', 'G', 
#                      'Win_Pct', 'Win_Pct_rank',
#                      'Win_Pct_Conf', 'Win_Pct_Conf_rank', 
#                      'Win_Pct_P5', 'Win_Pct_P5_rank',
#                      'Win_Pct_vs_Winning', 'Win_Pct_vs_Winning_rank',
#                      'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf_rank',
#                      'Win_Pct_vs_Rank', 'Win_Pct_vs_Rank_rank',
#                      'Winning_Sns', 'Bowl_G', 'Win_Pct_at_SF',
#                      'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count', 
#                      'Weeks_Ranked']]

# oops = df_ranks[df_ranks['Win_Pct'] <= float(sf['Win_Pct'])]

# #------------------------------------------------------------------------------
# # All Time (as many games, or more, as Frost) - Who meets Frost's criteria?
# #------------------------------------------------------------------------------
# # # 0. Put unique identifier for each tenure in dataframe
# # df_final = pd.DataFrame()
# # idx_tenure = 0;
# # for tup, grp in tqdm.tqdm(df_coaches.groupby(['School', 'Coach'])):
# #     list_tenures = extract_all_tenures(grp)
# #     for df_tenure in list_tenures:
# #         df_tenure['tenure_index'] = [idx_tenure] * len(df_tenure)
# #         if len(df_final) == 0:
# #             df_final = df_tenure.copy()
# #         else:
# #             df_final = df_final.append(df_tenure.copy())
# #         idx_tenure = idx_tenure + 1

# # df_final = pd.DataFrame()
# # idx_tenure = 0;
# # for tup, grp in df_coaches.groupby(['School', 'Coach']):
# #     list_tenures = extract_all_tenures(grp)
# #     for df_tenure in list_tenures:
# #         df_tenure['tenure_index'] = [idx_tenure] * len(df_tenure)
# #         if len(df_final) == 0:
# #             df_final = df_tenure.iloc[[-1],:].copy()
# #         else:
# #             df_final = df_final.append(df_tenure.iloc[[-1],:].copy())
# #         idx_tenure = idx_tenure + 1

# # 1. Isolate all FBS coaches since  1971 at their 40th game
# df_subset = df_coaches[df_coaches['G'] == sf_gp]

# # 2. Identify those coaches who share characteristics with Frost
# #   - Winning % less than or equal to 40% (Frost is at 37.5%)
# #   - 0 appearances
# #   - 2 or less wins vs. ranked teams (Factor in some fudge factor to Frost's record)

# oops = df_subset[(df_subset['Win_Pct_at_SF'] <= .375) &
#                  (df_subset['Bowl_G'] <= 0) & 
#                  (df_subset['W_vs_Rank'] <= 2) &
#                  (df_subset['Winning_Sns'] == 0) &
#                  (df_subset['Win_Pct_vs_Winning'] <= float(sf['Win_Pct_vs_Winning'])) & 
#                  (df_subset['Win_Pct_P5'] <= float(sf['Win_Pct_P5'])) & 
#                  (df_subset['Win_Pct_Conf'] <= float(sf['Win_Pct_Conf']))]
# oops = oops[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Winning_Sns', 
#          'Sn', 'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning',
#          'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 
#          'Bowl_G', 'Win_Pct_at_SF', 'AP_Post_25_count', 'AP_Post_10_count', 
#          'AP_Post_5_count',
#          'Weeks_Ranked', 'Weeks_Ranked_Pct.', 'Tenure_Index']]

# # 3. Extract final end-of-tenure stats for each coach (i.e. final season)
# df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(oops['Tenure_Index']))]
# df = pd.DataFrame()
# idx_tenure = 0;
# for tup, grp in df_match.groupby(['School', 'Coach']):
#     list_tenures = extract_all_tenures(grp)
#     for df_tenure in list_tenures:
#         df_tenure['Tenure_Index'] = [idx_tenure] * len(df_tenure)
#         if len(df) == 0:
#             df = df_tenure.iloc[[-1],:].copy()
#         else:
#             df = df.append(df_tenure.iloc[[-1],:].copy())
#         idx_tenure = idx_tenure + 1

# # 4. Drop unneeded columns
# df = df[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Winning_Sns', 
#          'Sn', 'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning',
#          'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 
#          'Bowl_G', 'Win_Pct_at_SF', 'AP_Post_25_count', 'AP_Post_10_count', 
#          'AP_Post_5_count',
#          'Weeks_Ranked', 'Weeks_Ranked_Pct.']]
# # df = df[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Winning_Sns', 
# #          'Sn', 'G', 'W', 'L', 'Win_Pct',
# #          'G_Conf', 'W_Conf', 'L_Conf', 'Win_Pct_Conf',
# #          'G_P5', 'W_P5', 'L_P5', 'Win_Pct_P5',
# #          'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 'Win_Pct_vs_Winning',
# #          'G_vs_Winning_Conf', 'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 'Win_Pct_vs_Winning_Conf',
# #          'W_vs_Rank', 'L_vs_Rank', 'Win_Pct_vs_Rank', 
# #          'W_Sn', 'L_Sn', 'Win_Pct_Sn', 'W_Sn_Conf', 'L_Sn_Conf', 'Win_Pct_Sn_Conf',
# #          'Bowl_G', 'Bowl_W', 'Bowl_L', 'Win_Pct_Bowl', 'Win_Pct_at_SF',
# #          'AP_Pre_count', 'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count',
# #          'Weeks_Ranked', 'Weeks_Ranked_Pct.']]

# #------------------------------------------------------------------------------
# # All Time (End of Year 4) 
# #   - No winning season
# #   - No bowl games
# #   - No wins over Top 25 teams
# #       * or some variation of that
# #   - No winning seasons in conference
# #------------------------------------------------------------------------------
# # 1. Isolate all FBS coaches since  1971 at the end of year 4
# df_yr4 = pd.DataFrame()
# for tup, grp in df_coaches.groupby(['Tenure_Index', 'Coach', 'Sn']):
#     # add the last game of the 4th year to the master dataframe
#     if tup[2] == 4:
#         if len(df_yr4) == 0:
#             df_yr4 = grp.iloc[[-1],:].copy()
#         else:
#             df_yr4 = df_yr4.append(grp.iloc[[-1],:].copy())
# # Find Ron Meyer's tenure and drop it from the list
# df_yr4 = df_yr4[df_yr4['Coach'] != 'Ron Meyer']

# # 2. Identify those coaches who share characteristics with Frost
# #   - Winning % less than or equal to 39% (assumed record of 17-44 or worse)
# #   - 0 winning seasons
# #   - 0 bowl appearances
# #   - 1 or less wins vs. ranked teams (Factor in some fudge factor to Frost's record)

# # oops = df_yr4[(df_yr4['Win_Pct_at_SF'] < .39) &
# #               (df_yr4['Winning_Sns'] <= 0) &
# #               (df_yr4['Bowl_G'] <= 0) & 
# #               (df_yr4['W_vs_Rank'] <= 1)
# #               ]

# # oops = df_yr4[(df_yr4['Winning_Sns'] <= 0) &
# #               (df_yr4['Bowl_G'] <= 0) & 
# #               (df_yr4['W_vs_Rank'] <= 1)
# #               ]

# oops = df_yr4[(df_yr4['Winning_Sns'] <= 0) &
#               (df_yr4['Bowl_G'] <= 0)
#               ]

# # oops = df_yr4[(df_yr4['Win_Pct_at_SF'] < .39) &
# #               (df_yr4['Winning_Sns'] <= 0) &
# #               (df_yr4['Bowl_G'] <= 0) & 
# #               (df_yr4['W_vs_Rank'] == 0)
# #               ]

# # 3. Extract final end-of-tenure stats for each coach (i.e. final season)
# df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(oops['Tenure_Index']))]
# df = pd.DataFrame()
# idx_tenure = 0;
# for tup, grp in df_match.groupby(['School', 'Coach']):
#     list_tenures = extract_all_tenures(grp)
#     for df_tenure in list_tenures:
#         df_tenure['Tenure_Index'] = [idx_tenure] * len(df_tenure)
#         if len(df) == 0:
#             df = df_tenure.iloc[[-1],:].copy()
#         else:
#             df = df.append(df_tenure.iloc[[-1],:].copy())
#         idx_tenure = idx_tenure + 1

# # 4. Drop unneeded columns
# df = df[['Season', 'School', 'Coach', 'Conf', 'Power5', 'G', 'Winning_Sns', 
#          'Sn', 'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning',
#          'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 
#          'Bowl_G', 'Win_Pct_at_SF',
#          'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count',
#          'Weeks_Ranked', 'Weeks_Ranked_Pct.']]

# ts = datetime.date.fromtimestamp(time.time())
# df.to_csv(r'data\processed\Coaches\year_4_no_winning_seasons_{ts}.csv', index = False)

# #------------------------------------------------------------------------------
# # Subset the data to coaches have coached at least the same number of games as Scott
# df_history = df_coaches[df_coaches['G'] >= sf_gp]
# df_history = df_history.reset_index(drop = True)

# # Create a subset snap-shot to isolate all coaching records to match Scott's timeframe (i.e. Games coached)
# df_snapshot = df_coaches[df_coaches['G'] == sf_gp]
# df_snapshot = df_snapshot.reset_index(drop = True)

# # Isolate Scott Frost's Winning %
# sf_win_pct = float(df_yr_4[df_yr_4['coach'] == 'Scott Frost']['cum_win_pct'])

# # Subset the data to be only coaches within the last 25 years
# df_yr_4 = df_yr_4[df_yr_4['year'] >= 1991]

# # # Save coaches with 4 or more years of tenure to disk
# # ts = datetime.date.fromtimestamp(time.time())
# # df_yr_4.to_csv(rf'data\raw\Coaches\coaching_history_year_3_{ts}.csv', index = False)

# # Subset the data to coaches with a winning percentage the same as or worse than Scott
# df_bad = df_yr_4[df_yr_4['cum_win_pct'] < sf_win_pct]

# # Save coaches who are as bad as Scott (or worse) to disk
# ts = datetime.date.fromtimestamp(time.time())
# df_bad.to_csv(rf'data\raw\Coaches\coaching_history_bad_{ts}.csv', index = False)

# pd.DataFrame.mean(df_bad['total_win_pct'])
# pd.DataFrame.mean(df_bad['total_seasons'])

# #------------------------------------------------------------------------------
# # Visualize Results
# #------------------------------------------------------------------------------
# import plotly.graph_objects as go
# import plotly.express as px

# # data
# label = ['Coaching Tenures Since 1970','Year 3, 29+ Games Coached','Did Not Last',
#          'Win % >= 40.6','Win % < 40.6', '.500 record or better', 'Worse than .500 record', 'Multiple 10 Top AP Seasons']
# source = [0, 0 ,1, 1, 4, 4, 5]
# target = [1, 2, 3, 4, 5, 6, 7]
# value = [835, 362, 523, 312, 26, 286, 6]
# # data to dict, dict to sankey
# link = dict(source = source, target = target, value = value)
# node = dict(label = label, pad=50, thickness=5)
# data = go.Sankey(link = link, node=node)
# # plot
# fig = go.Figure(data)
# fig.show()