#! /usr/bin/python3
import arcade
import os
from spells import *
from battle import *
from pyglet.gl import GL_NEAREST
from pyglet.gl import GL_LINEAR

# Constants used to scale our sprites from their original size
TILE_SCALING = 1
CHARACTER_SCALING = TILE_SCALING
ITEM_SCALING = TILE_SCALING * 0.75
SPRITE_PIXEL_SIZE = 32
GRID_PIXEL_SIZE = 32  #(SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 3

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.

LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100


PLAYER_START_X = 32 #SPRITE_PIXEL_SIZE * TILE_SCALING * 2
PLAYER_START_Y = 96  #(SPRITE_PIXEL_SIZE * TILE_SCALING * 1) - 200



# Constants used to track if the player is facing left or right

RIGHT_FACING = 0
LEFT_FACING = 1
UP_FACING = 2
DOWN_FACING = 3
FACE_DIRECTION = [RIGHT_FACING, LEFT_FACING, UP_FACING, DOWN_FACING]

def load_texture_pair(filename):
  return [
      arcade.load_texture(filename),
      arcade.load_texture(filename, mirrored=True)]

def load_seperate_texture_pair(filename1, filename2):
  pass



class PlayerCharacter(arcade.Sprite):


  def __init__(self):
    # Set up parent class
    super().__init__()

    # Default to face-right
    self.character_face_direction = RIGHT_FACING

    # Used for flipping between image sequences
    self.cur_texture = 0
    self.scale = CHARACTER_SCALING
    self.last_coordinates = []

    # Track our state
    self.jumping = False
    self.climbing = False
    self.is_on_ladder = False
    self.is_down = False

    self.right_state = 0
    self.left_state = 0
    self.up_state = 0
    self.down_state = 0

    #0.75 of a second
    self.PLAYER_ANIMATION_SPEED = 0.5
    self.PLAYER_WALKING_ANIMATION_SPEED = 0.25 * self.PLAYER_ANIMATION_SPEED
    #Keep track for frame updates for characters
    self.GLOBAL_DELTA_TIME = 0

    # --- Load Textures ---
#    self.all_textures      = arcade.load_spritesheet("../assets/images/world_jorge/world_jorge{i}.png",32,32,2,2)

    # Load textures for walking
    self.walk_textures_right = []
    self.walk_textures_left = []
    self.walk_textures_down = []
    self.walk_textures_up = []
    #Get the right facing walk textures
    for i in range(2):
      texture = arcade.load_texture(f"../assets/images/world_jorge/world_jorge_{i}.png")
      self.walk_textures_right.append(texture)
    #Left facing textures, textures 2 and 3
    for i in range(2,4):
      texture = arcade.load_texture(f"../assets/images/world_jorge/world_jorge_{i}.png")
      self.walk_textures_left.append(texture)
    #Down facing textures
    for i in range(4,6):
      texture = arcade.load_texture(f"../assets/images/world_jorge/world_jorge_{i}.png")
      self.walk_textures_down.append(texture)
    #Up facing textures
    for i in range(6,8):
      texture = arcade.load_texture(f"../assets/images/world_jorge/world_jorge_{i}.png")
      self.walk_textures_up.append(texture)


    # Set the initial texture
    self.texture = self.walk_textures_right[0]

    # Hit box will be set based on the first image used. If you want to specify
    # a different hit box, you can do it like the code below.
    #Bottom_Left, Bottom_Right, Top_Right, Top_Left
    #(x1, y1), (x2, y2), (x3, y3), (x4, y4)
    self.set_hit_box([[-16,-16], [10,-16], [10,10], [-16,10]])
    #self.set_hit_box(self.texture.hit_box_points)
    self.walking_sound = arcade.load_sound("../assets/music/walk.wav")

  def update_animation(self, delta_time):
    self.GLOBAL_DELTA_TIME += delta_time
    is_idle = False
    #arcade.play_sound(self.walking_sound)
    change_x = 0
    change_y = 0
    if self.center_x < self.last_coordinates[0]:
      self.character_face_direction = LEFT_FACING
      change_x = -1
    elif self.center_x > self.last_coordinates[0]:
      self.character_face_direction = RIGHT_FACING
      change_x = 1
    elif self.center_y < self.last_coordinates[1]:
      self.character_face_direction = DOWN_FACING
      change_y = -1
    elif self.center_y > self.last_coordinates[1]:
      self.character_face_direction = UP_FACING
      change_y = 1
    else:
      change_x = 0
      change_y = 0
      is_idle = True


    if self.GLOBAL_DELTA_TIME > 1:
      self.GLOBAL_DELTA_TIME = 0


    if (self.GLOBAL_DELTA_TIME > self.PLAYER_WALKING_ANIMATION_SPEED) and not is_idle:
      arcade.play_sound(self.walking_sound)
      self.cur_texture += 1
      self.GLOBAL_DELTA_TIME = 0
      if self.cur_texture > 1:
        self.cur_texture = 0

    elif self.GLOBAL_DELTA_TIME > self.PLAYER_ANIMATION_SPEED:
      self.cur_texture += 1
      self.GLOBAL_DELTA_TIME = 0
      if self.cur_texture > 1:
        self.cur_texture = 0

    if change_y > 0:
      self.texture = self.walk_textures_up[self.cur_texture]
      return
    elif change_y < 0:
      self.texture = self.walk_textures_down[self.cur_texture]
      return
    # Idle animation
    if change_x == 0:
      self.right_state = 0
      self.left_state = 0
      self.up_state = 0
      self.down_state = 0
      self.is_down = False
      self.texture = self.walk_textures_right[self.cur_texture]
      return

    # Walking animation
    if self.character_face_direction == LEFT_FACING:
      self.texture = self.walk_textures_left[self.cur_texture]
    elif self.character_face_direction == RIGHT_FACING:
      self.texture = self.walk_textures_right[self.cur_texture]
    return

