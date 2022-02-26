#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 09:39:36 2021

@author: reideej1

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import glob
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
# path_dir = pathlib.Path(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis')
path_dir = pathlib.Path(os.getcwd())
if 'cfbAnalysis' not in str(path_dir):
    path_dir = path_dir.joinpath('cfbAnalysis')
os.chdir(path_dir)

# Scrape Data for all coaches at 44 games coached
games_sf = 44

# Ingest the most recent game-by-game history file
df_all_games = pd.read_csv(max(glob.iglob(
    r'data\raw\Team History\ALL_records*.csv'), key=os.path.getmtime))

# Ingest the most recent year-by-year history file
df_schools = pd.read_csv(max(glob.iglob(
    r'data\raw\Team History\team_history*.csv'), key=os.path.getmtime))

# Merge game-by-game data with year-by-year data
df_coaches = create_week_by_week_dataframe(df_all_games, df_schools, games_sf)

# Save coaching data to disk
ts = datetime.date.fromtimestamp(time.time())
df_coaches.to_csv(rf'data\processed\Coaches\coaching_history_{ts}_44_games.csv', 
                  index = False)

#------------------------------------------------------------------------------
'''
    At Game 44, what are Frost's future prospects
    
    The following code will analyze the 5 remaining scenarios for Scott Frost in 2021
    
    After 44 games played
        - Goes 3-9, no bowl, no winning season, no wins over Top 25 teams
        - Goes 4-8, no bowl, no winning season, 0 or 1 wins over Top 25 teams
        - Goes 5-7, no bowl, no winning season, 0, 1 or 2 wins over Top 25 teams
        - Goes 6-6, 1 bowl, no winning season, 0, 1 or 2 wins over Top 25 teams
        - Goes 7-5, 1 bowl, 1 winning season, 0, 1 or 2 wins over Top 25 teams
'''
#------------------------------------------------------------------------------
# 1 grab most recent version of 44 game file
df_coaches = pd.read_csv(max(glob.iglob(
    r'data\processed\Coaches\coaching_history*_44_games.csv'), key=os.path.getmtime))

# 2. Drop unneeded columns
df_coaches = df_coaches[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Winning_Sns', 
                         'Sn', 'G', 'W', 'L', 'Win_Pct',
                         'G_Conf', 'W_Conf', 'L_Conf', 'Win_Pct_Conf',
                         'G_P5', 'W_P5', 'L_P5', 'Win_Pct_P5',
                         'G_vs_Winning', 'W_vs_Winning', 'L_vs_Winning', 
                         'Win_Pct_vs_Winning',
                         'G_vs_Winning_Conf', 'W_vs_Winning_Conf', 'L_vs_Winning_Conf', 
                         'Win_Pct_vs_Winning_Conf',
                         'W_vs_Rank', 'L_vs_Rank', 'Win_Pct_vs_Rank', 
                         'Bowl_G', 'Bowl_W', 'Bowl_L', 'Win_Pct_Bowl', 'Win_Pct_at_SF',
                         'AP_Pre_count', 'AP_Post_25_count', 
                         'AP_Post_10_count', 'AP_Post_5_count',
                         'Weeks_Ranked', 'Weeks_Ranked_Pct.', 'Tenure_Index']]

# 3. Isolate all FBS coaches since  1971 at the end of their 4th season
df_year_4 = df_coaches[df_coaches['Sn'] == 4]
# Extract the last-game for each coach at the end of their 4th season
df_subset = pd.DataFrame()
for tup, grp in tqdm.tqdm(df_year_4.groupby('Tenure_Index')):
    if len(df_subset) == 0:
        df_subset = grp.iloc[[-1],:].copy()
    else:
        df_subset = df_subset.append(grp.iloc[[-1],:].copy())
#------------------------------------------------------------------------------
# Outcome D. Go 3-1 in final 4 games
#   - Final record of 6-6, 1 bowl, no winning season, 0, 1 or 2 wins over Top 25 teams
#------------------------------------------------------------------------------
df_match_frost = df_subset[(df_subset['Win_Pct'] <= .41) &
                           (df_subset['Bowl_G'] <= 1) & 
                           (df_subset['W_vs_Rank'] <= 2) &
                           (df_subset['Winning_Sns'] == 0)]

# Extract final end-of-tenure stats for each coach (i.e. final season)
df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(df_match_frost['Tenure_Index']))]
df_last_sn = pd.DataFrame()
idx_tenure = 0;
for tup, grp in tqdm.tqdm(df_match.groupby(['School', 'Coach'])):
    if len(df_last_sn) == 0:
        df_last_sn = grp.iloc[[-1],:].copy()
    else:
        df_last_sn = df_last_sn.append(grp.iloc[[-1],:].copy())
