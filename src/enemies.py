#! /usr/bin/python3
import ast
import arcade
import sys
import os

RIGHT_FACING = 0
LEFT_FACING = 1


# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 1.75
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 64
GRID_PIXEL_SIZE = 64  # (SPRITE_PIXEL_SIZE * TILE_SCALING)


class EnemyCharacter(arcade.Sprite):
    # Carbon copy of the player class for testing

    def __init__(self, enemy_name):
        # Set up parent class
        print(enemy_name)
        super().__init__()
        self.name = enemy_name
        self.framelength_idle = 32
        self.framesize_left = 32
        self.framesize_right = 32
        self.framesize_up = None
        self.framesize_down = None
        self.framesize_attack1 = 32
        self.framesize_attack2 = None
        self.framesize_attack3 = None
        self.framesize_attack4 = None
        self.framelength_idle = 4
        self.framelength_left = 4
        self.framelength_right = 4
        self.framelength_up = None
        self.framelength_down = None
        self.framelength_attack1 = 6
        self.framelength_attack2 = None
        self.framelength_attack3 = None
        self.framelength_attack4 = None
        self.playbackspeed_idle = 1
        self.playbackspeed_left = 1
        self.playbackspeed_right = 1
        self.playbackspeed_up = None
        self.playbackspeed_down = None
        self.playbackspeed_attack1 = 1
        self.playbackspeed_attack2 = None
        self.playbackspeed_attack3 = None
        self.playbackspeed_attack4 = None
        self.hitbox_idle = [[-10, -10], [10, -10], [10, 10], [-10, 10]]
        self.hitbox_left = [[-10, -10], [10, -10], [10, 10], [-10, 10]]
        self.hitbox_right = [[-10, -10], [10, -10], [10, 10], [-10, 10]]
        self.hitbox_up = None
        self.hitbox_down = None
        self.hitbox_attack1 = [[-10, -10], [10, -10], [10, 10], [-10, 10]]
        self.hitbox_attack2 = None
        self.hitbox_attack3 = None
        self.hitbox_attack4 = None
        self.attack1_damage = 1
        self.attack2_damage = None
        self.attack3_damage = None
        self.attack4_damage = None
        self.attack1_element = "normal"
        self.attack2_element = None
        self.attack3_element = None
        self.attack4_element = None
        self.attack1_frequency = 1
        self.attack2_frequency = None
        self.attack3_frequency = None
        self.attack4_frequency = None
        self.attack1_range = 100
        self.attack2_range = None
        self.attack3_range = None
        self.attack4_range = None
        self.attack1_movementtype = 0
        self.attack2_movementtype = None
        self.attack3_movementtype = None
        self.attack4_movementtype = None
        self.spells = None
        self.movement_type = 1
        self.speed = 1
        self.scale_multiplier = 1
        self.experience = 10
        self.gold = 1
        self.item_drop = ["Slime Ball"]
        self.itemdrop_chance = [10]
        self.health = 3
        # Default to face-right
        self.character_face_direction = LEFT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING * self.scale_multiplier

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.is_down = False

        self.right_state = 0
        self.left_state = 0
        self.up_state = 0
        self.down_state = 0

        self.animationset_left = []
        self.animationset_right = []
        self.animationset_up = []
        self.animationset_down = []
        self.animationset_attack1 = []
        self.animationset_attack2 = []
        self.animationset_attack3 = []
        self.animationset_attack4 = []

    def setup(self):
        print("In enemy setup")
        path = get_enemy(self.name)
        if path:
            get_properties(self, path)
        else:
            print("Failed to load enemy")
            sys.exit(0)
        load_animations(self, path)
        pass
    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.up_state]
            self.jumping = True

            self.set_hit_box([[-5, -32], [5, -32], [25, 10], [-25, 10]])

            if self.up_state == 7:
                pass
            else:
                self.up_state += 1
            return

        elif self.change_y < 0 and not self.jumping:
            self.texture = self.down_texture_pair[self.down_state]
            self.set_hit_box([[-30, -32], [19, -32], [20, -20], [0, -20]])
            if self.down_state == 7:
                pass
            else:
                self.down_state += 1
            return
        elif self.change_y < 0 and self.jumping:
            self.texture = self.fall_texture_pair[self.down_state]
            self.set_hit_box([[-5, -32], [5, -32], [25, 10], [-25, 10]])

            if self.down_state == 7:
                pass
            else:
                self.down_state += 1

        # Idle animation
        if self.change_x == 0:
            self.jumping = False
            self.right_state = 0
            self.left_state = 0
            self.up_state = 0
            self.down_state = 0
            self.cur_texture = 0
            self.is_down = False
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.set_hit_box([[-30, -32], [19, -32], [20, 10], [0, 0]])
            return

        # Walking animation
        self.cur_texture += 1

        if self.cur_texture > 7:
            self.cur_texture = 3
        if self.character_face_direction == LEFT_FACING:
            self.set_hit_box([[0, -32], [30, -32], [15, 10], [-10, 0]])
        elif self.character_face_direction == RIGHT_FACING:
            self.set_hit_box([[-30, -32], [19, -32], [20, 10], [0, 0]])

        self.texture = self.walk_textures[self.cur_texture][
            self.character_face_direction
        ]


