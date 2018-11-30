College Football Analysis
==============================

![Project Logo](https://github.com/ereidelbach/Images/blob/master/CFB%20Logo.png?raw=true)

# Data Processing Flow

1. Run scrape_CFBStats.py
- Scrape data from the CFBStats based on user input (e.g. all available years or a specific year)
2. Run aggregate_CFBStats_by_team.py
- Aggregates all yearly statistics for each team into one file per sub-category per year**
3. Run aggregate_CFBStats_by_year.py
- Aggregates all files for each team into one file per statistical category 

This flow results in one 17 total files containing all statistical data from all teams and players from 2009-2018.  These files, listed below, are contained in the folder /data/interim/CFBStats/ALL/merged_final.

- game_defense.csv
- game_offense.csv
- game_special_defense.csv
- game_special_offense.csv
- players_defense.csv
- players_offense.csv
- players_special_kicking.csv
- players_special_return.csv
- records.csv
- rosters.csv
- schedules.csv
- situational_defense.csv
- situational_offense.csv
- split_defense.csv
- split_offense.csv
- split_special_defense.csv
- split_special_offense.csv

**NOTE:  Examples of categories include 'offense', 'defense' and 'special teams' whereas sub-categories are specific subsets of the categories.  For example, sub-categories of 'offense' would include 'passing', 'rushing', or 'receiving.'
------------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
