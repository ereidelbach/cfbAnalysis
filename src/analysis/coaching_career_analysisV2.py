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
            df_coach['cum_win_pct'] = df_coach.apply(lambda row: row['cum_W'] / row['cum_GP'] if row['cum_GP'] != 0 else 0, axis = 1)
    else:
        df_coach['cum_win_pct'] = df_coach.apply(lambda row: row['cum_W'] / row['cum_GP'] if row['cum_GP'] != 0 else 0, axis = 1)
    
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

def create_week_by_week_dataframe(df_all_games, df_schools):
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
            
    Outputs
    -------
        df_engineered : Pandas DataFrame
            A dataframe containing all historic week-by-week results infused
                with coaches' names
    '''           
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
        elif school[0] == 'Utah State' and school[1] == 2021:
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
    
    # rename/reorder columns    
    df_coaches = df_coaches.rename(columns = {'G':'Week',
                                              'Year':'Season',
                                              'Opp':'Pts_Opp',
                                              'Cum_W':'W_Sn',
                                              'Cum_L':'L_Sn',
                                              'T':'T_Sn'})
    df_coaches = df_coaches[['Season', 'Week', 'Date', 'Day', 'Rank', 'School', 
                             'Coach', 'Conf', 'Home_Away', 'Rank_Opp', 'Opponent', 
                             'Conf_Opp', 'Result', 'Pts', 'Pts_Opp', 'W_Sn', 
                             'L_Sn', 'T_Sn', 'AP_Pre', 'AP_High', 'AP_Post', 
                             'Notes', 'Bowl', 'url_boxscore']]
    
    # Engineer variables for each coach's stint/tenure at a given school
    df_engineered = pd.DataFrame()
    for index, grp in df_coaches.groupby(['School', 'Coach']):
        if len(df_engineered) == 0:
            df_engineered = add_tenure_features(grp)
        else:
            df_engineered = df_engineered.append(add_tenure_features(grp))
        
    return df_engineered

def add_tenure_features(df_coach):
    '''
    Purpose: Manage the engineering of features across a coach's tenure at a
        a given school (while also accounting for those coaches who have 
        multiple coaching stints/tenures at the same school)

    Inputs   
    ------
        df_coach : Pandas DataFrame
            Contains data for all seasons a coach has coached at a given school
            
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
                df_stint = df_coach[df_coach['Season'] <= year_stint_end]
            # handle coaching stints 2 through num_stints - 1
            elif stint_count < num_stints-1:
                year_stint_end = list_stint_end[stint_count]
                year_stint_end_prev = list_stint_end[stint_count-1]
                df_stint = df_coach[df_coach['Season'] <= year_stint_end]
                df_stint = df_stint[df_stint['Season'] > year_stint_end_prev]
            # handle the last coaching stint
            else:
                year_stint_end_prev = list_stint_end[stint_count-1]
                df_stint = df_coach[df_coach['Season'] > year_stint_end_prev]
            # engineer new features and add to coach's tenure dataframe
            if len(df_coach_eng) == 0:
                df_coach_eng = engineer_stint_features(df_stint)
            else:
                df_coach_eng = df_coach_eng.append(engineer_stint_features(df_stint))
            print(f"Coach: {df_stint['Coach'].iloc[0]}, Games: {len(df_stint)}")
    # Step 2.B. Handle coaches with only a single stint at the respective school
    else:
        df_coach_eng = engineer_stint_features(df_coach)
        
    return df_coach_eng
        
