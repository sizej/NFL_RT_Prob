from flask import Flask, request
from cleaner_data2 import Game
import matplotlib.pyplot as plt 
import os
import numpy as np 

app = Flask(__name__)

g = 2018121600
game = Game(g)
if not str(g) in os.listdir('web_app/static'):
    os.mkdir(f'web_app/static/{g}')

def time_remaining(gsr):
    if gsr > 2700:
        mnt = int((gsr - 2700)//60)
        sec = int((gsr - 2700) - (mnt * 60))
        if sec < 10:
            sec = f'0{sec}'
        return f'Q1 - {mnt}:{sec}'
    elif gsr > 1800:
        mnt = int((gsr - 1800)//60)
        sec = int((gsr - 1800) - (mnt * 60))
        if sec < 10:
            sec = f'0{sec}'
        return f'Q2 - {mnt}:{sec}'
    elif gsr > 900:
        mnt = int((gsr - 900)//60)
        sec = int((gsr - 900) - (mnt * 60))
        if sec < 10:
            sec = f'0{sec}'
        return f'Q3 - {mnt}:{sec}'
    else:
        mnt = int((gsr - 0)//60)
        sec = int(gsr - (mnt * 60))
        if sec < 10:
            sec = f'0{sec}'
        return f'Q4 - {mnt}:{sec}'

pred_dict = {0: 'TD', 1: 'FG', 2: 'punt', 3: 'other'}

@app.route('/')
def home_page():
    game.play_num = 0
    return '''
    <form action="/next_play" method='POST' >
        <input type="submit" />
    </form>
    '''

@app.route('/next_play', methods = ['POST'])
def get_random():
    game.get_next_play()
    g_deet = game.game_deets
    s_deet = game.sitch_deets
    pl_deet = game.play_deets
    pos_deet = game.poss_deets
    fname = game.fname
    game_clock = time_remaining(s_deet['game_seconds_remaining'])
    if g_deet['posteam'] == g_deet['away_team']:
        home_score = int(g_deet['posteam_score'])
        away_score = int(g_deet['defteam_score'])
    else:
        home_score = int(g_deet['defteam_score'])
        away_score = int(g_deet['posteam_score'])
    if g_deet['pos_fave'] == 1:
        favorite = g_deet['posteam']
    elif g_deet['posteam'] == g_deet['away_team']:
        favorite = g_deet['home_team']
    else:
        favorite = g_deet['away_team']
    if pos_deet['end_of_poss'] == 1:
        actual_outcome = pos_deet['target_cat']
    else:
        actual_outcome = "?"
    
    if s_deet['yardline_100'] >= 50:
        yardline = g_deet['posteam'] + ' ' + str(100 - s_deet['yardline_100'])
    else:
        if g_deet['posteam'] == g_deet['home_team']:
            yardline = g_deet['away_team'] + ' ' + str(s_deet['yardline_100'])
        else:
            yardline = g_deet['home_team'] + ' ' + str(s_deet['yardline_100'])
    html = f''' <body>
                <h2> Game: </h2>
                <table style="width:60%">
                    <tr>
                        <th>Away Team<th>
                        <th>Home Team<th>
                        <th>Possession<th>
                        <th>Favorite<th>
                        <th>Spread<th>
                        <th>Total<th>
                        <th>Away Score<th>
                        <th>Home Score<th>
                    </tr>
                    <tr>
                        <th>{g_deet['away_team']}<th>
                        <th>{g_deet['home_team']}<th>
                        <th>{g_deet['posteam']}<th>
                        <th>{favorite}<th>
                        <th>{g_deet['spread']}<th>
                        <th>{g_deet['total']}<th>
                        <th>{home_score}<th>
                        <th>{away_score}<th>
                    </tr>
                </table>
                <h2> Possession: </h2>
                <table style="width:60%">
                    <tr>
                        <th>Down<th>
                        <th>Distance<th>
                        <th>Yardline<th>
                        <th>Goal to Go<th>
                        <th>Game Clock<th>
                        <th>Pos TO Rem.<th>
                        <th>Def TO Rem.<th>
                    </tr>
                    <tr>
                        <th>{int(s_deet['down'])}<th>
                        <th>{s_deet['ydstogo']}<th>
                        <th>{yardline}<th>
                        <th>{int(s_deet['goal_to_go'])}<th>
                        <th>{game_clock}<th>
                        <th>{int(s_deet['posteam_timeouts_remaining'])}<th>
                        <th>{int(s_deet['defteam_timeouts_remaining'])}<th>
                    </tr>
                </table>
                <img src="{fname}">
                <h2> Prediction: </h2>
                <table style="width:30%">
                    <tr>
                        <th>Model Prediction<th>
                        <th>Actual Outcome<th>
                    </tr>
                    <tr>
                        <th>{pred_dict[pos_deet['prediction']]}<th>
                        <th>{actual_outcome}<th>
                    </tr>
                </table>
                <h2> Previous Play: </h2>
                <table style="width:50%">
                    <tr>
                        <th>Desc<th>
                    </tr>
                    <tr>
                        <th>{pl_deet['desc']}<th>
                    </tr>
                </table>
                </body>
                <form action="/next_play" method='POST' >
                    <input type="submit" />
                </form>
                '''
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    