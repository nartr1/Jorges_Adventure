#! /usr/bin/python3
import arcade
import os
from spells import *
from battle import *
from world_travelling import *


def main():
  window = Battle()
  #window = World()
  window.setup()
  arcade.run()


if __name__ == "__main__":
  main()
