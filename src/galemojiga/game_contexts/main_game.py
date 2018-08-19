import time
import pygame
from pygame.locals import *
from galemojiga.GameContext import GameContext
from galemojiga.GameObject import GameObject, Bullet
from galemojiga.game_contexts.levels import Level1, Level2
import galemojiga.SpriteHelpers as sprites
import galemojiga.game_contexts.enemies as enemies
import galemojiga.colors as colors
import galemojiga.globals as globals

MAX_PLAYERS = 3

FIRE_DELAY = 0.25

P1_MOVEMENT_KEYS = [K_w, K_s, K_a, K_d]
P2_MOVEMENT_KEYS = [K_i, K_k, K_j, K_l]
P3_MOVEMENT_KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

class MovementKeys:
    def __init__(self, player_number):
        if player_number == 1:
            self.keys = P1_MOVEMENT_KEYS
        elif player_number == 2:
            self.keys = P2_MOVEMENT_KEYS
        elif player_number == 3:
            self.keys = P3_MOVEMENT_KEYS
        else:
            self.keys = P3_MOVEMENT_KEYS

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

SPECIAL_TYPES = {'NONE': None}


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
        self.special_type = SPECIAL_TYPES['NONE']
        self.image = 'player_ship'
        self.firing = False
        self.firing_special = False
        self.hit_scale = [-10,-5]


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
        if time_since_last_shot >= FIRE_DELAY:
            if self.firing is True:
                bullet = Bullet(game_context=self.game_context,
                                position=[self.position[0]+15,self.position[1]],
                                speed= [0,-10],
                                launched_by=self.number,
                                strength=1)
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




class MainGameContext(GameContext):

    def __init__(self, size, player_count=1):
        if player_count > MAX_PLAYERS:
            raise SystemExit

        super().__init__(size)

        self.player_count = player_count
        self.players = []
        for i in range(1, self.player_count + 1):
            player = Player(game_context=self,
                            number=i,
                            movement_keys=MovementKeys(i))
            self.players.append(player)

        self.enemies = []
        self.bullets = []

        self.image_dict = {
            'player_ship': sprites.load_ship_p1(),
            'orange_bullet': sprites.load_orange_bullet(),
            'smile': sprites.load_smile(),
            'wink': sprites.load_wink(),
            'cryer_1': sprites.load_cryer_1(),
            'cryer_2': sprites.load_cryer_2(),
            'tear': sprites.load_tear(),
            'devil': sprites.load_devil()
        }

        self.levels = [Level1(), Level2()]
        self.level_index = 0
        self.new_level_delay = 5
        self.level_finish_time = 0

    def update(self, screen, input_dict):

        # TODO for now, i'm wiping the entire surface on each blit
        # TODO a better way would be to blit only sections that are changing
        self.surface.fill(colors.BLACK)

        # run level events
        self.process_level_events()

        # process collisions
        self.process_player_collisions()
        self.process_bullet_collisions()

        # process player movement and shooting
        self.process_player_inputs(input_dict)

        # process enemy movement and behavior
        self.process_enemy_behavior()

        # proces bullets
        self.process_bullets()

        # process environment
        self.process_environment()

        screen.blit(self.surface, self.surface.get_rect())

    def _current_level_or_None(self):
        if self.level_index >= len(self.levels):
            return None
        return self.levels[self.level_index]

    def process_level_events(self):

        level = self._current_level_or_None()

        if level is None:
            return

        # check if spawning is complete, and if so, if enemies are all killed
        if level.spawning_complete and level.complete is False:
            if len(self.enemies) == 0:
                level.complete = True
                self.level_finish_time = time.time()


        if level.complete:
            if time.time() - self.level_finish_time >= self.new_level_delay:
                self.level_index += 1
            else:
                time_left = str(int(5 - (time.time() - self.level_finish_time)))
                print("New Level in: {}".format(time_left))

        level.update(self)



    def process_player_collisions(self):
        for player in self.players:
            for enemy in self.enemies:
                if player.hit_rect.colliderect(enemy.hit_rect):
                    player.hit_by(enemy)
                    enemy.hit_by(player)


    def process_bullet_collisions(self):
        for bullet in self.bullets:
            if bullet.launched_by == 'enemy':
                for player in self.players:
                    if bullet.hit_rect.colliderect(player.hit_rect):
                        player.hit_by(bullet)
                        bullet.hit_by(player)
            else:
                for enemy in self.enemies:
                    if bullet.hit_rect.colliderect(enemy.hit_rect):
                        enemy.hit_by(bullet)
                        bullet.hit_by(enemy)

        self.enemies = [e for e in self.enemies if not e.dead]
        self.bullets = [b for b in self.bullets if not b.dead]

    def process_player_inputs(self, input_dict):
        for player in self.players:
            player.update(input_dict)
            self.surface.blit(self.image_dict[player.image], player.rect)

    def process_enemy_behavior(self):
        for enemy in self.enemies:
            enemy.update(game_context=self)
            self.surface.blit(self.image_dict[enemy.image], enemy.rect)

    def process_bullets(self):
        for bullet in self.bullets:
            bullet.update()
            self.surface.blit(self.image_dict[bullet.image], bullet.rect)

    def process_environment(self):
        return None






