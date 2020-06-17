#! /usr/bin/python3
import arcade
import os
from spells import *
from battle import *

# Constants
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 1.75
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 64
GRID_PIXEL_SIZE = 64  #(SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.60
PLAYER_JUMP_SPEED = 15


# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.

LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100


PLAYER_START_X = 100 #SPRITE_PIXEL_SIZE * TILE_SCALING * 2
PLAYER_START_Y = 400  #(SPRITE_PIXEL_SIZE * TILE_SCALING * 1) - 200



# Constants used to track if the player is facing left or right

RIGHT_FACING = 0
LEFT_FACING = 1



def main():
  window = MyGame()
  window.setup()
  arcade.run()


if __name__ == "__main__":
  main()
