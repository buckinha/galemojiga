import sys
import time
import os
import pygame
from galemojiga.GameInputs import get_input_dict
import galemojiga.globals
from galemojiga.game_contexts.main_game import MainGameContext
from galemojiga.game_contexts.main_menu import MainMenuContext
from galemojiga.SpriteSheet import SpriteSheet
import galemojiga.globals as globals


class GameMaster:

    def __init__(self, window_size=galemojiga.globals.MAIN_WINDOW_SIZE):
        self.width = window_size[0]
        self.height = window_size[1]
        self.game_objects = []
        self.player_count = 1
        self.difficulty = 1

        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)

        pygame.font.init()
        self.debug_font = pygame.font.SysFont('Comic Sans MS', 12)
        self.menu_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.sprite_master = SpriteMaster()

        self.contexts = {
            'main_menu': MainMenuContext(self, window_size),
            'main_game': None,
            'high_score': None
        }
        self.current_context = self.contexts['main_menu']

    @property
    def window_size(self):
        return (self.width, self.height)

    def set_context(self, context_name):
        if context_name in self.contexts:
            print('Setting Context to: {}'.format(context_name))
            self.current_context = self.contexts[context_name]

    def reset_context(self, context_name):
        if context_name == 'main_menu':
            self.contexts['main_menu'] = MainMenuContext(game_master=self,
                                                         size=self.window_size)
        if context_name == 'main_game':
            self.contexts['main_game'] = MainGameContext(game_master=self,
                                                         size=self.window_size,
                                                         player_count=self.player_count,
                                                         difficulty=self.difficulty,
                                                         debug_font=self.debug_font)

    def run(self):

        while True:
            events = [e for e in pygame.event.get()]

            # check quit
            for event in events:
                if event.type == pygame.QUIT: sys.exit()

            event_dict = get_input_dict(events)

            self.current_context.update(self.screen, event_dict)

            if self.current_context.game_over:
                break

            pygame.display.flip()
            time.sleep(0.02)


class SpriteMaster:
    def __init__(self):
        self.sprite_sheets = {
            'people': SpriteSheet('emojione-sprite-40-people.png'),
            'objects': SpriteSheet('emojione-sprite-40-objects.png'),
            'food': SpriteSheet('emojione-sprite-40-food.png'),
            'nature': SpriteSheet('emojione-sprite-40-nature.png'),
            'symbols': SpriteSheet('emojione-sprite-40-symbols.png'),
            'travel': SpriteSheet('emojione-sprite-40-travel.png'),
            'activity': SpriteSheet('emojione-sprite-40-activity.png')
        }

    def get_image(self, sheet, position):
        if sheet in self.sprite_sheets:
            return self.sprite_sheets[sheet].image_at(position)
        else:
            return None

if __name__ == "__main__":
    game = GameMaster()
    game.run()