df_p5 = df_last_sn[df_last_sn['Power5'] == True]
        
print('Outcome C: 2-2 in final 4 games')
print(f'Total Coaches: {len(df_last_sn)}')
print(f'Total FBS Coaches: {df_last_sn.Power5.value_counts()[1]}')
print(f'Median Tenure: {df_last_sn.Sn.median()}')
print(f'Median Games Coached: {df_last_sn.G.median()}')
print(f'Total Coaches with Winning Seasons: {df_last_sn.Winning_Sns.ge(1).sum()}')
print(f'Total Coaches with Bowl Games: {df_last_sn.Bowl_G.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 25: {df_last_sn.AP_Post_25_count.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 10: {df_last_sn.AP_Post_10_count.ge(1).sum()}')
   
'''
    The six coaches who ever had a team finish in the AP Top 25    
        - Ron Meyer at SMU (only coach with a top 10 finish)
            * last coached in 1981
            * program was on suspension and later received the death penalty
        - Mike Neu at Ball St. (Active)
        - David Cutcliffe at Duke (Active) 
        - Lee Corse at Indiana (last year at school: 1982)
        - Dan McCarney at Iowa State (last year at school: 2006)
        - Greg Schanio at Rutgers (tenure that ended in 2011)
        
    Ron Meyer had 2 teams finish in the Top 25, the rest only did it 1 time
    
    Only 1 coach had a team ranked in the preseason Top 25 
        * the 1 year they also finished ranked in the postseason Top 25
'''


#------------------------------------------------------------------------------
# Outcome A. Go 0-4 in final 4 games
#   - Final record of 3-9, no bowl, no winning season, no wins over Top 25 teams
#------------------------------------------------------------------------------
win_0 = df_subset[(df_subset['Win_Pct_at_SF'] <= .341) &
                  (df_subset['Bowl_G'] == 0) &
                  (df_subset['W_vs_Rank'] == 0) &
                  (df_subset['Winning_Sns'] == 0)]

# Extract final end-of-tenure stats for each coach (i.e. final season)
df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(win_0['Tenure_Index']))]
df_last_sn = pd.DataFrame()
idx_tenure = 0;
for tup, grp in tqdm.tqdm(df_match.groupby(['School', 'Coach'])):
    if len(df_last_sn) == 0:
        df_last_sn = grp.iloc[[-1],:].copy()
    else:
        df_last_sn = df_last_sn.append(grp.iloc[[-1],:].copy())
        
print('Outcome A: 0-4 in final 4 games')
print(f'Total Coaches: {len(df_last_sn)}')
print(f'Total FBS Coaches: {df_last_sn.Power5.value_counts()[1]}')
print(f'Median Tenure: {df_last_sn.Sn.median()}')
print(f'Median Games Coached: {df_last_sn.G.median()}')
print(f'Total Coaches with Winning Seasons: {df_last_sn.Winning_Sns.ge(1).sum()}')
print(f'Total Coaches with Bowl Games: {df_last_sn.Bowl_G.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 25: {df_last_sn.AP_Post_25_count.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 10: {df_last_sn.AP_Post_10_count.ge(1).sum()}')
   
'''
    The three coaches who ever had a team finish in the AP Top 25    
        - David Cutcliffe at Duke (Active) 
        - Dan McCarney at Iowa State (last year at school: 2006)
        - Greg Schanio at Rutgers (tenure that ended in 2011)
        
    All of them only did it 1 time    
    
    Only 1 coach had a team ranked in the preseason Top 25 
        * the 1 year they also finished ranked in the postseason Top 25
'''
     
#------------------------------------------------------------------------------
# Outcome B. Go 1-3 in final 4 games
#   - Final record of 4-8, no bowl, no winning season, 0 or 1 wins over Top 25 teams
#------------------------------------------------------------------------------
win_1 = df_subset[(df_subset['Win_Pct_at_SF'] <= .364) &
                  (df_subset['Bowl_G'] == 0) & 
                  (df_subset['W_vs_Rank'] <= 1) &
                  (df_subset['Winning_Sns'] == 0)]

# Extract final end-of-tenure stats for each coach (i.e. final season)
df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(win_1['Tenure_Index']))]
df_last_sn = pd.DataFrame()
idx_tenure = 0;
for tup, grp in tqdm.tqdm(df_match.groupby(['School', 'Coach'])):
    if len(df_last_sn) == 0:
        df_last_sn = grp.iloc[[-1],:].copy()
    else:
        df_last_sn = df_last_sn.append(grp.iloc[[-1],:].copy())
        
