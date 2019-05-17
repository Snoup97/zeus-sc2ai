import sc2
from Bot.BuildOrders.TwoBasePush import TwoBaseMain
from Bot.BuildOrders.CannonRush import CannonMain
from random import randint

chosen_build = randint(1, 2)


class ZeusBot(sc2.BotAI):
    def __init__(self):
        self.warpgateresearched = False

    async def on_step(self, iteration):
        await self.distribute_workers()
        if chosen_build == 1:
            await TwoBaseMain.execute_build(self)
        elif chosen_build == 2:
            await CannonMain.execute_build(self)
