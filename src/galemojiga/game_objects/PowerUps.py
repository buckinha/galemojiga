import random
import time
from galemojiga.game_objects.GameObject import GameObject
from galemojiga.game_objects.Bullets import Bullet, CandyBullet
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
        player_obj.coffee_gun = True


class PowerUpDoubleGun(PowerUp):

    def setup(self):
        self.frame_list = ['clinking_glasses']

    def _affect_player(self, player_obj):
        player_obj.double_gun = True


class SpecialGun(PowerUp):

    def setup(self):
        self.shots = 0
        self.ammo_spend_per_shot = 1
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
            self.shots -= self.ammo_spend_per_shot
            if self.shots <= 0:
                self.remove_from_player()

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


class ChiliGun(SpecialGun):

    def setup(self):
        super().setup()
        self.shots = 6
        self.ammo_spend_per_shot = .1
        self.fire_delay = 0.1
        self.frame_list = ['chili']
        self.powerup_sprite = 'chili'

    def _fire(self):
        pos = self.player.position

        flame = Bullet(game_context=self.player.game_context,
                       position=pos,
                       speed = [0, -15],
                       launched_by=self.player.number,
                       strength=3,
                       image='flame')
        flame.size = globals.ENEMY_SCALE
        self.player.game_context.bullets.append(flame)

class CandyGun(SpecialGun):
    def setup(self):
        super().setup()
        self.shots = 4
        self.fire_delay = 1
        self.frame_list = ['lollypop']
        self.powerup_sprite = 'lollypop'

    def _fire(self):
        pos = self.player.position

        candy = CandyBullet(game_context=self.player.game_context,
                            position=pos,
                            speed = [0, -15],
                            launched_by=self.player.number)
        candy.size = globals.ENEMY_SCALE
        self.player.game_context.bullets.append(candy)


def pick_powerup(game_context):
    r = random.randint(0,10)

    health_powerups = [PowerUpHealth1, PowerUpHealth1, PowerUpHealth1, PowerUpHealthMax]
    gun_powerups = [CandyGun, ChiliGun, SushiGun]


    missing_health_total = 0
    coffee_total = 0
    doublegun_total = 0
    for p in game_context.players:
        missing_health_total += (p.max_health - p.health)
        if p.coffee_gun:
            coffee_total += 1
        if p.double_gun:
            doublegun_total += 1

    if (missing_health_total / len(game_context.players)) >= 1:
        pup_list = gun_powerups + health_powerups
    else:
        pup_list = gun_powerups

    if coffee_total < len(game_context.players):
        pup_list.append(PowerUpCoffee)
    if doublegun_total < len(game_context.players):
        pup_list.append(PowerUpDoubleGun)

    # pick a special powerup
    pup = random.choice(pup_list)
    return pup()