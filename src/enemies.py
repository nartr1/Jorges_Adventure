#! /usr/bin/python3


class EnemyCharacter(arcade.Sprite):
    # Carbon copy of the player class for testing

    def __init__(self):
        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = LEFT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.is_down = False

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
        self.idle_texture_pair = arcade.load_spritesheet(
            "../assets/images/Jorge_HIDEF_Right.png", 64, 64, 2, 2
        )
        self.jump_texture_pair = arcade.load_spritesheet(
            "../assets/images/Jorge_HIDEF_Jump.png", 64, 64, 8, 8
        )
        self.down_texture_pair = arcade.load_spritesheet(
            "../assets/images/Jorge_HIDEF_Down.png", 64, 64, 8, 8
        )
        self.fall_texture_pair = arcade.load_spritesheet(
            "../assets/images/Jorge_HIDEF_Fall.png", 64, 64, 8, 8
        )

        # Load textures for walking
        self.walk_textures = []
        textures1 = arcade.load_spritesheet(
            "../assets/images/Jorge_HIDEF_Right.png", 64, 64, 8, 8
        )
        textures2 = arcade.load_spritesheet(
            "../assets/images/Jorge_HIDEF_Left.png", 64, 64, 8, 8
        )
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
        # Bottom_Left, Bottom_Right, Top_Right, Top_Left
        # (x1, y1), (x2, y2), (x3, y3), (x4, y4)
        # self.set_hit_box([[-30, -32], [19, -32], [20, 16], [-30, 0]])
        # self.set_hit_box(self.texture.hit_box_points)

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
