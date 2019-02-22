#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:55:02 2019

@author: ejreidelbach

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import cutie
import glob
import json
import os  
import pandas as pd
import pathlib
import re
import requests
import time
import tqdm
import urllib.request 

from bs4 import BeautifulSoup
from requests.packages.urllib3.util.retry import Retry

#==============================================================================
# Reference Variable Declaration
#==============================================================================
list_nfl = ['Arizona Cardinals'
            ,'Atlanta Falcons'
            ,'Baltimore Ravens'
            ,'Buffalo Bills'
            ,'Carolina Panthers'
            ,'Chicago Bears'
            ,'Cincinnati Bengals'
            ,'Cleveland Browns'
            ,'Dallas Cowboys'
            ,'Denver Broncos'
            ,'Detroit Lions'
            ,'Green Bay Packers'
            ,'Houston Texans'
            ,'Indianapolis Colts'
            ,'Jacksonville Jaguars'
            ,'Kansas City Chiefs'
            ,'Los Angeles Chargers'
            ,'Los Angeles Rams'
            ,'Miami Dolphins'
            ,'Minnesota Vikings'
            ,'New England Patriots'
            ,'New Orleans Saints'
            ,'New York Giants'
            ,'New York Jets'
            ,'Oakland Raiders'
            ,'Philadelphia Eagles'
            ,'Pittsburgh Steelers'
            ,'St. Louis Rams'
            ,'San Francisco 49ers'
            ,'Seattle Seahawks'
            ,'Tampa Bay Buccaneers'
            ,'Tennessee Titans'
            ,'Washington Redskins'
            ]

#==============================================================================
# Function Definitions
#==============================================================================
def askUserForPositionURL():
    '''
    Purpose: On the command line, ask the user to input which position they 
        would like to scrape player-specific page URLs for.  If the user does 
        not want to scrape URLs for all positions, they will be asked what 
        posiiton they are specifically interested in.
        
    Inputs
    ------
        NONE
        
    Outputs
    -------
        scrape_position : string
            Position that the user requests data for 
            (allowed values are 'QB', 'WR', 'RB', 'DEF' or 'all') 
             ** NOTE: WR includes TE **
            [default = 'all']
    '''
    # Set the default for scraping to all positions
    scrape_position = 'all'
    
    # Prompt the user to select the years they would like to scrape URLs for
    list_all = ['Would you like to scrape URLS for all positions?', 
                'No',
                'Yes'
                ]
    all_positions = list_all[
            cutie.select(
                    list_all, 
                    caption_indices=[0],
                    selected_index=1)]
                
    # If the user wants all position URLs
    if all_positions == 'Yes':
        print('Proceeding to scrape URLs for all available positions.') 
        scrape_position = ['NONE', 'QB', 'WR', 'RB', 'DEF']
    # If the user wants URLs for a specific position
    else:
        years = ['Select the position for which you would like to scrape URLs:',
                 'NONE', 'QB', 'WR', 'RB', 'DEF']
        scrape_position = [years[cutie.select(years, caption_indices=[0], 
                                         selected_index=1)]]
        print(f'Proceeding to scrape URLs for {scrape_position}')
        
    return scrape_position

