import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.ensemble import RandomForestClassifier as RFC 
from sklearn.metrics import classification_report
from football_func import *



if __name__ == '__main__':
    start_cols = get_cols_start()
    start = pd.read_csv('data/start_pos_s3.csv', usecols = start_cols, nrows = 200)
    start['game_date'] = pd.to_datetime(start['game_date'])
    merge_cols = get_cols_merge()
    plays = pd.read_csc('data/all_plays_enhanced.csv', usecols = merge_cols, nrows = 10000)
    start = pd.merge(start, plays, how = 'left', on = [['game_id', 'play_id']]).copy()