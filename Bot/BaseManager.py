import sc2
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR


# Build 22 Probes per Nexus
async def build_workers(self):
    if (len(self.units(NEXUS)) * 22) > len(self.units(PROBE)):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))


# Build Pylon if under 5 Supply left
async def build_pylons(self):
    if self.supply_left < 5 and not self.already_pending(PYLON):
        nexuses = self.units(NEXUS).ready
        if nexuses.exists:
            if self.can_afford(PYLON):
                await self.build(PYLON, near=nexuses.first)


# ToDo search for better way to take Vaspenes
async def build_assimilators(self):
    for nexus in self.units(NEXUS).ready:
        vaspenes = self.state.vespene_geyser.closer_than(15.0, nexus)
        for vaspene in vaspenes:
            if not self.can_afford(ASSIMILATOR):
                break
            worker = self.select_build_worker(vaspene.position)
            if worker is None:
                break
            if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists and self.units(PYLON).exists:
                await self.do(worker.build(ASSIMILATOR, vaspene))


# Expand 2 Times
async def expand(self):
    if self.units(NEXUS).amount < 2 and self.can_afford(NEXUS):
        await self.expand_now()
