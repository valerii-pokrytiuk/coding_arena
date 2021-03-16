import json
from pprint import pprint
from time import sleep

import requests


class Fabricator:
    BASE_API_URL = 'http://localhost:8000'

    def __init__(self, username='no_specified', url=None):
        self.player = username
        self.api_url = url or self.BASE_API_URL

    def process_response(self, response):
        if response.status_code not in [200, 201]:
            print("Server error, ask Valera to fix his bugs!")
            print(response)
        elif message := response.json().get('message'):
            print(r"%s" % message)
        else:
            print(response)
        sleep(1)  # DDOS protection, pls do not remove

    def connect(self):
        print(requests.get(self.api_url + f'/{self.player}/connect/').json()['message'])

    def produce(self, units_str):
        response = requests.post(
            self.api_url + f'/{self.player}/produce/',
            json={'units': units_str},
        )
        self.process_response(response)

    def score(self):
        response = requests.get(self.api_url + f'/score/')
        self.process_response(response)

    def task(self):
        response = requests.get(
            self.api_url + f'/{self.player}/task/',
        )
        self.process_response(response)

    def skip(self):
        response = requests.get(
            self.api_url + f'/{self.player}/skip-task/',
        )
        self.process_response(response)

    def check(self, function):
        results = []
        data_list = requests.get(f'{self.api_url}/{self.player}/task/').json().get('data')

        for data in data_list:
            results.append(function(*data))

        response = requests.post(
            self.api_url + f'/{self.player}/check-solution/',
            json={'solution': results}
        )
        self.process_response(response)

    def map(self):
        response = requests.post(self.api_url + f'/{self.player}/map/')
        self.process_response(response)

    def order_stay(self):
        response = requests.post(self.api_url + f'/{self.player}/orders/stay/')
        self.process_response(response)

    def move(self, move_str='', x=0, y=0):
        if move_str:
            # expect string with letters u (up), r (right), d (down), l (left)
            for i in move_str:
                step = 5
                if i == 'u': y += step
                elif i == 'r': x += step
                elif i == 'd': y -= step
                elif i == 'l': x -= step

        response = requests.post(
            self.api_url + f'/{self.player}/move/',
            json={'move': [x, y]}
        )
        self.process_response(response)