def get_properties(enemy_object, enemy_path):
    properties = {}

    with open(enemy_path + "/" + "properties") as f:
        for line in f:
            print(line.split())
            (key, val) = line.split()
            properties[key] = val

    #  framesize_idle 32
    enemy_object.framesize_idle = int(properties["framesize_idle"])
    #  framesize_left 32
    enemy_object.framesize_left = int(properties["framesize_left"])
    #  framesize_right 32
    enemy_object.framesize_right = int(properties["framesize_right"])
    #  framesize_up None
    enemy_object.framesize_up = int(properties["framesize_up"])
    #  framesize_down None
    enemy_object.framesize_down = int(properties["framesize_down"])
    #  framesize_attack1 32
    enemy_object.framesize_attack1 = int(properties["framesize_attack1"])
    #  framesize_attack2 None
    enemy_object.framesize_attack2 = int(properties["framesize_attack2"])
    #  framesize_attack3 None
    enemy_object.framesize_attack3 = int(properties["framesize_attack3"])
    #  framesize_attack4 None
    enemy_object.framesize_attack4 = int(properties["framesize_attack4"])
    #  framelength_idle 4
    enemy_object.framelength_idle = int(properties["framelength_idle"])
    #  framelength_left 4
    enemy_object.framelength_left = int(properties["framelength_left"])
    #  framelength_right 4
    enemy_object.framelength_right = int(properties["framelength_right"])
    #  framelength_up None
    enemy_object.framelength_up = int(properties["framelength_up"])
    #  framelength_down None
    enemy_object.framelength_down = int(properties["framelength_down"])
    #  framelength_attack1 6
    enemy_object.framelength_attack1 = int(properties["framelength_attack1"])
    #  framelength_attack2 None
    enemy_object.framelength_attack2 = int(properties["framelength_attack2"])
    #  framelength_attack3 None
    enemy_object.framelength_attack3 = int(properties["framelength_attack3"])
    #  framelength_attack4 None
    enemy_object.framelength_attack4 = int(properties["framelength_attack4"])
    #  playbackspeed_idle 1
    enemy_object.playbackspeed_idle = int(properties["playbackspeed_idle"])
    #  playbackspeed_left 1
    enemy_object.playbackspeed_left = int(properties["playbackspeed_left"])
    #  playbackspeed_right 1
    enemy_object.playbackspeed_right = int(properties["playbackspeed_right"])
    #  playbackspeed_up None
    enemy_object.playbackspeed_up = int(properties["playbackspeed_up"])
    #  playbackspeed_down None
    enemy_object.playbackspeed_down = int(properties["playbackspeed_down"])
    #  playbackspeed_attack1
    enemy_object.playbackspeed_attack1 = int(properties["playbackspeed_attack1"])
    #  playbackspeed_attack2 None
    enemy_object.playbackspeed_attack2 = int(properties["playbackspeed_attack2"])
    #  playbackspeed_attack3 None
    enemy_object.playbackspeed_attack3 = int(properties["playbackspeed_attack3"])
    #  playbackspeed_attack4 None
    enemy_object.playbackspeed_attack4 = int(properties["playbackspeed_attack4"])
    #  hitbox_left [[-10,-10],[10,-10],[10,10],[-10,10]]
    enemy_object.hitbox_idle = ast.literal_eval(properties["hitbox_idle"])
    #  hitbox_left [[-10,-10],[10,-10],[10,10],[-10,10]]
    enemy_object.hitbox_left = ast.literal_eval(properties["hitbox_left"])
    #  hitbox_right [[-10,-10],[10,-10],[10,10],[-10,10]]
    enemy_object.hitbox_right = ast.literal_eval(properties["hitbox_right"])
    #  hitbox_up None
    enemy_object.hitbox_up = ast.literal_eval(properties["hitbox_up"])
    #  hitbox_down None
    enemy_object.hitbox_down = ast.literal_eval(properties["hitbox_down"])
    #  hitbox_attack1 [[-10,-10],[10,-10],[10,10],[-10,10]]
    enemy_object.hitbox_attack1 = ast.literal_eval(properties["hitbox_attack1"])
    #  hitbox_attack2 None
    enemy_object.hitbox_attack2 = ast.literal_eval(properties["hitbox_attack2"])
    #  hitbox_attack3 None
    enemy_object.hitbox_attack3 = ast.literal_eval(properties["hitbox_attack3"])
    #  hitbox_attack4 None
    enemy_object.hitbox_attack4 = ast.literal_eval(properties["hitbox_attack4"])
    #  attack1_damage 1
    enemy_object.attack1_damage = int(properties["attack1_damage"])
    #  attack2_damage None
    enemy_object.attack2_damage = int(properties["attack2_damage"])
    #  attack3_damage None
    enemy_object.attack3_damage = int(properties["attack3_damage"])
    #  attack4_damage None
    enemy_object.attack4_damage = int(properties["attack4_damage"])
    #  attack1_element normal
    enemy_object.attack1_element = properties["attack1_element"]
    #  attack2_element None
    enemy_object.attack2_element = properties["attack2_element"]
    #  attack3_element None
    enemy_object.attack3_element = properties["attack3_element"]
    #  attack4_element None
    enemy_object.attack4_element = properties["attack4_element"]
    #  attack1_frequency 1
    enemy_object.attack1_frequency = int(properties["attack1_frequency"])
    #  attack2_frequency None
    enemy_object.attack2_frequency = int(properties["attack2_frequency"])
    #  attack3_frequency None
    enemy_object.attack3_frequency = int(properties["attack3_frequency"])
    #  attack4_frequency None
    enemy_object.attack4_frequency = int(properties["attack4_frequency"])
    #  attack1_range 100
    enemy_object.attack1_range = int(properties["attack1_range"])
    #  attack2_range None
    enemy_object.attack2_range = int(properties["attack2_range"])
    #  attack3_range None
    enemy_object.attack3_range = int(properties["attack3_range"])
    #  attack4_range None
    enemy_object.attack4_range = int(properties["attack4_range"])
    #  attack1_movementtype 0
    enemy_object.attack1_movementtype = int(properties["attack1_movementtype"])
    #  attack2_movementtype None
    enemy_object.attack2_movementtype = int(properties["attack2_movementtype"])
    #  attack3_movementtype None
    enemy_object.attack3_movementtype = int(properties["attack3_movementtype"])
    #  attack4_movementtype None
    enemy_object.attack4_movementtype = int(properties["attack4_movementtype"])
    #  spells None
    enemy_object.spells = ast.literal_eval(properties["spells"])
    #  movement_type 0
    enemy_object.movement_type = int(properties["movement_type"])
    #speed 1
    enemy_object.speed = int(properties["movement_type"])
    #scale_multiplier 2
    enemy_object.scale_multiplier = int(properties["scale_multiplier"])
    #  experience 10
    enemy_object.experience = int(properties["experience"])
    #  gold 1
    enemy_object.gold = int(properties["gold"])
    #  item_drop ["Slime Ball"]
    enemy_object.item_drop = ast.literal_eval(properties["item_drop"])
    #  itemdrop_chance [10]
    enemy_object.itemdrop_chance = ast.literal_eval(properties["itemdrop_chance"])
    #  health 3
    enemy_object.health = int(properties["health"])
    pass