class World(arcade.View):

  def __init__(self):

    # Call the parent class and set up the window
    super().__init__()

    # Set the path to start with this program
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)

    # Track the current state of what key is pressed
    self.left_pressed = False
    self.right_pressed = False
    self.up_pressed = False
    self.down_pressed = False
    self.jump_needs_reset = False

    # These are 'lists' that keep track of our sprites. Each sprite should
    # go into a list.
    self.item_list = None
    self.wall_list = None
    self.background_list = None
    self.ladder_list = None
    self.player_list = None

    # Separate variable that holds the player sprite
    self.player_sprite = None

    # Our 'physics' engine
    self.physics_engine = None

    # Used to keep track of our scrolling
    self.view_bottom = 0
    self.view_left = 0
    self.end_of_map = 0

    # Keep track of the score
    self.score = 0

    # Load sounds

  def setup(self):

    # Used to keep track of our scrolling
    self.view_bottom = 0
    self.view_left = 0

    # Keep track of the score
    self.score = 0
    self.command_buffer = ""
    # Create the Sprite lists
    self.player_list = arcade.SpriteList()
    self.background_list = arcade.SpriteList()
    self.wall_list = arcade.SpriteList()
    self.enemy_list = arcade.SpriteList()
    # Set up the player, specifically placing it at these coordinates.
    self.player_sprite = PlayerCharacter()

    self.player_sprite.center_x = PLAYER_START_X
    self.player_sprite.center_y = PLAYER_START_Y
    self.player_list.append(self.player_sprite)

    # --- Load in a map from the tiled editor ---

    # Name of the layer in the file that has our platforms/walls
    platforms_layer_name = 'Platforms'
    moving_platforms_layer_name = 'Moving Platforms'

    # Name of the layer that has items for pick-up
    item_layer_name = 'Items'

    # Map name
    #map_name = f":resources:tmx_maps/map_with_ladders.tmx"
    map_name = "../assets/images/Jorges_Adventure_world.tmx"

    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(map_name)

    # Calculate the right edge of the my_map in pixels
    self.end_of_map = 32000  #my_map.map_size.width * GRID_PIXEL_SIZE

    # -- Platforms
    self.wall_list = arcade.tilemap.process_layer(my_map, "Collision", TILE_SCALING)

    # -- Enemies
    self.enemy_list = arcade.tilemap.process_layer(my_map, "Enemy", TILE_SCALING)

    # -- Moving Platforms
    moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer_name, TILE_SCALING)
    for sprite in moving_platforms_list:
      self.wall_list.append(sprite)

    # -- Background objects
    self.background_list = arcade.tilemap.process_layer(my_map, "Floor", TILE_SCALING)
    self.background_list2 = arcade.tilemap.process_layer(my_map, "Floor2", TILE_SCALING)
    # -- Background objects
    #self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders", TILE_SCALING)
    # -- Coins
    #self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALING)

    # --- Other stuff
    # Set the background color
    if my_map.background_color:
      arcade.set_background_color(my_map.background_color)

    # Create the 'physics engine'
    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)



  def on_draw(self):
    # Clear the screen to the background color
    arcade.start_render()

    # Draw our sprites
    self.background_list.draw(filter=GL_NEAREST)
    self.background_list2.draw(filter=GL_NEAREST)
    self.wall_list.draw(filter=GL_NEAREST)
    #self.ladder_list.draw()
    #self.coin_list.draw()
    self.player_list.draw(filter=GL_NEAREST)
    self.enemy_list.draw(filter=GL_NEAREST)
    # Draw our score on the screen, scrolling it with the viewport
    #arcade.draw_text(self.command_buffer, 32, 60, arcade.csscolor.GREY, 18, 0, "left", ('calibre','arial') )

    # Draw hit boxes.
    #for wall in self.wall_list:
    #    wall.draw_hit_box(arcade.color.BLACK, 3)
    #self.player_sprite.draw_hit_box(arcade.color.RED, 3)



  def process_keychange(self):
    self.player_sprite.last_coordinates = [self.player_sprite.center_x, self.player_sprite.center_y]
    if self.up_pressed:
