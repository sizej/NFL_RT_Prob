import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import datetime as dt 
from team_dict import team_dict
from football_func import *

def get_cols():
    fname = 'helpers/cols2use.txt'
    cols = []
    with open(fname, 'r') as f:
        for row in f:
            idx = row.find('\n')
            cols.append(row[:idx])
    return cols

def get_plays_df():       
    plays = pd.read_csv('data/plays_09_18.csv', nrows = 10000, usecols = cols)
    return plays

if __name__ == '__main__':
    cols = get_cols()
    plays = get_plays_df()
    plays['game_date'] = pd.to_datetime(plays['game_date'])
    
    # Get historical gambling info....
    hist = pd.read_csv('data/spreadspoke_scores.csv')
    hist['schedule_date'] = pd.to_datetime(hist['schedule_date'])
    m0 = hist['schedule_date'] >= plays['game_date'].min()
    m1 = hist['schedule_date'] <= plays['game_date'].max()
    hist['team_home'] = hist['team_home'].map(team_dict)
    hist['team_away'] = hist['team_away'].map(team_dict)
    hist['spread'] = np.abs(hist['spread_favorite'])
    hist.rename(columns = {'schedule_date': 'game_date',
                            'team_home': 'home_team',
                            'team_away': 'away_team',
                            'team_favorite_id': 'favorite'}, inplace=True)
    hist_cols = ['game_date', 'home_team', 'away_team', 'favorite', 'spread', 'over_under_line']
    hist_merge = hist[hist_cols][m0 & m1].copy()
    hist_merge['total'] = pd.to_numeric(hist_merge['over_under_line'])
    hist_merge.drop(['over_under_line'], axis = 1, inplace = True)
    plays = pd.merge(plays, hist_merge, how = 'left', on = ['game_date','home_team','away_team'])

    # Make some columns for expected points (total, pace, etc.)
    plays['pos_EP_total'] = plays.apply(lambda row: pos_expected_points(row), axis = 1)
    plays['def_EP_total'] = plays.apply(lambda row: def_expected_points(row), axis = 1)
    plays['pos_EP_pace'] = plays['posteam_score_post'] - (1 - plays['game_seconds_remaining']/3600) * plays['pos_EP_total']
    plays['def_EP_pace'] = plays['defteam_score_post'] - (1 - plays['game_seconds_remaining']/3600) * plays['def_EP_total']
    plays['pos_fave'] = (plays['posteam'] == plays['favorite']).astype(int)
    
    # Create unique drive_id for each possession
    plays['drive_id'] = plays.apply(lambda row: str(row['game_id']) + str(row['drive']), axis = 1)
    # Code the outcomes for each possession
    plays['play_TD'] = plays.apply(lambda row: touchdown_det(row['touchdown'], row['td_team'], row['posteam']), axis = 1)
    plays['play_FG'] = plays.apply(lambda row: fg_det(row['field_goal_result']), axis = 1)
    plays['play_punt'] = plays.apply(lambda row: punt_det(row['play_type']), axis = 1)
    drive_df = plays.groupby('drive_id').agg({'play_TD': 'sum',
                                                'play_FG': 'sum',
                                                'play_punt': 'sum'}).reset_index()
    drive_df['pos_other'] = drive_df.apply(lambda row: other_det(row), axis = 1)
    drive_df.columns = ['drive_id', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other']
    # This df has all plays and how that possession ends.....
    plays = pd.merge(plays, drive_df, how = 'left', left_on = 'drive_id', right_on = 'drive_id').copy()
    plays.to_csv('data/all_plays.csv')
    start = start_possession(plays)
    start.to_csv('data/start_pos.csv')