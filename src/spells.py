#! /usr/bin/python3
import arcade
from battle import *

SPELLPATH = "spells/"


class Spell(arcade.Sprite):

  def __init__(self):
    super().__init__()
    self.is_player = 1
    #We parse this out for form our spell
    self.command = ""
    player = 0
    enemy = 0
    command = 0
    self.cur_texture = 0
    self.damage_enemy = 0
    self.sprite_size = []
    #Where we store the sprite for our spell
    self.sprite = ""
    self.sprite1 = []
    self.sprite2 = []
    self.sprite3 = []
    #0 for casting, 1 for flying, 2 for on hit
    self.state = 0
    #How many frames each state takes up
    self.frame_range = []
    #3 sets of coordinates, one for each state [[][][]]
    self.hitboxes = []
    #Used for finding the correct spritesheet
    self.spellname = ""
    self.scale = 1
    self.spell_path = ""
    #Used for specific targetting
    self.x_offset = 0
    self.y_offset = 0
    #3 floats, one for each state
    self.frame_times = []

    #Tells us which particle effects we need
    self.effects= []

    self.scale = 0
    self.change_x = 0
    self.change_y = 0

  def setup(self, spellname, player, enemy):
    self.spellname = spellname
    if not self.is_player:
      # Position the start at the enemy's current location
      start_x = enemy.center_x
      start_y = enemy.center_y

      # Get the destination location for the bullet
      dest_x = player.center_x
      dest_y = player.center_y
    else:
      # Position the start at the enemy's current location
      start_x = player.center_x
      start_y = player.center_y

      # Get the destination location for the bullet
      dest_x = enemy.center_x
      dest_y = enemy.center_y

    self.spellpath = get_spell(self.spellname)
    self.get_spell_properties()


  #Combines the above functions to populate our spell
  def get_spell_properties(self):
    #get_sprite_size(spellname)
    attributes = []
    f = open(self.spellpath + "/properties", "r").readlines()
    for attribute in f:
      attributes.append(attribute.strip())
    #print(attributes)

    #self.sprite_size = attributes[0].split()

    self.frame_range.append(list(map(int, attributes[1].split() )))
    self.frame_range.append(list(map(int, attributes[2].split() )))
    self.frame_range.append(list(map(int, attributes[3].split() )))
    #print(self.frame_range)

    self.hitboxes.append(list(map(int, attributes[4].split() )))
    self.hitboxes.append(list(map(int, attributes[5].split() )))
    self.hitboxes.append(list(map(int, attributes[6].split() )))
    #print(self.hitboxes)

    self.sprite_size.append(list(map(int, attributes[7].split() )))
    self.sprite_size.append(list(map(int, attributes[8].split() )))
    self.sprite_size.append(list(map(int, attributes[9].split() )))
    print(self.sprite_size)

    #print(self.frame_range[0][1] - self.frame_range[0][0]+1)

    for i in range(self.frame_range[0][0],self.frame_range[0][1]):
      if i < 10:
        self.sprite1.append(arcade.load_texture(self.spellpath+'/'+self.spellname+"_0"+str(i)+".png"))
      else:
        self.sprite1.append(arcade.load_texture(self.spellpath+'/'+self.spellname+"_"+str(i)+".png"))

#    print(self.sprite1)
    #self.texture = self.sprite1
    #sprite2 = load_spritesheet(spellname+".png", )
    #get_spell_effects(spellname)
    #get_sprite_from_name(spellname)
    pass

  def collision(self):
    pass

  #How we are updating our frames every 1/60th of a second
  def update(self, delta_time):
    pass

def parse_command_string(p_action, p_spell, p_target, p_enemy_name):
  if get_action(p_spell) and get_spell(p_spell) and get_target(p_target) and get_enemy(p_enemy_name):
    return p_spell
  else:
    return p_spell #For now just have it execute no matter what
#    return False

  pass

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