def askUserForPositionInfo():
    '''
    Purpose: On the command line, ask the user to input which position they 
        would like to scrape statistical data for.  If the user does not want 
        to scrape data for all positions, they will be asked what posiiton they 
        are specifically interested in.
        
    Inputs
    ------
        NONE
        
    Outputs
    -------
        scrape_position : string
            Position that the user requests data for 
            (allowed values are 'NONE', 'QB', 'RB', 'FB', 'WR', 'TE', 
                  'CB', 'DB', 'DE', 'DT', 'DL', 'LB', 'NT', 'S' or 'all') 
             ** NOTE: WR includes TE **
            [default = 'all']
    '''
    # Set the default for scraping to all positions
    scrape_position = 'all'
    
    # Prompt the user to select the years they would like to scrape data for
    list_all = ['Would you like to scrape player info for all positions?', 
                'No',
                'Yes']
    all_positions = list_all[
            cutie.select(
                    list_all, 
                    caption_indices=[0],
                    selected_index=1)]
    
    # Scrape player-specific data for all positions
    if all_positions == 'Yes':
        print('Proceeding to scrape player info for all available posiitons.') 
        scrape_position = ['NONE', 'QB', 'RB', 'FB', 'WR', 'TE', 
                           'CB', 'DB', 'DE', 'DT', 'DL', 'LB', 'NT', 'S']
    # Scrape player-specific data for one position
    else:
        years = ['Select the position for which you would like to scrape player info:',
                 'NONE', 'QB', 'RB', 'FB', 'WR', 'TE',
                 'CB', 'DB', 'DE', 'DT', 'DL', 'LB', 'NT', 'S']
        scrape_position = [years[cutie.select(years, caption_indices=[0], 
                                         selected_index=1)]]
        print(f'Proceeding to scrape player info for {scrape_position}')
        
    return scrape_position

def mergePositionFiles(position, position_folder):
    '''
    Purpose: Merge all player-specific information for a position group 
        contained in multiple batch-specific files into one cohesive file

    Inputs
    ------
        position : string
            Position group for which data exists and must be merged
        position_folder : string
            Folder in which the specified position data is located
    
    Outputs
    -------
        df_merge : Pandas DataFrame containing all information for a specified
            position group (OUTPUT TO DISK -- `player_info_POS_merged.csv`)
    '''  
    # get a list of all .csv files in the directory
    list_files = glob.glob('positionData/' + position_folder + '/player_info_'
                           + position + '_*.csv')
    try:
        list_files.remove('positionData/' + position_folder + '/player_info_'
                          + position + '_all.csv')
    except:
        pass
    
    # merge all individual data files together into one cohesive player file
    list_dataframes = []
    for csv in list_files:
        df_file = pd.read_csv(csv)
        list_dataframes.append(df_file)
    df_all = pd.concat(list_dataframes, sort = True)
    
    # remove duplicates
    df_all.drop_duplicates(inplace=True)
    
    # remove empty rows or rows with non-player information
    df_all = df_all[~df_all['nameFull'].isin(['',' ', '- Team'])]
    
    # reset index for dataframe
    df_all.reset_index(inplace = True, drop = True)
    
    # two school variables exist: `college` and `school`
    #   - if a player has an NFL team, the NFL team will be in school and the
    #       actual school they attended will be in the variable `college`
    #   - move through each row and overwrite `school` with `college` as needed
    df_all['school'] = df_all.apply(lambda row: row['college'] if 
          pd.isna(row['college']) == False else row['school'], axis = 1)
    
    # drop the `college` variable
    df_all.drop('college', axis = 1, inplace = True)
    
    # remove NFL teams from the `school` variable
    for index, row in df_all.iterrows():
        if row['school'] in list_nfl:
            print(row.name)
    
    # standardize the `school` names
#    df_all['school'] = df_all['school'].apply(lambda x: renameSchool(x))
    df_all = renameSchool(df_all, 'school')
    
    # write aggregated data to disk
    df_all.to_csv('positionData/' + position_folder + '/player_info_' 
                  + position + '_all.csv', index = False)
 
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
    df_school_names = pd.read_csv(path_dir.joinpath(
            'positionData/school_abbreviations.csv'))    
     
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

