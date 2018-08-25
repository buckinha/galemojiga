import time
import random
import pygame
from pygame.locals import *
from galemojiga.GameContext import GameContext
from galemojiga.game_objects.Players import Player, MovementKeys
from galemojiga.game_contexts.levels import Level1, Level2, Level3, Level4, Level5, Level6
from galemojiga.game_objects.Effects import PartyParrotLeft, PartyParrotRight, PlayerStats
import galemojiga.SpriteHelpers as sprites
import galemojiga.colors as colors
import galemojiga.globals as globals


class MainGameContext(GameContext):

    def __init__(self, game_master, size, player_count=1,
                 difficulty=1, debug_font=None):
        if player_count > globals.MAX_PLAYERS:
            raise SystemExit

        super().__init__(game_master, size)

        self.player_count = player_count
        self.players = []
        self.player_stats_list = []
        self.player_scores = {}
        self.player_last_bonus_score = {}
        self.bonus_history = {}
        self.bonus_at = 100

        for i in range(1, self.player_count + 1):
            player = Player(game_context=self,
                            number=i,
                            movement_keys=MovementKeys(i))
            self.players.append(player)
            self.player_scores[i] = 0
            self.player_last_bonus_score[i] = 0
            self.bonus_history[i] = []
            status_obj = PlayerStats(player)
            self.player_stats_list.append(status_obj)

        self.effects = []
        self.enemies = []
        self.bullets = []
        self.powerups = []

        self.levels = [Level5(), Level1(), Level2(), Level3(), Level4(), Level5(), Level6()]
        self.level_index = 0
        self.new_level_delay = 5
        self.level_finish_time = 0

        self.debug_on = False
        self.debug_font = debug_font

    def trigger_game_over(self):
        self.quit_to_menu()

    def update(self, screen, input_dict):

        # TODO for now, i'm wiping the entire surface on each blit
        # TODO a better way would be to blit only sections that are changing
        self.surface.fill(colors.BLACK)

        # quit?
        self.check_quit(input_dict)

        # debug switches
        self.process_debug_switches(input_dict)

        # run level events
        self.process_level_events()

        # process effects
        self.process_effects()

        # process collisions
        self.process_player_collisions()
        self.process_bullet_collisions()

        # process player movement and shooting
        self.process_player_inputs(input_dict)

        # process enemy movement and behavior
        self.process_enemy_behavior()

        # proces bullets
        self.process_bullets()

        # process environment
        self.process_environment()
        self.process_powerups()

        self.draw_player_statuses()

        screen.blit(self.surface, self.surface.get_rect())

    def check_quit(self, input_dict):
        if K_ESCAPE in input_dict['key_up']:
            self.quit_to_menu()

    def quit_to_menu(self):
        self.game_master.reset_context('main_game')
        self.game_master.set_context('main_menu')

    def process_debug_switches(self, input_dict):
        if K_F8 in input_dict['key_up']:
            self.debug_on = not self.debug_on

        if not self.debug_on:
            return

        if self.debug_font is None:
            return

        # object counts
        bullet_t = 'BulletCount: {}'.format(len(self.bullets))
        textsurface = self.debug_font.render(bullet_t,
                                             True,
                                             (220, 220, 220))
        self.surface.blit(textsurface, (0, 0))

    def _current_level_or_None(self):
        if self.level_index >= len(self.levels):
            return None
        return self.levels[self.level_index]

    def process_level_events(self):

        level = self._current_level_or_None()

        if level is None:
            return

        # check if spawning is complete, and if so, if enemies are all killed
        if level.spawning_complete and level.complete is False:
            if len(self.enemies) == 0:
                level.complete = True
                self.level_finish_time = time.time()


        if level.complete:
            if time.time() - self.level_finish_time >= self.new_level_delay:
                self.level_index += 1
            else:
                time_left = str(int(5 - (time.time() - self.level_finish_time)))
                print("New Level in: {}".format(time_left))

        level.update(self)

    def add_party_parrots(self):
        for player in self.players:
            p_score = self.player_scores[player.number]
            last_bonus = self.player_last_bonus_score[player.number]
            if p_score - last_bonus > self.bonus_at:
                new_parrot = random.choice([PartyParrotLeft, PartyParrotRight])
                self.effects.append(new_parrot())
                self.player_last_bonus_score[player.number] = p_score


    def process_effects(self):
        self.add_party_parrots()
        for eff in self.effects:
            eff.update(game_context=self)
            self.surface.blit(self.game_master.sprite_master.get_image_name(eff.current_frame), eff.rect)

    def process_player_collisions(self):
        for player in self.players:
            for enemy in self.enemies:
                if player.hit_rect.colliderect(enemy.hit_rect):
                    player.hit_by(enemy)
                    enemy.hit_by(player)
            for pup in self.powerups:
                if player.hit_rect.colliderect(pup.hit_rect):
                    pup.affect_player(player)

    def process_bullet_collisions(self):
        for bullet in self.bullets:
            if bullet.launched_by == 'enemy':
                for player in self.players:
                    if bullet.hit_rect.colliderect(player.hit_rect):
                        player.hit_by(bullet)
                        bullet.hit_by(player)
            else:
                # player bullets
                for enemy in self.enemies:
                    if bullet.hit_rect.colliderect(enemy.hit_rect):
                        enemy.hit_by(bullet)
                        bullet.hit_by(enemy)
                        self.player_scores[bullet.launched_by] += 1

        self.enemies = [e for e in self.enemies if not e.dead]
        self.bullets = [b for b in self.bullets if not b.dead]

    def process_player_inputs(self, input_dict):
        for player in self.players:
            player.update(input_dict)
            self.surface.blit(self.game_master.sprite_master.get_image_name(
                player.current_frame), player.rect)
            if self.debug_on:
                pygame.draw.rect(self.surface, colors.BLUE,
                                 player.hit_rect, 1)

    def process_enemy_behavior(self):
        for enemy in self.enemies:
            enemy.update(game_context=self)
            img_name = enemy.current_frame
            self.surface.blit(self.game_master.sprite_master.get_image_name(img_name),
                              enemy.rect)
            if self.debug_on:
                pygame.draw.rect(self.surface, colors.RED,
                                 enemy.hit_rect, 1)

    def process_bullets(self):
        for bullet in self.bullets:
            bullet.update(game_context=self)
            self.surface.blit(self.game_master.sprite_master.get_image_name(bullet.current_frame), bullet.rect)
            if self.debug_on:
                pygame.draw.rect(self.surface, colors.RED,
                                 bullet.hit_rect, 1)

    def process_powerups(self):
        for pup in self.powerups:
            pup.update(game_context=self)
            self.surface.blit(self.game_master.sprite_master.get_image_name(pup.current_frame), pup.rect)
            if self.debug_on:
                pygame.draw.rect(self.surface, colors.GREEN,
                                 pup.hit_rect, 1)
        self.powerups = [p for p in self.powerups if not p.dead]

    def process_environment(self):
        return None

    def draw_player_statuses(self):
        for stats in self.player_stats_list:
            stats.update_surface(game_context=self)
            # the stats objects update their own surface, so just blit it
            self.surface.blit(stats.surface, stats.rect)






