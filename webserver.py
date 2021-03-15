import json
from copy import copy

from bottle import request, response, run, hook
from bottle import post, get, put, delete

from game import Game

game = Game()

def message_wrapper(view):
    def wrapped_view(*args, **kwargs):
        return {"message": view(*args, **kwargs)}
    return wrapped_view


@get('/<player>/connect/')
@message_wrapper
def connection_handler(player):
    if player in game.players:
        return f"Welcome, {player}!"
    return "Invalid username!"


@post('/<player>/produce/')
@message_wrapper
def produce(player):
    produce_str = request.json.get('units')
    return game.produce(player, produce_str)


@get('/<player>/task/')
def get_task(player):
    message, data = game.get_task(player)
    return {"message": message, "data": data}


@post('/<player>/check-solution/')
@message_wrapper
def check_solution(player):
    return game.process_solution(player, request.json.get('solution'))

@post('/<player>/move/')
@message_wrapper
def move(player):
    return game.move(player, request.json.get('move'))


# @get('/score/')
# def score_handler():
#     score = game.get_info()
#     return {"message": score}
#
#
# @post('/<player_index>/increase-score/')
# def increase_score_handler(player_index):
#     game.increase_killed(int(player_index))
#     return
#
#
# @post('/<player_index>/increase-control/')
# def increase_score_handler(player_index):
#     game.increase_controlled(int(player_index))
#     return


if __name__ == "__main__":
    run(host='0.0.0.0', port=8000)
