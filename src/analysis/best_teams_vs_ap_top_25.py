#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 13:12:31 2021

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

#------------------------------------------------------------------------------
'''
    In the October 16th matchup of Purdue vs. Iowa, it was mentioned that Purdue
    has the most wins over AP #2 teams. 
    
    This analysis will attempt to find which teams have the most wins over each
    ranking in the AP Top 25 (since 1971 -- the last 50 years)
'''
#------------------------------------------------------------------------------
# 1 grab most recent version of 44 game file
df_coaches = pd.read_csv(max(glob.iglob(
    r'data\processed\Coaches\coaching_history*_44_games.csv'), key=os.path.getmtime))

# 2. Drop unneeded columns
df_coaches = df_coaches[['Season', 'Week', 'Date', 'Day', 'Rank', 'School',
                        'Coach', 'Conf', 'Power5', 'Home_Away', 'Rank_Opp',
                        'Opponent', 'Conf_Opp', 'Power5_Opp', 'Result',
                        'Pts', 'Pts_Opp', 'Notes']]

# 3. Iterate over each ranking (1 through 25) and find which teams has the
#   most wins and the best overall winning pct. from ANY position
df_results = pd.DataFrame()
list_ranks = list(range(1,26))
for rank in list_ranks:
    # create subset dataframe of all games vs. teams with said ranking
    df_rank = df_coaches[df_coaches['Rank_Opp'] == rank]
    df_rank = df_rank.sort_values(by = ['Season', 'Week'])
    
    # calculate the number of wins for each team over said ranking
    series_wins = df_rank.groupby('School').apply(lambda row: row['Result'].eq('W').sum())
    
    # calculate the number of losses for each team over said ranking
    series_loss = df_rank.groupby('School').apply(lambda row: row['Result'].eq('L').sum())
    
    # calculate the number of ties for each team over said ranking
    series_ties = df_rank.groupby('School').apply(lambda row: row['Result'].eq('T').sum())
    
    # calculate the number of games for each team over said ranking
    series_games = df_rank.groupby('School').Result.count()
    series_games = series_games.rename(f'{rank}_games')
    
    # convert data to a dataframe
    df_results[f'{rank}_games'] = series_games
    df_results[f'{rank}_wins']  = series_wins
    df_results[f'{rank}_loss']  = series_loss
    df_results[f'{rank}_ties']  = series_ties
    
    # calculate the winning pct. of each team over said ranking
    df_results[f'{rank}_win_pct'] = df_results[f'{rank}_wins'] / df_results[f'{rank}_games']
    df_results[f'{rank}_win_pct'] = df_results[f'{rank}_win_pct'].round(2)

# 4. Iterate over each ranking (1 through 25) and find which teams has the
#   most wins and the best overall winning pct. from an UNRANKED position
df_results_unranked = pd.DataFrame()
list_ranks = list(range(1,26))
for rank in list_ranks:
    # create subset dataframe of all games vs. teams with said ranking
    df_rank = df_coaches[df_coaches['Rank_Opp'] == rank]
    df_rank = df_rank[pd.isna(df_rank['Rank'])]
    df_rank = df_rank.sort_values(by = ['Season', 'Week'])
    
    # calculate the number of wins for each team over said ranking
    series_wins = df_rank.groupby('School').apply(lambda row: row['Result'].eq('W').sum())
    
    # calculate the number of losses for each team over said ranking
    series_loss = df_rank.groupby('School').apply(lambda row: row['Result'].eq('L').sum())
    
    # calculate the number of ties for each team over said ranking
    series_ties = df_rank.groupby('School').apply(lambda row: row['Result'].eq('T').sum())
    
    # calculate the number of games for each team over said ranking
    series_games = df_rank.groupby('School').Result.count()
    series_games = series_games.rename(f'{rank}_games')
    
    # convert data to a dataframe
    df_results_unranked[f'{rank}_games'] = series_games
    df_results_unranked[f'{rank}_wins']  = series_wins
    df_results_unranked[f'{rank}_loss']  = series_loss
    df_results_unranked[f'{rank}_ties']  = series_ties
    
    # calculate the winning pct. of each team over said ranking
    df_results_unranked[f'{rank}_win_pct'] = df_results_unranked[
        f'{rank}_wins'] / df_results_unranked[f'{rank}_games']
    df_results_unranked[f'{rank}_win_pct'] = df_results_unranked[
        f'{rank}_win_pct'].round(2)
    
# 4. Isolate Nebraska results
df_neb = df_results.loc['Nebraska'].to_frame().T
df_neb = df_neb.fillna(0)
    
