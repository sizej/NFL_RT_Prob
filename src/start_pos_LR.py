from sklearn.linear_model import LogisticRegression as LogReg
import pandas as pd 
import numpy as np 
from football_func import *

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
    start = pd.read_csv('data/start_pos_train.csv')
    m0 = start['yardline_100'].notna()
    start = start[m0].copy()
    start['target'] = start.apply(lambda row: make_target(row), axis = 1)
    start.drop(['Unnamed: 0', 'game_date', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other'], axis = 1, inplace = True)
    train, test = tt_split(start)
    y_train = train.pop('target').values
    X_train = train.values
    y_test = test.pop('target').values
    X_test = test.values 
    mod = LogReg()
    mod.fit(X_train, y_train)
    score = mod.score(X_test, y_test)
