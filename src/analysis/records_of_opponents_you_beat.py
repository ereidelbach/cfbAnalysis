# Ingest the most recent game-by-game history file
df_all_games = pd.read_csv(max(glob.iglob(
    r'data\raw\Team History\ALL_records*.csv'), key=os.path.getmtime))

# Ingest the most recent year-by-year history file
df_schools = pd.read_csv(max(glob.iglob(
    r'data\raw\Team History\team_history*.csv'), key=os.path.getmtime))

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
                           df_schools[['School', 'Year', 'Overall_W', 'Overall_L', 'Overall_Pct', 'Conf_Pct']],
                           left_on = ['Season', 'Opponent'],
                           right_on = ['Year', 'School'])
df_team_records = df_team_records.drop_duplicates()
df_team_records = df_team_records[['Season', 'School', 'Overall_W', 'Overall_L', 'Overall_Pct', 'Conf_Pct']]
df_team_records = df_team_records.rename(columns = {'Overall_W':'Opp_W',
                                                    'Overall_L':'Opp_L',
                                                    'Overall_Pct':'Win_Pct_Opp',
                                                    'Conf_Pct':'Win_Pct_Conf_Opp',
                                                    'School':'Opponent'})
df_coaches = pd.merge(df_coaches, df_team_records, how = 'left', on = ['Season', 'Opponent'])

df_coaches_small = df_coaches[df_coaches['Season'] >= 2018]
df_coaches_small = df_coaches_small[df_coaches_small['Conf'] == 'Big Ten']
df_coaches_small = df_coaches_small[['Season', 'Week', 'School', 'Opponent', 
                                     'Result', 'Streak', 
                                     'Opp_W', 'Opp_L', 'Win_Pct_Opp']]

# list_data = []
# for season, grp in df_coaches_small.groupby(['Season', 'School']):
#     year   = season[0]
#     school = season[1]
#     wins   = round(grp['Opp_W'].mean(),1)
#     losses = round(grp['Opp_L'].mean(),1)
#     list_data.append([year, school, wins, losses])
    
# df_opp_record = pd.DataFrame(list_data, columns = ['Season', 'School', 'Wins', 'Losses'])

list_data = []
for school, grp in df_coaches_small.groupby(['School']):
    team   = school
    # subset to just wins
    grp_wins = grp[grp['Result'] == 'W']
    wins   = round(grp_wins['Opp_W'].mean(),1)
    losses = round(grp_wins['Opp_L'].mean(),1)
    win_pct = round(grp_wins['Opp_W'].sum()/(grp_wins['Opp_W'].sum() + grp_wins['Opp_L'].sum()),2)
    list_data.append([team, wins, losses, win_pct])
    
df_opp_record = pd.DataFrame(list_data, columns = ['School', 'Wins', 'Losses', 'Win Pct.'])