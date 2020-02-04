import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from football_func import *
from random import sample

plt.style.use('fivethirtyeight')

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

def get_cols_all():
    fname = 'helpers/all_plays_cols.txt'
    cols = []
    with open(fname, 'r') as f:
        for row in f:
            idx = row.find('\n')
            cols.append(row[:idx])
    return cols

def get_all_plays(c = None):
    df = pd.read_csv('data/all_plays2.csv', usecols = c)
    return df

def jitter(arr):
    j = np.random.rand(len(arr))
    return (j - 0.5)/10

def outcome_masks(df):
    m0 = df['ends_TD'] == 1
    m1 = df['ends_FG'] == 1
    m2 = df['ends_punt'] == 1
    m3 = df['ends_other'] == 1
    return m0, m1, m2, m3

if __name__ == '__main__':
    # plays = get_all_plays()
    # plays['game_date'] = pd.to_datetime(plays['game_date'])
    # plays_train, plays_hold = split_data(plays)
    # plays_train.to_csv('data/all_plays_train.csv')
    # plays_hold.to_csv('data/all_plays_holdout.csv')
    # del(plays_hold)
    cols = get_cols_all()
    plays = pd.read_csv('data/all_plays_train.csv', usecols = cols)
    cols = get_cols_start()
    start_pos = get_pos_starts(cols)
    start_pos.drop_duplicate(inplace = True)
    
    # scatter plot of yards to go and outcome
    fig, ax = plt.subplots(1,1, figsize = (10, 5))
    masks = outcome_masks(plays)
    colors = ['b', 'r', 'g' ,'orange']
    labels = ['TD', 'FG', 'Punt', 'Other']
    samp = plays.sample(10000)
    yard = samp['yardline_100'].notna()
    scrim = samp['down'].notna()
    for i, m in enumerate(masks):
        ax.scatter(samp['yardline_100'][scrim & yard & m], jitter(samp['yardline_100'][scrim & yard & m]), color = colors[i], alpha = 0.15, label = labels[i])
    ax.legend()
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xlabel('Yards to End Zone')
    ax.set_title('Outcome by Yards to the End Zone -- All Plays')
    plt.tight_layout(pad=1)
    plt.savefig('images/all_yards_scatter.jpeg')
    plt.close()

    fig, ax = plt.subplots(1,1, figsize = (10, 5))
    masks = outcome_masks(start_pos)
    colors = ['b', 'r', 'g' ,'orange']
    labels = ['TD', 'FG', 'Punt', 'Other']
    samp = start_pos.sample(10000)
    yard = samp['yardline_100'].notna()
    for i, m in enumerate(masks):
        ax.scatter(samp['yardline_100'][yard & m], jitter(samp['yardline_100'][yard & m]), color = colors[i], alpha = 0.15, label = labels[i])
    ax.legend()
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xlabel('Yards to End Zone')
    ax.set_title('Outcome by Yards to the End Zone -- 1st Play of Pos.')
    plt.tight_layout(pad=1)
    plt.savefig('images/start_pos_scatter.jpeg')
    plt.close()


    

