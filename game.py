import inspect
import json
import random
from collections import OrderedDict
from dataclasses import dataclass
from time import sleep

from redis import Redis

import tasks


@dataclass
class Unit:
    price: int
    production_key: str
    production_name: str
    description: str


@dataclass
class Player:
    color: str
    money: int = 0
    killed: int = 0
    controlled: int = 0


UNITS = [
    Unit(1, 'Z', 'Zergling', ''),
    Unit(1, 'M', 'Marine', ''),
    Unit(3, 'B', 'Baneling', ''),
    Unit(3, 'E', 'Medic', ''),
    Unit(4, 'F', 'Firebat', ''),
]
KEY_TO_UNIT_MAP = {u.production_key: u for u in UNITS}


class Game:
    COLORS = [
        'red',
        'blue',
        'green',

        'teal',
        'yellow',
        'violet',

        'pink',
        'purple',
        'brown',

        'orange',
        'white',
        'grey',
    ]
    ZOMBIES_KILLED = 0

    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.players = OrderedDict({color: {'unit': None, 'resolved': 0, 'killed': 0} for color in self.COLORS})
        self.tasks_list = []
        for name, obj in inspect.getmembers(tasks):
            if inspect.isclass(obj) and issubclass(obj, tasks.Task) and name != 'Task':
                self.tasks_list.append(obj)

    def produce(self, player_color, produce_str):
        player = self.players[player_color]
        production_keys = [char for char in produce_str]

        for key in production_keys:
            if key not in KEY_TO_UNIT_MAP:
                return f"Invalid key {key}"

        production_dict, total_price = self._get_production_dict_and_price(production_keys)
        if player.money < total_price:
            return "Not enough money to produce all this units"

        for unit_name, amount in production_dict.items():
            self.redis.publish(
                'game-commands', f"-create {amount} {unit_name} {player.number}"
            )
        return "Trying to produce units"

    def _get_production_dict_and_price(self, production_keys):
        production_dict = {}
        total_price = 0
        for key in production_keys:
            unit = KEY_TO_UNIT_MAP[key]
            if unit in production_dict:
                production_dict[unit] += 1
            else:
                production_dict[unit.production_name] = 1
            total_price += unit.price
        return production_dict, total_price

    def get_score(self):
        return {color: info['killed'] for color, info in self.players.items()}

    def increase_score(self, player_index):
        self.players[self.COLORS[player_index-1]]['killed'] += 1

    def process_solution(self, player_name, solution):
        unit = self.get_unit(player_name)
        if not unit:
            return f"Unit not found"
        sleep(2)
        if unit['solution'] == solution:
            self.redis.publish('game-commands', f"create {unit['unit']} {player_name} 1")
            self.players[player_name]['unit'] = None
            self.players[player_name]['resolved'] += 1
            self.set_unit(player_name)

            return f"Successfully produced {unit['unit']}"
        else:
            print(f"{player_name} sent {solution}, right is {unit['solution']}")
            return f"Failed to produce {unit['unit']}"

    def set_unit(self, player_name):
        new_unit = self.init_unit(self.players[player_name]['resolved']//10)
        self.players[player_name]['unit'] = new_unit

    def start(self, player_color):
        ...

    def get_task(self, player_color):
        ...