def engineer_stint_features(df_tenure):
    '''
    Purpose: Engineer features across a coach's tenure at a given school 

    Inputs   
    ------
        df_tenure : Pandas DataFrame
            Contains data for all seasons in a tenure for a given coach/school combo
            
    Outputs
    -------
        df_tenure : Pandas DataFrame
            Contains input data with newly engineered features 
    '''     
    df_tenure = df_coaches[(df_coaches['School'] == 'Nebraska') & (df_coaches['Coach'] == 'Scott Frost')].copy()
    df_tenure = df_coaches[(df_coaches['Coach'] == 'Mike Riley') & (df_coaches['School'] == 'Oregon State')]
    
    # 0. Total Seasons Coached at School
    df_tenure['Sn'] = df_tenure.groupby(['Season']).ngroup() + 1
    
    # 1. Total games at school
    df_tenure['G'] = list(range(1,len(df_tenure)+1))

    # 2. Total wins at school
    df_tenure['W'] = df_tenure.Result.eq('W').cumsum()
    
    # 3. Total losses at school
    df_tenure['L'] = df_tenure.Result.eq('L').cumsum()
    
    # 4. Total ties at school
    df_tenure['T'] = df_tenure.Result.eq('T').cumsum()
    
    # 5. Total win pct. at school
    if (len(df_tenure) == 1) and (int(df_tenure['G']) == 0):
            df_tenure['Win_Pct'] = 0
    else:
        df_tenure['Win_Pct'] = df_tenure.apply(lambda row: row['W'] / row['G'] 
                                               if row['G'] != 0 else 0, axis = 1)
    
    # 6. Create conf win/loss flag
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
    
    # 7. Total conference games at school
    df_tenure['G_Conf'] = df_tenure.Result_Conf.ne('').cumsum()
             
    # 8. Total conference wins at school
    df_tenure['W_Conf'] = df_tenure.Result_Conf.eq('W').cumsum()
    
    # 9. Total conference losses at school
    df_tenure['L_Conf'] = df_tenure.Result_Conf.eq('L').cumsum()
    
    # 10. Total conference ties at school
    df_tenure['T_Conf'] = df_tenure.Result_Conf.eq('T').cumsum()
    
    # 11. Total conferenc win pct. at school
    if (len(df_tenure) == 1) and (int(df_tenure['G_Conf']) == 0):
            df_tenure['Win_Pct_Conf'] = 0
    else:
        df_tenure['Win_Pct_Conf'] = df_tenure.apply(lambda row: row['W_Conf'] / row['G_Conf'] 
                                               if row['G_Conf'] != 0 else 0, axis = 1)
    # 12. Total bowl games at school
    df_tenure['Bowl'] = df_tenure[['Bowl']].fillna('')
    for idx, grp in df_tenure.groupby(['Season', 'Bowl']).ngroup()+1:
        print(idx)
    
    # 13. Total bowl wins at school
    df_coach['total_bowl_win'] = df_coach['bowl_win'].sum(axis = 0)
    
    # 14. Total AP Preseason rankings
    df_coach['total_ranked_pre'] = df_coach['ranked_pre'].sum(axis = 0)
    
    # 15. Total AP Postseason rankings
    df_coach['total_ranked_post'] = df_coach['ranked_post'].sum(axis = 0)
    
    # 16. Total Top 10 finishes
    df_coach['total_top_10'] = df_coach['ranked_top_10'].sum(axis = 0)
    
    # 17. Total Top 5 finishes
    df_coach['total_top_5'] = df_coach['ranked_top_5'].sum(axis = 0)
    


    
    # Create Total Wins vs. Ranked Teams column     
    
    # Create Total Losses vs. Ranked Teams column
    
    # Create Total Win Pct. vs Ranked Teams column
    
    return df_tenure

#==============================================================================
# Working Code
#==============================================================================
# Set the project working directory
path_dir = pathlib.Path(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis')
os.chdir(path_dir)

#------------------------------------------------------------------------------
# Scrape and compile data for individual team games
#------------------------------------------------------------------------------
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
df_coaches = create_week_by_week_dataframe(df_all_games, df_schools)

# Save coaching data to disk
ts = datetime.date.fromtimestamp(time.time())
df_coaches.to_csv(rf'data\raw\Coaches\coaching_history_{ts}.csv', index = False)

#------------------------------------------------------------------------------
# Start of Scott Frost Analysis
#------------------------------------------------------------------------------
# Ingest the most recent coaching history file
df_coaches = pd.read_csv(max(glob.iglob(r'data\raw\Coaches\coaching_history*.csv'), key=os.path.getmtime))
df_coaches = df_coaches.apply(pd.to_numeric, errors = 'ignore')

# # Subset the data to coaches in year 4
df_yr_4 = df_coaches[df_coaches['season'] == 4]

# Isolate Scott Frost's Games Played
sf_gp = int(df_yr_4[df_yr_4['coach'] == 'Scott Frost']['cum_GP'])

# Subset the data to coaches have coached at least the same number of games as Scott
df_yr_4 = df_yr_4[df_yr_4['cum_GP'] >= sf_gp]

# Isolate Scott Frost's Winning %
sf_win_pct = float(df_yr_4[df_yr_4['coach'] == 'Scott Frost']['cum_win_pct'])

# Subset the data to be only coaches within the last 25 years
df_yr_4 = df_yr_4[df_yr_4['year'] >= 1991]

# # Save coaches with 4 or more years of tenure to disk
# ts = datetime.date.fromtimestamp(time.time())
# df_yr_4.to_csv(rf'data\raw\Coaches\coaching_history_year_3_{ts}.csv', index = False)

# Subset the data to coaches with a winning percentage the same as or worse than Scott
df_bad = df_yr_4[df_yr_4['cum_win_pct'] < sf_win_pct]

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