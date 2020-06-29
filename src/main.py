#! /usr/bin/python3
import arcade
import os
from spells import *
import battle
import world_travelling

# Constants
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Explore!"

#battle_view = battle.Battle()
world_view = world_travelling.World()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    world_view.setup()
    window.show_view(world_view)
    arcade.run()

if __name__ == "__main__":
    main()
