import time
import copy
import random
from galemojiga.game_objects.GameObject import GameObject
from galemojiga.game_objects.Bullets import *
import galemojiga.globals as globals
from galemojiga.game_objects.Players import Player

ENEMY_OFFSET = 41

class Enemy(GameObject):

    def __init__(self, game_context):
        self.game_context = game_context
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
        elif isinstance(something, Player):
            self.health = 0

        if self.health <= 0:
            self.dead = True
            self.on_death()

    def update(self, game_context):
        super().update(game_context)
        if self.y >= globals.FLOOR + 100:
            self.dead = True

    def on_death(self):
        pass

class GenericLeftShimmier(Enemy):

    def __init__(self, game_context):
        super().__init__(game_context)
        self.move_list = [
            self._move_left_to_wall,
            self._move_down_one_unit,
            self._move_right_to_wall,
            self._move_down_one_unit
        ]

class GenericRightShimmier(Enemy):

    def __init__(self, game_context):
        super().__init__(game_context)
        self.x = globals.LEFT_WALL
        self.move_list = [
            self._move_right_to_wall,
            self._move_down_one_unit,
            self._move_left_to_wall,
            self._move_down_one_unit
        ]

class GenericDiveBomberLeft(Enemy):

    def __init__(self, game_context):
        super().__init__(game_context)
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

    def __init__(self, game_context):
        super().__init__(game_context)
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
    def __init__(self, game_context):
        super().__init__(game_context)
        self.speed_h = 5


class GenericLeftSideSwerver(GenericSwerver):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.x = globals.LEFT_WALL
        self.units_right = 5
        self.move_list = [
            [self._move_right_to_unit, self.units_right],
            self._move_down_one_unit,
            self._move_left_to_wall,
            self._move_down_one_unit
        ]

class GenericRightSideSwerver(GenericSwerver):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.x = globals.RIGHT_WALL
        self.units_left = 7
        self.move_list = [
            [self._move_left_to_unit, globals.H_UNITS - self.units_left],
            self._move_down_one_unit,
            [self._move_right_to_unit, globals.H_UNITS - 2],
            self._move_down_one_unit
        ]

