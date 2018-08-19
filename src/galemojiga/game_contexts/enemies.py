import time
import copy
import random
from galemojiga.GameObject import GameObject, Bullet
import galemojiga.globals as globals


SHIMMY_SPEED = 3
SHIMMY_DOWN_TIME = .25
SHIMMY_DOWN_DIST = 25
DIVE_SPEED = 10
SHIMMY_START_STATE = {'direction': 'right', 'down_start_time': 0}
DIVE_BOMBER_START_STATE = {'direction': 'left'}
ENEMY_OFFSET = 41


class MovementStyle:

    def __init__(self, style):
        self.direction = 'right'
        self.style = style
        self.down_total = 0
        if self.style in ['default', 'shimmy']:
            self.move_state = copy.deepcopy(SHIMMY_START_STATE)
        elif self.style == 'dive_bomber':
            self.move_state = copy.deepcopy(DIVE_BOMBER_START_STATE)

    def next(self, x, y):
        if self.style in ['default', 'shimmy']:
            return self.mv_style_shimmy(x, y)
        else:
            return self.mv_dive_bomber(x, y)

    def mv_dive_bomber(self, x, y):

        new_x = x
        new_y = y

        if self.direction in ['left', 'right']:
            # randomly do a dive
            if random.randint(0,1000) < 3:
                print('diving')
                self.direction = 'down'

        if self.direction == 'left':
            new_x -= SHIMMY_SPEED
            if new_x <= 0:
                new_x = 0
                self.direction = 'right'

        if self.direction == 'right':
            new_x += SHIMMY_SPEED
            if new_x >= globals.MAIN_WINDOW_SIZE[0] - ENEMY_OFFSET:
                new_x = globals.MAIN_WINDOW_SIZE[0] - ENEMY_OFFSET
                self.direction = 'left'

        if self.direction == 'down':
            new_y = y + DIVE_SPEED

        if self.direction == 'up':
            new_y = y - DIVE_SPEED

        if new_y >= globals.MAIN_WINDOW_SIZE[1] - 20:
            self.direction = 'up'

        if (new_y <= 0) and (self.direction == 'up'):
            self.new_y = 0
            self.direction = random.choice(['left', 'right'])

        return [new_x, new_y]

    def mv_style_shimmy(self, x, y):
        new_x = x
        new_y = y
        if self.direction == 'left':
            new_x -= SHIMMY_SPEED
        elif self.direction == 'right':
            new_x += SHIMMY_SPEED

        if (new_x <= 0) and (self.direction is not 'down'):
            new_x = 0
            self.direction = 'down'
            self.move_state['down_start_time'] = time.time()

        if (new_x >= globals.MAIN_WINDOW_SIZE[0] - ENEMY_OFFSET) and \
                (self.direction is not 'down'):
            new_x = globals.MAIN_WINDOW_SIZE[0] - ENEMY_OFFSET
            self.direction = 'down'
            self.move_state['down_start_time'] = time.time()

        if self.direction == 'down':
            new_y += SHIMMY_SPEED
            self.down_total += SHIMMY_SPEED

            if self.down_total >= SHIMMY_DOWN_DIST:
                self.down_total = 0
                # stop going down
                if new_x <= 10:
                    self.direction = 'right'
                else:
                    self.direction = 'left'

        return [new_x, new_y]

class Enemy(GameObject):

    def __init__(self):
        super().__init__()
        self.hit_scale = [-10, -10]
        self.movement_style = MovementStyle('default')
        self.image_list = ['smile', 'wink']
        self.image = self.image_list[0]
        self.frame_index = 0
        self.frame_rate = 0.5
        self.last_frame_switch = time.time()
        self.health = 2
        self.dead = False

    def update(self, game_context):
        self.position = self.movement_style.next(x=self.position[0],
                                                 y=self.position[1])
        now = time.time()
        if now - self.last_frame_switch >= self.frame_rate:
            self.last_frame_switch = now
            self.frame_index += 1
            if self.frame_index >= len(self.image_list):
                self.frame_index = 0
            self.image = self.image_list[self.frame_index]

    def hit_by(self, something):
        if isinstance(something, Bullet):
            self.health -= something.strength
        if self.health <= 0:
            self.dead = True

class EnemySmiley(Enemy):
    def __init__(self):
        super().__init__()

class EnemyCryer(Enemy):
    def __init__(self):
        super().__init__()
        self.movement_style = MovementStyle('shimmy')
        self.image_list = ['cryer_1', 'cryer_2']
        self.health = 3
        self.tear_chance = 5
        self.tear_chance_max = 1000
        self.last_tear_time = 0

    def update(self, game_context):
        super().update(game_context)
        if random.randint(0,self.tear_chance_max)  <= self.tear_chance:
            tear = Bullet(game_context=game_context,
                          position=copy.copy(self.position),
                          speed=(0,5),
                          launched_by='enemy',
                          strength=1,
                          image='tear')
            game_context.bullets.append(tear)

class EnemyDevil(Enemy):

    def __init__(self):
        super().__init__()
        self.movement_style = MovementStyle('dive_bomber')
        self.image_list = ['devil']
        self.health = 4