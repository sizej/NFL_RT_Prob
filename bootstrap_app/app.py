from flask import Flask, request, render_template
from cleaner_data2 import Game
import matplotlib.pyplot as plt
import os
import numpy as np
from app_func import *
from app_func import pred_dict


app = Flask(__name__)




@app.route('/', methods = ['GET','POST'])
def home_page():
    global game
    # modeled_games = [2018090600, 2018093012, 2018101405, 2018102102,
    #                 2018111107, 2018120205, 2018120208, 2018120903, 2018121600]
    # g = np.random.choice(modeled_games)
    g = 2018120913
    game = Game(g)
    if not str(g) in os.listdir('bootstrap_app/static'):
        os.mkdir(f'bootstrap_app/static/{g}')
    game.play_num = 0
    return f'''{render_template('index.html')}
    <body>
    <center>
    <h1> THE ELIMINATOR!!! </h1>
    <img src="https://media.giphy.com/media/TgQCVpkQSZ81G/giphy.gif" style="width:1200px;height:600px;" style="padding-bottom:1em">
    <p>  </p>
    <p>  </p>
    <p> <i>***Dominic Toretto does NOT ENDORSE the Eliminator! You should play anyway. </i></p>
    </body>
    <form action="/next_play" method='POST' >
        <input type="submit" value="Let's Play!" class="button-style"/>
    </form>
    </center>
    '''

@app.route('/next_play', methods = ['GET','POST'])
def get_random():
    global game
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
                 <head>
                <body>
                    <div class='pred-play__container'>
                        <div class='previous-container'>
                            <table class="table table-hover table-bordered">
                                <thead>
                                    <tr>
                                        <th>Previous Play</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>{pl_deet['desc']}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="game-columns">
                        <div class="game-container">
                            <h2> Game: </h2>
                            <table class="table table-dark table-bordered table-hover vertical-table">
                                <tr>
                                    <th>Away Team</th>
                                    <td>{g_deet['away_team']}</td>
                                </tr>
                                <tr>
                                    <th>Home Team</th>
                                    <td>{g_deet['home_team']}</td>
                                </tr>
                                <tr>
                                    <th>Possession</th>
                                    <td>{g_deet['posteam']}</td>
                                </tr>
                                <tr>
                                    <th>Favorite</th>
                                    <td>{favorite}</td>
                                </tr>
                                <tr>
                                    <th>Spread</th>
                                    <td>{g_deet['spread']}</td>
                                </tr>
                                <tr>
                                    <th>Total</th>
                                    <td>{g_deet['total']}</td>
                                </tr>
                                <tr>
                                    <th>Away Score</th>
                                    <td>{away_score}</td>
                                </tr>
                                <tr>
                                    <th>Home Score</th>
                                    <td>{home_score}</td>
                                </tr>
                            </table>
                        </div>
                        <div class="possession-container">
                            <h2> Possession: </h2>
                            <table class="table table-dark table-hover table-bordered vertical-table">
                                <tr>
                                    <th>Down</th>
                                    <td>{int(s_deet['down'])}</td>
                                </tr>
                                <tr>
                                    <th>Distance</th>
                                    <td>{s_deet['ydstogo']}</td>
                                </tr>
                                <tr>
                                    <th>Yardline</th>
                                    <td>{yardline}</td>
                                </tr>
                                <tr>
                                    <th>Goal to Go</th>
                                    <td>{int(s_deet['goal_to_go'])}</td>
                                </tr>
                                <tr>
                                    <th>Game Clock</th>
                                    <td>{game_clock}</td>
                                </tr>
                                <tr>
                                    <th>Pos TO Rem.</th>
                                    <td>{int(s_deet['posteam_timeouts_remaining'])}</td>
                                </tr>
                                <tr>
                                    <th>Def TO Rem.</th>
                                    <td>{int(s_deet['defteam_timeouts_remaining'])}</td>
                                </tr>
                            </table>
                        </div>
                        <div class="graph-container">
                            <img src="{fname}">
                        </div>
                    </div>

                    <div class='btn-container'>
                        <form action="/next_play" method='POST'>
                            <input type="submit" value="Next Play" class="button-style margin-right"/>
                        </form>
                        <form action="/" method='POST' >
                            <input type="submit" value="Start Over" class="button-style"/>
                        </form>
                    </div>
                </body>
                </center>
                '''
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)