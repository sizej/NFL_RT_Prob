import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from football_func import *
from random import sample
from team_dict import team_dict
import datetime as dt

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

def plot_totals(df):
    '''
    Takes in plays df and plots the expected total against the observed total
    '''
    df['actual_total'] = df['score_home'] + df['score_away']
    fig, ax = plt.subplots(1,1, figsize = (8,6))
    ax.scatter(df['total'], df['actual_total'], alpha = 0.2, color = 'b')
    ax.plot(df['total'], df['total'], linestyle = '--', linewidth = 1, alpha = 0.75, color = 'r')
    ax.set_ylabel('Actual')
    ax.set_xlabel('Over-Under')
    ax.set_title('Total Points - Actual v Over-Under Line')
    plt.tight_layout(pad = 1)
    plt.savefig('images/actual_total.jpeg')

def fave_score_det(row):
    if row['home_team'] == row['favorite']:
        return row['score_home']
    else:
        return row['score_away']

def dawg_score_det(row):
    if row['home_team'] != row['favorite']:
        return row['score_home']
    else:
        return row['score_away']

def plot_fave_totals(df):
    '''
    Takes in plays df and plots the expected total for favorites against the observed total
    '''
    fig, ax = plt.subplots(1, 1, figsize = (8, 6))
    ax.scatter(df['fave_EP'], df['fave_score'], alpha = 0.2, color = 'b')
    ax.plot(df['fave_EP'], df['fave_EP'], linestyle = '--', linewidth = 1, color = 'r', alpha = 0.75)
    ax.set_ylabel('Actual')
    ax.set_xlabel('Expected')
    ax.set_title('Actual v Expected Points -- Favorites')
    plt.tight_layout(pad = 1)
    plt.savefig('images/favorites_points.jpeg')
    plt.close()

def plot_dawg_totals(df):
    '''
    Takes in plays df and plots the expected total for underdawgs against the observed total
    '''
    fig, ax = plt.subplots(1, 1, figsize = (8, 6))
    ax.scatter(df['dawg_EP'], df['dawg_score'], alpha = 0.2, color = 'b')
    ax.plot(df['dawg_EP'], df['dawg_EP'], linestyle = '--', linewidth = 1, color = 'r', alpha = 0.75)
    ax.set_ylabel('Actual')
    ax.set_xlabel('Expected')
    ax.set_title('Actual v Expected Points -- Underdawgs')
    plt.tight_layout(pad = 1)
    plt.savefig('images/dawgs_points.jpeg')
    plt.close()

def plot_season_totals(df):
    '''
    Season by season scoring totals
    '''
    df['season'] = [x.year for x in df['game_date']]
    season = df.groupby('season').agg({'total': 'mean'}).reset_index()
    fig, ax = plt.subplots(1,1)
    ax.bar(season['season'], season['total'], color = 'b', label = 'Mean Total', alpha = 0.85)
    ax.set_title('Mean Total by Season')
    ax.set_ylabel('Points per Game')
    ax.set_xlabel('Season')
    ax.set_xticks(np.arange(2009,2019))
    ax.set_xticklabels(season['season'])
    plt.xticks(rotation = 45)
    plt.tight_layout(pad = 1)
    plt.savefig('images/season_total.jpeg')
    plt.close()

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
    start_pos.drop_duplicates(inplace = True)
    start_pos['game_date'] = pd.to_datetime(start_pos['game_date'])
    start_pos['pos_home'] = (start_pos['posteam'] == start_pos['home_team']).astype(int)
    start_pos.drop(['posteam', 'home_team'], axis = 1, inplace = True)
    start_train, start_hold = split_data(start_pos)
    start_train.to_csv('data/start_pos_train.csv')
    start_hold.to_csv('data/start_pos_holdout.csv')
    del(start_hold)
    start_pos = start_train.copy()
    
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

    fig, ax = plt.subplots(1,1, figsize = (10,5))
    masks = outcome_masks(start_pos)
    colors = ['b', 'r', 'g' ,'orange']
    labels = ['TD', 'FG', 'Punt', 'Other']
    samp = start_pos.sample(10000)
    for i, m in enumerate(masks):
        ax.scatter(samp['game_seconds_remaining'][m]/60, jitter(samp['game_seconds_remaining'][m]), alpha = 0.15, color = colors[i], label = labels[i])
    ax.legend()
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xlabel('Minutes Left in Game')
    ax.set_title('Outcome by Time Left at Start of Possession')
    plt.tight_layout(pad = 1)
    plt.savefig('images/outcome_by_time.jpeg')
    plt.close()

    hist = pd.read_csv('data/Archive/spreadspoke_scores.csv')
    hist['schedule_date'] = pd.to_datetime(hist['schedule_date'])
    m0 = hist['schedule_date'] >= plays['game_date'].min()
    m1 = hist['schedule_date'] <= plays['game_date'].max()
    hist['team_home'] = hist['team_home'].map(team_dict)
    hist['team_away'] = hist['team_away'].map(team_dict)
    hist['spread'] = np.abs(hist['spread_favorite'])
    hist.rename(columns = {'schedule_date': 'game_date',
                            'team_home': 'home_team',
                            'team_away': 'away_team',
                            'team_favorite_id': 'favorite',
                            'over_under_line': 'total'}, inplace=True)
    hist_cols = ['game_date', 'home_team', 'away_team', 'favorite', 'spread', 'total', 'score_home', 'score_away']
    games = hist[hist_cols][m0 & m1].copy()
    games['total'] = pd.to_numeric(games['total'])
    games['spread'] = pd.to_numeric(games['spread'])
    games['fave_score'] = games.apply(lambda row: fave_score_det(row), axis = 1)
    games['dawg_score'] = games.apply(lambda row: dawg_score_det(row), axis = 1)
    games['fave_EP'] = (games['total'] + games['spread'])/2 + np.abs(games['spread'])
    games['dawg_EP'] = (games['total'] + games['spread'])/2
    plot_totals(games)
    plot_fave_totals(games)
    plot_dawg_totals(games)
    plot_season_totals(games)
