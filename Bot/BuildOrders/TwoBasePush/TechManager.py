from sc2.constants import CYBERNETICSCORE, RESEARCH_WARPGATE


# ToDo Bug Fix Sometimes Warpgate isnt researched
async def researchwarp(self):
    for core in self.units(CYBERNETICSCORE).ready.noqueue:
        if self.can_afford(RESEARCH_WARPGATE) and not self.warpgateresearched:
            await self.do(core(RESEARCH_WARPGATE))
            self.warpgateresearched = True
