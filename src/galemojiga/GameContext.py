import pygame
import galemojiga.colors as colors

class GameContext:

    def __init__(self, size):
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.game_over = False

    def update(self, screen, input_dict):
        self.surface.fill(colors.BLACK)
        screen.blit(self.surface, self.surface.get_rect())

    def trigger_game_over(self):
        self.game_over = True