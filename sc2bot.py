import asyncio
import sys

import aiohttp
import sc2
from redis import Redis
from sc2 import run_game, maps, Race, sc2process, UnitTypeId, unit
from sc2.cache import property_immutable_cache
from sc2.player import Bot, Computer


APPLY_PATCH = False


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


# Custom objects ids monkey patch
@property_immutable_cache
def type_id(self) -> UnitTypeId:
    unit_type = self._proto.unit_type
    if unit_type not in self._bot_object._game_data.unit_types:
        try:
            self._bot_object._game_data.unit_types[unit_type] = UnitTypeId(unit_type)
        except ValueError:
            return
    return self._bot_object._game_data.unit_types[unit_type]
unit.Unit.type_id = type_id


class NemesisProjectBot(sc2.BotAI):
    async def on_start(self):
        self.client.game_step = 5
        while message := redis_listener.get_message():
            ...

    async def on_step(self, iteration: int):
        while message := redis_listener.get_message():
            command = message['data']
            await self.chat_send(command)


if __name__ == "__main__":
    redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_listener = redis.pubsub(ignore_subscribe_messages=True)
    redis_listener.subscribe('game-commands')
    run_game(
        maps.get("colonists_fab"),
        [Bot(Race.Terran, NemesisProjectBot())],
        realtime=True
    )
