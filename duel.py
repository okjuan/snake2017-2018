#
#
#

import itertools
import random

from copy import deepcopy

from shared import *
from gameObjects import *

def print_snake_data(snake):
    print " --- snake data --"
    for el in snake:
        print el, "::", snake[el]
    print " -- end snake data -- "

def minmax(board, snake_list, us, food_list):
    future_games = enumerate_boards(board, snake_list, food_list)
    board.print_board()
    for f in future_games:
        b = f['board']
        b.print_board()
    moves = get_moves_from_id(us, snake_list, board)
    print "Valid moves:", moves

    return random.choice(moves) #crashes if empty, which is appropriate.
def enumerate_boards(board, snake_list, food_list):
    move_set = []
    for snake in snake_list:
        snake_moves = []
        cur_snake_obj = get_snake(snake['id'], snake_list)
        head = get_head_coords(cur_snake_obj)
        for valid_move in board.get_valid_moves(head[0], head[1]):
            snake_moves.append({snake['id'] : valid_move})
        move_set.append(snake_moves)

    info_list = []
    all_move_comb = itertools.product(*move_set)
    new_snake_list = snake_list[:]
    for comb in all_move_comb:
        #NOTE hardcopy of snakelist and food. we change things from here on out
        info_list.append(get_board_from_moves(board, comb, deepcopy(snake_list), deepcopy(food_list)))

    return info_list

#movelist should be a list of keyvalue pairs,
# { id: move} where move is a valid move.
def get_board_from_moves(board, move_list, snake_list, food_list):
    for move in move_list:
        enact_move(board, move, snake_list, food_list)

    compute_collisions(snake_list)

    new_board = Board(board.height, board.width, snake_list, food_list)
    game_info = dict(
        board=new_board,
        snake_list=snake_list,
        food_list=food_list
    )
    return game_info

#NOTE
# -- Look into rules about food getting spawned?
# -- answer may lie in server source code?
# -- predict future food???
def enact_move(board, move_info, snake_list, food_list):
    assert len(move_info) == 1
    snake_id, move = move_info.items()[0]
    snake = get_snake(snake_id, snake_list)
    head = get_head_coords(snake)
    x, y = get_tile_from_move(head, move)
    tile = board.get_tile(x, y)
    if tile and tile.is_food():
        snake['health_points'] = 100
        food_list.remove([x, y])
    else:
        snake['health_points'] = snake['health_points'] - 1
        snake['coords'].pop() #didn't eat, so the entire body moves forward

    snake['coords'].insert(0, [x, y])

def compute_collisions(snake_list):
    dead_snakes = []

    for snake in snake_list:
        cur_snake_head = get_head_coords(snake)
        for other_snake in snake_list:
            #only worry about collisions if its not the same snake
            if not other_snake['id'] == snake['id']:
                other_snake_head = get_head_coords(other_snake)

                #head on head collision
                if cur_snake_head == other_snake_head:
                    col_winner(snake, other_snake, dead_snakes)

                #look over the other snakes body.
                for coord in other_snake['coords'][1:]:
                    #snake head ran into another snake body
                    if coord == cur_snake_head:
                        dead_snakes.append(snake['id'])

def col_winner(snek_one, snek_two, dead_snakes):
    snake_one_length = len(snek_one['coords'])
    snake_two_length = len(snek_two['coords'])

    if snake_one_length > snake_two_length:
        dead_snakes.append(snek_two['id'])
        return
    if snake_two_length > snake_one_length:
        dead_snakes.append(snek_one['id'])
        return

    if snake_one_length == snake_two_length:
        dead_snakes.append(snek_two['id'])
        dead_snakes.append(snek_one['id'])

def score_board(board, us):
    pass