def load_animations(enemy_object, enemy_path):
    if enemy_object.framelength_idle:
        enemy_object.animationset_idle = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_idle.png", enemy_object.framesize_left, enemy_object.framesize_idle, enemy_object.framelength_idle, enemy_object.framelength_idle)
    else:
        pass
    if enemy_object.framelength_left:
        enemy_object.animationset_left = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_left.png", enemy_object.framesize_left, enemy_object.framesize_left, enemy_object.framelength_left, enemy_object.framelength_left)
    else:
        pass
    if enemy_object.framelength_right:
        enemy_object.animationset_right = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_right.png", enemy_object.framesize_right, enemy_object.framesize_right, enemy_object.framelength_right, enemy_object.framelength_right)
    else:
        pass
    if enemy_object.framelength_up:
        enemy_object.animationset_up = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_up.png", enemy_object.framesize_up, enemy_object.framesize_up, enemy_object.framelength_up, enemy_object.framelength_up)
    else:
        pass
    if enemy_object.framelength_down:
        enemy_object.animationset_down = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_down.png", enemy_object.framesize_down, enemy_object.framesize_down, enemy_object.framelength_down, enemy_object.framelength_down)
    else:
        pass
    if enemy_object.framelength_attack1:
        enemy_object.animationset_attack1 = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_attack1.png", enemy_object.framesize_attack1, enemy_object.framesize_attack1, enemy_object.framelength_attack1, enemy_object.framelength_attack1)
    else:
        pass
    if enemy_object.framelength_attack2:
        enemy_object.animationset_attack2 = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_attack2.png", enemy_object.framesize_attack2, enemy_object.framesize_attack2, enemy_object.framelength_attack2, enemy_object.framelength_attack2)
    else:
        pass
    if enemy_object.framelength_attack3:
        enemy_object.animationset_attack3 = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_attack3.png", enemy_object.framesize_attack3, enemy_object.framesize_attack3, enemy_object.framelength_attack3, enemy_object.framelength_attack3)
    else:
        pass
    if enemy_object.framelength_attack4:
        enemy_object.animationset_attack4 = arcade.load_spritesheet(enemy_path+"/"+enemy_object.name+"_attack4.png", enemy_object.framesize_attack4, enemy_object.framesize_attack4, enemy_object.framelength_attack4, enemy_object.framelength_attack4)
    else:
        pass
    pass
    enemy_object.texture = enemy_object.animationset_idle[0]
# See if the spell exists
def get_enemy(enemy_name):
    enemy_path = ""

    for dirname, dirnames, filenames in os.walk("./enemies/"):
        for subdirname in dirnames:
            if enemy_name in subdirname:
                # print(os.path.join(dirname, subdirname))
                enemy_path = os.path.join(dirname, subdirname)
    if enemy_path:
        print(enemy_path)
        return enemy_path
    else:
        print("\n\n\n\nIn get_enemy\n\n\n\n")
        return False