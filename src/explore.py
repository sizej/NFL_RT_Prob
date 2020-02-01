import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

# plays = pd.read_csv('play_by_play/NFL Play by Play 2009-2018 (v5).csv', nrows=5000)

if __name__ == '__main__':
    hist = pd.read_csv('historical_results/spreadspoke_scores.csv')
    hist['point_diff'] = np.absolute(hist['score_home'] - hist['score_away'])
    
    # fig, ax = plt.subplots(1,1)
    # ax.hist(hist['point_diff'], bins = 30)
    # plt.savefig('allgames.jpeg')
    # plt.close()    
    
    # close_games = hist[hist['spread_favorite'].notna()].copy()
    # close_games['spread'] = np.absolute(hist['spread_favorite'])
    # m1 = close_games['spread'] <= 2
    # fig, ax = plt.subplots(1,1)
    # ax.hist(close_games['point_diff'][m1], bins = 30)
    # plt.savefig('closegames.jpeg')
    # plt.close()

    plays = pd.read_csv('play_by_play/plays_09_18.csv')
    
