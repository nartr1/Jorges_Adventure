#! /usr/bin/python3
import arcade
from battle import *
import math

SPELLPATH = "spells/"

class Spell(arcade.Sprite):

  """
  This class represents the spells on our screen. It is a child class of
  the arcade library's "Sprite" class.
  """
  #If both of these are zero, the sprite stays still
  follows_player = 1
  follows_enemy = 0
  follow_target = 0
  follows_mouse = 0
  spawn_above = 0
  spawn_below = 0

  #Sprite will die if it touches a wall
  collides_with_walls = 0

  #State can be 0,1,or 2. This is to keep track of whichanimation set we're using
  state = 0

  #Animation states keep track of our frame
  animation_state = 0

  #These sets holds our animation frames
  animation_set1 = []
  animation_set2 = []
  animation_set3 = []

  #Tells us when to kill off the sprite, -1 means it lives until the battle ends, 0 means it's dead, anything else is a countdown timer
  time_to_die = -1

  #Where the spell is fired from
  spell_origin = 0
  #Target will be used to determine where the spell is going
  spell_target = 0
  #How fast the spell moves towards the target
  spell_speed  = 10


  def follow_sprite(self, player_sprite, SPRITE_SPEED):

    """
    This function will move the current sprite towards whatever
    other sprite is specified as a parameter.
    We use the 'min' function here to get the sprite to line up with
    the target sprite, and not jump around if the sprite is not off
    an exact multiple of SPRITE_SPEED.
    """
    if self.center_y < player_sprite.center_y:
      self.center_y += min(SPRITE_SPEED, player_sprite.center_y - self.center_y)
    elif self.center_y > player_sprite.center_y:
      self.center_y -= min(SPRITE_SPEED, self.center_y - player_sprite.center_y)


    if self.center_x < player_sprite.center_x:
      self.center_x += min(SPRITE_SPEED, player_sprite.center_x - self.center_x)
    elif self.center_x > player_sprite.center_x:
      self.center_x -= min(SPRITE_SPEED, self.center_x - player_sprite.center_x)


  def follow_target(self, target):
    if self.center_y < target[1]:
      self.center_y += min(self.spell_speed, target[1] - self.center_y)
    elif self.center_y > target[1]:
      self.center_y -= min(self.spell_speed, self.center_y - target[1])


    if self.center_x < target[0]:
      self.center_x += min(self.spell_speed, target[0] - self.center_x)
    elif self.center_x > target[0]:
      self.center_x -= min(self.spell_speed, self.center_x - target[0])


  def move_to_target(self, player_sprite, target, speed):
    x_diff = target[0] - player_sprite.center_x
    y_diff = target[1] - player_sprite.center_y
    angle = math.atan2(y_diff, x_diff)

    # Taking into account the angle, calculate our change_x
    # and change_y. Velocity is how fast the bullet travels.
    self.change_x = math.cos(angle) * speed
    self.change_y = math.sin(angle) * speed

    self.center_x = self.center_x + self.change_x
    self.center_y = self.center_y + self.change_y


  #When the sprite needs to appear above or below the target
  def spawn_below(self, target, speed):
    self.center_x = target[0]
    self.center_y = target[1] - 50
    pass

  def spawn_above(self, target, speed):
    self.center_x = target[0]
    self.center_y = target[1] + 50
    pass

  #Takes time, kills off the sprite when the time is right
  def die_in(current_time, time_to_die):
    pass

  #This tells us what animations to play when we hit something
  def on_collide():
    pass

def parse_command_string(p_action, p_spell, p_target, p_enemy_name):
  if get_action(p_spell) and get_spell(p_spell) and get_target(p_target) and get_enemy(p_enemy_name):
    return p_spell
  else:
    return p_spell #For now just have it execute no matter what
#    return False
  pass

###############################################################################################################################
#Setting of the spell properties and attributes go in here
###############################################################################################################################
def get_spell_object(spellname, player_coordinates):

  this_spell = Spell(":resources:images/items/coinGold.png", 1)

  #get_spell_properties
  #get_spell_animations
  #get_spell_origin

  this_spell.center_x = player_coordinates[0]
  this_spell.center_y = player_coordinates[1]
  return this_spell

def get_command_string():
  return input("Please enter an action: ")

def remove_spaces(in_string):
  out_string = ""
  for i in range(len(in_string)):
    if in_string[i] != ' ':
      out_string += in_string[i]
    else:
      continue
  return out_string

action_list = ["throw"]
target_list = ["at"]
enemy_list = ["bob"]

#See if the spell exists
def get_spell(p_spell):
  spell_path = ""

  for dirname, dirnames, filenames in os.walk('./spells/'):
    for subdirname in dirnames:
      if  p_spell in subdirname:
        #print(os.path.join(dirname, subdirname))
        spell_path = os.path.join(dirname, subdirname)
  if spell_path:
    print(spell_path)
    return spell_path
  else:
    print("\n\n\n\nIn get_spell\n\n\n\n")
    return False

#Find index of the action
def get_action(command_list):
  for action in command_list:
    if action in action_list:
      return command_list.index(action)
    else:
      return False

#Find where we're targetting the spell at
def get_target(command_list):
  for target in command_list:
    if target in target_list:
      return command_list.index(target)
    else:
      return False

#Find which enemy on screen we wish to attack
def get_enemy(command_list):
  for enemy in command_list:
    if enemy in enemy_list:
      return True
    else:
      return False
    pass


def command_parsing(command):

  player_action = None
  player_spell = None
  player_target = None
  player_enemy_name = None

  print(command)

  #Get spaces, then seperates words
  command_list = command.split(' ')
  print(command_list)

  command_list = list(filter(None, command_list))

  #Get number of words
  command_words_num = len(command_list)

  if command_words_num == 4:
    player_action = command_list[0].lower()
    player_spell  = command_list[1].lower()
    player_target  = command_list[2].lower()
    player_enemy_name  = command_list[3].lower()
  else:
    return False #For now, going to add better command parsing later

  print("Action :", player_action)
  print("Spell  :", player_spell)
  print("Target :", player_target)
  print("Enemy  :", player_enemy_name)


  if parse_command_string(player_action, player_spell, player_target, player_enemy_name):
    return player_spell
  else:
    return False

def main():
  while True:
    if command_parsing(get_command_string()):
      print("Success!")
    else:
      print("Oh fuck...")

if __name__ == "__main__":
  print("Actions: ", action)
  print("Spells : ", spell)
  print("Targets: ", target)
  print("Enemies: ", enemy_name)
  main()
