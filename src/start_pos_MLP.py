import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.metrics import Precision, Recall, Accuracy
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt 
import pandas as pd 
from football_func import *
from sklearn.preprocessing import StandardScaler as scale 


if __name__ == '__main__':
    start = pd.read_csv('data/start_pos_train.csv')
    start = remove_na_yardline(start)
    val = pd.read_csv('data/start_pos_holdout.csv')
    val = remove_na_yardline(val)
    target_dict = {'TD': 0, 'FG': 1, 'punt': 2, 'other': 3}
    start['target'] = start.apply(lambda row: make_target(row), axis = 1)
    start['target_num'] = start['target'].map(target_dict)
    start['is_EOH'] = start.apply(lambda row: end_of_half_det(row), axis = 1)
    # start['pos_leads'] = (start['posteam_score'] > start['defteam_score']).astype(int)
    # start['game_date'] = pd.to_datetime(start['game_date'])
    # start['month'] = [x.month for x in start['game_date']]
    # start = pd.concat([start, pd.get_dummies(start['month'], prefix = 'month_is')], axis = 1).copy()
    val['target'] = val.apply(lambda row: make_target(row), axis = 1)
    val['target_num'] = val['target'].map(target_dict)
    val['is_EOH'] = val.apply(lambda row: end_of_half_det(row), axis = 1)
    # val['pos_leads'] = (val['posteam_score'] > val['defteam_score']).astype(int)
    # val['game_date'] = pd.to_datetime(val['game_date'])
    # val['month'] = [x.month for x in val['game_date']]
    # val = pd.concat([val, pd.get_dummies(val['month'], prefix = 'month_is')], axis = 1).copy()
    # val['month_is_1'] = np.zeros(val.shape[0])
    to_drop = ['Unnamed: 0', 'game_date', 'game_id', 'ends_TD', 'ends_FG', 'ends_punt', 'ends_other', 'target', 'target_num', 'month']
    targets = ['ends_TD', 'ends_FG', 'ends_punt', 'ends_other']
    features = [c for c in start.columns if c not in to_drop]
    scaled_train = start[features].copy()
    for c in scaled_train.columns:
        scaled_train[c] = scaled_train[c]/scaled_train[c].max()

    y_train = start[targets].values
    X_train = scaled_train.values

    scaled_val = val[features].copy()
    for c in scaled_val.columns: 
        if scaled_val[c].max() > 0:
            scaled_val[c] = scaled_val[c] / scaled_val[c].max()
        else:
            scaled_val[c] = np.zeros(scaled_val.shape[0])
    
    X_val = scaled_val[features].values
    y_val = val[targets].values

    n_samples, n_feats = X_train.shape
    layer1_units = 200
    layer2_units = 100
    layer3_units = 50
    n_classes = 4
    batch = 20
    ep = 10

    model = Sequential()
    layer1 = Dense(units=layer1_units,
                    input_dim=n_feats,
                    kernel_initializer='uniform',
                    activation='relu')

    layer2 = Dense(units=layer2_units,
                    input_dim=layer1_units,
                    kernel_initializer='uniform',
                    activation='selu')
    
    layer3 = Dense(units=layer3_units,
                    input_dim=layer2_units,
                    kernel_initializer='uniform',
                    activation='selu')

    output_layer = Dense(units = n_classes, 
                    input_dim = layer3_units,
                    kernel_initializer = 'uniform',
                    activation = 'softmax')
      
    model.add(layer1)
    model.add(layer2)
    model.add(layer3)
    model.add(output_layer)

    model.compile(loss='categorical_crossentropy', 
                optimizer="adamax", metrics=["accuracy"])
    model.fit(X_train, y_train, epochs=ep, batch_size=batch, verbose=1,
              validation_split=0.1)
    # print('Evaluating on test.......')
    # model.evaluate(X_test, y_test)
    print('Evaluating on validation......')
    model.evaluate(X_val, y_val)
    model.save('data/mlp_model_test.h5')
