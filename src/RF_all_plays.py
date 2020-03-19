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
    plays = AllPlays(cols_file = 'RF')
    rf = RFC(n_estimators = 250, min_samples_leaf = 2, bootstrap = False, n_jobs = -1)
    rf.fit(plays.X_train, plays.y_train)
    model_score = rf.score(plays.X_test, plays.y_test)
    print(f'RF accuracy: {model_score:0.4f}')

    # Plot feature importances
    idx = np.argsort(rf.feature_importances_)[::-1]
    # plot_feat_imp(idx, plays.features, rf.feature_importances_, n = 10, fname = 'images/rf3_feat_imp.jpeg')

    holdout_score = rf.score(plays.X_holdout, plays.y_holdout)
    y_holdout_pred = rf.predict(plays.X_holdout)
    print(f'Holdout Accuracy: {holdout_score:0.4f}')
    rpt = classification_report(y_holdout_pred, plays.y_holdout)
    pprint(rpt)

    if holdout_score >= 0.54:
        fname = 'helpers/rf_model.pkl'
        pickle.dump(rf, open(fname, 'wb'))

    # Get a trial game for step-through analysis
    game = np.random.choice(plays.holdout['game_id'])
    m0 = plays.holdout['game_id'] == game
    X_trial = plays.holdout[plays.features][m0].values
    y_trial = plays.holdout['target_num'][m0].values
    y_pred = rf.predict(X_trial)
    y_pred_probs = rf.predict_proba(X_trial)
    trial_score = rf.score(X_trial, y_trial)
    print(f'Trial accuracy: {trial_score:0.4f}')

    print(game)
    
    cols = ['outcome', 'prediction', 'prob0', 'prob1', 'prob2', 'prob3']
    f = plays.features + cols
    game_arr = np.concatenate((X_trial, y_trial.reshape(-1, 1), y_pred.reshape(-1, 1), y_pred_probs), axis = 1)
    game_df = pd.DataFrame(game_arr, columns = f)
    game_df['game_id'] = [game for x in game_df['outcome']]
    game_df.to_csv('data/Archive/sample_preds.csv')
