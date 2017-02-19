#
#
# N. Kobald - 2017-02-04
#

import os, json
from flask import Flask, request
from deprecated import *
from shared import *
from duel import *
from gameObjects import *
OUR_SNAKE_NAME = '1'

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"


#Logic about which algorithm gets run,
#and some basic parsing
def pick_move(data):
    print "Init board."
    board = Board(data['height'], data['width'], data['snakes'], data['food'])
    print "Cal minmax."
    move = minmax(board, data['snakes'], data['you'], data['food'], 0)
    print "Minmax returned", move
    return move


#page to dump data
@app.route('/hello')
def hello():
    return "Hello World!"

def print_data(data):
    for key in data:
        print key, ":", data[key]

@app.route('/start', methods=['POST'])
def start():
    print "Got started pinged."
    data = request.get_json(force=True) #dict
    #print_data(data)
    response = dict(
        color='#369',
        name='Bennet',
        taunt='My. Treat.'
    )
    return json.dumps(response)

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json(force=True) #dict
    print "Got pinged."
    print_data(data)
    direction = pick_move(data)
    response = {
        'move':direction,
        'taunt':'Lets raise the ROOOF'
    }
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
