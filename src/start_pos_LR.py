from sklearn.linear_model import LogisticRegression as LogReg
import pandas as pd 
import numpy as np 
from football_func import *
from statsmodels.discrete.discrete_model import MNLogit as MLogReg
from statsmodels.tools import add_constant

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


if __name__ == '__main__':
    start = pd.read_csv('data/start_pos_train.csv', nrows = 5000)
    m0 = start['yardline_100'].notna()
    start = start[m0].copy()
    start['target'] = start.apply(lambda row: make_target(row), axis = 1)
    start.drop(['Unnamed: 0', 'game_date', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other'], axis = 1, inplace = True)
    train, test = tt_split(start)
    train.drop(['game_id'], axis = 1, inplace = True)
    test.drop(['game_id'], axis = 1, inplace = True)
    y_train = train.pop('target').values
    X_train = train.values
    y_test = test.pop('target').values
    X_test = test.values
    mod = LogReg(solver = 'saga', max_iter = 2000, multi_class = 'multinomial', n_jobs = -1)
    mod.fit(X_train, y_train)
    mod_score = mod.score(X_test, y_test)
    # X_train = add_constant(X_train)
    # stats_mod = MLogReg(y_train, X_train).fit(method = 'nm', maxiter = 2000)
    # X_test = add_constant(X_test)
    # y_pred_p = stats_mod.predict(X_test)

    
    # acc = make_scorer(accuracy_score)
    # params = {'solver': ['lbfgs', 'sag', 'saga'],
    #             'max_iter': [100, 500, 1000, 5000],
    #             'multi_class': ['multinomial', 'ovr']}
    # grid = search(LogReg(), params, scoring = acc, n_jobs = -1)
    # grid.fit(X_train, y_train)
    
    # mod_lbfgs = LogReg(solver = 'lbfgs', max_iter = n, multi_class = 'multinomial')
    # mod_lbfgs.fit(X_train, y_train)
    # lbfgs_score = mod.score(X_test, y_test)
    # mod
    # LogReg best params = max_iter: 5000, multi-class: 'multinomial', 'solver': saga
    # Accuracy about 48.7%