print('Outcome B: 1-3 in final 4 games')
print(f'Total Coaches: {len(df_last_sn)}')
print(f'Total FBS Coaches: {df_last_sn.Power5.value_counts()[1]}')
print(f'Median Tenure: {df_last_sn.Sn.median()}')
print(f'Median Games Coached: {df_last_sn.G.median()}')
print(f'Total Coaches with Winning Seasons: {df_last_sn.Winning_Sns.ge(1).sum()}')
print(f'Total Coaches with Bowl Games: {df_last_sn.Bowl_G.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 25: {df_last_sn.AP_Post_25_count.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 10: {df_last_sn.AP_Post_10_count.ge(1).sum()}')
   
'''
    The five coaches who ever had a team finish in the AP Top 25    
        - Ron Meyer at SMU (only coach with a top 10 finish)
            * last coached in 1981
            * program was on suspension and later received the death penalty
        - David Cutcliffe at Duke (Active) 
        - Lee Corse at Indiana (last year at school: 1982)
        - Dan McCarney at Iowa State (last year at school: 2006)
        - Greg Schanio at Rutgers (tenure that ended in 2011)
        
    Ron Meyer had 2 teams finish in the Top 25, the rest only did it 1 time
    
    Only 1 coach had a team ranked in the preseason Top 25 
        * the 1 year they also finished ranked in the postseason Top 25
'''
     
#------------------------------------------------------------------------------
# Outcome C. Go 2-2 in final 4 games
#   - Final record of 5-7, no bowl, no winning season, 0, 1 or 2 wins over Top 25 teams
#------------------------------------------------------------------------------
win_2 = df_subset[(df_subset['Win_Pct_at_SF'] <= .387) &
                  (df_subset['Bowl_G'] == 0) & 
                  (df_subset['W_vs_Rank'] <= 2) &
                  (df_subset['Winning_Sns'] == 0)]

# Extract final end-of-tenure stats for each coach (i.e. final season)
df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(win_2['Tenure_Index']))]
df_last_sn = pd.DataFrame()
idx_tenure = 0;
for tup, grp in tqdm.tqdm(df_match.groupby(['School', 'Coach'])):
    if len(df_last_sn) == 0:
        df_last_sn = grp.iloc[[-1],:].copy()
    else:
        df_last_sn = df_last_sn.append(grp.iloc[[-1],:].copy())
        
print('Outcome C: 2-2 in final 4 games')
print(f'Total Coaches: {len(df_last_sn)}')
print(f'Total FBS Coaches: {df_last_sn.Power5.value_counts()[1]}')
print(f'Median Tenure: {df_last_sn.Sn.median()}')
print(f'Median Games Coached: {df_last_sn.G.median()}')
print(f'Total Coaches with Winning Seasons: {df_last_sn.Winning_Sns.ge(1).sum()}')
print(f'Total Coaches with Bowl Games: {df_last_sn.Bowl_G.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 25: {df_last_sn.AP_Post_25_count.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 10: {df_last_sn.AP_Post_10_count.ge(1).sum()}')
   
'''
    The five coaches who ever had a team finish in the AP Top 25    
        - Ron Meyer at SMU (only coach with a top 10 finish)
            * last coached in 1981
            * program was on suspension and later received the death penalty
        - David Cutcliffe at Duke (Active) 
        - Lee Corse at Indiana (last year at school: 1982)
        - Dan McCarney at Iowa State (last year at school: 2006)
        - Greg Schanio at Rutgers (tenure that ended in 2011)
        
    Ron Meyer had 2 teams finish in the Top 25, the rest only did it 1 time
    
    Only 1 coach had a team ranked in the preseason Top 25 
        * the 1 year they also finished ranked in the postseason Top 25
'''

#------------------------------------------------------------------------------
# Outcome D. Go 3-1 in final 4 games
#   - Final record of 6-6, 1 bowl, no winning season, 0, 1 or 2 wins over Top 25 teams
#------------------------------------------------------------------------------
win_3 = df_subset[(df_subset['Win_Pct_at_SF'] <= .41) &
                  (df_subset['Bowl_G'] <= 1) & 
                  (df_subset['W_vs_Rank'] <= 2) &
                  (df_subset['Winning_Sns'] == 0)]

# Extract final end-of-tenure stats for each coach (i.e. final season)
df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(win_3['Tenure_Index']))]
df_last_sn = pd.DataFrame()
idx_tenure = 0;
for tup, grp in tqdm.tqdm(df_match.groupby(['School', 'Coach'])):
    if len(df_last_sn) == 0:
        df_last_sn = grp.iloc[[-1],:].copy()
    else:
        df_last_sn = df_last_sn.append(grp.iloc[[-1],:].copy())
        
