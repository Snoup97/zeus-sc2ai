from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
    CYBERNETICSCORE, WARPGATE, STALKER, WARPGATETRAIN_STALKER, ROBOTICSFACILITY, IMMORTAL
import random


# Build the Army
async def build_offensive_force(self):
    if self.time > 360 and self.units(NEXUS).amount < 3:
        return

    for robo in self.units(ROBOTICSFACILITY).ready.noqueue:
        if self.can_afford(IMMORTAL) and self.supply_left > 0:
            await self.do(robo.train(IMMORTAL))

    for gw in self.units(GATEWAY).ready.noqueue:
        if self.can_afford(STALKER) and self.supply_left > 0:
            await self.do(gw.train(STALKER))

    for wg in self.units(WARPGATE).ready.noqueue:
        pylon = self.units(PYLON).ready.random.position
        placement = await self.find_placement(WARPGATETRAIN_STALKER, near=pylon, placement_step=1)
        if self.can_afford(STALKER) and self.supply_left > 0:
            if self.units(IMMORTAL).amount >= 4 or self.units(ROBOTICSFACILITY).ready.noqueue.amount == 0:
                await self.do(wg.warp_in(STALKER, placement))


def find_target(self, state):
    if len(self.known_enemy_units) > 0:
        return random.choice(self.known_enemy_units)
    elif len(self.known_enemy_structures) > 0:
        return random.choice(self.known_enemy_structures)
    else:
        return self.enemy_start_locations[0]


# ToDo find way to group army
async def attack(self):
    # {UNIT: [n to fight, m to defend]}
    aggressive_units = {STALKER: [8, 1],
                        IMMORTAL: [2, 1]}

    for UNIT in aggressive_units:
        if self.units(STALKER).amount > 12 and self.units(IMMORTAL).amount > 4:
            for s in self.units(UNIT).idle:
                await self.do(s.attack(find_target(self, self.state)))

        elif self.units(UNIT).amount > aggressive_units[UNIT][1]:
            if len(self.known_enemy_units) > 0:
                for s in self.units(UNIT).idle:
                    await self.do(s.attack(random.choice(self.known_enemy_units)))
