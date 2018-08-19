import sys
import time
import os
import pygame
from galemojiga.GameInputs import get_input_dict
import galemojiga.globals
from galemojiga.game_contexts.main_game import MainGameContext


class GameMain:

    def __init__(self, window_size=galemojiga.globals.MAIN_WINDOW_SIZE):
        self.width = window_size[0]
        self.height = window_size[1]
        self.game_objects = []

        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)

        pygame.font.init()
        self.debug_font = pygame.font.SysFont('Comic Sans MS', 12)

        self.current_context = MainGameContext(window_size,
                                               player_count=2,
                                               debug_font=self.debug_font)

    @property
    def window_size(self):
        return (self.width, self.height)

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

if __name__ == "__main__":
    game = GameMain()
    game.run()