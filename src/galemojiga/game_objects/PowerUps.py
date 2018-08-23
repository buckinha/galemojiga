import random
from galemojiga.game_objects.GameObject import GameObject
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


def pick_powerup():
    r = random.randint(0,10)
    if r <= 6:
        return PowerUpHealth1()

    # pick a special powerup
    choices = [PowerUpCoffee(), PowerUpHealthMax(), PowerUpDoubleGun()]
    return random.choice(choices)