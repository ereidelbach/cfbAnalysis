#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 14:35:41 2021

@author: reideej1

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import datetime
import glob
import matplotlib.pyplot as plt
import math
import numpy as np
import os  
import pandas as pd
import pathlib
import seaborn as sns

from matplotlib.backends.backend_pdf import PdfPages
#==============================================================================
# Reference Variable Declaration
#==============================================================================

#==============================================================================
# Function Definitions
#==============================================================================
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
    df_school_names = pd.read_csv('data/raw/school_abbreviations_and_pictures.csv')
     
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
 
def plot_corr_heatmap(df_corr, **kwargs):
    '''
    Purpose
    -------
    Given a correlation matrix, output 
    
    Parameters (Required)
    ---------------------
    df_corr : Pandas DataFrame
        - The correlation matrix of all variables with 
        
    Parameters (Optional)
    ---------------------
    color :
            
    palette : string, default == 'blues'
        - the desired color palette to use in the heatmap
    color_range : list of ints, default = [-1, 1]
        - the min / max values that will be mapped to the color palette
    size : list of ints, default == [1]*len(x)
        - the size of each x,y pairs' correlation magnitude
    size_range : list of ints, default == [0, 1]
        - the absolute limits (min and max) of the correlation values in the matrix
    size_scale : int, default == 500
        - the scale size to be used when generating the heatmap in seaborn
    marker : string, default == 's' (i.e. square)
        - the shape to be used in the heatmap plot
    x_order
        - the order in which to list variables on the x-axis of the plot
    y_order : list of strings
        - the order in which to list variables on the y-axis of the plot

    Returns
    -------
    NONE
    '''
    # melt the dataframe such that each spot in the table (i.e. correlation value)
    #   is now it's own row
    df_melted = pd.melt(df_corr.reset_index(), id_vars='index')
    df_melted.columns = ['x', 'y', 'value']
    
    # fill NaNs with 0s
    df_melted = df_melted.fillna(0)
    
    # extract the x and y values for the table (i.e. the variable names)
    x = df_melted['x']
    y = df_melted['y']
    
    #-------------------------------------------------------------------------
    # Initalize all keyword arguments for heatmap generation
    #-------------------------------------------------------------------------
    # Color 
    if 'color' in kwargs:
        color = kwargs['color']
    else:
        #color = [1]*len(x)
        color = df_melted['value']

    # Palette
    if 'palette' in kwargs:
        palette = kwargs['palette']
        n_colors = len(palette)
    else:
        n_colors = 256 # Use 256 colors for the diverging color palette
        palette = sns.color_palette("Blues", n_colors) 

    # Color Range
    if 'color_range' in kwargs:
        color_min, color_max = kwargs['color_range']
    else:
        color_min, color_max = min(color), max(color) 

    # Size
    if 'size' in kwargs:
        size = kwargs['size']
    else:
        #size = [1]*len(x)
        size = df_melted['value'].abs()

    # Size Range
    if 'size_range' in kwargs:
        size_min, size_max = kwargs['size_range'][0], kwargs['size_range'][1]
    else:
        size_min, size_max = min(size), max(size)

    # Size Scale
    size_scale = kwargs.get('size_scale', 500)
        
    # X-Order
    if 'x_order' in kwargs: 
        x_names = [t for t in kwargs['x_order']]
    else:
        x_names = [t for t in sorted(set([v for v in x]))]
    x_to_num = {p[1]:p[0] for p in enumerate(x_names)}

    # Y-Order
    if 'y_order' in kwargs: 
        y_names = [t for t in kwargs['y_order']]
    else:
        y_names = [t for t in sorted(set([v for v in y]))]
        y_names = y_names[::-1] # reverse the order of the list
    y_to_num = {p[1]:p[0] for p in enumerate(y_names)}
   
    # Marker
    marker = kwargs.get('marker', 's')

    # If a keyword argument doesn't match one of the above handlers, add it to
    #   a dictionary that will be passed along to the plotting function
    kwargs_pass_on = {k:v for k,v in kwargs.items() if k not in [
         'color', 'palette', 'color_range', 'size', 'size_range', 'size_scale', 'marker', 'x_order', 'y_order'
    ]}
    
    #--------------------------------------------------------------------------
    # Define Helper Functions
    #--------------------------------------------------------------------------
    def value_to_color(val):
        if color_min == color_max:
            return palette[-1]
        else:
            # position of value in the input range, relative to the length of the input range
            val_position = float((val - color_min)) / (color_max - color_min) 
            # bound the position betwen 0 and 1
            val_position = min(max(val_position, 0), 1) 
            # target index in the color palette
            ind = int(val_position * (n_colors - 1)) 
            return palette[ind]
        
    def value_to_size(val):
        ''' Helper function that translates the magnitude of the correlation into
            the size of the shape that will be plotted to represent the x,y pairs'
            correlation to one another in the plot
        '''
        if size_min == size_max:
            return 1 * size_scale
        else:
            # position of value in the input range, relative to the length of the input range
            val_position = (val - size_min) * 0.99 / (size_max - size_min) + 0.01 
            # bound the position betwen 0 and 1
            val_position = min(max(val_position, 0), 1) 
            return val_position * size_scale

    # Setup a 1x15 grid
    plot_grid = plt.GridSpec(1, 15, hspace=0.2, wspace=0.1) 
