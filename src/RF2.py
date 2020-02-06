import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.ensemble import RandomForestClassifier as RFC 
from sklearn.metrics import classification_report
from football_func import *
from pprint import pprint



if __name__ == '__main__':
    start_cols = get_cols_start()
    start = pd.read_csv('data/start_pos_s3.csv', usecols = start_cols)
    start = remove_na_yardline(start)
    start['game_date'] = pd.to_datetime(start['game_date'])
    start['is_EOH'] = start.apply(lambda row: end_of_half_det(row), axis = 1)
    start['target'] = start.apply(lambda row: make_target(row), axis = 1)
    merge_cols = get_cols_merge()
    plays = pd.read_csv('data/all_plays_enhanced.csv', usecols = merge_cols)
    start = pd.merge(start, plays, how = 'left', on = ['game_id', 'play_id']).copy()
    start.dropna(inplace = True)
    del(plays)
    train, val = split_data(start)
    del(start)
    to_drop = ['Unnamed: 0', 'home_team', 'posteam', 'game_date', 'game_id', 'play_id', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other', 'target']
    features = [c for c in train.columns if c not in to_drop]
    X_train = train[features].values
    y_train = train['target'].values
    X_test = val[features].values
    y_test = val['target'].values

    rf = RFC(n_estimators = 500, max_depth = 40, min_samples_leaf = 5, bootstrap = False, n_jobs = -1)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    score = rf.score(X_test, y_test)
    pprint(f'RF Accuracy: {score:0.4f}')

    report = classification_report(y_test, y_pred)
    pprint(report)

    feat_imp_idx = np.argsort(rf.feature_importances_)[::-1]
    plot_feat_imp(feat_imp_idx, features, rf.feature_importances_, 7, 'images/rf2.jpeg')