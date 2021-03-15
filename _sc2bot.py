import sc2
from redis import Redis
from sc2 import run_game, maps, Race, sc2process, Difficulty, AIBuild
from sc2.player import Bot, Computer


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
        maps.get("fab_submarine"),
        [Bot(Race.Terran, NemesisProjectBot()),
         Computer(Race.Terran, Difficulty.Medium),
         Computer(Race.Zerg, Difficulty.Hard, AIBuild.Rush)],
        realtime=True
    )
