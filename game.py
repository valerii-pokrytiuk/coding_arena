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


UNITS = [
    # Unit(1, 'Z', 'Zergling', ''),
    Unit(1, 'M', 'Marine', ''),
    # Unit(3, 'B', 'Baneling', ''),
    Unit(3, 'E', 'Medic', ''),
    Unit(4, 'F', 'Firebat', ''),
]
KEY_TO_UNIT_MAP = {u.production_key: u for u in UNITS}


@dataclass
class Player:
    color: str
    number: int
    money: int = 10
    killed: int = 0
    controlled: int = 0
    resolved: int = 0
    task: tasks.Task = None


PLAYER_COLORS_MAP = {
        'red': 10,
        'blue': 1,
        'green': 11,
        'yellow': 12,
}


class Game:
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.tasks_list = self.get_tasks_list()
        self.players = self.get_players()

    def get_tasks_list(self):
        tasks_list = []
        for name, obj in inspect.getmembers(tasks):
            if inspect.isclass(obj) and issubclass(obj, tasks.Task) and name != 'Task':
                tasks_list.append(obj)
        return tasks_list

    def get_players(self):
        players = OrderedDict()
        for color, number in PLAYER_COLORS_MAP.items():
            players[color] = Player(
                color=color,
                number=number,
                task=self.generate_task(),
            )
        return players

    def move(self, player_color, x, y):
        self.redis.publish(
            'game-commands', f'-move {x} {y} {self.players[player_color].number}'
        )
        return "Trying to move..."

    def show_map(self):
        self.redis.publish('game-commands', f'-map')
        return "Showing map"

    def order_stay(self, player_color):
        self.redis.publish('game-commands', f'-stay {self.players[player_color].number}')
        return "Order has been issued!"

    def order_follow(self, player_color):
        self.redis.publish('game-commands', f'-follow {self.players[player_color].number}')
        return "Order has been issued!"

    def produce(self, player_color, produce_str):
        player = self.players[player_color]
        production_keys = [char for char in produce_str]

        for key in production_keys:
            if key not in KEY_TO_UNIT_MAP:
                return f"Invalid key {key}"

        production_dict, total_price = self._get_production_dict_and_price(production_keys)
        if player.money < total_price:
            return f"Not enough energy to produce all this units. Your balance is {player.money}⚡"

        for unit_name, amount in production_dict.items():
            self.redis.publish(
                'game-commands', f"-create {amount} {unit_name} {player.number}"
            )

        player.money -= total_price
        return f"Trying to produce units. You have {player.money}⚡ left."

    def _get_production_dict_and_price(self, production_keys):
        production_dict = {}
        total_price = 0
        for key in production_keys:
            unit = KEY_TO_UNIT_MAP[key]
            if unit.production_name in production_dict:
                production_dict[unit.production_name] += 1
            else:
                production_dict[unit.production_name] = 1
            total_price += unit.price
        return production_dict, total_price

    def process_solution(self, player_name, solutions_list):
        player = self.players[player_name]
        task = player.task
        for i in range(len(task.solutions_list)):
            try:
                player_solution = solutions_list[i]
            except IndexError:
                return "Not enough data"
            if player_solution != task.solutions_list[i]:
                return f"Invalid solution {player_solution} for input {task.data_list[i]}"

        player.money += task.complexity*2
        player.task = self.generate_task()
        return f"Task solved, your balance is {player.money}⚡"

    def get_task(self, player_name):
        task = self.players[player_name].task
        return {'type': task.type, 'task': task.task, 'data': task.data_list}

    def skip_task(self, player_color):
        player = self.players[player_color]
        if player.money >= 1:
            player.money -= 1
        player.task = self.generate_task()
        return f"New task assigned, your current balance is {player.money}⚡."

    def generate_task(self):
        return random.choice(self.tasks_list)()
