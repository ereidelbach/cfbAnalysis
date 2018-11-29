#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 12:15:20 2018

@author: ejreidelbach

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import os  
import pandas as pd
import pathlib

#==============================================================================
# Reference Variable Declaration
#==============================================================================

#------------------------------------------------------------------------------
# Staticts Variable Renaming Dictionary
#------------------------------------------------------------------------------
dict_stat_rename = {
        'rushing':
            {'att':'rush_att',
             'yards':'rush_yds',
             'avg.':'rush_avg',
             'td':'rush_att',
             'att/g':'rush_att/g',
             'yards/g':'rush_yds/g',
             }
        ,'passing':
            {'att':'pass_att',
             'comp':'pass_comp',
             'pct.':'pass_comp%',
             'yards':'pass_yds',
             'yards/att':'pass_yds/att',
             'td':'pass_td',
             'int':'pass_int',
             'rating':'pass_rating',
             'att/g':'pass_att/g',
             'yards/g':'pass_yds/g',
             }
        ,'receiving':
            {'rec.':'rec_att',
             'yards':'rec_yards',
             'avg.':'rec_avg',
             'td':'rec_td',
             'rec./g':'rec_att/g',
             'yards/g':'rec_yds/g',
             }
        ,'punt_returns':
            {'ret.':'punt_ret_att',
             'yards':'punt_ret_yds',
             'avg.':'punt_ret_avg',
             'td':'punt_ret_td',
             'ret./g':'punt_ret_att/g',
             'yards/g':'punt_ret_yds/g',
             }
        ,'kickoff_returns':
            {'ret.':'kick_ret_att',
             'yards':'kick_ret_yds',
             'avg.':'kick_ret_avg',
             'td':'kick_ret_td',
             'ret./g':'kick_ret_att/g',
             'yards/g':'kick_ret_yds/g',
             }
        ,'punting':
            {'punts':'punt_num',
             'yards':'punt_yds',
             'avg.':'punt_avg',
             'punts/g':'punt_num/g',
             'yards/g':'punt_yds/g',
             }
        ,'kickoffs':
            {'kickoffs':'kickoff_num',
             'yards':'kickoff_yds',
             'avg.':'kickoff_avg',
             'touchback':'kickoff_tb',
             'touchback %':'kickoff_tb%',
             'out-of-bounds':'kickoff_oob',
             'onside':'kickoff_onside',
             }
        ,'place_kicking':
            {'fg_att.':'fg_att',
             'fg_pct.':'fg_pct',
             'xp_att.':'xp_att',
             'xp_pct.':'xp_pct',
             }
        ,'total_offense':
            {'rush yards':'rush_yds',
             'pass yards':'pass_yds',
             'plays':'play_num',
             'total yards':'yds_total',
             'yards/play':'yds/play',
             'yards/g':'yds/g',
             }
        ,'interceptions':
            {'int.':'int_num',
             'yards':'int_yds',
             'td':'int_td',
             'int./g':'int/g',
             }
        ,'fumble_returns':
            {'fum. ret.':'fum_ret',
             'yards':'fum_ret_yds',
             'td':'fum_ret_td',
             }
        ,'tackles':
            {'solo':'tkl_solo',
             'assisted':'tkl_ass',
             'total':'tkl_tot',
             'total/g':'tkl_tot/g',
             }
        ,'tackles_for_loss':
            {'tfl':'tfl_num',
             'tfl yards':'tfl_yds',
             'tfl/g':'tfl/g',
             }
        ,'sacks':
            {'sacks':'sack_num',
             'sack yards':'sack_yds',
             'sacks/g':'sacks/g',
             }
        ,'misc._defense':
            {'passes broken up':'pbu',
             'qb hurries':'qb_hurry',
             'fumbles forced':'fum_forced',
             'kicks/punts blocked':'kick_blocks',
             }
        ,'first_downs':
            {'rush':'1down_run',
             'pass':'1down_pass',
             'penalty':'1down_pen',
             'total':'1down_total',
             }
        ,'penalties':
            {'pen.':'pen_num',
             'yards':'pen_yds',
             'pen./g':'pen/g',
             'yards/g':'pen_yds/g',
             }
        ,'3rd_down_conversions':
            {'attempts':'3down_att',
             'conversions':'3down_conv',
             'conversion %':'3down_conv%',
             }
        ,'4th_down_conversions':
            {'attempts':'4down_att',
             'conversions':'4down_conv',
             'conversion %':'4down_conv%',
             }
        ,'red_zone_conversions':
            {'attempts':'rz_att',
             'scores':'rz_scores',
             'score %':'rz_score%',
             'td':'rz_td',
             'td %':'rz_td%',
             'fg':'rz_fg',
             'fg %':'rz_fg%',
             }
        ,'turnover_margin':
            {'fum. gain':'fum_gain',
             'int. gain':'int_gain',
             'total gain':'to_gain',
             'fum. lost':'fum_lost',
             'int. lost':'int_lost',
             'total lost':'to_lost',
             'margin':'to_margin',
             'margin/g':'to_margin/g',
             }
            }

#==============================================================================
# Function Definitions
#==============================================================================
def renameVariables(df_stats, sub_category):
    '''
    Purpose: Rename every variable in a DataFrame to match the format dictated
        by a category-specific variable dictionary.  The purpose of this is
        to ensure all variables are in a format that allow for easy reference
        and analysis (no spaces, limited special characters, stat specific
        naming scheme, etc...)

    Input:   
        (1) df_stats (DataFrame): Pandas DataFrame containing stat-specific
                data with variable names in their original form (as found on t
                the CFBStats website)
        (2) sub_category (string): Statistical sub-category of the DataFrame 
                being passed to the function -- used to reference the desired
                variable names in the associated category dictionary
    
    Output: 
        (1) df_stats (DataFrame): Updated version of the original DataFrame
                with all variables renamed to match the desired format
    '''
    if sub_category in list(dict_stat_rename.keys()):
        df_stats = df_stats.rename(columns = dict_stat_rename[sub_category])
    
    return df_stats
    
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
#dir_path = pathlib.Path('/home/ejreidelbach/Projects/')
#os.chdir(r'/home/ejreidelbach/Projects')
