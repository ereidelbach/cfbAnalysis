import glob
import os
import pandas as pd

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

#------------------------------------------------------------------------------
# Start of Scott Frost Analysis (DO THIS BEFORE ALL OTHER ANALYSIS)
#------------------------------------------------------------------------------
# Ingest the most recent coaching history file
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

#------------------------------------------------------------------------------
# All Time (End of Year 4) 
#   - No winning season
#   - No bowl games
#   - No wins over Top 25 teams
#       * or some variation of that
#   - No winning seasons in conference
#------------------------------------------------------------------------------
# 1. Isolate all FBS coaches since  1936 at the end of year 4
df_yr4 = pd.DataFrame()
for tup, grp in df_coaches.groupby(['Tenure_Index', 'Coach', 'Sn']):
    # add the last game of the 4th year to the master dataframe
    if tup[2] == 4:
        if len(df_yr4) == 0:
            df_yr4 = grp.iloc[[-1],:].copy()
        else:
            df_yr4 = df_yr4.append(grp.iloc[[-1],:].copy())
# 1. Find Ron Meyer's tenure and drop it from the list
#       - You don't get counted for getting your school the death penalty
df_yr4 = df_yr4[df_yr4['Coach'] != 'Ron Meyer']

# 2. Identify those coaches who share characteristics with Frost
#   - 0 winning seasons
#   - 0 bowl appearances
oops = df_yr4[(df_yr4['Winning_Sns'] <= 0) &
              (df_yr4['Bowl_G'] <= 0)
              ]
oops2 = df_yr4[(df_yr4['Winning_Sns'] <= 0) &
              (df_yr4['Bowl_G'] <= 1)
              ]

# 3. Extract final end-of-tenure stats for each coach (i.e. final season)
df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(oops2['Tenure_Index']))]
df = pd.DataFrame()
for tup, grp in df_match.groupby(['School', 'Coach']):
    list_tenures = extract_all_tenures(grp)
    for df_tenure in list_tenures:
        if len(df) == 0:
            df = df_tenure.iloc[[-1],:].copy()
        else:
            df = df.append(df_tenure.iloc[[-1],:].copy())

# 4. Drop unneeded columns
df = df[['Season', 'School', 'Coach', 'Conf', 'Power5', 'G', 'Sn', 'Winning_Sns', 
         'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 'Win_Pct_vs_Winning',
         'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 
         'Bowl_G', 'AP_Post_25_count', 'AP_Post_10_count', 'AP_Post_5_count',
         'Weeks_Ranked', 'Weeks_Ranked_Pct.']]
df = df.reset_index(drop = True)

# 5. Save to disk
ts = datetime.date.fromtimestamp(time.time())
df.to_csv(rf'data\processed\Coaches\year_4_no_winning_seasons_{ts}.csv', index = False)

# 6. Isolate coaches who made it to Year 5 after 4 straight losing seasonste
df_yr_5 = df_coaches[(df_coaches['Tenure_Index'].isin(oops2['Tenure_Index'])) & (df_coaches['Sn'] == 5)]
df_match = df_coaches[df_coaches['Tenure_Index'].isin(list(df_yr_5['Tenure_Index']))]
df_5 = pd.DataFrame()
for tup, grp in df_match.groupby(['School', 'Coach']):
    list_tenures = extract_all_tenures(grp)
    for df_tenure in list_tenures:
        if len(df_5) == 0:
            df_5 = df_tenure.iloc[[-1],:].copy()
        else:
            df_5 = df_5.append(df_tenure.iloc[[-1],:].copy())
df_5 = df_5[['Season', 'School', 'Coach', 'Conf', 'Power5', 'G', 'Sn', 
             'Winning_Sns', 'Win_Pct', 'Win_Pct_Conf', 'Win_Pct_P5', 
             'Win_Pct_vs_Winning', 'Win_Pct_vs_Winning_Conf', 'Win_Pct_vs_Rank', 
             'Bowl_G', 'AP_Post_25_count', 'AP_Post_10_count', 
             'AP_Post_5_count', 'Weeks_Ranked', 'Weeks_Ranked_Pct.']]
df_5 = df_5.reset_index(drop = True)

# 7. Save to disk
ts = datetime.date.fromtimestamp(time.time())
df_5.to_csv(rf'data\processed\Coaches\year_5_no_winning_seasons_after_year_4{ts}.csv', index = False)


#------------------------------------------------------------------------------
# How many coaches have lost 6 games in a row?? 
#
#   1936 - 2021
#
#------------------------------------------------------------------------------
# Ingest the most recent coaching history file
df_coaches = pd.read_csv(max(glob.iglob(
    r'data\processed\Coaches\coaching_history*.csv'), key=os.path.getmtime))
df_coaches = df_coaches.apply(pd.to_numeric, errors = 'ignore')

# Restrict data to those coaches who lost 6 or more games in a row in a single season
df_losers = df_coaches[df_coaches['Streak'] == 'L 6']
df_losers = df_losers[['Season', 'School', 'Coach', 'Conf', 'Power5', 'Tenure_Index']] 

# Count how many times each coach appears at the same school with a 6 game losing streak
df_losers['count'] = df_losers.groupby(['School', 'Coach']).cumcount()+1

# How many coaches have done it twice at any level (since 1936)
df_losers = df_losers[df_losers['count'] >= 2]

# Iterate through all coaches and keep the most recent record for the coach
df_final = pd.DataFrame()
for tup, grp in df_losers.groupby(['School', 'Coach']):
    # if grp['Coach'].values[0] == 'Pat Fitzgerald':
    #     break
    if len(df_final) == 0:
        df_final = grp.iloc[[-1],:].copy()
    else:
        df_final = df_final.append(grp.iloc[[-1],:].copy())

# How many did this at the Powe5 level
df_p5 = df_final[df_final['Power5'] == True]
# How many did this in the Big Ten
df_bigten = df_final[df_final['Conf'] == 'Big Ten']