from importlib import reload
import argparse

import sys
import asyncio

import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

from Bot import ZeusBot


def main():
    player_config = [
        Bot(Race.Protoss, ZeusBot.ZeusBot()),
        Computer(Race.Random, Difficulty.Medium)
    ]

    gen = sc2.main._host_game_iter(
        sc2.maps.get("AutomatonLE"),
        player_config,
        realtime=False
    )

    while True:
        r = next(gen)

        reload(ZeusBot)
        player_config[0].ai = ZeusBot.ZeusBot()
        gen.send(player_config)


if __name__ == "__main__":
    main()
