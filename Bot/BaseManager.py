import sc2
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, CYBERNETICSCORE, WARPGATE


# Build 22 Probes per Nexus
async def build_workers(self):
    if (len(self.units(NEXUS)) * 22) > len(self.units(PROBE)):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))


# Build Pylon if under 5 Supply left
async def build_pylons(self):
    if self.supply_left < 5 and len(self.units(PYLON).not_ready) < 2:
        nexus = self.units(NEXUS).random
        if self.can_afford(PYLON):
            await self.build(PYLON, near=nexus.position.towards(self.game_info.map_center, 8))


# ToDo search for better way to take Vaspenes
async def build_assimilators(self):
    for nexus in self.units(NEXUS).ready:
        vaspenes = self.state.vespene_geyser.closer_than(15.0, nexus)
        for vaspene in vaspenes:
            if self.can_afford(ASSIMILATOR) and self.units(NEXUS).amount == 1 and self.units(ASSIMILATOR).amount == 0:
                worker = self.select_build_worker(vaspene.position)
                await self.do(worker.build(ASSIMILATOR, vaspene))

            if self.can_afford(ASSIMILATOR) and self.units(NEXUS).amount > 1 and self.units(ASSIMILATOR).amount < 4:
                worker = self.select_build_worker(vaspene.position)
                await self.do(worker.build(ASSIMILATOR, vaspene))


# Expand 2 Times | Third time after 6 Mins
async def expand(self):
    if self.units(NEXUS).amount < 2 and self.units(GATEWAY).amount >= 1:
        if self.can_afford(NEXUS):
            await self.expand_now()

    if self.units(NEXUS).amount < 3 and self.time > 360:
        if self.can_afford(NEXUS):
            await self.expand_now()


# Build Army Buildings
async def offensive_force_buildings(self):
    if self.units(PYLON).ready.exists:

        # Random Pylon
        pylon = self.units(PYLON).ready.random

        # Build Cybercore
        if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
            if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                await self.build(CYBERNETICSCORE, near=pylon)

        if self.units(GATEWAY).amount == 0 and self.units(NEXUS).amount == 1:
            if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                await self.build(GATEWAY, near=pylon)

        if len(self.units(GATEWAY)) + len(self.units(WARPGATE)) < 8 and self.units(NEXUS).amount == 2:
            if self.warpgateresearched and self.can_afford(GATEWAY):
                await self.build(GATEWAY, near=pylon)
