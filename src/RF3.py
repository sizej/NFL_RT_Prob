import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from obj import PossessionStart
from sklearn.ensemble import RandomForestClassifier as RFC 
from sklearn.metrics import classification_report
from football_func import *
from pprint import pprint
from sklearn.inspection import plot_partial_dependence as plot_pd



if __name__ == '__main__':
    start = PossessionStart('data/start_pos_s3.csv')
    # merge_cols = get_cols_merge()
    # plays = pd.read_csv('data/all_plays_enhanced.csv', usecols = merge_cols)
    # start = pd.merge(start, plays, how = 'left', on = ['game_id', 'play_id']).copy()
    # start.dropna(inplace = True)
    # del(plays)
    # train, val = split_data(start)
    # del(start)
    # to_drop = ['Unnamed: 0', 'home_team', 'posteam', 'game_date', 'game_id', 'play_id', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other', 'target']
    # features = [c for c in train.columns if c not in to_drop]
    # X_train = train[features].values
    # y_train = train['target'].values
    # target_dict = {'TD': 0, 'FG': 1, 'punt': 2, 'other': 3}
    # target = [target_dict[x] for x in y_train]
    # X_test = val[features].values
    # y_test = val['target'].values

    # rf = RFC(n_estimators = 500, max_depth = 40, min_samples_leaf = 5, bootstrap = False, n_jobs = -1)
    # rf.fit(X_train, target)
    # #y_pred = rf.predict(X_test)
    # #score = rf.score(X_test, y_test)
    # #pprint(f'RF Accuracy: {score:0.4f}')

    # #report = classification_report(y_test, y_pred)
    # #pprint(report)

    # feat_imp_idx = np.argsort(rf.feature_importances_)[::-1]
    # # plot_feat_imp(feat_imp_idx, features, rf.feature_importances_, 7, 'images/rf2.jpeg')
    
    # # Attempt at partial dependence -- failed.....
    # target_dict = {'TD': 0, 'FG': 1, 'punt': 2, 'other': 3}
    # target = [target_dict[x] for x in y_train]
    # for i in range(4):
    #     plot_pd(rf, X_train, features = feat_imp_idx[:7], feature_names = np.array(features)[feat_imp_idx[:7], target = i)