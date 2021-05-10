import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ingest coaching history data
df_coaches = pd.read_csv(r'C:\Users\reideej1\Downloads\Scott Frost\coaching_history_2020-12-02.csv')

# Create pop-tooltips
label_coaches = []
source = []
target = []
value = []

dict_conf = {'CUSA':0,
             'ACC':1, 
             'American':2,
             'Sun Belt':3,
             'MWC':4,
             'MAC':5,
             'SEC':6,
             'Big Ten':7,
             'Big 12':8,
             'Pac-12':9,
             'Ind':10}

# Node info
label_nodes = ['CUSA', 'ACC', 'American', 'Sun Belt', 'MWC', 'MAC', 
               'SEC', 'Big Ten', 'Big 12', 'Pac-12', 'Ind', 
               'Coaches 3 or more seasons', 'Coached 2 seasons or less']

# Subset the data to coaches in their 3rd year with more
df_last = df_coaches.groupby(['coach', 'school']).tail(1)

#-- 1. Set Wins and Losses in first three season
for index, row in df_last.iterrows():
    coach_entry = (str(row['coach'] + ', ' + row['school']))
    label_coaches.append(coach_entry)
    source.append(row['conf'])
    if row['total_games'] >= 30:
        target.append('Yes')
    else:
        target.append('No')
    value.append(1)
    
df_last['label'] = label_coaches
df_last['source'] = source
df_last['target'] = target
df_last['value'] = value

# Isolate Scott Frost's Winning %
sf_win_pct = float(df_yr_3[df_yr_3['coach'] == 'Scott Frost']['cum_win_pct'])
# Isolate Scott Frost's Games Played
sf_gp = int(df_yr_3[df_yr_3['coach'] == 'Scott Frost']['cum_GP'])

# Subset the data to coaches have coached at least the same number of games as Scott
df_yr_3 = df_yr_3[df_yr_3['cum_GP'] >= sf_gp]

# Subset the data to coaches with a winning percentage the same as or worse than Scott
#df_40 = df_yr_3[df_yr_3['cum_win_pct'] < sf_win_pct]
df_40 = df_yr_3[df_yr_3['cum_win_pct'] < .40625]