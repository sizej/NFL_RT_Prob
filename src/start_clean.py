import pandas as pd
import numpy as np 
import datetime as dt 
from team_dict import team_dict
from football_func import *
import boto3

if __name__ == '__main__':
    p = pd.read_csv('all_plays.csv')
    print(p.columns)