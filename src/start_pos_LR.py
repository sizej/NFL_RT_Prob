from sklearn.linear_model import LogisticRegression as LogReg
import pandas as pd 
import numpy as np 
from football_func import *
from statsmodels.discrete.discrete_model import MNLogit
from statsmodels.tools import add_constant
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler as scale 

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

def end_of_half_det(row):
    '''
    Binary flag for possessions starting w/in the last two minutes of half.
    '''
    if (1800 <= row['game_seconds_remaining'] <= 1920) or row['game_seconds_remaining'] <= 120:
        return 1
    else:
        return 0

def scree_plot(ax, pca, n_components_to_plot=8, title=None):
    """Make a scree plot showing the variance explained (i.e. variance
    of the projections) for the principal components in a fit sklearn
    PCA object.
    
    Parameters
    ----------
    ax: matplotlib.axis object
      The axis to make the scree plot on.
      
    pca: sklearn.decomposition.PCA object.
      A fit PCA object.
      
    n_components_to_plot: int
      The number of principal components to display in the scree plot.
      
    title: str
      A title for the scree plot.
    """
    num_components = pca.n_components_
    ind = np.arange(num_components)
    vals = pca.explained_variance_ratio_
    ax.plot(ind, vals, color='blue')
    ax.scatter(ind, vals, color='blue', s=50)

    for i in range(num_components):
        ax.annotate(r"{:2.2f}%".format(vals[i]), 
            (ind[i]+0.2, vals[i]+0.005), 
            va="bottom", 
            ha="center", 
            fontsize=12)

    ax.set_xticklabels(ind, fontsize=12)
    ax.set_ylim(0, max(vals) + 0.05)
    ax.set_xlim(0 - 0.45, n_components_to_plot + 0.45)
    ax.set_xlabel("Principal Component", fontsize=12)
    ax.set_ylabel("Variance Explained (%)", fontsize=12)
    if title is not None:
	    ax.set_title(title, fontsize=16)


if __name__ == '__main__':
    start = pd.read_csv('data/start_pos_train.csv')
    m0 = start['yardline_100'].notna()
    start = start[m0].copy()
    start['target'] = start.apply(lambda row: make_target(row), axis = 1)
    start['is_EOH'] = start.apply(lambda row: end_of_half_det(row), axis = 1)
    start['pos_leads'] = (start['posteam_score'] > start['defteam_score']).astype(int)
    to_drop = ['Unnamed: 0', 'game_date', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other']
    sk = start.copy()
    sk.drop(to_drop, axis = 1, inplace = True)
    sk_train, sk_test = tt_split(sk)
    y_train = sk_train.pop('target').values
    X_train = sk_train.values
    y_test = sk_test.pop('target').values
    X_test = sk_test.values
    mod = LogReg(solver = 'saga', max_iter = 5000, multi_class = 'multinomial', n_jobs = -1)
    mod.fit(X_train, y_train)
    mod_score = np.around(mod.score(X_test, y_test), 3)

    holdout = pd.read_csv('data/start_pos_holdout.csv')
    m0 = holdout['yardline_100'].notna()
    holdout = holdout[m0].copy()
    holdout['target'] = holdout.apply(lambda row: make_target(row), axis = 1)
    holdout['is_EOH'] = holdout.apply(lambda row: end_of_half_det(row), axis = 1)
    holdout['pos_leads'] = (holdout['posteam_score'] > holdout['defteam_score']).astype(int)
    to_drop.append('game_id')
    holdout.drop(to_drop, axis = 1, inplace = True)
    holdout_y = holdout.pop('target').values
    holdout_X = holdout.values
    val_score = np.around(mod.score(holdout_X, holdout_y), 3)
    print(mod_score, val_score)









    # ### PCA doesn't help......
    # cat = ['pos_fave', 'pos_home', 'is_EOH']
    # pca_df = start.copy()
    # pca_df.drop(['Unnamed: 0', 'game_date', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other'], axis = 1, inplace = True)
    # train, test = tt_split(pca_df)
    # y_train = train.pop('target').values
    # num = [c for c in train.columns if c not in cat]
    # X_train_cat = train[cat].values
    # X_train_num = train[num].values
    # ss = scale()
    # X_train_scaled = ss.fit_transform(X_train_num)
    # pca = PCA(n_components = 8)
    # X_pc = pca.fit_transform(X_train_scaled)
    # X_train = np.concatenate((X_pc[:,:2], X_train_cat), axis = 1)
    # mod2 = LogReg(solver = 'saga', max_iter = 5000, multi_class = 'multinomial')
    # mod2.fit(X_train, y_train)
    # y_test = test.pop('target').values
    # X_test_cat = test[cat].values
    # X_test_num = ss.transform(test[num].values)
    # X_test_pc = pca.transform(X_test_num)
    # X_test = np.concatenate((X_test_pc[:,:2], X_test_cat), axis = 1)
    # mod2_score = np.around(mod2.score(X_test, y_test),3)
    

    
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
