from Bot.BuildOrders.CannonRush import CannonRush


async def execute_build(self):
    await CannonRush.execute_rush(self)
