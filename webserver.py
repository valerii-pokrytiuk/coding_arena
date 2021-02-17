import json
from copy import copy

from bottle import request, response, run, hook
from bottle import post, get, put, delete

from game import Game

game = Game()


@get('/<player>/connect/')
def connection_handler(player):
    if player in game.COLORS:
        message = f"Welcome to Arena, {player}!"
    else:
        message = "Invalid username!"
    return {"message": message}


@post('/<player>/produce/')
def produce(player):
    produce_str = request.json.get('units')
    return {"message": game.produce(player, produce_str)}


@get('/<player>/task/')
def get_task(player):
    return {"message": game.get_task(player)}


@get('/score/')
def score_handler():
    score = game.get_score()
    return json.dumps(score)


@post('/<player_index>/increase-score/')
def increase_score_handler(player_index):
    game.increase_score(int(player_index))
    return


if __name__ == "__main__":
    run(host='0.0.0.0', port=8000)
