import sc2
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
 CYBERNETICSCORE, STALKER, RESEARCH_WARPGATE, WARPGATE, WARPGATETRAIN_STALKER
from Bot import BaseManager, ArmyManager


class ZeusBot(sc2.BotAI):
    def __init__(self):
        self.warpgateresearched = False

    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.researchwarp()
        await BaseManager.build_workers(self)
        await BaseManager.build_pylons(self)
        await BaseManager.build_assimilators(self)
        await BaseManager.expand(self)
        await BaseManager.offensive_force_buildings(self)
        await ArmyManager.build_offensive_force(self)
        await ArmyManager.attack(self)

    async def researchwarp(self):
        for core in self.units(CYBERNETICSCORE).ready.noqueue:
            if self.can_afford(RESEARCH_WARPGATE) and not self.warpgateresearched:
                await self.do(core(RESEARCH_WARPGATE))
                self.warpgateresearched = True
