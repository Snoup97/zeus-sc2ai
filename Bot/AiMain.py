import sc2
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
 CYBERNETICSCORE, STALKER
import random
from Bot import BaseManager

openingMessage = '(glhf)'


class ZeusBot(sc2.BotAI):

    async def on_step(self, iteration):
        await self.distribute_workers()
        await BaseManager.build_workers(self)
        await BaseManager.build_pylons(self)
        await BaseManager.build_assimilators(self)
        await BaseManager.expand(self)
        await self.distribute_workers()
        await self.offensive_force_buildings()
        await self.build_offensive_force()
        await self.attack()

    # Build Army Buildings
    async def offensive_force_buildings(self):
        if self.units(PYLON).ready.exists:

            # Random Pylon
            pylon = self.units(PYLON).ready.random

            # Build Cybercore
            if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon)

            if len(self.units(GATEWAY)) < 8:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)

    # Build the Army
    async def build_offensive_force(self):
        for gw in self.units(GATEWAY).ready.noqueue:
            if self.can_afford(STALKER) and self.supply_left > 0:
                await self.do(gw.train(STALKER))

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def attack(self):
        # {UNIT: [n to fight, m to defend]}
        aggressive_units = {STALKER: [15, 1]}

        for UNIT in aggressive_units:
            if self.units(UNIT).amount > aggressive_units[UNIT][0] and self.units(UNIT).amount > aggressive_units[UNIT][1]:
                for s in self.units(UNIT).idle:
                    await self.do(s.attack(self.find_target(self.state)))

            elif self.units(UNIT).amount > aggressive_units[UNIT][1]:
                if len(self.known_enemy_units) > 0:
                    for s in self.units(UNIT).idle:
                        await self.do(s.attack(random.choice(self.known_enemy_units)))