from sklearn.naive_bayes import GaussianNB as GNB 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from football_func import *


if __name__ == '__main__':
    start = pd.read_csv('data/start_pos_train.csv')
    start = remove_na_yardline(start)
    val = pd.read_csv('data/start_pos_holdout.csv')
    val = remove_na_yardline(val)
    target_dict = {'TD': 0, 'FG': 1, 'punt': 2, 'other': 3}
    start['target'] = start.apply(lambda row: make_target(row), axis = 1)
    start['target_num'] = start['target'].map(target_dict)
    start['is_EOH'] = start.apply(lambda row: end_of_half_det(row), axis = 1)
    start['pos_home'] = 
    val['target'] = val.apply(lambda row: make_target(row), axis = 1)
    val['target_num'] = val['target'].map(target_dict)
    val['is_EOH'] = val.apply(lambda row: end_of_half_det(row), axis = 1)
    to_drop = ['Unnamed: 0', 'game_date', 'game_id', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other', 'target', 'target_num', 'month']
    targets = ['ends_TD', 'ends_FG', 'ends_punt', 'ends_other']
    features = [c for c in start.columns if c not in to_drop]
    X_train = start[features].values
    y_train = start['target'].values
    X_test = val[features].values
    y_test = val['target'].values
    nb = GNB()
    nb.fit(X_train, y_train)
    score = nb.score(X_test, y_test)