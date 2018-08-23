import time
import copy
import random
from galemojiga.game_objects.GameObject import GameObject
from galemojiga.game_objects.Bullets import Bullet, BulletTear
import galemojiga.globals as globals

ENEMY_OFFSET = 41

class Enemy(GameObject):

    def __init__(self):
        super().__init__()
        self.x = globals.RIGHT_WALL
        self.y = globals.CEILING
        self.size = globals.ENEMY_SCALE
        self.hit_scale = [-4, -4]
        self.frame_list = ['smile', 'wink']
        self.health = 2
        self.dead = False
        self.speed_h = 3
        self.speed_v = 3
        self.strength = 1

    def hit_by(self, something):
        if isinstance(something, Bullet):
            self.health -= something.strength
        if self.health <= 0:
            self.dead = True

    def update(self, game_context):
        super().update(game_context)
        if self.y >= globals.FLOOR + 100:
            self.dead = True

class GenericLeftShimmier(Enemy):

    def __init__(self):
        super().__init__()
        self.move_list = [
            self._move_left_to_wall,
            self._move_down_one_unit,
            self._move_right_to_wall,
            self._move_down_one_unit
        ]

class GenericRightShimmier(Enemy):

    def __init__(self):
        super().__init__()
        self.x = globals.LEFT_WALL
        self.move_list = [
            self._move_right_to_wall,
            self._move_down_one_unit,
            self._move_left_to_wall,
            self._move_down_one_unit
        ]

class GenericDiveBomberLeft(Enemy):

    def __init__(self):
        super().__init__()
        self.speed_v = 6
        self.move_list = [
            [self._move_left_random, 5, 1000],
            self._move_down_to_floor,
            self._move_up_to_ceiling,
            self._move_left_to_wall,
            [self._move_right_random, 5, 1000],
            self._move_down_to_floor,
            self._move_up_to_ceiling,
            self._move_right_to_wall
        ]

class GenericDiveBomberRight(Enemy):

    def __init__(self):
        super().__init__()
        self.speed_v = 6
        self.x = globals.LEFT_WALL
        self.move_list = [
            [self._move_right_random, 5, 1000],
            self._move_down_to_floor,
            self._move_up_to_ceiling,
            self._move_right_to_wall,
            [self._move_left_random, 5, 1000],
            self._move_down_to_floor,
            self._move_up_to_ceiling,
            self._move_left_to_wall
        ]


class GenericSwerver(Enemy):
    def __init__(self):
        super().__init__()
        self.speed_h = 5


class GenericLeftSideSwerver(GenericSwerver):
    def __init__(self):
        super().__init__()
        self.x = globals.LEFT_WALL
        self.move_list = [
            [self._move_right_to_unit, 5],
            self._move_down_one_unit,
            self._move_left_to_wall,
            self._move_down_one_unit
        ]

class GenericRightSideSwerver(GenericSwerver):
    def __init__(self):
        super().__init__()
        self.x = globals.RIGHT_WALL
        self.move_list = [
            [self._move_left_to_unit, globals.H_UNITS - 5],
            self._move_down_one_unit,
            [self._move_right_to_unit, globals.H_UNITS],
            self._move_down_one_unit
        ]

class GenericFaller(Enemy):
    def __init__(self):
        super().__init__()
        self.move_list = [self._move_down_forever]


class EnemyBomb(GenericFaller):
    def __init__(self):
        super().__init__()
        self.frame_list = ['bomb']
        self.strength = 3
        self.health = 8


class GenericDropper(Enemy):
    def __init__(self):
        super().__init__()
        self.spawn_probability = [10, 1000]

    def update(self, game_context):
        if random.randint(0, self.spawn_probability[1]) <= self.spawn_probability[0]:
            self.spawn_drop(game_context)
        super().update(game_context)

    def spawn_drop(self, game_context):
        pass


class GenericDropperRight(GenericDropper):
    def __init__(self):
        super().__init__()
        self.x = globals.LEFT_WALL - 25
        self.move_list = [self._move_right_forever]


class GenericDropperLeft(GenericDropper):
    def __init__(self):
        super().__init__()
        self.x = globals.RIGHT_WALL + 25
        self.move_list = [self._move_left_forever]


class EnemyHelicopterRight(GenericDropperRight):
    def __init__(self):
        super().__init__()
        self.frame_list = ['helicopter']

    def update(self, game_context):
        super().update(game_context)

    def spawn_drop(self, game_context):
        bomb = EnemyBomb()
        bomb.x = self.x
        bomb.y = self.y + 20
        game_context.enemies.append(bomb)

class EnemyTrain(Enemy):
    def __init__(self):
        super().__init__()
        self.x = globals.RIGHT_WALL + 20
        self.y = globals.FLOOR - 150
        self.move_list = [self._move_left_forever]


class EnemyTrainLocomotive(EnemyTrain):
    def __init__(self):
        super().__init__()
        self.frame_list = ['train_0']

class EnemyTrainCar(EnemyTrain):
    def __init__(self):
        super().__init__()
        self.frame_list = ['train_1']


class EnemyDevilLeft(GenericDiveBomberLeft):

    def __init__(self):
        super().__init__()
        self.frame_list = ['devil']
        self.health = 4


class EnemyDevilRight(GenericDiveBomberRight):

    def __init__(self):
        super().__init__()
        self.frame_list = ['devil']
        self.health = 4


class EnemyWinkerLeft(GenericLeftShimmier):
    def __init__(self):
        super().__init__()


class EnemyWinkerRight(GenericRightShimmier):
    def __init__(self):
        super().__init__()
        self.x = globals.LEFT_WALL


class GenericCryer(Enemy):
    def __init__(self):
        super().__init__()
        self.frame_list = ['cryer_1', 'cryer_2']
        self.health = 3
        self.tear_chance = 5
        self.tear_chance_max = 1000
        self.last_tear_time = 0

    def update(self, game_context):
        super().update(game_context)
        if random.randint(0,self.tear_chance_max)  <= self.tear_chance:
            tear = BulletTear(game_context=game_context,
                              position=[self.x, self.y])

            game_context.bullets.append(tear)

class EnemyCryerLeft(GenericLeftShimmier, GenericCryer):
    pass

class EnemyCryerRight(GenericLeftShimmier, GenericCryer):
    def __init__(self):
        super().__init__()
        self.x = globals.LEFT_WALL