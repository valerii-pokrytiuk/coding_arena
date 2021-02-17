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
        if response.status_code in [500, 404]:
            print("Server error, ask Valera to fix his bugs!")
        elif message := response.json().get('message'):
            pprint(message)
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

    def get_task(self):
        response = requests.get(
            self.api_url + f'/{self.player}/task/',
        )
        self.process_response(response)

    def check_solution(self, function):
        results = []

        data_list = requests.get(
            self.api_url + f'/{self.player}/task/',
        ).json().get('data')

        for data in data_list:
            results.append(function(data))

        response = requests.post(
            self.api_url + f'/{self.player}/check-solution/',
            json={'solution': results}
        )

        self.process_response(response)