from flask import Flask, request, render_template
from cleaner_data2 import Game
import matplotlib.pyplot as plt 
import os
import numpy as np 
from app_func import *
from app_func import pred_dict


app = Flask(__name__)

g = 2018121600
game = Game(g)
if not str(g) in os.listdir('bootstrap_app/static'):
    os.mkdir(f'bootstrap_app/static/{g}')


@app.route('/', methods = ['GET','POST'])
def home_page():
    game.play_num = 0
    return f'''{render_template('index.html')}
    <body>
    <center>
    <h1> THE ELIMINATOR!!! </h1>
    <img src="https://img1.looper.com/img/gallery/these-things-happen-in-every-single-terminator-movie/intro-1564072959.jpg" >
    <p> <i>***Arnold does NOT ENDORSE the Eliminator! You should play anyway. </i></p>
    </body>
    <form action="/next_play" method='POST' >
        <input type="submit" value="Let's Play!" style="height:50px;width:200px"/>
    </form>
    </center>
    '''

@app.route('/next_play', methods = ['GET','POST'])
def get_random():
    game.get_next_play()
    g_deet = game.game_deets
    s_deet = game.sitch_deets
    pl_deet = game.play_deets
    pos_deet = game.poss_deets
    fname = game.fname
    game_clock = time_remaining(s_deet['game_seconds_remaining'])
    actual_outcome = outcome_det(pos_deet)
    favorite = fave_det(g_deet)
    home_score, away_score = score_det(g_deet)
    yardline = yard_det(g_deet, s_deet)

    html = f''' 
                {render_template('index.html')}
                <center>
                <form action="/next_play" method='POST' >
                    <input type="submit" value="Next Play", style="height:50px;width:200px"/>
                </form>
                 <head>
                <body>
                <div class="row">
                    <div class="column">
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
                    </div>
                    <div class="column">
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
                    </div>
                </div>
                </body>
                <form action="/" method='POST' >
                    <input type="submit" value="Start Over" style="height:50px;width:200px"/>
                </form>
                </center>
                '''
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    