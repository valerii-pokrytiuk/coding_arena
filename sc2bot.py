import asyncio
import sys

import aiohttp
import requests
import sc2
from redis import Redis
from sc2 import run_game, maps, Race, sc2process
from sc2.player import Bot


DEBUG_PATH = '/Users/admin/Library/Application Support/Blizzard/StarCraft II/UserLogs/Python Arena_24447110/'
READ_LINES = 0
BASE_URL = 'http://localhost:8000'


# Long game startup monkey patch
async def _connect(self):
    for i in range(60*3):
        if self._process is None:
            sys.exit()
        await asyncio.sleep(1)
        try:
            self._session = aiohttp.ClientSession()
            ws = await self._session.ws_connect(self.ws_url, timeout=120)
            return ws
        except aiohttp.client_exceptions.ClientConnectorError:
            await self._session.close()
sc2process.SC2Process._connect = _connect


class NemesisProjectBot(sc2.BotAI):
    async def on_start(self):
        self.client.game_step = 5
        open(DEBUG_PATH+'arena_debug.txt', "w").close()

    async def on_step(self, iteration: int):
        while message := redis_listener.get_message():
            command = message['data']
            await self.chat_send(command)

        if iteration % 3 == 0:
            with open(DEBUG_PATH+'arena_debug.txt', 'r') as file:
                global READ_LINES
                line_number = 0
                for line in file:
                    line_number += 1
                    if line_number > READ_LINES:
                        key, value = line.split(' ')
                        value = value[:-1]
                        if key == 'KILLED_ZOMBIES':
                            requests.post(BASE_URL+f'/set-zombies/{value}/')
                        elif key == 'INCREASE':
                            requests.post(BASE_URL+f'/{value}/increase-score/')
                READ_LINES = line_number


if __name__ == "__main__":
    redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_listener = redis.pubsub(ignore_subscribe_messages=True)
    redis_listener.subscribe('game-commands')
    run_game(
        maps.get("coding_arena"),
        [Bot(Race.Terran, NemesisProjectBot())],
        realtime=True
    )
