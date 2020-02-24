import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from cleaner_class import *
from sklearn.ensemble import RandomForestClassifier as RFC 
from sklearn.metrics import classification_report
from football_func import *
from pprint import pprint


if __name__ == '__main__':
    plays = AllPlays(cols_file = 'RF')
    rf = RFC(n_estimators = 500, min_samples_leaf = 5, bootstrap = False, n_jobs = -1)
    rf.fit(plays.X_train, plays.y_train)
    model_score = rf.score(plays.X_test, plays.y_test)
    print(f'RF accuracy: {model_score:0.4f}')