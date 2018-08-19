import pygame

class GameObject:

    def __init__(self):
        self.position = [0, 0]
        self.hit_scale = [0, 0]
        self.hit_offset = [0, 0]
        self.size = [41,41]

    @property
    def rect(self):
        # TODO shouldn't instantiate this every time.
        return pygame.Rect((self.position), (self.size))

    @property
    def hit_rect(self):
        r = self.rect.inflate(*self.hit_scale)
        r = r.move(*self.hit_offset)
        return r


