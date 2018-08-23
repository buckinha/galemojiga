import random
import time
from galemojiga.game_objects.GameObject import GameObject
from galemojiga.game_objects.Bullets import Bullet
import galemojiga.globals as globals

class PowerUp(GameObject):
    def __init__(self):
        super().__init__()
        self.move_list = [self._move_down_forever]
        self.size = globals.ENEMY_SCALE
        self.setup()

    def setup(self):
        pass

    def affect_player(self, player_obj):
        self.dead = True
        self._affect_player(player_obj)

    def _affect_player(self, player_obj):
        pass


class PowerUpHealth1(PowerUp):

    def setup(self):
        self.frame_list = ['heart']

    def _affect_player(self, player_obj):
        player_obj.health += 1
        if player_obj.health > player_obj.max_health:
            player_obj.health = player_obj.max_health

class PowerUpHealthMax(PowerUp):

    def setup(self):
        self.frame_list = ['heart_box']

    def _affect_player(self, player_obj):
        player_obj.health = player_obj.max_health


class PowerUpCoffee(PowerUp):

    def setup(self):
        self.frame_list = ['coffee']

    def _affect_player(self, player_obj):
        if player_obj.fire_delay > globals.FAST_FIRE_DELAY:
            player_obj.fire_delay = globals.FAST_FIRE_DELAY


class PowerUpDoubleGun(PowerUp):

    def setup(self):
        self.frame_list = ['clinking_glasses']

    def _affect_player(self, player_obj):
        player_obj.double_gun = True


class SpecialGun(PowerUp):

    def setup(self):
        self.shots = 0
        self.last_shot_time = 0
        self.fire_delay = 1
        self.powerup_sprite = 'sushi_bento'

    def fire(self):
        if self.player is None:
            return

        if self.player.game_context is None:
            return

        now = time.time()
        if now - self.last_shot_time >= self.fire_delay:
            self.last_shot_time = now
            self._fire()

    def _affect_player(self, player_obj):
        player_obj.special_gun = self
        self.player = player_obj

    def _fire(self):
        pass

    def remove_from_player(self):
        # remove references to each other
        if self.player is not None:
            self.player.special_gun = None
            self.player = None

class SushiGun(SpecialGun):

    def setup(self):
        super().setup()
        self.shots = 6
        self.frame_list = ['sushi_bento']
        self.powerup_sprite = 'sushi_bento'

    def _fire(self):
        pos = self.player.position
        pos[0] -= 15
        sushi_sprites = ['sushi_rice', 'tempura', 'nigiri', 'nigiri', 'dumpling']
        for i in range(5):
            piece = Bullet(game_context=self.player.game_context,
                           position=pos,
                           speed = [i-2, -10],
                           launched_by=self.player.number,
                           strength=10,
                           image=random.choice(sushi_sprites))
            piece.size = globals.ENEMY_SCALE
            self.player.game_context.bullets.append(piece)
        self.shots -= 1
        if self.shots <= 0:
            self.remove_from_player()

def pick_powerup():
    r = random.randint(0,10)
    if r <= 11:
        return SushiGun()

    # pick a special powerup
    choices = [SushiGun(), PowerUpCoffee(), PowerUpHealthMax(), PowerUpDoubleGun()]
    return random.choice(choices)