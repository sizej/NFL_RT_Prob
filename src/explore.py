import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

def get_pos_starts(c = None):
    df = pd.read_csv('data/start_pos_test.csv', usecols = c)
    return df

def get_cols():
    fname = 'helpers/start_pos_cols.txt'
    cols = []
    with open(fname, 'r') as f:
        for row in f:
            idx = row.find('\n')
            cols.append(row[:idx])
    return cols

if __name__ == '__main__':
    cols = get_cols()
    start_df = get_pos_starts(c = cols)


