import time
import galemojiga.globals as globals
from galemojiga.game_objects.Enemies import *

FULL_ROW_POSITIONS = [[globals.LEFT_WALL + i*globals.UNIT, globals.CEILING] for i in range(globals.H_UNITS)]

class WaveEmpty:

    def spawn(self, game_context):
        pass


def full_row_of(game_context, enemy_type):
    enemies = []
    for pos in FULL_ROW_POSITIONS:
        en = enemy_type(game_context)
        en.position = pos
        enemies.append(en)
    return enemies



class WaveWinkersLeft:

    def spawn(self, game_context):
        for enemy in full_row_of(game_context, EnemyWinkerLeft):
            game_context.enemies.append(enemy)


class Wave2Devils:
    def __init__(self):
        pass

    def spawn(self, game_context):

        devil1 = EnemyDevilLeft(game_context)
        devil2 = EnemyDevilRight(game_context)
        game_context.enemies.append(devil1)
        game_context.enemies.append(devil2)

class WaveWinkersAndCryersLeft:

    def __init__(self):
        pass

    def spawn(self, game_context):
        for i in range(globals.H_UNITS):
            if i % 2 == 0:
                enemy = EnemyCryerLeft(game_context)
            else:
                enemy = EnemyWinkerLeft(game_context)

            enemy.x += i * globals.UNIT
            game_context.enemies.append(enemy)

class WaveWinkersAndDevilsLeft:

    def spawn(self, game_context):
        for i in range(globals.H_UNITS):
            if i % 2 == 0:
                enemy = EnemyCryerLeft(game_context)
            else:
                enemy = EnemyDevilLeft(game_context)

            enemy.x += i * globals.UNIT
            game_context.enemies.append(enemy)

class WaveCryersLeft:

    def spawn(self, game_context):
        for enemy in full_row_of(game_context, EnemyCryerLeft):
            game_context.enemies.append(enemy)


class WaveCarsLeft:

    def spawn(self, game_context):
        for i in range(10):
            car = GenericLeftSideSwerver(game_context)
            car.frame_list = ['car_{}'.format(random.randint(0,7))]
            car.x = globals.LEFT_WALL - (i*27) - 50
            game_context.enemies.append(car)

class WaveCarsRight:
    def spawn(self, game_context):
        for i in range(10):
            car = GenericRightSideSwerver(game_context)
            car.frame_list = ['car_{}'.format(random.randint(0, 7))]
            car.x = globals.RIGHT_WALL + (i*27) + 50
            game_context.enemies.append(car)

class WaveCarsBoth:
    def spawn(self, game_context):
        left = WaveCarsLeft()
        right = WaveCarsRight()
        left.spawn(game_context)
        right.spawn(game_context)


class WaveHelicoptersTrio:
    def spawn(self, game_context):
        for i in range(3):
            heli = EnemyHelicopterRight(game_context)
            heli.y = random.randint(0,100) + globals.CEILING
            game_context.enemies.append(heli)

class WaveTrain:
    def spawn(self, game_context):
        loco = EnemyTrainLocomotive(game_context)
        loco.x = globals.RIGHT_WALL
        game_context.enemies.append(loco)
        for i in range(6):
            car = EnemyTrainCar(game_context)
            car.x = globals.RIGHT_WALL + ((i+1)*20)
            game_context.enemies.append(car)

class WaveCrazy4:
    def spawn(self, game_context):
        for i in range(4):
            crazy = EnemyCrazyBouncer(game_context)
            game_context.enemies.append(crazy)

class WaveTwoMonkeys:
    def spawn(self, game_context):
        m1 = EnemyMonkeyLeft(game_context)
        m2 = EnemyMonkeyRight(game_context)
        game_context.enemies.append(m1)
        game_context.enemies.append(m2)


class WaveZombieWall:
    def spawn(self, game_context):
        for i in range(len(FULL_ROW_POSITIONS)):
            if i%2 == 0:
                zombie = Zombie1(game_context)
            else:
                zombie = Zombie2(game_context)
            zombie.position = FULL_ROW_POSITIONS[i]
            zombie.y -= 20
            game_context.enemies.append(zombie)

class WaveThreeVampires:
    def spawn(self, game_context):
        vamp_l = VampireLeft(game_context)
        vamp_r = VampireRight(game_context)
        vamp_m = VampireRight(game_context)
        vamp_m.x = globals.H_MIDDLE
        game_context.enemies.append(vamp_l)
        game_context.enemies.append(vamp_r)
        game_context.enemies.append(vamp_m)

class WaveFourGhosts:
    def spawn(self, game_context):
        for i in range(4):
            ghost = EnemyGhost(game_context)
            game_context.enemies.append(ghost)

class WaveRandomPoop:
    def spawn(self, game_context):
        for i in range(2):
            poop = GenericFaller(game_context)
            poop.position = random.choice(FULL_ROW_POSITIONS)
            poop.frame_list = ['poop']
            game_context.enemies.append(poop)


class WaveTwoSantas:
    def spawn(self, game_context):
        for i in range(2):
            santa = EnemySanta(game_context)
            santa.x = globals.H_MIDDLE + i*100
            game_context.enemies.append(santa)


