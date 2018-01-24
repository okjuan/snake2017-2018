import os
import json
import sys
from datetime import time

from flask import Flask
from flask import request

from food_fetcher import pick_move_to_food, find_snakes_that_just_ate
from objects import Board
from shared import create_snake_dict

OUR_SNAKE_NAME = '1'
PREV_DATA_BY_GAME_ID = dict()
DEBUG = True

taunts = ["10% LUCK, 20% SSSSLITHER", "I look like.. MOM'S SPAGHETTI"]

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"


def pick_move(start_time, data, board, snake_dict, mode=None):
    move = pick_move_to_food(start_time, data, board, snake_dict)
    return move


# page to dump data
@app.route('/hello')
def hello():
    return "Hello World!"


def print_data(data):
    print("DATA\n********************")
    for key in data:
        print(key, ":", data[key])


@app.route('/start', methods=['POST'])
def start():
    data = request.get_json(force=True)
    PREV_DATA_BY_GAME_ID[data['game_id']] = dict(prev_food_list=None)
    response = dict(
        color='#369',
        name='7geese guy',
        taunt='My. Treat.'
    )
    return json.dumps(response)


@app.route('/move', methods=['POST'])
def move():
    print("\nPINGED\n********************")
    start_time = time()
    data = request.get_json(force=True)  # dict
    # print(data)

    snake_dict = create_snake_dict(data['snakes'])
    board = Board(data['height'], data['width'], snake_dict, data['food'])
    #prev_food_list = PREV_DATA_BY_GAME_ID[data['game_id']]['prev_food_list']

    # insert info about which snakes ate last turn into data object
    # data['ate_last_turn'] = find_snakes_that_just_ate(data, prev_food_list, board)
    # save food info for this move since we will use it next turn to determine who ate
    # TODO: determine if we can just make a shallow copy
    # PREV_DATA_BY_GAME_ID.get(data['game_id']).get('prev_food_list') = data['food'][:]

    # TODO pick a default
    if len(sys.argv) == 1:
        mode = 'food-fetcher'
    else:
        mode = sys.argv[1]

    move = pick_move(start_time, data, board, snake_dict, mode)
    response = {
        'move': move,
        'taunt': 'Squaack'
    }
    end_time = time()
    # print("Took", end_time - start_time, "seconds to compute move.")
    return json.dumps(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
