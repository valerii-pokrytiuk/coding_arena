from bottle import request, response, run, hook
from bottle import post, get, put, delete

from game import Game

game = Game()

def message_wrapper(view):
    def wrapped_view(*args, **kwargs):
        result = view(*args, **kwargs)
        if type(result) == str:
            return {"message": result}
        return result
    return wrapped_view


def check_player(view):
    def wrapped_view(*args, **kwargs):
        if player := kwargs.get('player'):
            if player not in game.players:
                response.status = 400
                return "Invalid username!"
        return view(*args, **kwargs)
    return wrapped_view

@get('/<player>/connect/')
@message_wrapper
@check_player
def connection_handler(player):
    if player in game.players:
        return f"Welcome, {player}!"

@post('/<player>/produce/')
@message_wrapper
@check_player
def produce(player):
    produce_str = request.json.get('units')
    return game.produce(player, produce_str)


@get('/<player>/task/')
@message_wrapper
@check_player
def get_task(player):
    return game.get_task(player)


@get('/<player>/task/skip/')
@message_wrapper
@check_player
def skip_task(player):
    return game.skip_task(player)


@post('/<player>/task/check-solution/')
@message_wrapper
@check_player
def check_solution(player):
    return game.process_solution(player, request.json.get('solution'))

@post('/<player>/map/')
@message_wrapper
@check_player
def show_map(player):
    return game.show_map()

@post('/<player>/orders/stay/')
@message_wrapper
@check_player
def order_stay(player):
    return game.order_stay(player)

@post('/<player>/orders/follow/')
@message_wrapper
@check_player
def order_follow(player):
    return game.order_follow(player)


@post('/<player>/move/')
@message_wrapper
@check_player
def move(player):
    return game.move(player, *request.json.get('move'))


if __name__ == "__main__":
    run(host='0.0.0.0', port=8000)
