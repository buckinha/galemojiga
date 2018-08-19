import pygame
import time

class GameObject:

    def __init__(self):
        self.position = [0, 0]
        self.hit_scale = [0, 0]
        self.hit_offset = [0, 0]
        self.size = [41,41]
        self.frame_list = [None]
        self.frame_index = 0
        self.frame_rate = 0.5
        self.frame_last_update = 0

    @property
    def rect(self):
        # TODO shouldn't instantiate this every time.
        return pygame.Rect((self.position), (self.size))

    @property
    def hit_rect(self):
        r = self.rect.inflate(*self.hit_scale)
        r = r.move(*self.hit_offset)
        return r

    @property
    def current_frame(self):
        return self.frame_list[self.frame_index]

    def update(self, game_context=None):
        # check next frame
        if time.time() - self.frame_last_update > self.frame_rate:
            self.frame_index += 1

        if self.frame_index >= len(self.frame_list):
            self.frame_index = 0