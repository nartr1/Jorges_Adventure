#! /usr/bin/python3
import arcade
import os

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



    # Track our state
    self.jumping = False
    self.climbing = False
    self.is_on_ladder = False

    self.right_state = 0
    self.left_state = 0
    self.up_state = 0
    self.down_state = 0




    # --- Load Textures ---
    # Images from Kenney.nl's Asset Pack 3
    # main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
    # main_path = ":resources:images/animated_characters/female_person/femalePerson"
    main_path = ":resources:images/animated_characters/male_person/malePerson"

    # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
    # main_path = ":resources:images/animated_characters/zombie/zombie"
    # main_path = ":resources:images/animated_characters/robot/robot"


    # Load textures for idle standing
    self.idle_texture_pair = arcade.load_spritesheet("../assets/images/Jorge_HIDEF_Right.png",64,64,2,2)
    self.jump_texture_pair = arcade.load_spritesheet("../assets/images/Jorge_HIDEF_Jump.png",64,64,8,8)
    self.down_texture_pair = arcade.load_spritesheet("../assets/images/Jorge_HIDEF_Down.png",64,64,8,8)
    self.fall_texture_pair = arcade.load_spritesheet("../assets/images/Jorge_HIDEF_Fall.png",64,64,8,8)


      # Load textures for walking
    self.walk_textures = []
    textures1 = arcade.load_spritesheet("../assets/images/Jorge_HIDEF_Right.png",64,64,8,8)
    textures2 = arcade.load_spritesheet("../assets/images/Jorge_HIDEF_Left.png",64,64,8,8)
    for i in range(8):
#      texture = load_texture_pair(f"{main_path}_walk{i}.png")
      self.walk_textures.append([textures1[i], textures2[i]])


    # Load textures for climbing
    self.climbing_textures = []
    texture = arcade.load_texture(f"{main_path}_climb0.png")
    self.climbing_textures.append(texture)
    texture = arcade.load_texture(f"{main_path}_climb1.png")
    self.climbing_textures.append(texture)



    # Set the initial texture
    self.texture = self.idle_texture_pair[0]

    # Hit box will be set based on the first image used. If you want to specify
    # a different hit box, you can do it like the code below.
    #Bottom_Left, Bottom_Right, Top_Right, Top_Left
    #(x1, y1), (x2, y2), (x3, y3), (x4, y4)
    self.set_hit_box([[-30, -32], [19, -32], [20,10], [0, 0]])
    #self.set_hit_box([[-30, -32], [19, -32], [20, 16], [-30, 0]])
    #self.set_hit_box(self.texture.hit_box_points)



  def update_animation(self, delta_time: float = 1/60):

    # Figure out if we need to flip face left or right
    if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
      self.character_face_direction = LEFT_FACING

    elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
      self.character_face_direction = RIGHT_FACING


    if self.change_y > 0:
      self.texture = self.jump_texture_pair[self.up_state]
      self.jumping = True
      if self.up_state == 7:
        pass
      else:
        self.up_state += 1
      return

    elif self.change_y < 0 and not self.jumping:
      self.texture = self.fall_texture_pair[self.down_state]
      if self.down_state == 7:
        pass
      else:
        self.down_state += 1
      return
    elif self.change_y < 0 and self.jumping:
      self.texture = self.down_texture_pair[self.down_state]
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
      self.texture = self.idle_texture_pair[self.character_face_direction]
      return

    # Walking animation
    self.cur_texture += 1

    if self.cur_texture > 7:
      self.cur_texture = 3

    self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]



class MyGame(arcade.Window):

  def __init__(self):

    # Call the parent class and set up the window
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

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
    self.coin_list = None
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
    self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
    self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
    self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")



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
    self.coin_list = arcade.SpriteList()

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
    coins_layer_name = 'Coins'

    # Map name
    #map_name = f":resources:tmx_maps/map_with_ladders.tmx"
    map_name = "../assets/images/jorges_adventure_map_testing.tmx"

    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(map_name)

    # Calculate the right edge of the my_map in pixels
    self.end_of_map = 48 * 33  #my_map.map_size.width * GRID_PIXEL_SIZE

    # -- Platforms
    self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)


    # -- Moving Platforms
    moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer_name, TILE_SCALING)
    for sprite in moving_platforms_list:
      self.wall_list.append(sprite)

    # -- Background objects
    self.background_list = arcade.tilemap.process_layer(my_map, "Background", TILE_SCALING)
    # -- Background objects
    self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders", TILE_SCALING)
    # -- Coins
    self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALING)

    # --- Other stuff
    # Set the background color
    if my_map.background_color:
      arcade.set_background_color(my_map.background_color)

    # Create the 'physics engine'
    self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY, ladders=self.ladder_list)



  def on_draw(self):
    # Clear the screen to the background color
    arcade.start_render()



    # Draw our sprites
    self.wall_list.draw()
    self.background_list.draw()
    self.ladder_list.draw()
    self.coin_list.draw()
    self.player_list.draw()

    # Draw our score on the screen, scrolling it with the viewport
    score_text = f"Score: {self.score}"
    arcade.draw_text(self.command_buffer, 32, 60, arcade.csscolor.GREY, 18, 0, "left", ('calibre','arial') )



    # Draw hit boxes.

    # for wall in self.wall_list:

    #     wall.draw_hit_box(arcade.color.BLACK, 3)

    #

    self.player_sprite.draw_hit_box(arcade.color.RED, 3)



  def process_keychange(self):
    # Process up/down
    if self.up_pressed and not self.down_pressed:
#      if self.physics_engine.is_on_ladder():
      self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED

