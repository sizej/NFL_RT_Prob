import pandas as pd
import numpy as np 
import datetime as dt 
from team_dict import team_dict
from football_func import *
import boto3

b1 = 'capstone2data'
c = 'all_plays2.csv'
c1 = 'all_plays.csv'

boto3_conn = boto3.resource('s3')
s3_client = boto3.client('s3')
f = s3_client.download_file(b1, c, c1)

if __name__ == '__main__':
    p = pd.read_csv('all_plays.csv')
    start = start_possession(p)
    start.to_csv('start_pos2.csv')
    s3_client.upload_file('start_pos2.csv', b1, 'start_pos2_s3.csv')