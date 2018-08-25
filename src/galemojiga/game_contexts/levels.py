import time
import galemojiga.globals as globals
from galemojiga.game_objects.Enemies import *

FULL_ROW_POSITIONS = [[i*globals.UNIT, globals.CEILING] for i in range(globals.H_UNITS)]

class WaveEmpty:

    def spawn(self, game_context):
        pass


def full_row_of(enemy_type):
    enemies = []
    for pos in FULL_ROW_POSITIONS:
        en = enemy_type()
        en.position = pos
        enemies.append(en)
    return enemies


class WaveWinkersLeft:

    def spawn(self, game_context):
        for enemy in full_row_of(EnemyWinkerLeft):
            game_context.enemies.append(enemy)


class Wave2Devils:
    def __init__(self):
        pass

    def spawn(self, game_context):

        devil1 = EnemyDevilLeft()
        devil2 = EnemyDevilRight()
        game_context.enemies.append(devil1)
        game_context.enemies.append(devil2)

class WaveWinkersAndCryersLeft:

    def __init__(self):
        pass

    def spawn(self, game_context):
        for i in range(globals.H_UNITS):
            if i % 2 == 0:
                enemy = EnemyCryerLeft()
            else:
                enemy = EnemyWinkerLeft()

            enemy.x += i * globals.UNIT
            game_context.enemies.append(enemy)

class WaveWinkersAndDevilsLeft:

    def spawn(self, game_context):
        for i in range(globals.H_UNITS):
            if i % 2 == 0:
                enemy = EnemyCryerLeft()
            else:
                enemy = EnemyDevilLeft()

            enemy.x += i * globals.UNIT
            game_context.enemies.append(enemy)

class WaveCryersLeft:

    def spawn(self, game_context):
        for enemy in full_row_of(EnemyCryerLeft):
            game_context.enemies.append(enemy)


class WaveCarsLeft:

    def spawn(self, game_context):
        for i in range(5):
            car = GenericLeftSideSwerver()
            car.frame_list = ['car_{}'.format(random.randint(0,7))]
            car.x += globals.UNIT * i
            game_context.enemies.append(car)

class WaveCarsRight:
    def spawn(self, game_context):
        for i in range(5):
            car = GenericRightSideSwerver()
            car.frame_list = ['car_{}'.format(random.randint(0, 7))]
            car.x -= globals.UNIT * i
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
            heli = EnemyHelicopterRight()
            heli.y = random.randint(0,100) + globals.CEILING
            game_context.enemies.append(heli)

class WaveTrain:
    def spawn(self, game_context):
        loco = EnemyTrainLocomotive()
        loco.x = globals.RIGHT_WALL
        game_context.enemies.append(loco)
        for i in range(6):
            car = EnemyTrainCar()
            car.x = globals.RIGHT_WALL + ((i+1)*20)
            game_context.enemies.append(car)

class WaveCrazy4:
    def spawn(self, game_context):
        for i in range(4):
            crazy = EnemyCrazyBouncer()
            game_context.enemies.append(crazy)

class TwoMonkeys:
    def spawn(self, game_context):
        m1 = EnemyMonkeyLeft()
        m2 = EnemyMonkeyRight()
        game_context.enemies.append(m1)
        game_context.enemies.append(m2)

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
        self.waves = [WaveWinkersLeft(),
                      WaveWinkersLeft(),
                      WaveWinkersLeft(),
                      WaveWinkersAndCryersLeft(),
                      WaveWinkersLeft(),
                      WaveWinkersAndCryersLeft()]
        self.waves_spawned = [False] * len(self.waves)


class Level2(LevelAbstract):

    def __init__(self):
        super().__init__()
        self.wave_time_gap = 6
        self.waves = [WaveWinkersLeft(),
                      WaveWinkersAndCryersLeft(),
                      WaveCryersLeft(),
                      WaveWinkersAndCryersLeft(),
                      Wave2Devils(),
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
                      [TwoMonkeys(), 4]]
