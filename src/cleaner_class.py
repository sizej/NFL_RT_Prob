import pandas as pd 
import numpy as np 
import datetime as dt 
from random import sample 
from team_dict import team_dict


class PossessionStart(object):

    def __init__(self, fname):
        self.get_start_cols()
        self.raw = pd.read_csv(fname, usecols = self.cols)
        self.clean_up()
        self.make_splits()

    def get_start_cols(self):
        fname = 'helpers/start_pos_cols.txt'
        cols = []
        with open(fname, 'r') as f:
            for row in f:
                idx = row.find('\n')
                cols.append(row[:idx])
        self.cols = cols

    def add_cols(self):
        self.raw['target_cat'] = self.raw.apply(lambda row: self.make_target_cat(row), axis = 1)
        self.raw['target_num'] = self.raw.apply(lambda row: self.make_target_num(row), axis = 1)
        self.raw['is_EOH'] = self.raw.apply(lambda row: self.end_of_half_det(row), axis = 1)

    def clean_up(self):
        self.raw = self.remove_na_yardline()
        self.raw['game_date'] = pd.to_datetime(self.raw['game_date'])
        self.add_cols()

    def remove_na_yardline(self):
        m0 = self.raw['yardline_100'].notna()
        return self.raw[m0].copy()

    def make_target_cat(self, row):
        if row['ends_TD'] == 1:
            return 'TD'
        elif row['ends_FG'] == 1:
            return 'FG'
        elif row['ends_punt'] == 1:
            return 'punt'
        else:
            return 'other'

    def make_target_num(self, row):
        target_dict = {'TD': 0, 'FG': 1, 'punt': 2, 'other': 3}
        return target_dict[row['target_cat']]

    def end_of_half_det(self, row):
        if (1800 <= row['game_seconds_remaining'] <= 1920) or row['game_seconds_remaining'] <= 120:
            return 1
        else:
            return 0
    
    def tt_split(self, train_prop = 0.8):
        games = set(self.raw['game_id'].unique())
        size = int(train_prop * len(games))
        train_idx = sample(games, k = size)
        test_idx = [x for x in games if x not in train_idx]
        m0 = self.raw['game_id'].isin(train_idx)
        m1 = self.raw['game_id'].isin(test_idx)
        df1 = self.raw[m0].copy()
        df1.drop(['game_id'], axis = 1, inplace = True)
        df2 = self.raw[m1].copy()
        df2.drop(['game_id'], axis = 1, inplace = True)
        return df1, df2

    def make_splits(self):
        cutoff = dt.datetime(2018,1,1)
        m0 = self.raw['game_date'] < cutoff
        m1 = self.raw['game_date'] >= cutoff
        self.modeling = self.raw[m0].copy()
        self.holdout = self.raw[m1].copy()
        self.train, self.test = self.tt_split()
        

class HistGames(object):
    '''
    Cleaner class for the historical game data.
    '''

    def __init__(self, fname = 'data/Archive/spreadspoke_scores.csv'):
        self.df = pd.read_csv(fname)
        self.teams = team_dict
        self.clean_up()
    
    def clean_up(self):
        self.df['schedule_date'] = pd.to_datetime(self.df['schedule_date'])
        m0 = self.df['schedule_date'] > dt.datetime(2006,1,1)
        self.df['team_home'] = self.df['team_home'].map(self.teams)
        self.df['team_away'] = self.df['team_away'].map(self.teams)
        self.df['spread'] = np.abs(self.df['spread_favorite'])
        self.df.rename(columns = {'schedule_date': 'game_date',
                            'team_home': 'home_team',
                            'team_away': 'away_team',
                            'team_favorite_id': 'favorite'}, inplace=True)
        hist_cols = ['game_date', 'schedule_week', 'home_team', 'away_team', 'favorite', 'spread', 'over_under_line']
        self.merge = self.df[hist_cols][m0].copy()
        self.merge['total'] = pd.to_numeric(self.merge['over_under_line'])
        self.merge.drop('over_under_line', axis = 1, inplace = True)


