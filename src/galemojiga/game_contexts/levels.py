import time
import galemojiga.globals as globals
from galemojiga.game_objects.Enemies import Enemy, EnemySmiley, EnemyCryer, EnemyDevil

FULL_ROW_COUNT = int(globals.MAIN_WINDOW_SIZE[0] / 41)
FULL_ROW_POSITIONS = [[i*41,0] for i in range(FULL_ROW_COUNT)]

class WaveEmpty:
    def __init__(self):
        pass
    def spawn(self, game_context):
        pass

def full_row_of(enemy_type):
    enemies = []
    for pos in FULL_ROW_POSITIONS:
        en = enemy_type()
        en.position = pos
        enemies.append(en)
    return enemies


class WaveSmileyShimmy:
    def __init__(self):
        pass

    def spawn(self, game_context):
        for enemy in full_row_of(EnemySmiley):
            game_context.enemies.append(enemy)


class Wave2Devils:
    def __init__(self):
        pass

    def spawn(self, game_context):

        devil1 = EnemyDevil()
        devil1.position = [50, 0]
        devil2 = EnemyDevil()
        devil2.position = [globals.MAIN_WINDOW_SIZE[0] - 50, 0]
        game_context.enemies.append(devil1)
        game_context.enemies.append(devil2)

class WaveSmileysAndCryers:

    def __init__(self):
        pass

    def spawn(self, game_context):
        row_count = int(globals.MAIN_WINDOW_SIZE[0] / 41)
        for i in range(row_count):
            if i%3 == 0:
                enemy = EnemyCryer()
                enemy.position[0] = i * 41
            else:
                enemy = Enemy()
                enemy.position[0] = i * 41
            game_context.enemies.append(enemy)

class WaveSmileysAndDevils:

    def __init__(self):
        pass

    def spawn(self, game_context):
        row_count = int(globals.MAIN_WINDOW_SIZE[0] / 41)
        for i in range(row_count):
            if i%3 == 0:
                enemy = EnemyDevil()
                enemy.position[0] = i * 41
            else:
                enemy = Enemy()
                enemy.position[0] = i * 41
            game_context.enemies.append(enemy)

class WaveCryers:
    def __init__(self):
        pass

    def spawn(self, game_context):
        for enemy in full_row_of(EnemyCryer):
            game_context.enemies.append(enemy)


class LevelAbstract:
    def __init__(self):
        self.spawning_complete = False
        self.complete = False
        self.wave = 0
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

            if self.waves_spawned[self.wave] is False:
                self.waves[self.wave].spawn(game_context)
                self.waves_spawned[self.wave] = True
                self.wave += 1
                self.wave_start_time = now

        if self.wave >= len(self.waves):
            print('Spawning Complete')
            self.spawning_complete = True


class Level1(LevelAbstract):

    def __init__(self):
        super().__init__()
        self.waves = [WaveSmileyShimmy(),
                      WaveSmileyShimmy(),
                      WaveSmileyShimmy(),
                      WaveEmpty(),
                      WaveSmileysAndCryers(),
                      WaveSmileyShimmy(),
                      WaveSmileysAndCryers()]
        self.waves_spawned = [False] * len(self.waves)


class Level2(LevelAbstract):

    def __init__(self):
        super().__init__()
        self.waves = [WaveSmileyShimmy(),
                      WaveSmileysAndCryers(),
                      WaveCryers(),
                      WaveEmpty(),
                      WaveSmileysAndCryers(),
                      Wave2Devils(),
                      WaveSmileysAndCryers(),
                      WaveSmileysAndDevils(),
                      WaveCryers()]
        self.waves_spawned = [False] * len(self.waves)
