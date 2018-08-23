import time
from galemojiga.game_objects.GameObject import GameObject
from galemojiga.game_objects.Bullets import Bullet
import galemojiga.globals as globals


class MovementKeys:
    def __init__(self, player_number):
        if player_number == 1:
            self.keys = globals.P1_MOVEMENT_KEYS
        elif player_number == 2:
            self.keys = globals.P2_MOVEMENT_KEYS
        elif player_number == 3:
            self.keys = globals.P3_MOVEMENT_KEYS
        else:
            self.keys = globals.P3_MOVEMENT_KEYS

    @property
    def up(self):
        return self.keys[0]

    @property
    def down(self):
        return self.keys[1]

    @property
    def left(self):
        return self.keys[2]

    @property
    def right(self):
        return self.keys[3]


class Player(GameObject):
    def __init__(self, game_context, number, movement_keys, position=None):
        super().__init__()
        if position is None:
            self.position = [globals.H_MIDDLE, globals.FLOOR - 40]
        else:
            self.position = [position[0], position[1]]

        self.game_context = game_context
        self.number = number
        self.movement_key_list = movement_keys
        self.speed_right = 0
        self.speed_left = 0
        self.speed_up = 0
        self.speed_down = 0
        self.speed_horizontal_magnitude = 4
        self.speed_vertical_magnitude = 0
        self.last_shot_time = 0
        self.health = 4
        self.max_health = 5
        self.special_ammo = 0
        self.special_type = globals.SPECIAL_TYPES['NONE']
        self.frame_list = ['p{}_ship'.format(self.number)]
        self.bullet_image = 'p{}_bullet'.format(self.number)
        self.firing = False
        self.firing_special = False
        self.fire_delay = globals.FIRE_DELAY
        self.size=[19,45]
        self.hit_offset= [18, 5]

        self.powerup = None
        self.base_bullet_str = 1
        if self.difficulty == 1:
            self.power_factor = 2
        elif self.difficulty == 2:
            self.power_factor = 1
        else:
            self.power_factor = 0.5


    @property
    def difficulty(self):
        return self.game_context.game_master.difficulty

    def process_movement_keys(self, input_dict):
        if self.movement_key_list is None:
            return

        # key ups (cancel motion in that direction
        if self.movement_key_list.up in input_dict['key_up']:
            self.speed_up = 0
        elif self.movement_key_list.down in input_dict['key_up']:
            self.speed_down = 0

        if self.movement_key_list.left in input_dict['key_up']:
            self.speed_left = 0
        elif self.movement_key_list.right in input_dict['key_up']:
            self.speed_right = 0

        # key downs (start motion in that direction, and ignore key ups)
        if self.movement_key_list.up in input_dict['key_down']:
            self.speed_up = self.speed_vertical_magnitude
        elif self.movement_key_list.down in input_dict['key_down']:
            self.speed_down = self.speed_vertical_magnitude

        if self.movement_key_list.left in input_dict['key_down']:
            self.speed_left = self.speed_horizontal_magnitude
        elif self.movement_key_list.right in input_dict['key_down']:
            self.speed_right = self.speed_horizontal_magnitude

    def process_firing_keys(self, input_dict):
        # in galemojiga, you can't move up and down, so i'm using those keys
        # for the two firing commands
        if self.movement_key_list.up in input_dict['key_up']:
            self.firing = False

        if self.movement_key_list.up in input_dict['key_down']:
            self.firing = True

        if self.movement_key_list.down in input_dict['key_down']:
            self.firing_special = True

    def move(self, input_dict):
        self.process_movement_keys(input_dict)
        self.x += (self.speed_right - self.speed_left)
        self.y += (self.speed_down - self.speed_up)

        if self.x < globals.LEFT_WALL:
            self.x = globals.LEFT_WALL

        if self.x + self.size[0] >= globals.RIGHT_WALL:
            self.x = globals.RIGHT_WALL - self.size[0]

        if self.y <= globals.CEILING:
            self.y = globals.CEILING

        if self.y + self.size[1] >= globals.FLOOR:
            self.y = globals.FLOOR - self.size[1]

    def fire(self, input_dict):
        self.process_firing_keys(input_dict)
        now = time.time()
        time_since_last_shot = now - self.last_shot_time
        if time_since_last_shot >= self.fire_delay:
            if self.firing is True:
                bullet = Bullet(game_context=self.game_context,
                                position=[self.x+22, self.y],
                                speed=globals.PLAYER_GUN_1_SPEED ,
                                launched_by=self.number,
                                strength=self.base_bullet_str*self.power_factor,
                                image=self.bullet_image)
                self.game_context.bullets.append(bullet)
                self.last_shot_time = now

    def update(self, input_dict):
        self.move(input_dict)
        self.fire(input_dict)

    def hit_by(self, enemy_or_bullet):
        if hasattr(enemy_or_bullet, 'strength'):
            self.health -= enemy_or_bullet.strength
            if self.health <= 0:
                self.game_context.trigger_game_over()


    def gain_powerup(self, powerup_obj):
        self.powerup = powerup_obj