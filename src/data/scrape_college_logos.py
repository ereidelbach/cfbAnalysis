#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 14:23:21 2018

@author: ejreidelbach

:DESCRIPTION:
    - Scrape FBS team, conference and bowl logos from www.sportslogos.net

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import os  
import pathlib
import requests
from requests.packages.urllib3.util.retry import Retry
import shutil
import tqdm
from bs4 import BeautifulSoup

#==============================================================================
# Function Definitions / Reference Variable Declaration
#==============================================================================
def soupifyURL(url):
    '''
    Purpose: Turns a specified URL into BeautifulSoup formatted HTML 

    Input: 
        (1) url (string): Link to the designated website to be scraped
    
    Output: 
        (1) soup (html): BeautifulSoup formatted HTML data stored as a
                complex tree of Python objects
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

def directoryCheck():
    '''
    Purpose: Run a check of the /images/ folder to see if a folder
        exists for team, bowl and conference logos which will be scraped from
        sportslogos.net
        
    Input:
        - NONE
    
    Outpu:
        - NONE
    '''
    # Check for the team folder
    pathlib.Path('images/logos_bowl').mkdir(parents=True, exist_ok=True)
    pathlib.Path('images/logos_conf').mkdir(parents=True, exist_ok=True)
    pathlib.Path('images/logos_team').mkdir(parents=True, exist_ok=True)
    return

def writeLogoToFile(logo_type, logo_size, name, url, path_project):
    '''
    Purpose: Given a url directing to an image, request the file and save
        it to the local drive
        
    Input:
        (1) logo_type (string): Type of logo being scraped [bowl, conf, team]
        (2) logo_size (string): Size of the logo being scraped [thumb, logo]
        (3) name (string): Name of the logo being scraped
        (4) url (string): Initial URL of logos to be scraped
        (5) path_project (pathlib Path): Directory file path of the project
        
    Output:
        - NONE
    '''   
    # create the logo filename
    filename = name + '_' + logo_size + '.' + url.split('.')[-1]
    # retrieve the image from the site
    response = requests.get(url, stream=True)
    # open the local file to write it to disk
    with open(path_project.joinpath('images/logos_' +
                                    logo_type, filename), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def scrapeLogos(path_project, url, type_logo):
    '''
    Purpose: Scrapes the logos for every FBS team, conference or bowl game
        
    Input:
        (1) path_project (pathlib Path): Directory file path of the project
        (2) url (string): Initial URL of logos to be scraped
        (3) type_logo (string): Type of logo being scraped [bowl, conf, team]
        
    Output:
        - NONE
    '''   
    soup = soupifyURL(url)
    
    logowall = soup.find('ul', {'class':'logoWall'})
    list_logos = logowall.findAll('li', {'style':'height:155px;'})
    
    for logo in tqdm.tqdm(list_logos):
        # find the item name
        name = logo.find('a').text.strip()
        name = name.replace('  ',' ').replace('/','-')
        # find the thumbnail logo
        url_thumb = logo.find('img')['src']
        # save the thumbnail to disk
        writeLogoToFile(type_logo, 'thumb', name, url_thumb, path_project)
        
        # find the large logo
        soup_largeA = soupifyURL('http://www.sportslogos.net/' 
                               + logo.find('a')['href'])
        logowall_large = soup_largeA.find('ul', {'class':'logoWall'})
        list_logos_large = logowall_large.findAll('li')
        soup_largeB = soupifyURL('http://www.sportslogos.net/' 
                                     + list_logos_large[-1].find('a')['href'])
        logo_large = soup_largeB.find('div', {'class':'mainLogo'})
        url_logo = logo_large.find('img')['src']
        # save the large logo to disk
        writeLogoToFile(type_logo, 'logo', name, url_logo, path_project)
        
#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
path_project = pathlib.Path(__file__).resolve().parents[2]
os.chdir(path_project)

# Ensure the folder we'll be writing to exists
directoryCheck()

# Step 1: Scrape conference logos from sportslogos.net
url_bowl = ('http://www.sportslogos.net/teams/list_by_league/68/' + 
            'NCAA_Bowl_Games/NCAA_Bowls/logos/')
scrapeLogos(path_project, url_bowl, 'bowl')

# Step 2: Scrape bowl logos from sportslogos.net
url_conf = ('http://www.sportslogos.net/teams/list_by_league/153/' + 
            'NCAA_Conferences/NCAA_Conf/logos/')
scrapeLogos(path_project, url_conf, 'conf')

# Step 3: Scrape team logos from sportslogos.net
team_logos_prefix = 'http://www.sportslogos.net/teams/list_by_league/'
list_team_logos = [
        '30/NCAA_Division_I_a-c/NCAA_a-c/logos/'
        ,'31/NCAA_Division_I_d-h/NCAA_d-h/logos/'
        ,'32/NCAA_Division_I_i-m/NCAA_i-m/logos/'
        ,'33/NCAA_Division_I_n-r/NCAA_n-r/logos/'
        ,'34/NCAA_Division_I_s-t/NCAA_s-t/logos/'
        ,'35/NCAA_Division_I_u-z/NCAA_u-z/logos/'
        ]
for team_logo_suffix in list_team_logos[4:]:
    url_team = team_logos_prefix + team_logo_suffix
    scrapeLogos(path_project, url_team, 'team')