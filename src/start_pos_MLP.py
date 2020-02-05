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
import boto3 
import pandas as pd 

boto3_conn = boto3.resource('s3')
s3_client = boto3.client('s3')
b1 = 'capstone2data'
c1 = 'start_pos_train.csv'
c2 = 'train.csv'
f = s3_client.download_file(b1, c1, c2)
c1 = 'start_pos_holdout.csv'
c2 = 'holdout.csv'
f = s3_client.download_file(b1, c1, c2)


if __name__ == '__main__':
    start = pd.read_csv('train.csv')
    start = remove_na_yardline(start)
    val = pd.read_csv('holdout.csv')
    val = remove_na_yardline(val)
    target_dict = {'TD': 0, 'FG': 1, 'punt': 2, 'other': 3}
    start['target'] = start.apply(lambda row: make_target(row), axis = 1)
    start['target_num'] = start['target'].map(target_dict)
    start['is_EOH'] = start.apply(lambda row: end_of_half_det(row), axis = 1)
    start['pos_leads'] = (start['posteam_score'] > start['defteam_score']).astype(int)
    val['target'] = val.apply(lambda row: make_target(row), axis = 1)
    val['target_num'] = val['target'].map(target_dict)
    val['is_EOH'] = val.apply(lambda row: end_of_half_det(row), axis = 1)
    val['pos_leads'] = (val['posteam_score'] > val['defteam_score']).astype(int)