def runInfoScraping(position, position_folder):
    '''
    Purpose: Obtain information on every player within a specified position
        group by scraping their player-specific page on ESPN.com

    Inputs
    ------
        position : string
            Position group to be scraped (i.e. 'QB', 'RB', 'FB', etc...)
        position_folder : string
            Folder in which the specified position data is located
    
    Outputs
    -------
        list_dicts : list of strings
            List in which each element is a dictionary containing 
            player-specific information obtained from ESPN.com
            (OUTPUT TO DISK -- `player_info_POS_#.csv`)
    '''           
    # specify the position folder URL filename
    filename = path_dir.joinpath(
            'positionData/' + position_folder + '/player_urls_' 
            + position_folder + '.csv')
    
    # Read in players from the URL dataframe in chunks
    #reader = pd.read_csv(filename, chunksize = 100)
    
    # Read in the URLs for the specified position folder
    df_urls = pd.read_csv(filename)
    # Subset the URLs down to players that player the specified position
    df_urls = df_urls[df_urls['position'] == position]
    # Convert the URL dataframe to a list of dictionaries
    list_url_dicts = df_urls.to_dict('records')
    
    # split list into batches to counteract possible scraping time-out
    list_url_batches = [list_url_dicts[i:i+100] for i in range(
            0, len(list_url_dicts), 100)]
    
    # For each player scraped, retreive their personal inforamtion
    count = 0
    for batch in tqdm.tqdm(list_url_batches):
        list_dicts = scrapePlayerInfo(batch)
        df_batch = pd.DataFrame(list_dicts)
        df_batch.to_csv('positionData/' + position_folder + '/player_info_' 
                        + position + '_' + str(count) + '.csv', index=False)
        count += 1   

def scrapePlayerInfo(list_urls):
    '''
    Purpose: Extract player information for every URL provided (from ESPN.com)

    Inputs
    ------
        list_urls : list of dictionaries
            Each dictionary contains a URL for player-specific page on ESPN.com
            and the player's position
            
    Outputs
    -------
        list_player : list of dictionaries
            List in which each element is a dictionary containing 
            player-specific information
    '''
    list_players = []
    for player_dict in tqdm.tqdm(list_urls):
        url = player_dict['url']
        position = player_dict['position']        
        
        dict_player = {}
        dict_player['url'] = url
        soup = soupifyURL(url)
        
        playerHeader = soup.find('div', {'class':'PlayerHeader'})
        if playerHeader != None:
            #----------------------------------------------------------------------
            # Name Values
            #----------------------------------------------------------------------
            # Name - First
            nameFirst = playerHeader.find(
                    'span', {'class':'truncate min-w-0 fw-light'}).text
            dict_player['nameFirst'] = nameFirst
            # Name - Last
            dict_player['nameLast'] = playerHeader.find(
                    'span', {'class':'truncate min-w-0'}).text
            # Name - Full
            dict_player['nameFull'] = (dict_player['nameFirst'] + ' ' + 
                       dict_player['nameLast'])
            #----------------------------------------------------------------------
            # School and Position
            #----------------------------------------------------------------------
            school = playerHeader.find(
                    'ul',{'class':('PlayerHeader__Team_Info list flex pt1 pr4 ' + 
                                   'min-w-0 flex-basis-0 flex-shrink flex-grow ' + 
                                   'nowrap')})
            if len(school.findAll('li')) == 3:
                # School
                dict_player['school'] = school.findAll('li')[0].text
            # Position
            dict_player['position'] = position
    
            #----------------------------------------------------------------------
            # Height, Weight, College, Hometown, Date of Birth (DOB) and Draft Info
            #----------------------------------------------------------------------
            playerBio = playerHeader.find('div', {'class':('flex brdr-clr-gray-07'+
                                                           ' pl4 bl bl--dotted n8')})
            bio_vars = playerBio.find(
                    'div', {'class':'PlayerHeader__Bio_List flex flex-column ttu ' 
                            + 'clr-gray-04 mr4'})
            list_bio_vars = [bio_var.text for bio_var in bio_vars]
            bio_values = playerBio.find(
                    'div', {'class':'PlayerHeader__Bio_List flex flex-column ' +
                            'clr-black fw-medium'})
            list_bio_values = [bio_value.text for bio_value in bio_values]
    
            #----------- Height and Weight -------------#
            if 'HT/WT' in list_bio_vars:
                try:
                    value = list_bio_values[list_bio_vars.index('HT/WT')]
                    # Height 
                    height = value.split(',')[0].strip()
                    dict_player['height'] = height
                    if 'm' not in height:   # some heights are in meters
                        # Height (in Inches)
                        dict_player['heightInches'] = int(
                                height.split("'")[0])*12 + int(
                                height.split(" ")[1].split('"')[0])
                        # Weight (in lbs)
                        dict_player['weight'] = value.split(
                                ',')[1].strip().split(' ')[0]
                except:
                    pass
    
            #----------- Hometown -------------#
            if 'Hometown' in list_bio_vars:
                hometown = list_bio_values[list_bio_vars.index('Hometown')]
                if hometown != 'USA':
                    # Hometown
                    dict_player['hometown'] = hometown
                    # Hometown - City
                    try:
                        dict_player['hometownCity'] = hometown.split(', ')[0]
                        # Hometown - State        
                        dict_player['hometownState'] = hometown.split(', ')[1]
                    except:
                        pass
                    
            #----------- Date of Birth (DoB) -------------#
            if 'DOB' in list_bio_vars:
                dob = list_bio_values[list_bio_vars.index('DOB')].strip()
                dict_player['birthday'] = dob
                
            #----------- College -------------#
            if 'College' in list_bio_vars:
                dict_player['college'] = list_bio_values[list_bio_vars.index('College')]
             
            #----------- Draft Info -------------#
            if 'Draft Info' in list_bio_vars:
                draftInfo = list_bio_values[list_bio_vars.index('Draft Info')].strip()
                dict_player['draftYear'] = draftInfo.split(':')[0]
                dict_player['draftRound'] = draftInfo.split('Rd ')[1].split(',')[0]
                dict_player['draftRoundPick'] = draftInfo.split('Pk ')[1].split(' ')[0]
                dict_player['draftTeam'] = draftInfo.split(' ')[-1].strip('(').strip(')')
    
            #----------------------------------------------------------------------
            # Pictures (School and Player)
            #----------------------------------------------------------------------
            # Picture URL (school)
            pictureSchool = playerHeader.find('div', {
                    'class':'Image__Wrapper aspect-ratio--1x1'})
            if pictureSchool != None:
                if pictureSchool.source['srcset'] != ('https://a.espncdn.com/' + 
                                       'combiner/i?img=/i/teamlogos/leagues/500/' + 
                                       'nfl.png&w=250&h=250'):
                    dict_player['pictureSchool'] = pictureSchool.source['srcset']
            # Picture URL (player)
            picturePlayer = playerHeader.find('div', {
                    'class':'Image__Wrapper aspect-ratio--auto'})
            if picturePlayer != None:
                dict_player['picturePlayer'] = picturePlayer.source['srcset']
            
        # Add player dictionary to list of all players scraped
        list_players.append(dict_player)
        
        time.sleep(1)
        
    return list_players