<<<<<<< HEAD
print('Outcome C: 2-2 in final 4 games')
=======
print('Outcome D: 3-1 in final 4 games')
>>>>>>> cad461064c4abc0337572911242823e11ab1910a
print(f'Total Coaches: {len(df_last_sn)}')
print(f'Total FBS Coaches: {df_last_sn.Power5.value_counts()[1]}')
print(f'Median Tenure: {df_last_sn.Sn.median()}')
print(f'Median Games Coached: {df_last_sn.G.median()}')
print(f'Total Coaches with Winning Seasons: {df_last_sn.Winning_Sns.ge(1).sum()}')
print(f'Total Coaches with Bowl Games: {df_last_sn.Bowl_G.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 25: {df_last_sn.AP_Post_25_count.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 10: {df_last_sn.AP_Post_10_count.ge(1).sum()}')
   
'''
    The six coaches who ever had a team finish in the AP Top 25    
        - Ron Meyer at SMU (only coach with a top 10 finish)
            * last coached in 1981
            * program was on suspension and later received the death penalty
        - Mike Neu at Ball St. (Active)
        - David Cutcliffe at Duke (Active) 
        - Lee Corse at Indiana (last year at school: 1982)
        - Dan McCarney at Iowa State (last year at school: 2006)
        - Greg Schanio at Rutgers (tenure that ended in 2011)
        
    Ron Meyer had 2 teams finish in the Top 25, the rest only did it 1 time
    
    Only 1 coach had a team ranked in the preseason Top 25 
        * the 1 year they also finished ranked in the postseason Top 25
'''
#------------------------------------------------------------------------------
# Outcome E. Go 4-0 in final 4 games
#   - Final record of 7-5, 1 bowl, 1 winning season, 0, 1 or 2 wins over Top 25 teams
#------------------------------------------------------------------------------
win_4 = df_subset[(df_subset['Win_Pct_at_SF'] <= .432) &
                  (df_subset['Bowl_G'] <= 1) & 
                  (df_subset['W_vs_Rank'] <= 2) &
                  (df_subset['Winning_Sns'] <= 1)]

# Extract final end-of-tenure stats for each coach (i.e. final season)
df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(win_4['Tenure_Index']))]
df_last_sn = pd.DataFrame()
idx_tenure = 0;
for tup, grp in tqdm.tqdm(df_match.groupby(['School', 'Coach'])):
    if len(df_last_sn) == 0:
        df_last_sn = grp.iloc[[-1],:].copy()
    else:
        df_last_sn = df_last_sn.append(grp.iloc[[-1],:].copy())
        
<<<<<<< HEAD
print('Outcome C: 2-2 in final 4 games')
=======
print('Outcome E: 4-0 in final 4 games')
>>>>>>> cad461064c4abc0337572911242823e11ab1910a
print(f'Total Coaches: {len(df_last_sn)}')
print(f'Total FBS Coaches: {df_last_sn.Power5.value_counts()[1]}')
print(f'Median Tenure: {df_last_sn.Sn.median()}')
print(f'Median Games Coached: {df_last_sn.G.median()}')
print(f'Total Coaches with Winning Seasons: {df_last_sn.Winning_Sns.ge(1).sum()}')
print(f'Total Coaches with Bowl Games: {df_last_sn.Bowl_G.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 25: {df_last_sn.AP_Post_25_count.ge(1).sum()}')
print(f'Total Coaches with Teams Ranked in Post-Season AP Top 10: {df_last_sn.AP_Post_10_count.ge(1).sum()}')
   
'''
    This is the land of hope for Scott Frost:
        
    22 coaches had teams finish in the AP-25, but only 8 did it at least 2 times
        - Ron Turner at Illinois (last year at school: 2004)
        - Larry Smith at Missouri (last year at school: 2000)
        - Howard Schnellenberger at Louisville (last year at school: 1994)
        - Walt Harris at Pittsburgh (last year at school: 2004)
        - Glen Mason at Kansas (last year at school: 1996)
        - Ron Meyer at SMU (last year at school: 1981)
        - Bill Snyder at Kansas St. (last year at school: 2005)
        - Bill McCartney at Colorado (last year at school: 1994)
    
    Only 2 coaches did it 3 or more times:
        - Bill Snyder at Kansas St. (last year at school: 2005)
        - Bill McCartney at Colorado (last year at school: 1994)
'''