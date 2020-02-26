from flask import Flask, request
from cleaner_data import Predictions
import pickle
import matplotlib.pyplot as plt 

app = Flask(__name__)

with open('data/predictions.pkl', 'rb') as f:
    pred = pickle.load(f)

@app.route('/')
def home_page():
    return '''
    <form action="/random_game" method='POST' >
        <input type="submit" />
    </form>
    '''

@app.route('/random_game', methods = ['POST'])
def get_random():
    pred.pick_random()
    x = pred.next_play()
    show = str(x) + '''<form action="/next_play" method='POST' >
        <input type="submit" />
    </form>
    '''
    return show
 

@app.route('/next_play', methods = ['POST'])
def predict():
    x = pred.next_play()
    text = ''' <body>
            <img src="~/DSI/repos/NFL_RT_Data/images/last_play.jpeg">
            </body>
            <form action="/next_play" method='POST' >
            <input type="submit" />
            </form>
            '''
    show = str(x) + text
    return show


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
