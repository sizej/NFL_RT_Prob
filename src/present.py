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

def add_end_poss(df):
    out = pd.DataFrame()
    for game in df['game_id'].unique():
        m0 = df['game_id'] == game 
        temp = df[m0].copy()
        drive_nums = temp['drive'].values
        ends = []
        for i, d in enumerate(drive_nums[:-1]):
            if d == drive_nums[i+1]:
                ends.append(0)
            else:
                ends.append(1)
        ends.append(0)
        temp['end_of_poss'] = ends
        out = out.append(temp).copy()
    return out
        

if __name__ == '__main__':
    with open('data/predictions.pkl', 'rb') as f:
        pred = pickle.load(f)   
    for i in range(10):
        pred.pick_random()
        pred.export_game()

    games = add_end_poss(pred.df)
    m0 = games['end_of_poss'] == 1
    ends = games[m0]
    rpt = classification_report(ends['target_num'], ends['prediction'])
