import random
import pygame
from galemojiga.game_objects.GameObject import GameObject
import galemojiga.globals as globals
import galemojiga.colors as colors
from galemojiga.game_objects.PowerUps import *



class PartyParrotLeft(GameObject):

    def __init__(self):
        super().__init__()
        self.frame_list = ['parrot_{}'.format(i) for i in range(10)]
        self.frame_rate = 0.05
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
                    pup = pick_powerup(game_context)
                    pup.x = self.x
                    pup.y = self.y+10
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
        self.size = [(globals.WINDOW_WIDTH/3)-25, 95]
        self.surface = pygame.Surface(self.rect.size)
        self.x = (self.player.number - 1) * (self.size[0]) + (4 * self.player.number)
        self.y = globals.FLOOR
        self.surface.set_colorkey(colors.TRANSPARENT)
        self.scoreboard = Scoreboard()

    def update_surface(self, game_context):
        self.surface.fill(color=colors.BLACK)
        self.update_health_image(game_context)
        self.update_score_image(game_context)
        self.update_special_weapon_image(game_context)
        self.draw_border()

    def draw_border(self):
        if self.player.number == 1:
            color = colors.BLUE
        elif self.player.number == 2:
            color = colors.LIGHTGREY
        else:
            color = colors.DARKGREY
        pygame.draw.rect(self.surface, color, ((0,0), self.size), 3)

    def update_score_image(self, game_context):
        x_offset = 10
        y_offset = 60
        score = game_context.player_scores[self.player.number]
        img = self.scoreboard.get_scoreboard(score, game_context)
        self.surface.blit(img, (x_offset, y_offset))

    def update_health_image(self, game_context):
        x_offset = 10
        y_offset = 10
        sprites_to_draw = min(self.player.health, self.player.max_health)
        img = game_context.game_master.sprite_master.get_image_name('heart')
        for i in range(sprites_to_draw):
            self.surface.blit(img, (x_offset + ((4-i)*25), y_offset))

    def update_special_weapon_image(self, game_context):
        if self.player.special_gun is not None:
            x_offset = 10
            y_offset = 35
            sprites_to_draw = min(int(self.player.special_gun.shots), 5)
            r_justify_offset = (5 - sprites_to_draw) * 25
            sprite = self.player.special_gun.powerup_sprite
            img = game_context.game_master.sprite_master.get_image_name(sprite)
            for i in range(sprites_to_draw):
                self.surface.blit(img, (x_offset + r_justify_offset + (i*25), y_offset))


class Scoreboard(GameObject):

    def __init__(self):
        super().__init__()
        self.size = [(globals.WINDOW_WIDTH/3)-25, 25]
        self.surface = pygame.Surface(self.rect.size)

    def get_digits(self, score):
        if score <= 0:
            return [0]

        s = int(score)
        digits = []
        while s / 10 >= 1:
            digits.append(s % 10)
            s = int(s / 10)
        digits.append(s)

        return [i for i in reversed(digits)]

    def get_scoreboard(self, score, game_context):
        self.surface.fill(color=colors.BLACK)
        digits = self.get_digits(score)
        w = globals.ENEMY_SCALE[0]
        h = globals.ENEMY_SCALE[1]

        #right-justify
        offset = 0
        if len(digits) <= 4:
            offset = (5 - len(digits)) * w

        for i in range(len(digits)):
            img = game_context.game_master.sprite_master.get_image_name(str(digits[i]))
            self.surface.blit(img, ((i*w + offset, 0), (w, h)))
        return self.surface