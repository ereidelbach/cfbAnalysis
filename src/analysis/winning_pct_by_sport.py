import glob
import pandas as pd

# read in basketball data
list_files = glob.glob(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\raw\Random\cbb*.csv')               

df_cbb = pd.DataFrame()
for file in list_files:        
    df_year = pd.read_csv(file, encoding = "ISO-8859-1")
    year = int(file.split("\\")[-1].split('_')[-1].replace('.csv',''))
    df_year['Season'] = year
    df_year = df_year.dropna(subset = ['W'])
    df_cbb = df_cbb.append(df_year)
df_cbb.columns = ['cbb_' + x if x not in ['School', 'Season', 'Conf',] else x for x in df_cbb.columns]   
    
# read in football data
list_files = glob.glob(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\raw\Random\cfb*.csv')               

df_cfb = pd.DataFrame()
for file in list_files:        
    df_year = pd.read_csv(file, encoding = "ISO-8859-1")
    year = int(file.split("\\")[-1].split('_')[-1].replace('.csv',''))
    df_year['Season'] = year
    df_year = df_year.dropna(subset = ['W'])
    df_cfb = df_cfb.append(df_year)
df_cfb = df_cfb.drop(columns = ['Conf'])
df_cfb.columns = ['cfb_' + x if x not in ['School', 'Season'] else x for x in df_cfb.columns]    
    
df_cbb = renameSchool(df_cbb, 'School')
df_cfb = renameSchool(df_cfb, 'School')

# subset data to FBS teams
df_all = pd.merge(df_cfb, df_cbb, how = 'left', on = ['Season', 'School'])
df_all = df_all[['Season', 'School', 'Conf', 'cfb_Rk', 'cfb_W', 'cfb_L', 
                 'cbb_Rk', 'cbb_W', 'cbb_L', 'cfb_AP Rank', 'cfb_OSRS',
                 'cfb_DSRS', 'cfb_SRS', 'cfb_Scoring_Off', 'cfb_Scoring_Def',
                 'cfb_Passing_Off', 'cfb_Passing_Def', 'cfb_Rushing_Off',
                 'cfb_Rushing_Def', 'cfb_Total_Off', 'cfb_Total_Def', 
                 'cbb_Pts', 'cbb_Opp', 'cbb_MOV', 'cbb_SOS', 'cbb_OSRS', 
                 'cbb_DSRS', 'cbb_SRS', 'cbb_ORtg', 'cbb_DRtg', 'cbb_NRtg']]

# sum wins over all 4 years
df_summary = df_all.groupby('School')['cfb_W', 'cfb_L', 'cbb_W', 'cbb_L'].sum()

# calculate winning %: (1) Football, (2) Basketball, (3) All
df_summary['cfb_win_%'] = round(df_summary['cfb_W'] / (df_summary['cfb_W'] + df_summary['cfb_L']), 3)
df_summary['cbb_win_%'] = round(df_summary['cbb_W'] / (df_summary['cbb_W'] + df_summary['cbb_L']), 3)
df_summary['all_win_%'] = round((df_summary['cfb_win_%'] + df_summary['cbb_win_%']) / 2, 3)
df_summary['rank_cfb'] = df_summary['cfb_win_%'].rank(ascending = False, method = 'min')
df_summary['rank_cbb'] = df_summary['cbb_win_%'].rank(ascending = False, method = 'min')
df_summary['rank_all'] = df_summary['all_win_%'].rank(ascending = False, method = 'min') 

# sum wins over all 4 years
df_moos_cfb = df_all.groupby('School')['cfb_W', 'cfb_L'].sum()
df_moos_cfb = df_moos_cfb.reset_index(drop = False)
df_moos_cbb = df_all[df_all['Season'] > 2018].groupby('School')['cbb_W', 'cbb_L'].sum()
df_moos_cbb = df_moos_cbb.reset_index(drop = False)
df_moos = pd.merge(df_moos_cfb, df_moos_cbb, how = 'left', on = 'School')

# calculate winning %: (1) Football, (2) Basketball, (3) All
df_moos['cfb_win_%'] = round(df_moos['cfb_W'] / (df_moos['cfb_W'] + df_moos['cfb_L']), 3)
df_moos['cbb_win_%'] = round(df_moos['cbb_W'] / (df_moos['cbb_W'] + df_moos['cbb_L']), 3)
df_moos['all_win_%'] = round((df_moos['cfb_win_%'] + df_moos['cbb_win_%']) / 2, 3)
df_moos['rank_cfb'] = df_moos['cfb_win_%'].rank(ascending = False, method = 'min')
df_moos['rank_cbb'] = df_moos['cbb_win_%'].rank(ascending = False, method = 'min')
df_moos['rank_all'] = df_moos['all_win_%'].rank(ascending = False, method = 'min') 
df_moos['tot_W'] = df_moos['cfb_W'] + df_moos['cbb_W']
df_moos['tot_L'] = df_moos['cfb_L'] + df_moos['cbb_L'] 
df_moos['tot_win_%'] = df_moos['tot_W'] / (df_moos['tot_W'] + df_moos['tot_L'])