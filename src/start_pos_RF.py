from sklearn.ensemble import AdaBoostClassifier as ABC
from sklearn.ensemble import RandomForestClassifier as RFC 
from sklearn.tree import DecisionTreeClassifier as DTC 
import pandas as pd 
import numpy as np 
from sklearn.metrics import accuracy_score, make_scorer
from football_func import * 
import matplotlib.pyplot as plt 

def plot_feat_imp(idx, features, feat_importances,  n = 5):
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
    plt.savefig('images/rf_feat_imp.jpeg')

def guesser(probs, max_thresh = 0.6, diff_thresh = 0.03):
    '''
    Returns a guess that is (sometimes) different from max.
    '''
    guesses = []
    for p in probs:
        idx = np.argsort(p)[::-1]
        diffs = np.max(p) - p
        if max(p) >= max_thresh:
            guesses.append(idx[0])
        else:
            options = p[np.where(diffs <= diff_thresh)]
            guess = np.random.choice(options)
            guesses.append(np.where(p == guess)[0][0])
    return guesses

if __name__ == '__main__':
    start = pd.read_csv('data/start_pos_train.csv')
    start = remove_na_yardline(start)
    val = pd.read_csv('data/start_pos_holdout.csv')
    val = remove_na_yardline(val)
    target_dict = {'TD': 0, 'FG': 1, 'punt': 2, 'other': 3}
    start['target'] = start.apply(lambda row: make_target(row), axis = 1)
    start['target_num'] = start['target'].map(target_dict)
    start['is_EOH'] = start.apply(lambda row: end_of_half_det(row), axis = 1)
    start['pos_leads'] = (start['posteam_score'] > start['defteam_score']).astype(int)
    val['target'] = val.apply(lambda row: make_target(row), axis = 1)
    val['target_num'] = val['target'].map(target_dict)
    val['is_EOH'] = val.apply(lambda row: end_of_half_det(row), axis = 1)
    val['pos_leads'] = (val['posteam_score'] > val['defteam_score']).astype(int)
    to_drop = ['Unnamed: 0', 'game_date', 'game_id', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other', 'target', 'target_num']
    targets = ['ends_TD', 'ends_FG', 'ends_punt', 'ends_other']
    features = [c for c in start.columns if c not in to_drop]
    train, test = tt_split(start)
    y_train = train['target_num'].values
    X_train = train[features].values
    abc = ABC(base_estimator = DTC(max_depth = 2), n_estimators = 500, learning_rate = 0.25)
    abc.fit(X_train, y_train)
    y_test = test['target_num'].values
    X_test = test[features].values
    score = abc.score(X_test, y_test)
    print(f'Test: {score:0.3f}')
    X_val = val[features].values
    y_val = val['target_num']
    val_score = abc.score(X_val, y_val)
    print(f'AB Validation: {val_score:0.3f}')
    
    
    rf = RFC(n_estimators = 500, max_depth = 40, bootstrap = False, max_features = 5, min_samples_leaf = 10, n_jobs = -1)
    X_train = train[features].values
    y_train = train['target'].values
    rf.fit(X_train, y_train)
    y_test = test['target'].values
    X_test = test[features].values
    test_score = rf.score(X_test, y_test)
    d = {f: i for f, i in zip(features, rf.feature_importances_)} 
    print(f'Test: {test_score:0.3f}')
    y_val = val['target'].values
    val_score = rf.score(X_val, y_val)
    print(f'RF Validation: {val_score:0.3f}')

    feat_imp_idx = np.argsort(rf.feature_importances_)[::-1]
    plot_feat_imp(feat_imp_idx, features, rf.feature_importances_, 7)
    