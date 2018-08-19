from galemojiga.game_objects.GameObject import GameObject
import galemojiga.globals as globals
import random

class PowerUp(GameObject):
    def __init__(self):
        super().__init__()

class PartyParrot(GameObject):

    def __init__(self):
        super().__init__()
        self.frame_list = ['parrot_{}'.format(i) for i in range(10)]
        self.frame_rate = 0.2
        self.dead = False
        self.direction = 'right'
        self.horizontal_speed = 5
        self.powerup = None
        self.powerup_launched = False
        drop_buffer = 50
        self.launch_point = random.randint(drop_buffer,
                                           globals.MAIN_WINDOW_SIZE[0]-drop_buffer)

    def update(self, game_context):
        super().update()

        if self.direction == 'right':
            self.position[0] += self.horizontal_speed
        elif self.direction == 'left':
            self.position[0] -= self.horizontal_speed

        buffer = 50
        if self.position[0] < (0 - buffer):
            self.dead = True
        if self.position[0] > globals.MAIN_WINDOW_SIZE[0] + buffer:
            self.dead = True

        buffer = self.horizontal_speed
        if self.powerup_launched is False:
            if self.position[0] < self.launch_point + buffer:
                if self.position[0] > self.launch_point - buffer:
                    self.powerup_launched = True
                    pup = PowerUp()
                    game_context.powerups.append(pup)