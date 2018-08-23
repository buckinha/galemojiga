import pygame
import time
import random
import galemojiga.globals as globals

class GameObject:

    def __init__(self):
        self.x = globals.LEFT_WALL
        self.y = globals.CEILING

        self.speed_h = 5
        self.speed_v = 5

        self.move_list = [self._hold]
        self.move_index = 0

        self.move_memory = None

        self.hit_scale = [0, 0]
        self.hit_offset = [0, 0]

        self.size = [41,41]

        self.frame_list = [None]
        self.frame_index = 0
        self.frame_rate = 0.5
        self.frame_last_update = 0

        self.dead = False

    @property
    def position(self):
        return [self.x, self.y]

    @position.setter
    def position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    @property
    def rect(self):
        # TODO shouldn't instantiate this every time.
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    @property
    def hit_rect(self):
        r = self.rect.inflate(*self.hit_scale)
        r = r.move(*self.hit_offset)
        return r

    @property
    def current_frame(self):
        return self.frame_list[self.frame_index]


    def update(self, game_context):
        self.do_move()

        # check next frame
        now = time.time()
        if now - self.frame_last_update > self.frame_rate:
            self.frame_index += 1
            self.frame_last_update = now

        if self.frame_index >= len(self.frame_list):
            self.frame_index = 0

    def do_move(self):
        # there are no moves in the move list, so just hold still
        if len(self.move_list) == 0:
            return

        # if for whatever reason we've gone past the end of the list, just go back
        if self.move_index > len(self.move_list):
            self.move_index = 0

        # now actually do the thing by calling the function stored in the list
        # if the item is itself a list, the first item is the handle, and the
        # rest of the items are it's args
        mv_item = self.move_list[self.move_index]
        if hasattr(mv_item, '__iter__'):
            mv_item[0](*mv_item[1:])
        else:
            mv_item()

    def _next_move(self):
        self.move_memory = None
        self.move_index += 1
        if self.move_index >= len(self.move_list):
            self.move_index = 0

    def _move_left_to_unit(self, to_unit):
        self.x -= self.speed_h
        if self.x < globals.LEFT_WALL:
            self.x = globals.LEFT_WALL
        if self.x < to_unit * globals.UNIT:
            self._next_move()

    def _move_right_to_unit(self, to_unit):
        self.x += self.speed_h
        if self.x + self.size[0] > globals.RIGHT_WALL:
            self.x = globals.RIGHT_WALL - self.size[0]
        if self.x > to_unit * globals.UNIT:
            self._next_move()

    def _move_down_to_unit(self, to_unit):
        self.y += self.speed_v
        if self.y + self.size[1] >= globals.FLOOR:
            self.y = globals.FLOOR - self.size[1]
        if self.y >= to_unit * globals.UNIT:
            self._next_move()

    def _move_up_to_unit(self, to_unit):
        self.y -= self.speed_v
        if self.y <= globals.CEILING:
            self.y = globals.CEILING
        if self.y <= to_unit * globals.UNIT:
            self._next_move()

    def _move_right_random(self, i, out_of):
        if random.randint(0, out_of) <= i:
            self._next_move()
        else:
            self._move_right_to_wall()

    def _move_left_random(self, i, out_of):
        if random.randint(0, out_of) <= i:
            self._next_move()
        else:
            self._move_left_to_wall()

    def _move_down_random(self, i, out_of):
        if random.randint(0, out_of) <= i:
            self._next_move()
        else:
            self._move_down_to_floor()

    def _move_up_random(self, i, out_of):
        if random.randint(0, out_of) <= i:
            self._next_move()
        else:
            self._move_up_to_ceiling()

    def _move_left_to_wall(self):
        self._move_left_to_unit(0)
        if self.x <= globals.LEFT_WALL:
            self._next_move()

    def _move_right_to_wall(self):
        self._move_right_to_unit(globals.H_UNITS)
        if self.x >= globals.RIGHT_WALL - self.size[0]:
            self._next_move()

    def _move_down_to_floor(self):
        self._move_down_to_unit(globals.V_UNITS)
        if self.y + self.size[1] >= globals.FLOOR:
            self._next_move()

    def _move_up_to_ceiling(self):
        self._move_up_to_unit(0)
        if self.y <= globals.CEILING:
            self._next_move()

    def _move_down_one_unit(self):
        # remember the current y value, if this is the first time
        if self.move_memory is None:
            self.move_memory = self.y

        self.y += self.speed_v

        if self.y - self.move_memory >= globals.UNIT:
            self.y = self.move_memory + globals.UNIT
            self._next_move()

    def _move_up_one_unit(self):
        # remember the current y value, if this is the first time
        if self.move_memory is None:
            self.move_memory = self.y

        self.y -= self.speed_v

        if self.move_memory - self.y <= globals.UNIT:
            self.y = self.move_memory - globals.UNIT
            self._next_move()

    def _move_right_one_unit(self):
        # remember the current x value, if this is the first time
        if self.move_memory is None:
            self.move_memory = self.x

        self.x += self.speed_h

        if self.x - self.move_memory >= globals.UNIT:
            self.x = self.move_memory + globals.UNIT
            self._next_move()

    def _move_left_one_unit(self):
        # remember the current x value, if this is the first time
        if self.move_memory is None:
            self.move_memory = self.x

        self.x -= self.speed_h

        if self.move_memory - self.x <= globals.UNIT:
            self.x = self.move_memory - globals.UNIT
            self._next_move()

    def _move_down_forever(self):
        self.y += self.speed_v
        if self.y > globals.FLOOR + 100:
            self.dead = True

    def _move_up_forever(self):
        self.y -= self.speed_v
        if self.y <= -100:
            self.dead = True

    def _move_left_forever(self):
        self.x -= self.speed_h
        if self.x < globals.LEFT_WALL - 100:
            self.dead = True

    def _move_right_forever(self):
        self.x += self.speed_h
        if self.x >= globals.RIGHT_WALL + 100:
            self.dead = True

    def _hold(self):
        # just stay put
        return