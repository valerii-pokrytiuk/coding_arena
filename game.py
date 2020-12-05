import inspect
import json
import random
from collections import OrderedDict
from time import sleep

from redis import Redis

import tasks


class Game:
    COMPLEXITY_TO_BREED = {
        0: ['Zergling', 'Zergling', 'Zergling', 'Medic'],
        1: ['Marine', 'Marine', 'Zealot'],
        2: ['Roach', 'Firebat', 'Adept', 'Baneling'],
        3: ['Hydralisk', 'Marauder', 'Stalker'],
        # 4: ['Ravager']
    }
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
        self.current_id = 0
        self.redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.players = OrderedDict({color: {'unit': None, 'resolved': 0, 'killed': 0} for color in self.COLORS})
        self.tasks_list = []
        for name, obj in inspect.getmembers(tasks):
            if inspect.isclass(obj) and issubclass(obj, tasks.Task) and name != 'Task':
                self.tasks_list.append(obj)

    def get_id(self):
        self.current_id += 1
        return self.current_id

    def get_score(self):
        return {color: info['killed'] for color, info in self.players.items()}

    def increase_score(self, player_index):
        self.players[self.COLORS[player_index-1]]['killed'] += 1

    def get_unit(self, player_name: str):
        return self.players.get(player_name, {}).get('unit', None)

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

    def init_unit(self, complexity):
        allowed_tasks = [task for task in self.tasks_list if task.complexity <= complexity]
        task = random.choice(allowed_tasks)()
        unit = {
            'id': self.get_id(),
            'unit': random.choice(self.COMPLEXITY_TO_BREED[task.complexity]),
            'type': type(task).__name__,
            'task': task.task,
            'data': json.dumps(task.data),
            'solution': task.solution,
        }
        return unit

    def start(self):
        for player_name in self.COLORS:
            self.set_unit(player_name)
