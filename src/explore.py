import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from football_func import *

def get_pos_starts(c = None):
    df = pd.read_csv('data/start_pos_test.csv', usecols = c)
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

if __name__ == '__main__':
    plays = get_all_plays()
    plays['game_date'] = pd.to_datetime(plays['game_date'])
    plays_train, plays_hold = split_data(plays)
    plays_hold.to_csv('data/all_plays_holdout.csv')
    del(plays_hold)
    cols = get_cols_all()
    plays_train = plays_train[cols].copy()


