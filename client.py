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
        if response.status_code == 500:
            print("Server error, ask Valera to fix his bugs!")
        elif message := response.json().get('message'):
            print(message)
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
        pprint(requests.get(self.api_url + f'/score/').json())

    def get_task(self):
       ...

    def check_solution(self, function):
        ...