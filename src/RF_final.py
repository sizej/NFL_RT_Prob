import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from cleaner_data import *
from sklearn.ensemble import RandomForestClassifier as RFC 
from sklearn.metrics import classification_report
from football_func import *
from pprint import pprint
import pickle 

plt.style.use('fivethirtyeight')

if __name__ == '__main__':
    with open('data/all_pickle.pkl', 'rb') as f:
        plays = pickle.load(f)
    with open('data/rf_model.pkl', 'rb') as f:
        rf = pickle.load(f)

    pred = Predictions(plays, rf)
    fname = 'data/predictions.pkl'
    pickle.dump(pred, open(fname, 'wb'))