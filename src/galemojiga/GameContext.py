import pygame
import galemojiga.colors as colors

class GameContext:

    def __init__(self, game_master, size):
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.game_over = False
        self.game_master = game_master

    def update(self, screen, input_dict):
        self.surface.fill(colors.BLACK)
        screen.blit(self.surface, self.surface.get_rect())

    def trigger_game_over(self):
        self.game_over = True