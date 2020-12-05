import json
from pprint import pprint
from time import sleep

import requests


class Fabricator:
    BASE_API_URL = 'http://localhost:8000'

    def __init__(self, username='no_specified', url=None):
        self.player = username
        self.api_url = url or self.BASE_API_URL

    def connect(self):
        print(requests.get(self.api_url + f'/{self.player}/connect/').json()['message'])

    def get_unit(self):
        unit = requests.get(self.api_url + f'/{self.player}/unit/').json()
        try:
            unit['data'] = json.loads(unit['data'])
        except json.JSONDecodeError:
            ...
        return unit

    def produce(self, data):
        response = requests.post(
            self.api_url + f'/{self.player}/produce/',
            json={'data': json.dumps(data)},
        )
        print(response.json()['message'])
        return response

    def score(self):
        pprint(requests.get(self.api_url + f'/score/').json())

    def autobuild(self, database):
        run = True
        while run:
            unit = self.get_unit()
            if unit['type'] in database:
                self.produce(database[unit['type']]())
            else:
                print(f"Unknown type {unit['type']}")
                run = False
