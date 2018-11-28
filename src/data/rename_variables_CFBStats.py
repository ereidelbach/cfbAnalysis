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
# Game Log Statistics
#------------------------------------------------------------------------------
dict_game_rushing = {
        }
dict_game_passing = {'att':'pass_att',
                     'comp':'pass_comp',
                     'pct.':'pass_comp%',
                     'yards':'pass_yds',
                     'yards/att':'pass_yds/att',
                     'td':'pass_td',
                     'int':'pass_int',
                     'rating':'pass_rating',
                     }
dict_game_receiving = {'rec.':'rec',
                       'yards':'rec_yards',
                       'avg.':'rec_avg',
                       'td':'rec_td',
                       }
dict_game_puntreturns = {'ret.':'punt_ret_att',
                         'yards':'punt_ret_yds',
                         'avg.':'punt_ret_avg',
                         'td':'punt_ret_td',
                         }
dict_game_kickreturns = {'ret.':'kick_ret_att',
                         'yards':'kick_ret_yds',
                         'avg.':'kick_ret_avg',
                         'td':'kick_ret_td',
                         }
dict_game_punting = {'punts':'punt',
                     'yards':'punt_yds',
                     'avg.':'punt_avg',
                     }
dict_game_kickoffs = {'kickoffs':'kickoff_num',
                      'yards':'kickoff_yds',
                      'avg.':'kickoff_avg',
                      'touchback':'kickoff_tb',
                      'touchback %':'kickoff_tb%',
                      'out-of-bounds':'kickoff_oob',
                      'onside':'kickoff_onside',
                      }
dict_game_placekicking = {'fg_att.':'fg_att',
                          'fg_made':'fg_made',
                          'fg_pct.':'fg_pct',
                          'xp_att.':'xp_att',
                          'xp_made':'xp_made',
                          'xp_pct.':'xp_pct',
                          }
dict_game_scoring = {
        }
dict_game_totaloffense = {
        }
dict_game_interceptions = {'int.':'int',
                           'yards':'int_yds',
                           'td':'int_td',
                           }
dict_game_fumblereturns = {'fum. ret.':'fum_ret',
                           'yards':'fum_ret_yds',
                           'td':'fum_ret_td',
                           }
dict_game_tackles = {
        }
dict_game_tfl = {
        }
dict_game_sacks = {
        }
dict_game_miscdefense = {'passes broken up':'pbu',
                         'qb hurries':'qb_hurry',
                         'fumbles forced':'fum_forced',
                         'kicks/punts blocked':'kick_blocks',
                         }
dict_game_1downs = {'rush':'1down_run',
                    'pass':'1down_pass',
                    'penalty':'1down_pen',
                    'total':'1down_total',
                    }
dict_game_penalties = {'pen.':'pen',
                       'yards':'pen_yds',
                       'pen./g':'pen/g',
                       'yards/g':'pen_yds/g',
                       }
dict_game_3downs = {'attempts':'3down_att',
                    'conversions':'3down_conv',
                    'conversion %':'3down_conv%',
                    }
dict_game_4downs = {'attempts':'4down_att',
                    'conversions':'4down_conv',
                    'conversion %':'4down_conv%',
                    }
dict_game_redzone = {
        }
dict_game_turnovermargin = {
        }
#------------------------------------------------------------------------------
# Split Statistics
#------------------------------------------------------------------------------
dict_split = {
        }
#------------------------------------------------------------------------------
# Player Statistics
#------------------------------------------------------------------------------
dict_player = {
        }

#==============================================================================
# Function Definitions
#==============================================================================
def renameVariables(df_stats, category, sub_category):
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
        (2) category (string): Statistical category that the DataFrame belongs
                to (e.g. Game Log, Split or Player Statistics)
        (3) sub_category (string): Statistical sub-category of the DataFrame 
                being passed to the function -- used to reference the desired
                variable names in the associated category dictionary
    
    Output: 
        (1) df_stats (DataFrame): Updated version of the original DataFrame
                with all variables renamed to match the desired format
    '''
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
dir_path = pathlib.Path('/home/ejreidelbach/Projects/')
#os.chdir(r'/home/ejreidelbach/Projects')
