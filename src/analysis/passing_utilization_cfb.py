import pandas as pd
import glob
import os
import pathlib

def renameSchool(df, name_var):
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
    df_school_names = pd.read_csv(
        r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\raw\school_abbreviations_and_pictures.csv')
     
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
            
    df[name_var] = df[name_var].apply(
            lambda x: dict_school_names[x] if str(x) != 'nan' else '')
        
    return df   

# load all team receiving data for all available years
df_receiving = pd.DataFrame()
dir_stats = r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\interim\CFBStats\ALL\players'
list_fnames = glob.glob(dir_stats + '/receiving_player*.csv')
for fname in list_fnames:
    df_year = pd.read_csv(fname)
    if len(df_receiving) == 0:
        df_receiving = df_year.copy()
    else:
        df_receiving = df_receiving.append(df_year)

# standardize school names
df_receiving = renameSchool(df_receiving, 'team')

# import team stats to integrate with individual stats
path_team = pathlib.Path(os.path.abspath(os.curdir), 'data', 'processed', 'CFBStats', 'team')
files = path_team.glob('*.csv')
latest = max(files, key=lambda f: f.stat().st_mtime)
df_teams = pd.read_csv(latest)

#--- Merge team historic stats with player data to include:
#   A. Add conference to each player row
#   B. Add Power 5 status to each player row
#   C. Add # of wins to each player row (for the season)
#   D. Add # of losses to each player row (for the season)
#   E. Add bowl status to each player row (for the season)     
df_teams = df_teams[['School', 'Year', 'Conf', 'W', 'L', 'T', 'Pct', 'Coach(es)', 'Bowl']]
df_teams = df_teams.rename(columns={'School':'team', 'Year':'season',
    'W':'Team_W', 'L':'Team_L', 'T':'Team_T', 'Pct':'Team_Pct', 'Coach(es)':'Coach'})
df_teams.columns = [x.lower() for x in list(df_teams.columns)]
df_teams['Power5'] = [True if x in ['ACC', 'Big 12', 'Big Ten', 'Pac-12', 'SEC'] 
                      else False for x in df_teams['conf']]
# merge team data with "situational" stats
df_receiving = pd.merge(df_receiving, df_teams, how='left', on=['season', 'team'])

# mark DBs and Athletes as wide receivers
df_receiving['pos'] = df_receiving['pos'].apply(lambda x: 'WR' if x in ['ATH','DB'] else x)
# change any QBs above 10 catches on the season to WRs
df_receiving['pos'] = df_receiving.apply(lambda row: 'WR' if (
    row['pos'] == 'QB' and row['rec.'] >= 10)  else row['pos'], axis = 1)

# group all teams by year -- then determine their total catches/tds/yards by position
df_rec_by_year = df_receiving.groupby(['pos', 'team', 'conf', 'season'])['rec.', 'yards', 'td'].sum()
df_rec_by_year = df_rec_by_year.reset_index()

# calculate % of Catches, TDs and Yards by position group
list_rows = []
for group in df_rec_by_year.groupby(['team', 'conf', 'season'])['rec.', 'yards', 'td']:
    #------------------- CATCHES ----------------------------------------------    
    try:
        catches_wr    = int(group[1][group[1]['pos'] == 'WR']['rec.'])
    except:
        catches_wr    = 0
    try:
        catches_rb    = int(group[1][group[1]['pos'] == 'RB']['rec.'])
    except:
        catches_rb    = 0
    try:
        catches_te    = int(group[1][group[1]['pos'] == 'TE']['rec.'])
    except:
        catches_te    = 0
    try:
        catches_other = int(group[1][~group[1]['pos'].isin(['WR','RB','TE'])]['rec.'])
    except:
        catches_other = 0
            
    try:
        pct_catches_wr    = catches_wr / (catches_wr + catches_rb + catches_te + catches_other)
    except:
        pct_cathces_wr    = 0
    try:
        pct_catches_rb    = catches_rb / (catches_wr + catches_rb + catches_te + catches_other)
    except:
        pct_catches_rb    = 0
    try:
        pct_catches_te    = catches_te / (catches_wr + catches_rb + catches_te + catches_other)
    except:
        pct_catches_te    = 0
    try:
        pct_catches_other = catches_other / (catches_wr + catches_rb + catches_te + catches_other)
    except:
        pct_catches_other = 0

    #------------------- YARDS ------------------------------------------------    
    try:
        yards_wr    = int(group[1][group[1]['pos'] == 'WR']['yards'])
    except:
        yards_wr    = 0
    try:
        yards_rb    = int(group[1][group[1]['pos'] == 'RB']['yards'])
    except:
        yards_rb    = 0
    try:
        yards_te    = int(group[1][group[1]['pos'] == 'TE']['yards'])
    except:
        yards_te    = 0
    try:
        yards_other = int(group[1][~group[1]['pos'].isin(['WR','RB','TE'])]['yards'])    
    except:
        yards_other = 0
        
    try:
        pct_yards_wr    = yards_wr / (yards_wr + yards_rb + yards_te + yards_other)
    except:
        pct_yards_wr    = 0
    try:
        pct_yards_rb    = yards_rb / (yards_wr + yards_rb + yards_te + yards_other)
    except:
        pct_yards_rb    = 0
    try:
        pct_yards_te    = yards_te / (yards_wr + yards_rb + yards_te + yards_other)
    except:
        pct_yards_te   = 0
    try:
        pct_yards_other = yards_other / (yards_wr + yards_rb + yards_te + yards_other)
    except:
        pct_yards_other = 0

    #------------------- TDs --------------------------------------------------
    try:
        td_wr    = int(group[1][group[1]['pos'] == 'WR']['td'])
    except:
        td_wr    = 0
    try:
        td_rb    = int(group[1][group[1]['pos'] == 'RB']['td'])
    except:
        td_rb    = 0
    try:
        td_te    = int(group[1][group[1]['pos'] == 'TE']['td'])
    except:  
        td_te    = 0
    try:
        td_other = int(group[1][~group[1]['pos'].isin(['WR','RB','TE'])]['td'])
    except:
        td_other = 0
    try:
        pct_td_wr    = td_wr / (td_wr + td_rb + td_te + td_other)
    except:
        pct_td_wr    = 0 
    try:              
        pct_td_rb    = td_rb / (td_wr + td_rb + td_te + td_other)
    except:
        pct_td_rb    = 0
    try:
        pct_td_te    = td_te / (td_wr + td_rb + td_te + td_other)
    except:
        pct_td_te    = 0
    try:
        pct_td_other = td_other / (td_wr + td_rb + td_te + td_other)
    except:
        pct_td_other = 0
    
    list_rows.append([group[1]['team'].iloc[0], group[1]['conf'].iloc[0], group[1]['season'].iloc[0],
                 pct_catches_wr, pct_catches_rb, pct_catches_te, pct_catches_other,
                 pct_yards_wr, pct_yards_rb, pct_yards_te, pct_yards_other,
                 pct_td_wr, pct_td_rb, pct_td_te, pct_td_other,
                 catches_wr, catches_rb, catches_te, catches_other,
                 yards_wr, yards_rb, yards_te, yards_other,
                 td_wr, td_rb, td_te, td_other])
    
df_final = pd.DataFrame(list_rows)
df_final.columns = ['team', 'conf', 'season', 
                   'pct_catches_wr', 'pct_catches_rb', 'pct_catches_te', 'pct_catches_other',
                   'pct_yards_wr', 'pct_yards_rb', 'pct_yards_te', 'pct_yards_other',
                   'pct_td_wr', 'pct_td_rb', 'pct_td_te', 'pct_td_other',
                   'catches_wr', 'catches_rb', 'catches_te', 'catches_other',
                   'yards_wr', 'yards_rb', 'yards_te', 'yards_other',
                   'td_wr', 'td_rb', 'td_te', 'td_other']
df_final = df_final.round(2)

test = df_final[df_final['team'] == 'Nebraska']

# df_rec_by_year = df_rec_by_year[df_scoring['split'] == 'All Games']
# df_rec_by_year = df_rec_by_year[df_scoring['season'].isin([2018,2019,2020])]