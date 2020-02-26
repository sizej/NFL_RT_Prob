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
    with open('data/predictions.pkl', 'rb') as f:
        pred = pickle.load(f)
    for i in range(10):
        pred.pick_random()
        pred.export_game()