#      self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
      self.player_sprite.change_x = 0
      self.player_sprite.center_y += 2
    if self.down_pressed:
#      self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
      self.player_sprite.change_x = 0
      self.player_sprite.center_y -= 2

    if self.right_pressed:
#      self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
      self.player_sprite.change_y = 0
      self.player_sprite.center_x += 2
    if self.left_pressed:
#      self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
      self.player_sprite.change_y = 0
      self.player_sprite.center_x -= 2

    else:
      self.player_sprite.change_x = 0
      self.player_sprite.change_y = 0

  def on_key_press(self, key, modifiers):
    if key == arcade.key.UP:
      self.up_pressed = True

    elif key == arcade.key.DOWN:
      self.down_pressed = True

    elif key == arcade.key.LEFT:
      self.left_pressed = True

    elif key == arcade.key.RIGHT:
      self.right_pressed = True

    self.process_keychange()

  def on_key_release(self, key, modifiers):
    if key == arcade.key.UP:
      self.up_pressed = False

    elif key == arcade.key.DOWN:
      self.down_pressed = False

    elif key == arcade.key.LEFT:
      self.left_pressed = False

    elif key == arcade.key.RIGHT:
      self.right_pressed = False

    self.process_keychange()

  def on_update(self, delta_time):
    # Move the player with the physics engine
    self.physics_engine.update()

    # Update animations
    self.process_keychange()

    #self.item_list.update_animation(delta_time)
    self.background_list.update_animation(delta_time)
    self.player_list.update_animation(delta_time)

    # Update walls, used with moving platforms
#    self.wall_list.update()
    # See if the moving wall hit a boundary and needs to reverse direction.

#    for wall in self.wall_list:
#      if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
#        wall.change_x *= -1

#      if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
#        wall.change_x *= -1

#      if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
#        wall.change_y *= -1

#      if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
#        wall.change_y *= -1



    # See if we hit any coins
    enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)

    # Loop through each enemy we hit (if any) and battle it
    for enemy in enemy_hit_list:
      current_battle = Battle()
      print(enemy.properties)
      current_battle.setup(enemy.properties["name"])
      self.window.show_view(current_battle)
      # Figure out how many points this coin is worth
    #  if 'Points' not in coin.properties:
    #    print("Warning, collected a coin without a Points property.")

    #  else:
    #    points = int(coin.properties['Points'])
    #    self.score += points

      # Remove the coin
    #  coin.remove_from_sprite_lists()
      #arcade.play_sound(self.collect_coin_sound)



    # Track if we need to change the viewport
    changed_viewport = False

    # --- Manage Scrolling ---

    # Scroll left
    left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN

    if self.player_sprite.left < left_boundary:
      self.view_left -= left_boundary - self.player_sprite.left
      changed_viewport = True

    # Scroll right
    right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN

    if self.player_sprite.right > right_boundary:
      self.view_left += self.player_sprite.right - right_boundary
      changed_viewport = True

    # Scroll up
    top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
    if self.player_sprite.top > top_boundary:
      self.view_bottom += self.player_sprite.top - top_boundary
      changed_viewport = True

    # Scroll down
    bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
    if self.player_sprite.bottom < bottom_boundary:
      self.view_bottom -= bottom_boundary - self.player_sprite.bottom
      changed_viewport = True

    if changed_viewport:
      # Only scroll to integers. Otherwise we end up with pixels that
      # don't line up on the screen
      self.view_bottom = int(self.view_bottom)
      self.view_left = int(self.view_left)

      # Do the scrolling
      arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)
