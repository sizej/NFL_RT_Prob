import pandas as pd 
import numpy as np 
from random import sample 
import datetime as dt 
import matplotlib.pyplot as plt 

def pos_expected_points(row):
    '''
    Calculates expected total points for the offense, based on over-under line, spread, and team
    '''
    if row['posteam'] == row['favorite']:
        return row['spread'] + ((row['total'] - row['spread'])/ 2)
    else:
        return (row['total'] - row['spread'])/ 2

def def_expected_points(row):
    '''
    Calculates expected total points for the defense, based on over-under line, spread, and team
    '''
    if row['posteam'] == row['favorite']:
        return (row['total'] - row['spread'])/ 2
    else:
        return row['spread'] + ((row['total'] - row['spread'])/ 2)

def touchdown_det(touchdown, td_team, pos_team):
    '''
    Takes in row data and returns if play ended in touchdown for possessing team
    '''
    if touchdown == 1 and td_team == pos_team:
        return 1
    else:
        return 0

def fg_det(fg_result):
    '''
    Takes in row data and returns if play ended in made fg for possessing team
    '''
    if fg_result == 'made':
        return 1
    else:
        return 0

def punt_det(play):
    '''
    Takes in play_type and returns if punt was attempted or not
    '''
    if play == 'punt':
        return 1
    else:
        return 0

def other_det(row):
    '''
    If it isn't a TD, FG, or Punt, it's other...
    '''
    if row['play_TD'] + row['play_FG'] + row['play_punt'] == 0:
        return 1
    else:
        return 0

def start_possession(df):
    '''
    Takes in df of all plays, returns a df of just the plays that are the start of a new possesion.
    New possession does not include kick-off (un-timed down).
    '''
    c = df.columns
    first = pd.DataFrame(columns = c)
    for drive in df['drive_id'].unique():
        m0 = df['drive_id'] == drive
        m1 = df['down'] == 1
        drive = df[m0 & m1]
        m2 = drive['game_seconds_remaining'] == drive['game_seconds_remaining'].max()
        first = first.append(drive[c][m2]).copy()
    return first     

def split_data(df):
    '''
    Takes in df of plays, splits into training and hold-out sets, based on game date.
    '''
    train_mask = df['game_date'] <= dt.datetime(2018, 8, 1)
    hold_mask = df['game_date'] > dt.datetime(2018, 8, 1)
    return df[train_mask], df[hold_mask]

def tt_split(df, prop = 0.8):
    '''
    Takes in df and returns train-test split, based on game_id, so an entire game is either in training or test.
    '''
    games = set(df['game_id'].unique())
    size = int(prop * len(games))
    train_idx = sample(games, k = size)
    test_idx = [x for x in games if x not in train_idx]
    m0 = df['game_id'].isin(train_idx)
    m1 = df['game_id'].isin(test_idx)
    df1 = df[m0].copy()
    df1.drop(['game_id'], axis = 1, inplace = True)
    df2 = df[m1].copy()
    df2.drop(['game_id'], axis = 1, inplace = True)
    return df1, df2
 
 
def make_target(row):
    '''
    Convert target columns into single label column.
    '''
    if row['ends_TD'] == 1:
        return 'TD'
    elif row['ends_FG'] == 1:
        return 'FG'
    elif row['ends_punt'] == 1:
        return 'punt'
    else:
        return 'other'

def end_of_half_det(row):
    '''
    Binary flag for possessions starting w/in the last two minutes of half.
    '''
    if (1800 <= row['game_seconds_remaining'] <= 1920) or row['game_seconds_remaining'] <= 120:
        return 1
    else:
        return 0

def remove_na_yardline(df):
    '''
    Very few yardlines are missing - exclude them.
    '''
    m0 = df['yardline_100'].notna()
    return df[m0].copy()


def plot_feat_imp(idx, features, feat_importances,  n = 5, fname = 'images/test.jpeg'):
    '''
    Plot the top n features.
    '''
    labels = np.array(features)[idx[:n]]
    fig, ax = plt.subplots(1,1, figsize = (10,5))
    ax.barh(range(n), feat_importances[idx[:n]], color = 'b', alpha = 0.85)
    # ax.set_xticklabels(labels)
    ax.set_title('Feature Importance')
    plt.yticks(ticks = range(n), labels = labels)
    plt.tight_layout(pad = 1)
    plt.savefig(fname)

def get_pos_starts(c = None):
    df = pd.read_csv('data/start_pos2_s3.csv', usecols = c)
    return df

def get_cols_start():
    fname = 'helpers/start_pos_cols.txt'
    cols = []
    with open(fname, 'r') as f:
        for row in f:
            idx = row.find('\n')
            cols.append(row[:idx])
    return cols

def get_cols_merge():
    fname = 'helpers/cols_merge.txt'
    cols = []
    with open(fname, 'r') as f:
        for row in f:
            idx = row.find('\n')
            cols.append(row[:idx])
    return cols

if __name__ == '__main__':
    pass