def scrapePositionLinks(position):
    '''
    Purpose: Extract URLs for every player within a specified position group

    Inputs
    ------
        position : string
            Football position for which player info is to be scraped 
            (i.e. QB, RB, WR, TE, etc...)
    
    Outputs
    -------
        list_urls_position : list
            list of URLs which direct to individual player pages
    '''
    if position == 'QB':
        category = 'passing'
    elif position == 'RB':
        category = 'rushing'
    elif position in ['WR','TE']:
        category = 'receiving'
    elif position == 'DEF':
        category = 'defense'
    url = ('http://www.espn.com/college-football/conferences/statistics/' + 
           'player/_/stat/' + category + '/id/99')
    
    soup = soupifyURL(url)
    
    # Find the years available within the data
    list_years_available = []
    soup_years_available = soup.find('select', {'class':'tablesm'})
    html_years_available = soup_years_available.findAll('option')
    for html in html_years_available:
        list_years_available.append(html.text)

    # For every available year, scrape info for all position players in that year
    countList = 0
    for year in tqdm.tqdm(list_years_available):
        url_year = ('http://www.espn.com/college-football/conferences/' + 
                    'statistics/player/_/stat/' + category + '/year/' +
                    year + '/id/99')

        list_urls_position = []
        
        next_page = True
        count = 0
        while (next_page == True):
            soup = soupifyURL(url_year)
            table_players = soup.find('table', {'class':'tablehead'})
        
            # grab information for every player on screen
            for row in table_players.findAll('tr'):
                # skip the header unique to defense
                if (position == 'DEF') and (len(row) < 6):
                    continue                    
                info = row.findAll('td')[1]
                
                # only keep info for players that match the desired position
                if info.text != 'PLAYER':
                    url = info.a['href']
                    pos = info.text.split(', ')[1]
                    list_urls_position.append([url, pos])
                        
            # Check to see if another page of players exists
            soup_next_page = soup.find('div', {'class':'controls'})
            if soup_next_page.find('div', {'class':
                'jcarousel-next jcarousel-next-disabled'}) == None:
                url_year = 'http:' + soup_next_page.findAll('a')[-1]['href']
            else:
                next_page = False
            count+=1
            print(count)
        
        # Backup URL list to a .csv file for sanity reasons
        df = pd.DataFrame.from_records(
                list_urls_position, columns = ['url', 'position'])
        filename = path_dir.joinpath(
                'positionData/' + position + '/player_urls_' + position +
                '_' + str(countList) + '.csv')
        df.to_csv(filename, index=False) 
        countList += 1

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def scrapeURLs(position):
    '''
    Purpose: Obtain the urls for every player in a position group from ESPN.com
        for all available years

    Inputs
    ------
        position : string
            Position group to be scraped
    
    Outputs
    -------
        list_urls : list of strings
            List in which each element is a URL to a player-specific page
            on ESPN.com (OUTPUT TO DISK -- `player_urls_POS.csv`)
    '''    
    # Scrape player URLs for specified position
    scrapePositionLinks(position)
    
    # Create a master URL csv from all sub-files
    list_url_files = natural_sort(
            glob.glob('positionData/' + position + '/player_urls_' +
                      position + '_*.csv'))

    df_url = pd.DataFrame()
    for url_file in list_url_files:
        if len(df_url) == 0:
            df_url = pd.read_csv(url_file)
        else:
            df_url = df_url.append(pd.read_csv(url_file))
    df_url.drop_duplicates(inplace=True)

    filename = path_dir.joinpath(
            'positionData/' + position + '/player_urls_' + position + '.csv')
    df_url.to_csv(filename, index=False) 
    
    return df_url

