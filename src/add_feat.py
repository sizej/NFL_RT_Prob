import pandas as pd 
import numpy as np 


def home_yards(row):
    if row['posteam'] == row['home_team']:
        return row['yards_gained']
    else:
        return 0 

def away_yards(row):
    if row['posteam'] != row['home_team']:
        return row['yards_gained']
    else:
        return 0 

def pos_yards(row):
    if row['posteam'] == row['home_team']:
        return row['home_pp_cume_yds']
    else:
        return row['away_pp_cume_yds']

def pos_plays(row):
    if row['posteam'] == row['home_team']:
        return row['home_play_count']
    else:
        return row['away_play_count']

def pos_yds_per_play(row):
        if row['pos_play_count'] == 0:
            return 0
        elif row['posteam'] == row['home_team']:
            return row['home_pp_cume_yds'] / row['pos_play_count']
        else:
            return row['away_pp_cume_yds'] / row['pos_play_count']

def make_features(df):
    '''
    Returns the cumulative yards gained for a team in a game.
    '''
    out = pd.DataFrame()
    for game in df['game_id'].unique():
        m0 = df['game_id'] == game
        temp = df[m0].copy()
        temp['home_pp_cume_yds'] = temp['home_yards_gained'].cumsum() - temp['home_yards_gained']
        temp['away_pp_cume_yds'] = temp['away_yards_gained'].cumsum() - temp['away_yards_gained']
        temp['home_play'] = (temp['home_team'] == temp['posteam']).astype(int)
        temp['away_play'] = (temp['away_team'] == temp['posteam']).astype(int)
        temp['home_play_count'] = np.where(temp['home_play'] == 1, temp['home_play'].cumsum(), 0)
        temp['away_play_count'] = np.where(temp['away_play'] == 1, temp['away_play'].cumsum(), 0)
        temp.drop(['home_play', 'away_play'], axis = 1, inplace = True)
        out = out.append(temp).copy()
    return out


if __name__ == '__main__':
    plays = pd.read_csv('data/all_plays_S3.csv')
    m0 = plays['down'].notna()
    scrimmage = plays[m0].copy()
    scrimmage['home_yards_gained'] = scrimmage.apply(lambda row: home_yards(row), axis = 1)
    scrimmage['away_yards_gained'] = scrimmage.apply(lambda row: away_yards(row), axis = 1)
    scrimmage = make_features(scrimmage)
    scrimmage['pos_pp_cume_yds'] = scrimmage.apply(lambda row: pos_yards(row), axis = 1)
    scrimmage['pos_play_count'] = scrimmage.apply(lambda row: pos_plays(row), axis = 1)
    scrimmage['pos_yds_play'] = scrimmage.apply(lambda row: pos_yds_per_play(row), axis = 1)
    scrimmage.to_csv('data/all_plays_enhanced.csv')