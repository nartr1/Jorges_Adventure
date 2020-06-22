#! /usr/bin/python3
import arcade
from battle import *
import math

SPELLPATH = "spells/"

class Spell(arcade.Sprite):

  def __init__(self):
      # Set up parent class
    super().__init__()
    self.scaling = 1
    self.texture = None

    ###From Game###
    #This holds the spells directory
    self.spell_path = ""
    self.spell_name = ""

    #Either player or enemy name, let's us know what this spell can damage
    self.spell_caster = ""

    #Let's us keep track of if the spell has been cast, used for animations
    self.has_been_cast = 0
    #Where the spell is fired from
    self.spell_origin = 0
    #Target will be used to determine where the spell is going
    self.spell_target = 0
    #How fast the spell moves towards the target
    self.spell_speed  = 10

    #Just a basic square for testing and spawning in
    self.initial_hitbox = [[-10, -10], [10, -10], [10, 10], [-10, 10]]
    ###Movement###
    #If both of these are zero, the sprite stays still
    self.follows_player = 0
    self.follows_enemy = 0
    self.follows_target = 0
    self.follows_mouse = 0
    self.spawn_above = 0
    self.spawn_below = 0

    #Distance used when spawning the spell object
    self.distance = 0

    ###Properties###
    #How many hearts the target loses on hit from the spell, the caster is immune to this
    self.damage_on_hit = 0
    #Sprite will die if it touches a wall
    self.collides_with_walls = 0

    ###Hitboxes###
    #Holds the hitboxes for each animation set
    self.hitbox1 = []
    self.hitbox2 = []
    self.hitbox3 = []

    ###Animation###
    #State can be 0,1,or 2. This is to keep track of whichanimation set we're using
    self.state = 0

    #Animation states keep track of our frame
    self.animation_state = 0

    #Holds how big in pixels each frame is
    self.animation_size1 = 0
    self.animation_size2 = 0
    self.animation_size3 = 0

    #Holds how many frames our animation consists of
    self.animation_length1 = 0
    self.animation_length2 = 0
    self.animation_length3 = 0

    #The speed at which the animation plays, 1 being the default, .5 being half as fast, 2 being twice as fast
    self.animation_speed1 = 0
    self.animation_speed2 = 0
    self.animation_speed3 = 0

    #These sets holds our actual animation frames
    self.animation_set1 = []
    self.animation_set2 = []
    self.animation_set3 = []

    #Tells us when to kill off the sprite, -1 means it lives until the battle ends, 0 means it's dead, anything else is a countdown timer
    self.time_to_die = -1

    #Movement type 0
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

  #Movement type 1
  def follow_target(self, target):
    if self.center_y < target[1]:
      self.center_y += min(self.spell_speed, target[1] - self.center_y)
    elif self.center_y > target[1]:
      self.center_y -= min(self.spell_speed, self.center_y - target[1])


    if self.center_x < target[0]:
      self.center_x += min(self.spell_speed, target[0] - self.center_x)
    elif self.center_x > target[0]:
      self.center_x -= min(self.spell_speed, self.center_x - target[0])

  #Movement type 2
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


  #Movement type 3
  def spawn_below(self, target, speed, distance):
    self.center_x = target[0]
    self.center_y = target[1] - distance
    pass

  #Movement type4
  def spawn_above(self, target, speed, distance):
    self.center_x = target[0]
    self.center_y = target[1] + distance
    pass

  #Takes time, kills off the sprite when the time is right
  def die_in(self, current_time, time_to_die):
    if current_time + time_to_die == current_time:
      self.remove_from_sprite_lists()
    pass

  #This tells us what animations to play when we hit something
  def on_collision(self,):
    if self.collides_with_walls:
      self.remove_from_sprite_lists()
    pass