def soupifyURL(url):
    '''
    Purpose: Turns a specified URL into BeautifulSoup formatted HTML 

    Inputs
    ------
        url : string
            Link to the designated website to be scraped
    
    Outputs
    -------
        soup : html
            BeautifulSoup formatted HTML data stored as a complex tree of 
            Python objects
    '''
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    r = session.get(url)
    #r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')   
    return soup
    
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
path_dir = pathlib.Path('/home/ejreidelbach/Projects/draft-gem/src/static/')
os.chdir(path_dir)

# ask the user what position(s) to scrape URLs for
list_pos_scrape_url = askUserForPositionURL()

# scrape position information for the specified position group
for pos_scrape_url in list_pos_scrape_url:
    # ensure a position was actually selected
    if pos_scrape_url != 'NONE':
        # scrape the URLs for the specified position
        df_position_urls = scrapeURLs(pos_scrape_url)

# ask the user if they want to scrap player-specific information
list_pos_scrape_info = askUserForPositionInfo()

for position_scrape in list_pos_scrape_info:
    # ensure a position was actually selected    
    if position_scrape != 'NONE':
        position_folder = ''
        if position_scrape in ['WR', 'TE']:
            position_folder = 'WR'
        elif position_scrape in ['RB', 'FB']:
            position_folder = 'RB'
        elif position_scrape in ['QB']:
            position_folder = 'QB'
        elif position_scrape in ['CB', 'DB', 'DE', 'DT', 'DL', 'LB', 'NT', 'S']:
            position_folder = 'DEF'
        
        # scrape the player information for the specified position
        runInfoScraping(position_scrape, position_folder)
        
        # merge all the batched files into one cohesive group for each position
        mergePositionFiles(position_scrape, position_folder)