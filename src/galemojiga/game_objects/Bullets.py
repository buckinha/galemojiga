import random
from galemojiga.game_objects.GameObject import GameObject
import galemojiga.globals as globals

class Bullet(GameObject):
    def __init__(self, game_context, position, speed, launched_by,
                 strength, image='orange_bullet'):
        super().__init__()
        self.position = position
        self.size = globals.BULLET_SCALE

        # if speed is a tuple or list, use both items, otherwise, assume it's numeric
        if hasattr(speed, '__iter__'):
            self.speed_vertical = speed[0]
            self.speed_horizontal = speed[1]
        else:
            self.speed_vertical = speed
            self.speed_horizontal = 0

        self.launched_by = launched_by
        self.strength = strength

        self.dead = False

        self.frame_list = [image]

        self.game_context = game_context

        self.immune_ticks = 0
        self.expire_ticks = -1

    def update(self, game_context):
        self.x += self.speed_vertical
        self.y += self.speed_horizontal
        self.check_dismissal()

    def check_dismissal(self):
        buffer = 50
        if self.position[1] < -buffer or self.position[1] > globals.MAIN_WINDOW_SIZE[1] + buffer:
            self.dead = True
        if self.expire_ticks > 0:
            self.expire_ticks -= 1
            if self.expire_ticks == 0:
                self.dead = True

    def hit_by(self, anything):
        if self.immune_ticks <= 0:
            self.dead = True
            self.strength = 0
        else:
            self.immune_ticks -= 1


class BulletTear(Bullet):
    def __init__(self, game_context, position, speed=(0,5),
                 launched_by='enemy',
                 strength=1, image='tear'):
        super().__init__(game_context=game_context,
                         position=position, speed=speed,
                         launched_by=launched_by,
                         strength=strength, image=image)

        self.size = [14, 17]
        self.hit_offset = [4, 2]


class BulletFish(Bullet):
    def __init__(self, game_context, position, speed=(0,5),
                 launched_by='enemy',
                 strength=1, image='fish'):
        self.size = globals.BULLET_SCALE
        super().__init__(game_context=game_context,
                         position=position, speed=speed,
                         launched_by=launched_by,
                         strength=strength, image=image)



class BulletShatter(Bullet):

    def __init__(self, game_context, position, speed, launched_by,
                 strength, image):
        super().__init__(game_context, position, speed, launched_by,
                 strength, image)
        self.shard_image = 'bomb'
        self.shard_strength = 1
        self.shards = 8
        self.shard_speed_h = 10
        self.shard_speed_v = 10
        self.auto_shatter = False
        self.auto_shatter_at = globals.CEILING + 50
        self.shard_expire_ticks = 12
        self.shard_immune_ticks = 5

    def _random_shard_speed(self):
        spd_v = random.choice([-1, 0, 1]) * self.shard_speed_v
        spd_h = random.choice([-1, 0, 1]) * self.shard_speed_h
        # check for zero speeds
        if spd_v + spd_h == 0:
            spd_h = random.choice([-1,1]) * self.shard_speed_h
        return [spd_h, spd_v]

    def update(self, game_context):
        if self.auto_shatter:
            if abs(self.y - self.auto_shatter_at) < 50:
                self.hit_by('anything')
        super().update(game_context)

    def hit_by(self, anything):
        for i in range(self.shards):
            shard = Bullet(game_context=self.game_context,
                           position=self.position,
                           speed=self._random_shard_speed(),
                           launched_by=self.launched_by,
                           strength=self.shard_strength,
                           image=self.shard_image)
            shard.immune_ticks = self.shard_immune_ticks
            shard.expire_ticks = self.shard_expire_ticks
            shard.size = globals.ENEMY_SCALE
            self.game_context.bullets.append(shard)
        super().hit_by(anything)


class CandyBullet(BulletShatter):
    def __init__(self, game_context, position, speed, launched_by):
        super().__init__(game_context, position, speed, launched_by,
                 strength=1, image='candy')
        self.shard_image = 'candy'
        self.shard_strength = 1
        self.shards = 8
        self.shard_speed_h = 12
        self.shard_speed_v = 4
        self.auto_shatter = True
        self.auto_shatter_at = globals.CEILING

class MonkeyBullet(Bullet):
    def __init__(self, game_context, position):
        img = random.choice(['coconut', 'banana'])
        spd = [random.randint(-3,3), 6]
        super().__init__(game_context, position, spd, 'enemy',
                 strength=1, image=img)
        self.size = globals.ENEMY_SCALE

class SantaBullet(BulletShatter):
    def __init__(self, game_context, position, speed, launched_by):
        super().__init__(game_context, position, speed, launched_by,
                 strength=1, image='present')
        self.size = globals.ENEMY_SCALE
        present_list = ['socks', 'paint_pallet', 'book', 'racecar', 'football']
        self.shard_image = random.choice(present_list)
        self.shard_strength = 1
        self.shards = 4
        self.shard_speed_h = 4
        self.shard_speed_v = 4
        self.auto_shatter = True
        self.auto_shatter_at = globals.FLOOR - 50
        self.shard_expire_ticks = 25
        self.shard_immune_ticks = 0
