import pandas as pd 
import numpy as np 

def touchdown_det(touchdown, td_team, pos_team):
    '''
    Takes in row data and returns if play ended in touchdown for possessing team
    '''
    if touchdown == 1 and td_team == pos_team:
        return 1
    else:
        return 0

def fg_det(fg_result):
    '''
    Takes in row data and returns if play ended in made fg for possessing team
    '''
    if fg_result == 'made':
        return 1
    else:
        return 0

def punt_det(play):
    '''
    Takes in play_type and returns if punt was attempted or not
    '''
    if play == 'punt':
        return 1
    else:
        return 0

def other_det(row):
    '''
    If it isn't a TD, FG, or Punt, it's other...
    '''
    if row['pos_TD'] + row['pos_FG'] + row['pos_punt'] == 0:
        return 1
    else:
        return 0


def first_possession(df):
    '''
    Takes in df of all plays, returns a df of just the plays that are the start of a new possesion.
    New possession does not include kick-off (un-timed down).
    '''
    c = ['home_team', 'away_team', 'posteam', 'game_seconds_remaining', 'down', 'yardline_100']
    first = pd.DataFrame(columns = c)
    for drive in plays['drive_id'].unique():
        m0 = plays['drive_id'] == drive
        m1 = plays['down'] == 1
        drive = plays[m0 & m1]
        m2 = drive['game_seconds_remaining'] == drive['game_seconds_remaining'].max()
        first =first.append(drive[c][m2]).copy()
    return first     


if __name__ == '__main__':
    pass