class GenericFaller(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.move_list = [self._move_down_forever]


class EnemyBomb(GenericFaller):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['bomb']
        self.strength = 3
        self.health = 6
        self.exploded = False

    def update(self, game_context):
        super().update(game_context)

    def on_death(self):
        if self.exploded is False:
            self.exploded = True
            pos = self.position
            pos[0] -= 10
            pos[1] -= 10
            boom = BoomBig(self.game_context, pos, speed=(0, 0))
            self.game_context.bullets.append(boom)


class GenericDropper(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.spawn_probability = [10, 1000]

    def update(self, game_context):
        if random.randint(0, self.spawn_probability[1]) <= self.spawn_probability[0]:
            self.spawn_drop(game_context)
        super().update(game_context)

    def spawn_drop(self, game_context):
        pass


class GenericDropperRight(GenericDropper):
    def __init__(self,game_context):
        super().__init__(game_context)
        self.x = globals.LEFT_WALL - 25
        self.move_list = [self._move_right_forever]


class GenericDropperLeft(GenericDropper):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.x = globals.RIGHT_WALL + 25
        self.move_list = [self._move_left_forever]


class EnemyHelicopterRight(GenericDropperRight):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['helicopter']
        self.respawned = False

    def update(self, game_context):
        super().update(game_context)
        if self.x >= globals.RIGHT_WALL and self.respawned is False:
            new_copter = EnemyHelicopterRight(game_context)
            new_copter.y = self.y + (globals.UNIT * 2)
            new_copter.x = -25
            game_context.enemies.append(new_copter)
            self.respawned = True

    def spawn_drop(self, game_context):
        bomb = EnemyBomb(game_context)
        bomb.x = self.x
        bomb.y = self.y + 20
        game_context.enemies.append(bomb)

class EnemyTrain(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.x = globals.RIGHT_WALL + 20
        self.y = globals.FLOOR - 150
        self.move_list = [self._move_left_forever]


class EnemyTrainLocomotive(EnemyTrain):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['train_0']

class EnemyTrainCar(EnemyTrain):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['train_1']


class EnemyDevilLeft(GenericDiveBomberLeft):

    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['devil']
        self.health = 4


class EnemyDevilRight(GenericDiveBomberRight):

    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['devil']
        self.health = 4


class EnemyWinkerLeft(GenericLeftShimmier):
    def __init__(self, game_context):
        super().__init__(game_context)


class EnemyWinkerRight(GenericRightShimmier):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.x = globals.LEFT_WALL


class GenericCryer(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['cryer_1', 'cryer_2']
        self.health = 2
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
    def __init__(self, game_context):
        super().__init__(game_context)
        self.x = globals.LEFT_WALL


class GenericBouncer(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.x = random.choice([globals.LEFT_WALL, globals.RIGHT_WALL-self.size[0]])
        self.y = random.randint(globals.CEILING, globals.CEILING + 200)
        if self.x < globals.H_MIDDLE:
            self.speed_h = random.randint(3,5)
        else:
            self.speed_h = random.randint(3,5) * -1
        self.speed_v = random.randint(3,6)

    def update(self, game_context):
        super().update(game_context)
        if (self.x <= globals.LEFT_WALL) and (self.speed_h < 0):
            self.speed_h *= -1
        if (self.x >= globals.RIGHT_WALL) and (self.speed_h > 0):
            self.speed_h *= -1
        if (self.y >= globals.FLOOR) and (self.speed_v > 0):
            self.speed_v *= -1
        if (self.y <= globals.CEILING) and (self.speed_v < 0):
            self.speed_v *= -1

        self.x += self.speed_h
        self.y += self.speed_v

class EnemyCrazyBouncer(GenericBouncer):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['crazy_1', 'crazy_2', 'crazy_3', 'crazy_4']
        self.health = 4


class GenericSliderLeft(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.move_list = [self._move_left_to_wall, self._move_right_to_wall]
        self.x = globals.RIGHT_WALL

class GenericSliderRight(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.move_list = [self._move_right_to_wall, self._move_left_to_wall]
        self.x = globals.LEFT_WALL

class MonkeyBase(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.health = 10
        self.spawn_probability = [10,1000]
        self.frame_list = ['monkey_1', 'monkey_2', 'monkey_3']

    def update(self, game_context):
        if random.randint(0, self.spawn_probability[1]) <= self.spawn_probability[0]:
            self.spawn_drop(game_context)
        super().update(game_context)

    def spawn_drop(self, game_context):
        pos = [self.x, self.y + 25]
        game_context.bullets.append(MonkeyBullet(game_context, pos))

class EnemyMonkeyLeft(GenericSliderLeft, MonkeyBase):
    def __init__(self, game_context):
        super().__init__(game_context)


class EnemyMonkeyRight(GenericSliderRight, MonkeyBase):
    def __init__(self, game_context):
        super().__init__(game_context)


class Zombie1(GenericFaller):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['zombie_1']
        self.speed_v = 1
        self.health = 12

class Zombie2(GenericFaller):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['zombie_2']
        self.speed_v = 1
        self.health = 12

class EnemyBatLeft(GenericLeftSideSwerver):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.units_right = 7
        self.frame_list = ['bat']
        self.health = 1
        self.speed_v = 4
        self.speed_h = 4


class EnemyBatRight(GenericRightSideSwerver):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.units_left = 7
        self.frame_list = ['bat']
        self.health = 1
        self.speed_v = 4
        self.speed_h = 4


class VampireBase(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.health = 10
        self.spawn_probability = [20,1000]
        self.frame_list = random.choice([['vampire_1'], ['vampire_2']])

    def update(self, game_context):
        if random.randint(0, self.spawn_probability[1]) <= self.spawn_probability[0]:
            self.spawn_drop(game_context)
        super().update(game_context)

    def spawn_drop(self, game_context):
        pos = [self.x, self.y + 25]
        bat = random.choice([EnemyBatLeft, EnemyBatRight])(game_context)
        bat.position = pos
        game_context.enemies.append(bat)


class VampireLeft(GenericSliderLeft, VampireBase):
    def __init__(self, game_context):
        super().__init__(game_context)

class VampireRight(GenericSliderLeft, VampireBase):
    def __init__(self, game_context):
        super().__init__(game_context)

class EnemyGhost(GenericBouncer):
    def __init__(self,game_context):
        super().__init__(game_context)
        self.speed_h -= 1
        self.speed_v -= 1
        self.health = 5
        self.frame_list = ['ghost']

class EnemySanta(GenericSliderLeft, MonkeyBase):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['santa']
        self.health = 5
        self.spawn_probability = [5, 1000]

    def spawn_drop(self, game_context):
        pos = [self.x, self.y + 25]
        for i in range(2):
            spd = [i*2 - 2, 3]
            present = SantaBullet(game_context, pos, spd, 'enemy')
            game_context.bullets.append(present)


class GenericMarcher(Enemy):
    def __init__(self, game_context, column_assignment, move_delay):
        super().__init__(game_context)
        self.march_to_column = column_assignment
        self.move_delay = move_delay
        self.move_list = [
            [self._move_right_to_unit, self.march_to_column],
            [self._wait, self.move_delay],
            self._move_down_forever
        ]

class EnemySnowman(GenericMarcher):
    def __init__(self, game_context, column_assignment, move_delay):
        super().__init__(game_context, column_assignment, move_delay)
        self.frame_list = [random.choice(['snowman_1', 'snowman_2'])]

class GenericStraferRight(Enemy):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.shoot_chance = 5
        self.shoot_chance_out_of = 1000
        self.last_shot_time = 0
        self.move_list = [self._move_right_forever]
        self.bullet_type = BulletTear
        self.bullet_speed = [0,10]
        self.x = globals.LEFT_WALL - 50

    def update(self, game_context):
        super().update(game_context)
        if random.randint(0, self.shoot_chance_out_of) <= self.shoot_chance:
            bullet = self.bullet_type(game_context=game_context,
                                      position=[self.x, self.y],
                                      speed = self.bullet_speed,
                                      launched_by='enemy')

            game_context.bullets.append(bullet)


class EnemyPenguin(GenericStraferRight):
    def __init__(self, game_context):
        super().__init__(game_context)
        self.frame_list = ['penguin']
        self.health = 3
        self.bullet_type = BulletFish
        self.shoot_chance = 15
        self.shoot_chance_out_of = 1000


class EnemyWinkerMarcher(GenericMarcher):
    def __init__(self, game_context, column_assignment, move_delay):
        super().__init__(game_context, column_assignment, move_delay)
        self.frame_list = ['smile', 'wink']
        self.health = 2


class EnemyCrierMarcher(GenericMarcher):

    def __init__(self, game_context, column_assignment, move_delay):
        super().__init__(game_context, column_assignment, move_delay)
        self.frame_list = ['cryer_1', 'cryer_2']
        self.health = 2
        self.tear_chance = 5
        self.tear_chance_max = 1000
        self.last_tear_time = 0
        self.speed_h = 2

    def update(self, game_context):
        super().update(game_context)
        if random.randint(0, self.tear_chance_max) <= self.tear_chance:
            tear = BulletTear(game_context=game_context,
                              position=[self.x, self.y])

            game_context.bullets.append(tear)