# 5. Extract the results for each rank
df_final = pd.DataFrame()
for rank in list_ranks:
    dict_rank = {}
    dict_rank['rank'] = rank
    
    # Who has played the most games (ANY RANK)
    team_most_games = df_results[f'{rank}_games'].idxmax()
    dict_rank['most_games'] = (
        f'{team_most_games}' + ', ' + 
        # f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_games'])} games" + ', '
        f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_wins'])}" + '-' +
        f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_loss'])}" + '-' +
        f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_ties'])}" + ', ' + 
        f"{float(df_results.loc[f'{team_most_games}'][f'{rank}_win_pct'])}")
    # print(f"(Any Rank) Most games vs. the #{rank} team: {team_most_games}," +
    #       f"{int(df_results[f'{rank}_games'].max())}")
    # print(f"   --- Their record vs. the #{rank} team: " + 
    #       f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_wins'])}" + '-' + 
    #       f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_loss'])}" + '-' + 
    #       f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_ties'])}")

    # Who has the highest win percentage 
    #   - (min. of games is the 50% percentile of games played vs. that oppt)
    min_games = int(df_results[f'{rank}_games'].describe()['75%'])
    min_games = int(df_results[f'{rank}_games'].describe()['50%'])
    df_subset = df_results[df_results[f'{rank}_games'] >= min_games]
    team_best_pct = df_subset[f'{rank}_win_pct'].idxmax()
    dict_rank['team_best_pct'] = (
        f'{team_best_pct}' + ', ' + 
        # f"{int(df_results.loc[f'{team_best_pct}'][f'{rank}_games'])} games" + ', '
        f"{int(df_results.loc[f'{team_best_pct}'][f'{rank}_wins'])}" + '-' +
        f"{int(df_results.loc[f'{team_best_pct}'][f'{rank}_loss'])}" + '-' +
        f"{int(df_results.loc[f'{team_best_pct}'][f'{rank}_ties'])}" + ', ' + 
        f"{float(df_results.loc[f'{team_best_pct}'][f'{rank}_win_pct'])}")
    # print(f"Best Win Pct. vs. the #{rank} team: {team_best_pct}," + 
    #       f"{df_subset[f'{rank}_win_pct'].max()})")
    # print(f"   --- Their record vs. the #{rank} team: " + 
    #       f"{int(df_subset.loc[f'{team_best_pct}'][f'{rank}_wins'])}" + '-' + 
    #       f"{int(df_subset.loc[f'{team_best_pct}'][f'{rank}_loss'])}" + '-' + 
    #       f"{int(df_subset.loc[f'{team_best_pct}'][f'{rank}_ties'])}")
    
    # Who has played the most games (UNRANKED)
    team_most_games = df_results_unranked[f'{rank}_games'].idxmax()
    dict_rank['most_games_unranked'] = (
        f'{team_most_games}' + ', ' + 
        # f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_games'])} games" + ', '
        f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_wins'])}" + '-' +
        f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_loss'])}" + '-' +
        f"{int(df_results.loc[f'{team_most_games}'][f'{rank}_ties'])}" + ', ' + 
        f"{float(df_results.loc[f'{team_most_games}'][f'{rank}_win_pct'])}")
    # print(f"(Unranked) Most games vs. the #{rank} team: {team_most_games}," +
    #       f"{int(df_results_unranked[f'{rank}_games'].max())}")
    # print(f"   --- Their record vs. the #{rank} team: " + 
    #       f"{int(df_results_unranked.loc[f'{team_most_games}'][f'{rank}_wins'])}" + '-' + 
    #       f"{int(df_results_unranked.loc[f'{team_most_games}'][f'{rank}_loss'])}" + '-' + 
    #       f"{int(df_results_unranked.loc[f'{team_most_games}'][f'{rank}_ties'])}")
    
    # Who has the highest win percentage (UNRANKED)
    #   - (min. of games is the 75% percentile of games played vs. that oppt)
    min_games = int(df_results_unranked[f'{rank}_games'].describe()['75%'])
    min_games = int(df_results_unranked[f'{rank}_games'].describe()['50%'])
    df_subset = df_results_unranked[df_results_unranked[f'{rank}_games'] >= min_games]
    team_best_pct = df_subset[f'{rank}_win_pct'].idxmax()
    dict_rank['team_best_pct_unranked'] = (
        f'{team_best_pct}' + ', ' + 
        # f"{int(df_results.loc[f'{team_best_pct}'][f'{rank}_games'])} games" + ', '
        f"{int(df_results.loc[f'{team_best_pct}'][f'{rank}_wins'])}" + '-' +
        f"{int(df_results.loc[f'{team_best_pct}'][f'{rank}_loss'])}" + '-' +
        f"{int(df_results.loc[f'{team_best_pct}'][f'{rank}_ties'])}" + ', ' + 
        f"{float(df_results.loc[f'{team_best_pct}'][f'{rank}_win_pct'])}")
    # print(f"Best Win Pct. vs. the #{rank} team: {team_best_pct}," +
    #       f"{df_subset[f'{rank}_win_pct'].max()})")
    # print(f"   --- Their record vs. the #{rank} team: " + 
    #       f"{int(df_subset.loc[f'{team_best_pct}'][f'{rank}_wins'])}" + '-' + 
    #       f"{int(df_subset.loc[f'{team_best_pct}'][f'{rank}_loss'])}" + '-' + 
    #       f"{int(df_subset.loc[f'{team_best_pct}'][f'{rank}_ties'])}")
    
    # What is Nebraska's record vs. each team
    dict_rank['nebraska'] = (
        'Nebraska, ' + 
        f"{int(df_neb[f'{rank}_wins'])}" + '-' +
        f"{int(df_neb[f'{rank}_loss'])}" + '-' +
        f"{int(df_neb[f'{rank}_ties'])}" + ', ' + 
        f"{float(df_neb[f'{rank}_win_pct'])}")
    # print(f"Nebraska's record vs. the #{rank} team: " + 
    #       f"{int(df_neb[f'{rank}_wins'])}" + '-'  
    #       f"{int(df_neb[f'{rank}_loss'])}" + '-'
    #       f"{int(df_neb[f'{rank}_ties'])}")
    # print(f"   --- Nebraska's Win Pct. vs. the #{rank} team:" + 
    #       f"{float(df_neb[f'{rank}_win_pct'])}")
    # print('')
    
    if len(df_final) == 0:
        df_final = pd.DataFrame.from_dict(dict_rank, orient = 'index').T.copy()
    else:
        df_final = df_final.append(pd.DataFrame.from_dict(dict_rank, 
                                                          orient = 'index').T)
