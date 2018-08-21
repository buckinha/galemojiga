import random
import pygame
from galemojiga.game_objects.GameObject import GameObject
import galemojiga.globals as globals
import galemojiga.colors as colors


class PowerUp(GameObject):
    def __init__(self):
        super().__init__()

class PartyParrotLeft(GameObject):

    def __init__(self):
        super().__init__()
        self.frame_list = ['parrot_{}'.format(i) for i in range(10)]
        self.frame_rate = 0.1
        self.dead = False
        self.speed_h = 5
        self.move_list = [self._move_left_forever]
        self.x = globals.RIGHT_WALL
        self.powerup = None
        self.powerup_launched = False
        drop_width = int((globals.PLAY_WIDTH / 2) * 0.75)
        self.launch_point = globals.H_MIDDLE + random.randint(-drop_width, drop_width)

    def update(self, game_context):
        super().update(game_context)

        buffer = 50
        if self.position[0] < (0 - buffer):
            self.dead = True
        if self.position[0] > globals.MAIN_WINDOW_SIZE[0] + buffer:
            self.dead = True

        buffer = self.speed_h
        if self.powerup_launched is False:
            if self.position[0] < self.launch_point + buffer:
                if self.position[0] > self.launch_point - buffer:
                    self.powerup_launched = True
                    pup = PowerUp()
                    game_context.powerups.append(pup)

class PartyParrotRight(PartyParrotLeft):

    def __init__(self):
        super().__init__()
        self.move_list = [self._move_right_forever]
        self.x = globals.LEFT_WALL


class PlayerStats(GameObject):

    def __init__(self, player_obj):
        super().__init__()
        self.player = player_obj
        self.size = [(globals.WINDOW_WIDTH/3)-5, 95]
        self.surface = pygame.Surface(self.rect.size)
        self.x = (self.player.number - 1) * (self.size[0]) + (4 * self.player.number)
        self.y = globals.FLOOR
        self.surface.set_colorkey(colors.TRANSPARENT)

    def update_surface(self, game_context):
        self.surface.fill(color=colors.BLACK)
        self.draw_border()
        self.update_health_image(game_context)
        self.update_score_image(game_context)
        self.update_special_weapon_image(game_context)

    def draw_border(self):
        pygame.draw.rect(self.surface, colors.BLUE, ((0,0), self.size), 3)

    def update_score_image(self, game_context):
        pass

    def update_health_image(self, game_context):
        x_offset = 10
        y_offset = 10
        img = game_context.game_master.sprite_master.get_image_name('heart')
        for i in range(min(self.player.health, 4)):
            self.surface.blit(img, (x_offset + (i*25), y_offset))

    def update_special_weapon_image(self, game_context):
        pass