#    plot_grid = plt.GridSpec(1, len(df_corr), hspace=0.2, wspace=0.1) 
    # Use the left 14/15ths of the grid for the main plot
    ax = plt.subplot(plot_grid[:,:-1]) 
    
    # create a scatter plot of correlation values (i.e. our soon-to-be-heatmap)
    ax.scatter(
        x=[x_to_num[v] for v in x],
        y=[y_to_num[v] for v in y],
        marker=marker,
        s=[value_to_size(v) for v in size], 
        c=[value_to_color(v) for v in color],
        **kwargs_pass_on
    )
    # specify the x and y axis tick marks and tick labels as well as grid lines
    ax.set_xticks([v for k,v in x_to_num.items()])
    ax.set_xticklabels([k for k in x_to_num], rotation=45, horizontalalignment='right')
    ax.set_yticks([v for k,v in y_to_num.items()])
    ax.set_yticklabels([k for k in y_to_num])

    ax.grid(False, 'major')
    ax.grid(True, 'minor')
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)

    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    ax.set_facecolor('#F1F1F1')

    # Add color legend on the right side of the plot
    if color_min < color_max:
        ax = plt.subplot(plot_grid[:,-1])                   # Use the rightmost column of the plot
        col_x = [0]*len(palette)                            # Fixed x coordinate for the bars
        bar_y=np.linspace(color_min, color_max, n_colors)   # y coordinates for each of the n_colors bars

        bar_height = bar_y[1] - bar_y[0]
        ax.barh(
            y=bar_y,
            width=[5]*len(palette), # Make bars 5 units wide
            left=col_x,             # Make bars start at 0
            height=bar_height,
            color=palette,
            linewidth=0
        )
    
        ax.set_xlim(1, 2)                                       # Bars are going from 0 to 5 (crop them to the middle of that)
        ax.grid(False)                                          # Hide grid
        ax.set_facecolor('white')                               # Make background white
        ax.set_xticks([])                                       # Remove horizontal ticks
        ax.set_yticks(np.linspace(min(bar_y), max(bar_y), 3))   # Show vertical ticks for min, middle and max
        ax.yaxis.tick_right()                                   # Show vertical ticks on the right 
        
    fig = plt.gcf()

    # determine the size of the plot based on the number of variables
    fig_width = (df_corr.shape[0]) * 0.5
    fig_height = (df_corr.shape[1]) * 0.5
    #    fig.set_size_inches(10, 1)
    fig.set_size_inches(fig_width, fig_height)
        
    # save the figure to disk
    now = datetime.datetime.now()
    fig.savefig(fr"images\correlation_heatmap_{now.strftime('%Y-%m-%dT%H_%M_%S')}.png", dpi=200)
        
    return fig   
 
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
path_dir = pathlib.Path(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis')
os.chdir(path_dir)

#------------------------------------------------------------------------------
# NFL Draft Summary
#------------------------------------------------------------------------------
# load in school information
df_school_info = pd.read_csv('data/raw/school_abbreviations_and_pictures.csv')

# create an empty FBS dataframe
df_fbs = df_school_info[df_school_info['FBS'] == True]
df_fbs = df_fbs[['Team', 'Conference', 'ConferenceAbbrev', 'Power5', 
                 'FBS', 'urlSchool']]
df_fbs = df_fbs.rename({'urlSchool':'url_img', 'Team':'School'}, axis = 1)
length_fbs = len(df_fbs)

# duplicate each entry to create rows for all 22 years (2000 to 2021 season)
df_fbs = pd.concat([df_fbs]*22, ignore_index = True)

# sort by school name
df_fbs = df_fbs.sort_values(by = 'School')

# reset index
df_fbs = df_fbs.reset_index(drop = True)

# fill in all years with placeholder values
df_fbs['Year'] = pd.concat([pd.Series(list(range(2000, 2022)))]*length_fbs, ignore_index = True)

# load data from disk
df_draft = pd.read_csv('data/raw/NFL Draft/nfl_draft_all_2000_to_2021.csv')

# make a count of how many picks each school has for each year
df_draft_summary = df_draft.groupby(['Year', 'School']).size()
df_draft_summary = df_draft_summary.reset_index()
df_draft_summary.columns = ['Year', 'School', 'Num_Drafted']

# subset data to FBS schools
df_merge = pd.merge(df_fbs, df_draft_summary, how = 'left', on = ['School',  'Year'])

# sort dataframe by team, then year
df_merge = df_merge.sort_values(by = ['School', 'Year'])

# reorder columns
df_merge = df_merge[['Year', 'School', 'Num_Drafted', 'Conference', 
                     'ConferenceAbbrev', 'Power5', 'FBS', 'url_img']]

# fill in nas with 0s
df_merge['Num_Drafted'] = df_merge['Num_Drafted'].fillna(0)

# sort from latest year to earliest to enable "looking forward" sum
df_merge = df_merge.sort_values(by = ['School', 'Year'], ascending = [True, False])
# calculate rolling 4-year sum of draft picks
df_merge['num_drafted_4_year_sum']  = list(
    df_merge
    .groupby(['School'])['Num_Drafted']
    .rolling(4, min_periods = 0)
    .sum()
    )
# calculate rolling 4-year median of draft picks
df_merge['num_drafted_4_year_median']  = list(
    df_merge
    .groupby(['School'])['Num_Drafted']
    .rolling(4, min_periods = 0)
    .median()
    )
# re-sort table to back to original, chronological order
df_merge = df_merge.sort_values(by = ['School', 'Year'], ascending = [True, True])

# reorder columns
df_merge = df_merge[['Year', 'School', 'Num_Drafted', 'num_drafted_4_year_sum', 
                     'num_drafted_4_year_median',
                     'Conference', 'ConferenceAbbrev', 'Power5', 'FBS', 'url_img']]

#------------------------------------------------------------------------------
# 247 Composite
#------------------------------------------------------------------------------
# load 247 data
df_247 = pd.read_csv(r'data\raw\Recruiting\247Composite\247composite_all_2000_to_2021.csv')
df_247 = df_247.rename({'year':'Year', 'rank':'247_rank_year', 
                        'points':'247_composite_year', 'team':'School'}, axis = 1)

# merge 247 data with existing draft data
df_merge = pd.merge(df_merge, df_247, how = 'left', on = ['Year', 'School'])

# create rolling 247 composite score average (4-year average)
# calculate rolling 4-year sum of draft picks
df_merge['247_composite_4_year_median'] = list(
    df_merge
    .groupby(['School'])['247_composite_year']
    .rolling(4, min_periods = 0)
    .median()
    )

# create rolling 247 composite recruiting ranking average (4-year average)
df_merge['247_ranking_4_year_median'] = list(
    df_merge
    .groupby(['School'])['247_rank_year']
    .rolling(4, min_periods = 0)
    .median()
    )

#------------------------------------------------------------------------------
# Win-Loss Records
#------------------------------------------------------------------------------
# read in results data
df_results = pd.read_json(r'C:\Users\reideej1\Projects\a_Personal\cfbd\data\team_records_all_years.json')

# expand nested columns
col_names = ['total', 'conference_games', 'home_games', 'away_games']
col_names_short = ['total', 'conf', 'home', 'away']

for col_idx in range(0,4):
    col_name = col_names[col_idx]
    col_name_short = col_names_short[col_idx]
    df_temp = pd.json_normalize(df_results[col_name])
    df_temp.columns = [col_name_short + '_' + x for x in df_temp.columns]
    df_results = df_results.drop(columns = col_name)
    df_results = df_results.join(df_temp)

# drop nested columns
df_results = df_results.drop(columns = ['conference', 'division'])

# standardize school names
df_results = renameSchool(df_results, 'team')

# rename columns
df_results = df_results.rename({'year':'Year', 'team':'School'}, axis = 1)

# merge with Draft and 247 info
df_merge = pd.merge(df_merge, df_results, how = 'left', on = ['Year', 'School'])

#------------------------------------------------------------------------------
# Massey Info
#------------------------------------------------------------------------------
df_massey = pd.DataFrame()

list_files = glob.glob(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\raw\Massey\*.csv')
for fname in list_files:
    df_year = pd.read_csv(fname)
    if len(df_year.columns) > 15:
        df_year = df_year.iloc[:,0:15]
    df_year.columns = ['School', 'Division', 'Record', 'OVR_Rating', 'OVR_Rank',
                        'PWR_Rating', 'PWR_Rank', 'OFF_Rating', 'OFF_Rank',
                        'DEF_Rating', 'DEF_Rank', 'HFA_Rating', 'HFA_Rank', 
                        'SOS_Rating', 'SOS_Rank']
    df_year['Year'] = int(fname.split('_')[2].split('.')[0])
    df_year = df_year[['Year', 'School', 'OVR_Rating', 'OVR_Rank',
                        'PWR_Rating', 'PWR_Rank', 'OFF_Rating', 'OFF_Rank',
                        'DEF_Rating', 'DEF_Rank', 'HFA_Rating', 'HFA_Rank', 
                        'SOS_Rating', 'SOS_Rank']]
    if len(df_massey) == 0:
        df_massey = df_year.copy()
    else:
        df_massey = df_massey.append(df_year)
df_massey.to_csv(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\processed\Massey\massey_all_1991_to_2020.csv',
                  index = False)

# load data
df_massey = pd.read_csv(r'data\processed\Massey\massey_all_1991_to_2020.csv')

# merge with existing data
df_merge = pd.merge(df_merge, df_massey, how = 'left', on = ['Year', 'School'])

#------------------------------------------------------------------------------
# Analysis
#------------------------------------------------------------------------------
# save all data to disk
df_merge.to_csv(r'C:\Users\reideej1\Projects\a_Personal\cfbAnalysis\data\processed\draft_247_massey_analysis.csv', 
                index = False)
df_all =  pd.read_csv(r'data\processed\draft_247_massey_analysis.csv')

# drop 2000 - results don't start until 2001
df_subset = df_all[df_all['Year'] >= 2001]

# drop 2021 - season hasn't played out y et
df_subset = df_subset[df_subset['Year'] != 2021]

df_subset.plot.scatter('total_wins', '247_composite_4_year_median')
df_subset.plot.scatter('total_wins', 'num_drafted_4_year_sum')

df_corr = df_subset[['Num_Drafted', 
                  'num_drafted_4_year_sum',
                  'num_drafted_4_year_median', 
                  '247_composite_year',
                  '247_composite_4_year_median',
                  'total_wins', 
                  'conf_wins', 
                  'OVR_Rating', 
                  'PWR_Rating']].corr()

# corr = df_subset[['Num_Drafted', 
#                   'num_drafted_4_year_sum',
#                   'num_drafted_4_year_median', 
#                   '247_composite_year',
#                   '247_composite_4_year_median',
#                   'total_wins', 
#                   'conf_wins', 
#                   'OVR_Rating', 
#                   'PWR_Rating']].corr()
# ax = sns.heatmap(
#     corr, 
#     vmin=-1, vmax=1, center=0,
#     cmap=sns.diverging_palette(20, 220, n=200),
#     square=True
# )
# ax.set_xticklabels(
#     ax.get_xticklabels(),
#     rotation=45,
#     horizontalalignment='right'
# );

plot_corr_heatmap(df_corr, 
                  color_range = [-1, 1],                         # match the traditional correlation min/max of [-1,1]
                  palette=sns.diverging_palette(20, 220, n=256), # utilize a red/blue color palette
                  size_range = [0,1]                             # set min/max marker sizes to 0 and 1
                  )