#    elif self.physics_engine.can_jump() and not self.jump_needs_reset:
#      self.player_sprite.change_y = PLAYER_JUMP_SPEED
#      self.jump_needs_reset = True
      #arcade.play_sound(self.jump_sound)

    elif self.down_pressed and not self.up_pressed:
#      if self.physics_engine.is_on_ladder():
      self.player_sprite.change_y = -(PLAYER_MOVEMENT_SPEED+10)

    # Process up/down when on a ladder and no movement
#    if self.physics_engine.is_on_ladder():
#      if not self.up_pressed and not self.down_pressed:
#        self.player_sprite.change_y = 0
#      elif self.up_pressed and self.down_pressed:
#        self.player_sprite.change_y = 0

    # Process left/right
    if self.right_pressed and not self.left_pressed:
      self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
    elif self.left_pressed and not self.right_pressed:
      self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
    else:
      self.player_sprite.change_x = 0

  def on_key_press(self, key, modifiers):
    if key == arcade.key.UP:
      self.up_pressed = True

    elif key == arcade.key.DOWN:
      self.down_pressed = True

    elif key == arcade.key.LEFT:
      self.left_pressed = True

    elif key == arcade.key.RIGHT:
      self.right_pressed = True

    if (key == arcade.key.A):
      self.command_buffer += "A"

    if (key == arcade.key.B):
      self.command_buffer += "B"

    if (key == arcade.key.C):
      self.command_buffer += "C"

    if (key == arcade.key.D):
      self.command_buffer += "D"

    if (key == arcade.key.E):
      self.command_buffer += "E"

    if (key == arcade.key.F):
      self.command_buffer += "F"

    if (key == arcade.key.G):
      self.command_buffer += "G"

    if (key == arcade.key.H):
      self.command_buffer += "H"

    if (key == arcade.key.I):
      self.command_buffer += "I"

    if (key == arcade.key.J):
      self.command_buffer += "J"

    if (key == arcade.key.K):
      self.command_buffer += "K"

    if (key == arcade.key.L):
      self.command_buffer += "L"

    if (key == arcade.key.M):
      self.command_buffer += "M"

    if (key == arcade.key.N):
      self.command_buffer += "N"

    if (key == arcade.key.O):
      self.command_buffer += "O"

    if (key == arcade.key.P):
      self.command_buffer += "P"

    if (key == arcade.key.Q):
      self.command_buffer += "Q"

    if (key == arcade.key.R):
      self.command_buffer += "R"

    if (key == arcade.key.S):
      self.command_buffer += "S"

    if (key == arcade.key.T):
      self.command_buffer += "T"

    if (key == arcade.key.U):
      self.command_buffer += "U"

    if (key == arcade.key.V):
      self.command_buffer += "V"

    if (key == arcade.key.W):
      self.command_buffer += "W"

    if (key == arcade.key.X):
      self.command_buffer += "X"

    if (key == arcade.key.Y):
      self.command_buffer += "Y"

    if (key == arcade.key.Z):
      self.command_buffer += "Z"

    if(key == arcade.key.SPACE):
      self.command_buffer += ' '

    if (key == arcade.key.BACKSPACE) and (self.command_buffer):
      self.command_buffer = self.command_buffer[:-1]

    if len(self.command_buffer) > 50:
      self.command_buffer = self.command_buffer[0:50]

    self.process_keychange()

  def on_key_release(self, key, modifiers):
    if key == arcade.key.UP:
      self.up_pressed = False
      self.jump_needs_reset = False

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
    if self.physics_engine.can_jump():
      self.player_sprite.can_jump = False

    else:
      self.player_sprite.can_jump = True

    if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
      self.player_sprite.is_on_ladder = True
      self.process_keychange()

    else:
      self.player_sprite.is_on_ladder = False
    self.process_keychange()



    self.coin_list.update_animation(delta_time)
    self.background_list.update_animation(delta_time)
    self.player_list.update_animation(delta_time)

    # Update walls, used with moving platforms
    self.wall_list.update()
    # See if the moving wall hit a boundary and needs to reverse direction.

    for wall in self.wall_list:
      if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
        wall.change_x *= -1

      if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
        wall.change_x *= -1

      if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
        wall.change_y *= -1

      if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
        wall.change_y *= -1



    # See if we hit any coins
    coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

    # Loop through each coin we hit (if any) and remove it
    for coin in coin_hit_list:
      # Figure out how many points this coin is worth
      if 'Points' not in coin.properties:
        print("Warning, collected a coin without a Points property.")

      else:
        points = int(coin.properties['Points'])
        self.score += points



      # Remove the coin
      coin.remove_from_sprite_lists()
      #arcade.play_sound(self.collect_coin_sound)



    # Track if we need to change the viewport
    changed_viewport = False

    # --- Manage Scrolling ---

    # Scroll left
#    left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN

#    if self.player_sprite.left < left_boundary:
#      self.view_left -= left_boundary - self.player_sprite.left
#      changed_viewport = True

    # Scroll right
#    right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN

#    if self.player_sprite.right > right_boundary:
#      self.view_left += self.player_sprite.right - right_boundary
#      changed_viewport = True

    # Scroll up
#    top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
#    if self.player_sprite.top > top_boundary:
#      self.view_bottom += self.player_sprite.top - top_boundary
#      changed_viewport = True

    # Scroll down
#    bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
#    if self.player_sprite.bottom < bottom_boundary:
#      self.view_bottom -= bottom_boundary - self.player_sprite.bottom
#      changed_viewport = True

#    if changed_viewport:
      # Only scroll to integers. Otherwise we end up with pixels that
      # don't line up on the screen
#      self.view_bottom = int(self.view_bottom)
#      self.view_left = int(self.view_left)

      # Do the scrolling
#      arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)




def main():
  window = MyGame()
  window.setup()
  arcade.run()


if __name__ == "__main__":
  main()
