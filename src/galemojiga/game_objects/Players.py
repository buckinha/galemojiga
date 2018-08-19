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
            self.position = [globals.MAIN_WINDOW_SIZE[0]/2, globals.MAIN_WINDOW_SIZE[1]-55]
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
        self.health = 4000
        self.special_ammo = 0
        self.special_type = globals.SPECIAL_TYPES['NONE']
        self.image = 'p{}_ship'.format(self.number)
        self.bullet_image = 'p{}_bullet'.format(self.number)
        self.firing = False
        self.firing_special = False
        self.size=[19,45]
        self.hit_offset= [18, 5]
        self.powerup = None


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
        self.position[0] += (self.speed_right - self.speed_left)
        self.position[1] += (self.speed_down - self.speed_up)

        if self.position[0] < 0:
            self.position[0] = 0

        if self.position[0] >= globals.MAIN_WINDOW_SIZE[0] - 55:
            self.position[0] = globals.MAIN_WINDOW_SIZE[0] - 55

        if self.position[1] <= 0:
            self.position[1] = 0

        if self.position[1] >= globals.MAIN_WINDOW_SIZE[1] - 55:
            self.position[1]= globals.MAIN_WINDOW_SIZE[1] - 55

    def fire(self, input_dict):
        self.process_firing_keys(input_dict)
        now = time.time()
        time_since_last_shot = now - self.last_shot_time
        if time_since_last_shot >= globals.FIRE_DELAY:
            if self.firing is True:
                bullet = Bullet(game_context=self.game_context,
                                position=[self.position[0]+22,self.position[1]],
                                speed=globals.PLAYER_GUN_1_SPEED ,
                                launched_by=self.number,
                                strength=1, image=self.bullet_image)
                self.game_context.bullets.append(bullet)
                self.last_shot_time = now

    def update(self, input_dict):
        self.move(input_dict)
        self.fire(input_dict)

    def hit_by(self, enemy_or_bullet):
        if type(enemy_or_bullet) is Bullet:
            self.health -= enemy_or_bullet.strength
            if self.health <= 0:
                self.game_context.trigger_game_over()

    def gain_powerup(self, powerup_obj):
        self.powerup = powerup_obj