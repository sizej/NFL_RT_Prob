import pandas as pd 
import numpy as np 

def pos_expected_points(row):
    '''
    Calculates expected total points for the offense, based on over-under line, spread, and team
    '''
    if row['posteam'] == row['favorite']:
        return row['spread'] + ((row['total'] - row['spread'])/ 2)
    else:
        return (row['total'] - row['spread'])/ 2

def def_expected_points(row):
    '''
    Calculates expected total points for the defense, based on over-under line, spread, and team
    '''
    if row['posteam'] == row['favorite']:
        return (row['total'] - row['spread'])/ 2
    else:
        return row['spread'] + ((row['total'] - row['spread'])/ 2)

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
    if row['play_TD'] + row['play_FG'] + row['play_punt'] == 0:
        return 1
    else:
        return 0

def start_possession(df):
    '''
    Takes in df of all plays, returns a df of just the plays that are the start of a new possesion.
    New possession does not include kick-off (un-timed down).
    '''
    c = df.columns
    first = pd.DataFrame(columns = c)
    for drive in df['drive_id'].unique():
        m0 = df['drive_id'] == drive
        m1 = df['down'] == 1
        drive = df[m0 & m1]
        m2 = drive['game_seconds_remaining'] == drive['game_seconds_remaining'].max()
        first = first.append(drive[c][m2]).copy()
    return first     


if __name__ == '__main__':
    pass