###############################################################################################################################
#Setting of the spell properties and attributes go in here
###############################################################################################################################
def get_spell_object(spellname, player_coordinates, enemy_coordinates, caster):
  spell_path = get_spell(spellname)
  this_spell = Spell()
  this_spell.spell_path = spell_path
  this_spell.spell_name = spellname
  get_spell_animations(this_spell)
  print(this_spell.spawn_above)
  #get_spell_properties
    #damage
    #movement type
    #collides_with_walls
    #difficulty (Used for the casting minigame)
  #Testing hitboxes
  #get_spell_origin
  #get_spell_target
  if caster == "player":
    this_spell.spell_caster = "player"
    this_spell.target = enemy_coordinates
  else:
    this_spell.spell_caster = "enemy"
    this_spell.target = player_coordinates

  #get_spell_path_type
  this_spell.follows_mouse = 1
  this_spell.collides_with_walls = 1
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

def parse_command_string(p_action, p_spell, p_target, p_enemy_name):
  print("Parsing command string!")
  if get_action(p_action):
    print("Got action!")
    if get_spell(p_spell):
      print("Got spell!")
      if get_target(p_target):
        print("Got target!")
        if get_enemy(p_enemy_name):
          print("Got enemy name!")
          return p_spell
  else:
#    return p_spell #For now just have it execute no matter what
    print("Spell failed!")
    return False
  pass


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

#Get all of our animations for the spell sprite and set the initial texture to the first frame of the casting set
def get_spell_animations(spell_object):
  get_anim_state1(spell_object)
  get_anim_state2(spell_object)
  get_anim_state3(spell_object)

  spell_object.texture = spell_object.animation_set1[0]

#Animation for the casting effect
def get_anim_state1(spell_object):
  path = spell_object.spell_path
  #Get sprite size and length
  f = open(path+"/casting_properties", "r").readlines()
  spell_object.animation_size1 = int(f[0].strip())
  spell_object.animation_length1 = int(f[1].strip())
  spell_object.animation_speed1 = int(f[2].strip())

  #get the actual spritesheet
  spell_object.animation_set1 = arcade.load_spritesheet(path+'/'+spell_object.spell_name + "_casting.png", spell_object.animation_size1, spell_object.animation_size1,spell_object.animation_length1,spell_object.animation_length1)

#Animation for the flying/intermediate effect
def get_anim_state2(spell_object):
  path = spell_object.spell_path
  #Get sprite size and length
  f = open(path+"/casted_properties", "r").readlines()
  spell_object.animation_size2 = int(f[0].strip())
  spell_object.animation_length2 = int(f[1].strip())
  spell_object.animation_speed2 = int(f[2].strip())

  #get the actual spritesheet
  spell_object.animation_set2 = arcade.load_spritesheet(path+'/'+spell_object.spell_name + "_casted.png", spell_object.animation_size2, spell_object.animation_size2,spell_object.animation_length2,spell_object.animation_length2)

#Animation for the hit effects
def get_anim_state3(spell_object):
  path = spell_object.spell_path
  #Get sprite size and length
  f = open(path+"/hit_properties", "r").readlines()
  spell_object.animation_size3 = int(f[0].strip())
  spell_object.animation_length3 = int(f[1].strip())
  spell_object.animation_speed3 = int(f[2].strip())

  #get the actual spritesheet
  spell_object.animation_set3 = arcade.load_spritesheet(path+'/'+spell_object.spell_name + "_hit.png", spell_object.animation_size3, spell_object.animation_size3,spell_object.animation_length3,spell_object.animation_length3)

#Find index of the action
def get_action(action):
  if action in action_list:
    return True
  else:
    return False

#Find where we're targetting the spell at
def get_target(target):
  if target in target_list:
    return True
  else:
    return False

#Find which enemy on screen we wish to attack
def get_enemy(enemy):
  if enemy in enemy_list:
    return True
  else:
    return False

#This get's the keywords from a string, if they do not fit the format or are not found in the lists, then the spell fails and the command buffer fills with garbage
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
