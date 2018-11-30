#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:24:32 2018

@author: ejreidelbach

:DESCRIPTION:
    - Scrapes the CFBStats website, aggregates all statistic by team, then year
        and ultimately by statistical category for all years into 17 distinct
        .csv files located in /data/interim/ALL/merged_final

:REQUIRES:
   
:TODO:
"""

#import click
#import logging
#from pathlib import Path
#from dotenv import find_dotenv, load_dotenv
#
#
#@click.command()
#@click.argument('input_filepath', type=click.Path(exists=True))
#@click.argument('output_filepath', type=click.Path())
#def main(input_filepath, output_filepath):
#    """ Runs data processing scripts to turn raw data from (../raw) into
#        cleaned data ready to be analyzed (saved in ../processed).
#    """
#    logger = logging.getLogger(__name__)
#    logger.info('making final data set from raw data')
#
#
#if __name__ == '__main__':
#    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#    logging.basicConfig(level=logging.INFO, format=log_fmt)
#
#    # not used in this stub but often useful for finding various files
#    project_dir = Path(__file__).resolve().parents[2]
#
#    # find .env automagically by walking up directories until it's found, then
#    # load up the .env entries as environment variables
#    load_dotenv(find_dotenv())
#
#    main()

#==============================================================================
# Package Import
#==============================================================================
import os
import pathlib

from scrape_CFBStats import scrapeCFBStats
from aggregate_CFBStats_by_team import aggregate_data_by_team
from aggregate_CFBStats_by_category import aggregate_data_by_category

#==============================================================================
#--- Working Code
#==============================================================================

# Set the project working directory
path_project = pathlib.Path(__file__).resolve().parents[2]
os.chdir(path_project)

# Step 1: Scrape data from the CFBStats based on user input 
#           (e.g. all available years or a specific year)
scrapeCFBStats(path_project)

# Step 2: Aggregate all yearly statistics for each team into one file per 
#           team per sub-category
aggregate_data_by_team(path_project)

# Step 3: Aggregate all files for each team into one file per 
#           statistical category (said file includes data from all years)
aggregate_data_by_category(path_project)