from Bot.BuildOrders.TwoBasePush import TechManager, BaseManager, ArmyManager


async def execute_build(self):
    await TechManager.researchwarp(self)
    await BaseManager.build_workers(self)
    await BaseManager.build_pylons(self)
    await BaseManager.build_assimilators(self)
    await BaseManager.expand(self)
    await BaseManager.offensive_force_buildings(self)
    await ArmyManager.build_offensive_force(self)
    await ArmyManager.attack(self)