class AllPlays(object):
    '''
    Cleaner class for all plays.
    '''

    def __init__(self, fname = 'data/all_plays_enhanced2.csv', cols_file = 'LSTM'):
        self.cols_file = cols_file
        if self.cols_file == 'LSTM':
            self.use_cols = self.get_LSTM_cols()
        elif self.cols_file == 'RF':
            self.use_cols = self.get_cols_other()
        self.data = pd.read_csv(fname, usecols = self.use_cols)
        self.remove_useless_na()
        self.add_cols()
        self.make_splits()
        self.make_matrices()

    def make_matrices(self):
        cols_to_exclude = ['game_id', 'play_id', 'drive', 'game_date', 'posteam', 'home_team', 
                            'away_team', 'target_num', 'target_cat', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other']
        self.features = [c for c in self.train.columns if c not in cols_to_exclude]
        self.y_train = self.train['target_num'].values
        self.y_test = self.test['target_num'].values
        self.X_train = self.train[self.features].values
        self.X_test = self.test[self.features].values
    
    def get_LSTM_cols(self):
        fname = 'helpers/cols_all_plays_LSTM.txt'
        cols = []
        with open(fname, 'r') as f:
            for row in f:
                idx = row.find('\n')
                cols.append(row[:idx])
        return cols

    def get_cols_other(self):
        fname = 'helpers/cols_all_plays_RF.txt'
        cols = []
        with open(fname, 'r') as f:
            for row in f:
                idx = row.find('\n')
                cols.append(row[:idx])
        return cols

    def make_splits(self, test_date = dt.datetime(2018,1,1)):
        self.data['game_date'] = pd.to_datetime(self.data['game_date'])
        m0 = self.data['game_date'] < test_date
        self.modeling = self.data[m0].copy()
        self.holdout = self.data[~m0].copy()
        self.train, self.test = self.tt_split()


    def tt_split(self, train_prop = 0.8):
        games = set(self.modeling['game_id'].unique())
        size = int(train_prop * len(games))
        train_idx = sample(games, k = size)
        test_idx = [x for x in games if x not in train_idx]
        m0 = self.modeling['game_id'].isin(train_idx)
        m1 = self.modeling['game_id'].isin(test_idx)
        df1 = self.modeling[m0].copy()
        df1.drop(['game_id'], axis = 1, inplace = True)
        df2 = self.modeling[m1].copy()
        df2.drop(['game_id'], axis = 1, inplace = True)
        return df1, df2
    
    def add_cols(self):
        self.data['target_cat'] = self.data.apply(lambda row: self.make_target_cat(row), axis = 1)
        self.data['target_num'] = self.data.apply(lambda row: self.make_target_num(row), axis = 1)
        self.data['is_EOH'] = self.data.apply(lambda row: self.end_of_half_det(row), axis = 1)
        self.data['pos_home'] = (self.data['posteam'] == self.data['home_team']).astype(int)

    def remove_useless_na(self):
        m0 = self.data['yardline_100'].notna()
        m1 = self.data['posteam'].notna()
        m2 = self.data['pos_pp_cume_yds'].notna()
        m3 = self.data['game_seconds_remaining'].notna()
        self.data['posteam_score'].fillna(0, inplace = True)
        self.data['defteam_score'].fillna(0, inplace = True)
        self.data['pos_EP_pace'].fillna(0, inplace = True)
        self.data['def_EP_pace'].fillna(0, inplace = True)
        self.data['pos_pp_cume_yds'].fillna(0, inplace = True)
        self.data['pos_yds_play'].fillna(0, inplace = True)
        self.data = self.data[m0 & m1 & m2 & m3].copy()

    def make_target_cat(self, row):
        if row['ends_TD'] == 1:
            return 'TD'
        elif row['ends_FG'] == 1:
            return 'FG'
        elif row['ends_punt'] == 1:
            return 'punt'
        else:
            return 'other'

    def make_target_num(self, row):
        target_dict = {'TD': 0, 'FG': 1, 'punt': 2, 'other': 3}
        return target_dict[row['target_cat']]

    def end_of_half_det(self, row):
        if (1800 <= row['game_seconds_remaining'] <= 1920) or row['game_seconds_remaining'] <= 120:
            return 1
        else:
            return 0    
