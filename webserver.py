import json

from bottle import request, response, run, hook
from bottle import post, get, put, delete

from game import Game


game = Game()


@hook('after_request')
def set_headers():
    response.headers['Content-Type'] = 'application/json'


@get('/<player>/connect/')
def connection_handler(player):
    if player in game.COLORS:
        message = f"Welcome to Arena, {player}!"
    else:
        message = "Invalid username!"
    return {"message": message}


@get('/<player>/unit/')
def get_unit_handler(player):
    return UnitSchema(exclude=['solution', 'id']).dumps(game.get_unit(player))


@post('/<player>/produce/')
def produce_handler(player):
    try:
        solution = json.loads(request.json.get('data'))
        message = game.process_solution(player, solution)
    except json.JSONDecodeError as e:
        message = "Invalid format of solution"
    return {'message': message}


@get('/score/')
def score_handler():
    score = game.get_score()
    return json.dumps(score)


@post('/set-zombies/<amount>/')
def set_zombies_handler(amount):
    game.ZOMBIES_KILLED = int(amount)
    return


@post('/<player_index>/increase-score/')
def increase_score_handler(player_index):
    game.increase_score(int(player_index))
    return


if __name__ == "__main__":
    game.start()
    run(host='0.0.0.0', port=8000)