df_final = df_final.reset_index(drop = True)
        
# 6. Write to .xlsx file
import xlsxwriter

#--- Import team colors
df_colors = pd.read_csv(r'references\ncaa_colors.csv')

#--- Create Pandas Excel writer and write DataFrame to disk
writer = pd.ExcelWriter(r'data\processed\Coaches\teams_vs_top25.xlsx', 
                        engine = 'xlsxwriter')

#--- Conver the dataframe to an XlsxWriter excel object
df_final.to_excel(writer, sheet_name='Sheet1', index = False)

#--- Get the xlsxwriter objects from teh dataframe writer object
workbook = writer.book
worksheet = writer.sheets['Sheet1']

#--- Color cells by team
cell_format = workbook.add_format()

worksheet.write('A1', 'Rank')
worksheet.write('B1', 'Most Games (Any Rank)')
worksheet.write('C1', 'Best Win Pct. (Any Rank)')
worksheet.write('D1', 'Most Games (Unranked)')
worksheet.write('E1', 'Best Win Pct. (Unranked)')
worksheet.write('F1', "Nebrask's record")

for index_row, row in df_final.iterrows():
    for index_col in range(0,len(row)):
        value = row[index_col]
        
        # convert col # to letter
        cell_number = f'{xlsxwriter.utility.xl_col_to_name(index_col)}{index_row+2}'
        
        if index_col != 0:
            if value != 'Nebraska':
                team = value.split(', ')[0]
            else:
                team = 'Nebraska'     
            bg_color = df_colors[df_colors['spref_name'] == team]['primary_color'].iloc[0]
            font_color = df_colors[df_colors['spref_name'] == team]['secondary_color'].iloc[0]
            cell_format = workbook.add_format()
            cell_format.set_bg_color(bg_color)
            cell_format.set_font_color(font_color)
            cell_format.set_bold(True)
            worksheet.write(cell_number, value, cell_format)
        else:
            worksheet.write(cell_number, value)

#--- Set column widths
worksheet.set_column('A:A', 5)
worksheet.set_column('B:E', 24)
worksheet.set_column('F:F', 20)
        
#--- Close the writer
writer.close()
     
print(f"Index Row: {index_row}, " + f"Index Col: {index_col}, " + f"Value: {value}, " + 
      f"BG Color: {df_colors[df_colors['spref_name'] == team]['primary_color'].iloc[0]}, " +
      f"Font Color: {df_colors[df_colors['spref_name'] == team]['secondary_color'].iloc[0]}") 