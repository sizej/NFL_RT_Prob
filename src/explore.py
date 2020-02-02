import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import datetime as dt 
from team_dict import team_dict

if __name__ == '__main__':
    fname = 'helpers/cols2use.txt'
    cols = []
    with open(fname, 'r') as f:
        for row in f:
            idx = row.find('\n')
            cols.append(row[:idx])        
    plays = pd.read_csv('data/plays_09_18.csv', nrows = 10000, usecols = cols)
    plays['game_date'] = pd.to_datetime(plays['game_date'])
    hist = pd.read_csv('data/spreadspoke_scores.csv')
    hist['schedule_date'] = pd.to_datetime(hist['schedule_date'])
    m0 = hist['schedule_date'] >= plays['game_date'].min()
    hist['team_home'] = hist['team_home'].map(team_dict)
    hist['team_away'] = hist['team_away'].map(team_dict)
    hist.rename(columns = {'schedule_date': 'game_date',
                            'team_home': 'home_team',
                            'team_away': 'away_team'}, inplace=True)
    hist_cols = ['game_date', 'home_team', 'away_team', 'team_favorite_id', 'spread_favorite', 'over_under_line']
    hist_merge = hist[hist_cols][m0].copy()
    plays = pd.merge(plays, hist_merge, how = 'left', on = ['game_date','home_team','away_team'])
    plays['drive_id'] = plays.apply(lambda row: str(row['game_id']) + str(row['drive']), axis = 1)
    

    # drive_df = plays.groupby('drive_id').agg({'sp': 'sum',
    #                                             'field_goal_result': 'sum',
    #                                             'punt_blocked': 'sum',
    #                                             'fourth_down_failed': 'sum',
    #                                             'interception': 'sum',
    #                                             'fumble_lost': 'sum',
    #                                             'touchdown': 'sum',
    #                                             'field_goal_attempt': 'sum'})