class WaveBlockadeOf:
    def __init__(self, enemy_type, rows=5, row_delay=3):
        self.enemy_type = enemy_type
        self.row_count = rows
        self.row_delay = row_delay
        self.speed_h = 10
        self.speed_v = 2

    def spawn(self, game_context):
        rows = self.row_count
        row_buffer = globals.CEILING_BUFFER + globals.UNIT * 2
        for r in range(rows):
            for c in range(1, globals.H_UNITS - 1):
                move_delay = self.row_delay * (rows - r)
                e = self.enemy_type(game_context, c, move_delay)
                e.x = (c * globals.UNIT) - 500
                e.y = (r * globals.UNIT) + row_buffer
                e.speed_h = self.speed_h
                e.speed_v = self.speed_v
                game_context.enemies.append(e)

class WaveWinkerBlock(WaveBlockadeOf):
    def __init__(self, rows=5, row_delay=3):
        super().__init__(enemy_type=EnemyWinkerMarcher,
                         rows=rows, row_delay=row_delay)
        self.speed_h = 5

class WaveCrierBlock(WaveBlockadeOf):
    def __init__(self, rows=5, row_delay=3):
        super().__init__(enemy_type=EnemyCrierMarcher,
                         rows=rows, row_delay=row_delay)
        self.speed_h = 5


class WaveSnowmanBlockade(WaveBlockadeOf):
    def __init__(self):
        super().__init__(EnemySnowman)


class WavePenguins:
    def spawn(self, game_context):
        for i in range(3):
            penguin = EnemyPenguin(game_context)
            penguin.x -= i*35
            penguin.y = globals.get_v_unit_y_val(i + 1)
            game_context.enemies.append(penguin)


class LevelAbstract:
    def __init__(self):
        self.spawning_complete = False
        self.complete = False
        self.wave_idx = 0
        self.waves = []
        self.waves_spawned = []
        self.wave_time_gap = 5.5
        self.level_start_time = time.time()
        self.wave_start_time = self.level_start_time - self.wave_time_gap

    def reset(self):
        self.spawning_complete = False
        self.complete = False
        self.wave_idx = 0
        self.waves_spawned = [False] * len(self.waves)
        self.level_start_time = time.time()
        self.wave_start_time = self.level_start_time - self.wave_time_gap

    def update(self, game_context):
        if self.complete or self.spawning_complete:
            return

        now = time.time()
        if now - self.wave_start_time > self.wave_time_gap:

            if self.waves_spawned[self.wave_idx] is False:
                self.waves[self.wave_idx].spawn(game_context)
                self.waves_spawned[self.wave_idx] = True
                self.wave_idx += 1
                self.wave_start_time = now

        if self.wave_idx >= len(self.waves):
            print('Spawning Complete')
            self.spawning_complete = True


class TimedLevel(LevelAbstract):
    def __init__(self):
        super().__init__()
        self.delay_till = 0
        self.waves = [[None, 0]]

    def update(self, game_context):
        if self.complete or self.spawning_complete:
            return

        now = time.time()
        if now >= self.delay_till:
            wave, delay_seconds = self.waves[self.wave_idx]
            wave.spawn(game_context)
            self.delay_till = now + delay_seconds
            self.wave_idx += 1

        if self.wave_idx >= len(self.waves):
            print('Spawning Complete')
            self.spawning_complete = True


class Level1(LevelAbstract):

    def __init__(self):
        super().__init__()
        self.wave_time_gap = 6
        self.waves = [WaveWinkerBlock(rows=4),
                      WaveWinkersLeft(),
                      WaveWinkersLeft(),
                      WaveWinkersAndCryersLeft(),
                      WaveWinkerBlock(rows=4),
                      WaveWinkersAndCryersLeft()]
        self.waves_spawned = [False] * len(self.waves)


class Level2(LevelAbstract):

    def __init__(self):
        super().__init__()
        self.wave_time_gap = 6
        self.waves = [WaveWinkersLeft(),
                      WaveWinkersAndCryersLeft(),
                      WaveCrierBlock(rows=1),
                      WaveWinkersAndCryersLeft(),
                      Wave2Devils(),
                      WaveCrierBlock(rows=1),
                      WaveWinkersAndCryersLeft(),
                      WaveWinkersAndDevilsLeft(),
                      WaveCryersLeft()]
        self.waves_spawned = [False] * len(self.waves)


class Level3(LevelAbstract):

    def __init__(self):
        super().__init__()
        self.wave_time_gap = 2
        self.waves = [WaveCarsLeft(),
                      WaveCarsRight(),
                      WaveHelicoptersTrio(),
                      WaveTrain(),
                      WaveCarsRight(),
                      WaveCarsLeft(),
                      WaveTrain(),
                      WaveCarsBoth(),
                      WaveTrain(),
                      WaveHelicoptersTrio(),]
        self.waves_spawned = [False] * len(self.waves)


class Level4(TimedLevel):

    def __init__(self):
        super().__init__()
        self.waves = [[WaveCrazy4(), 1],
                      [WaveTwoMonkeys(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveTwoMonkeys(), 4],
                      [WaveCrazy4(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1],
                      [WaveRandomPoop(), 1]]


class LevelZombie(TimedLevel):
    def __init__(self):
        super().__init__()
        self.waves = [[WaveZombieWall(), 2],
                      [WaveThreeVampires(), 2],
                      [WaveZombieWall(), 2],
                      [WaveFourGhosts(), 2],
                      [WaveZombieWall(), 4]]

class LevelSanta(TimedLevel):
    def __init__(self):
        super().__init__()
        self.waves = [[WaveSnowmanBlockade(), 1],
                      [WaveTwoSantas(), 4],
                      [WavePenguins(), 10],
                      [WavePenguins(), 4],
                      [WaveSnowmanBlockade(), 2]]



LEVEL_LIST = [Level1, Level2, Level3, Level4, LevelSanta, LevelZombie]