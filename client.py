import sys
from inspect import getmembers, isfunction, currentframe
from time import sleep

import requests


def solve(resolving):
    def wrapper(func):
        func.resolving = resolving
        return func
    return wrapper

def process_response(func):
    def _process_response(response):
        if response.status_code in [500, 404]:
            print("Server error, ask Valera to fix his bugs!")
            print(response)
        elif 'message' in response.json():
            sleep(1)  # DDOS protection, pls do not remove
            print(response.json()['message'])
        else:
            print(response)
        return response

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if type(result) is requests.Response:
            return _process_response(result)

    return wrapper


class Gateway:
    BASE_API_URL = 'http://localhost:8000/'

    def __init__(self, player='not_specified', url=None):
        self.player_url = (url or self.BASE_API_URL) + player + '/'
        self.urls = {
            'connect': self.player_url + 'connect/',
            'produce': self.player_url + 'produce/',
            'task':    self.player_url + 'task/',
            'skip':    self.player_url + 'task/skip/',
            'check':   self.player_url + 'task/check-solution/',
            'map':     self.player_url + 'map/',
            'o_stay':  self.player_url + 'orders/stay/',
            'move':    self.player_url + 'move/',
        }

    @process_response
    def connect(self):
        return requests.get(self.urls['connect'])

    @process_response
    def produce(self, units_str):
        return requests.post(self.urls['produce'], json={'units': units_str})

    @process_response
    def task(self):
        response = requests.get(self.urls['task'])
        if response.status_code == 200:
            print(r"%s" % response.json()['task'])
            return
        return response

    @process_response
    def skip(self):
        return requests.get(self.urls['skip'])

    @process_response
    def check(self, function=None):
        task_response = requests.get(self.urls['task'])
        if task_response.status_code != 200:
            return task_response

        task = task_response.json()

        # try to find function in player environment
        if not function:
            function = self._find_suitable_function(task['type'])

        # if not found
        if not function:
            print("No function provided and no suitable functions found.")
            return

        results = []
        for data in task['data']:
            results.append(function(*data))

        return requests.post(self.urls['check'], json={'solution': results})

    @staticmethod
    def _find_suitable_function(task_type):
        for name, func in getmembers(sys.modules["__main__"], isfunction):
            try:
                if func.resolving == task_type:
                    return func
            except AttributeError:
                ...

    @process_response
    def map(self):
        return requests.post(self.urls['map'])

    @process_response
    def order_stay(self):
        return requests.post(self.urls['o_stay'])

    @process_response
    def move(self, x=0, y=0):
        return requests.post(self.urls['move'], json={'move': [x, y]})
