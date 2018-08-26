import time
import random
import pygame
from pygame.locals import *
from galemojiga.GameContext import GameContext
import galemojiga.colors as colors
import galemojiga.globals as globals


class MainMenuContext(GameContext):

    def __init__(self, game_master, size, player_count=1, debug_font=None):
        super().__init__(game_master, size)

        col1_x = 100 - 30
        col2_x = 300 - 30
        row1_y = 200
        row2_y = 250
        row3_y = 300
        button_y = 370
        self.selector_positions = {'players_1': (col1_x, row1_y),
                                   'players_2': (col1_x, row2_y),
                                   'players_3': (col1_x, row3_y),
                                   'difficulty_1': (col2_x, row1_y),
                                   'difficulty_2': (col2_x, row2_y),
                                   'difficulty_3': (col2_x, row3_y),
                                   'start': (col1_x, button_y),
                                   'quit': (col2_x, button_y)}

        self.selector_position = 'start'

    def update(self, screen, input_dict):
        self.surface.fill(colors.BLACK)

        self.draw_player_options()

        self.draw_start_quit_buttons()

        self.draw_selector(input_dict)
        self.draw_selection_arrows()

        screen.blit(self.surface, self.surface.get_rect())

        if K_RETURN in input_dict['key_up']:
            if self.selector_position == 'start':
                self.game_master.reset_context('main_game')
                self.game_master.set_context('main_game')
            if self.selector_position == 'quit':
                self.game_over = True
            elif self.selector_position == 'players_1':
                self.game_master.player_count = 1
            elif self.selector_position == 'players_2':
                self.game_master.player_count = 2
            elif self.selector_position == 'players_3':
                self.game_master.player_count = 3
            elif self.selector_position == 'difficulty_1':
                self.game_master.difficulty = 1
            elif self.selector_position == 'difficulty_2':
                self.game_master.difficulty = 2
            elif self.selector_position == 'difficulty_3':
                self.game_master.difficulty = 3

    def draw_player_selector_static_elements(self):

        # making a shortcut for ease of typing
        p = self.selector_positions

        player_select_text = 'Select Players'
        textsurface = self.game_master.menu_font.render(player_select_text,
                                                        True,
                                                        (220, 220, 220))
        text_pos = (p['players_1'][0], p['players_1'][1] - 30)
        self.surface.blit(textsurface, text_pos)
        img = self.game_master.sprite_master.get_image('objects',
                                                       (4, 10),
                                                       scale=globals.NORMAL_SCALE)

        def _add(t1, t2):
            return (t1[0] + t2[0], t1[1] + t2[1])

        controller_positions = [p['players_1'],
                                p['players_2'], _add(p['players_2'], (40, 0)),
                                p['players_3'], _add(p['players_3'], (40, 0)), _add(p['players_3'], (80, 0))]
        for pos in controller_positions:
            self.surface.blit(img, pos)

    def draw_difficulty_selector_static_elements(self):
        # making a shortcut for ease of typing
        p = self.selector_positions

        player_select_text = 'Select Difficulty'
        textsurface = self.game_master.menu_font.render(player_select_text,
                                                        True,
                                                        (220, 220, 220))
        text_pos = (p['difficulty_1'][0], p['difficulty_1'][1] - 30)
        self.surface.blit(textsurface, text_pos)
        img = self.game_master.sprite_master.get_image('people',
                                                       (13, 14),
                                                       scale=globals.NORMAL_SCALE)

        def _add(t1, t2):
            return (t1[0] + t2[0], t1[1] + t2[1])

        controller_positions = [p['difficulty_1'],
                                p['difficulty_2'], _add(p['difficulty_2'], (40, 0)),
                                p['difficulty_3'], _add(p['difficulty_3'], (40, 0)), _add(p['difficulty_3'], (80, 0))]
        for pos in controller_positions:
            self.surface.blit(img, pos)

    def draw_player_options(self):
        self.draw_player_selector_static_elements()
        self.draw_difficulty_selector_static_elements()

    def draw_start_quit_buttons(self):
        start_image_text = self.game_master.menu_font.render('START',
                                                        True,
                                                        (220, 220, 220))

        quite_image_text = self.game_master.menu_font.render('QUIT',
                                                        True,
                                                        (220, 220, 220))
        pos_start = list(self.selector_positions['start'])
        pos_start[1] += 10
        pos_quit = list(self.selector_positions['quit'])
        pos_quit[1] += 10
        self.surface.blit(start_image_text, pos_start)
        self.surface.blit(quite_image_text, pos_quit)

    def move_selector(self, input_dict):
        if (K_UP in input_dict['key_up']) or \
           (K_w in input_dict['key_up']):

            if self.selector_position == 'players_1':
                self.selector_position = 'start'
            elif self.selector_position == 'players_2':
                self.selector_position = 'players_1'
            elif self.selector_position == 'players_3':
                self.selector_position = 'players_2'
            elif self.selector_position == 'start':
                self.selector_position = 'players_3'

            elif self.selector_position == 'difficulty_1':
                self.selector_position = 'quit'
            elif self.selector_position == 'difficulty_2':
                self.selector_position = 'difficulty_1'
            elif self.selector_position == 'difficulty_3':
                self.selector_position = 'difficulty_2'
            elif self.selector_position == 'quit':
                self.selector_position = 'difficulty_3'

        if K_DOWN in input_dict['key_up'] or \
           (K_s in input_dict['key_up']):
            if self.selector_position == 'start':
                self.selector_position = 'players_1'
            elif self.selector_position == 'players_1':
                self.selector_position = 'players_2'
            elif self.selector_position == 'players_2':
                self.selector_position = 'players_3'
            elif self.selector_position == 'players_3':
                self.selector_position = 'start'

            elif self.selector_position == 'quit':
                self.selector_position = 'difficulty_1'
            elif self.selector_position == 'difficulty_1':
                self.selector_position = 'difficulty_2'
            elif self.selector_position == 'difficulty_2':
                self.selector_position = 'difficulty_3'
            elif self.selector_position == 'difficulty_3':
                self.selector_position = 'quit'

        if K_LEFT in input_dict['key_up'] or \
           (K_a in input_dict['key_up']):
            if self.selector_position == 'difficulty_1':
                self.selector_position = 'players_1'
            elif self.selector_position == 'difficulty_2':
                self.selector_position = 'players_2'
            elif self.selector_position == 'difficulty_3':
                self.selector_position = 'players_3'
            elif self.selector_position == 'players_1':
                self.selector_position = 'difficulty_1'
            elif self.selector_position == 'players_2':
                self.selector_position = 'difficulty_2'
            elif self.selector_position == 'players_3':
                self.selector_position = 'difficulty_3'
            elif self.selector_position == 'start':
                self.selector_position = 'quit'
            elif self.selector_position == 'quit':
                self.selector_position = 'start'

        if K_RIGHT in input_dict['key_up'] or \
           (K_d in input_dict['key_up']):
            if self.selector_position == 'players_1':
                self.selector_position = 'difficulty_1'
            elif self.selector_position == 'players_2':
                self.selector_position = 'difficulty_2'
            elif self.selector_position == 'players_3':
                self.selector_position = 'difficulty_3'
            elif self.selector_position == 'difficulty_1':
                self.selector_position = 'players_1'
            elif self.selector_position == 'difficulty_2':
                self.selector_position = 'players_2'
            elif self.selector_position == 'difficulty_3':
                self.selector_position = 'players_3'
            elif self.selector_position == 'start':
                self.selector_position = 'quit'
            elif self.selector_position == 'quit':
                self.selector_position = 'start'

    def draw_selector(self, input_dict):

        self.move_selector(input_dict)

        size = (170, 50)
        offset = (-5, -5)
        pos = self.selector_positions[self.selector_position]
        r = (pos[0] + offset[0],
             pos[1] + offset[1],
             size[0], size[1])
        pygame.draw.rect(self.surface, colors.BLUE, r, 3)

    def draw_player_selector_arrow(self, player_number):
        img = self.game_master.sprite_master.get_image('symbols', (2, 14))
        h_offset = 120

        pos = list(self.selector_positions['players_{}'.format(player_number)])
        pos[0] += h_offset
        self.surface.blit(img, pos)

    def draw_difficulty_selector_arrow(self, difficulty):
        img = self.game_master.sprite_master.get_image('symbols', (2, 14))
        h_offset = 120

        pos = list(self.selector_positions['difficulty_{}'.format(difficulty)])
        pos[0] += h_offset
        self.surface.blit(img, pos)

    def draw_selection_arrows(self):

        self.draw_player_selector_arrow(self.game_master.player_count)
        self.draw_difficulty_selector_arrow(self.game_master.difficulty)