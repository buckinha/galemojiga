import os
import pygame
from galemojiga.SpriteSheet import SpriteSheet
import galemojiga.globals as globals
import galemojiga.colors as colors


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

        self.image_name_dict = {
            'heart': ['symbols', [16, 10]],
            'heart_box': ['symbols', [6, 8]],
            'coffee': ['food', [8,9]],
            'clinking_glasses': ['food', [8, 2]],
            'sushi_bento': ['food', [7, 1]],
            'sushi_rice': ['food', [5, 1]],
            'tempura': ['food', [6, 1]],
            'nigiri': ['food', [6, 0]],
            'dumpling': ['food', [9, 3]],
            'chili': ['food', [2,0]],
            'flame': ['nature', [10,10]],
            'candy': ['food', [3,6]],
            'lollypop': ['food', [4, 6]],
            'helicopter': ['travel', [1, 7]],
            'bomb': ['objects', [3, 4]],
            'train_0': ['travel', [2, 7]],
            'train_1': ['travel', [3, 7]],
            'p1_bullet': ['symbols', [11, 7], globals.BULLET_SCALE],
            'p2_bullet': ['symbols', [7, 15], globals.BULLET_SCALE],
            'p3_bullet': ['symbols', [8, 15], globals.BULLET_SCALE],
            'orange_bullet': ['symbols', [11, 10], globals.BULLET_SCALE],
            'smile': ['people', [5, 15]],
            'wink': ['people', [6, 13]],
            'cryer_1': ['people', [3, 14]],
            'cryer_2': ['people', [14, 13]],
            'tear': ['nature', [7, 10], globals.BULLET_SCALE],
            'devil': ['people', [5, 13]],
            'crazy_1': ['people', [14, 10]],
            'crazy_2': ['people', [14, 11]],
            'crazy_3': ['people', [17, 10]],
            'crazy_4': ['people', [14, 12]],
            'monkey_1': ['nature', [11, 3]],
            'monkey_2': ['nature', [11, 4]],
            'monkey_3': ['nature', [11, 5]],
            'coconut': ['food', [0, 9]],
            'banana': ['food', [1, 3]],
            'selfie': ['people', [1,17]],
            'poop': ['people', [10,12]],
            '0': ['symbols', [2, 0]],
            '1': ['symbols', [0, 2]],
            '2': ['symbols', [2, 2]],
            '3': ['symbols', [3, 1]],
            '4': ['symbols', [0, 3]],
            '5': ['symbols', [2, 3]],
            '6': ['symbols', [4, 0]],
            '7': ['symbols', [4, 2]],
            '8': ['symbols', [0, 4]],
            '9': ['symbols', [2, 4]],
            'vampire_1': ['people', [18,2]],
            'vampire_2': ['people', [18,3]],
            'bat': ['nature', [3, 11]],
            'zombie_1': ['people', [18, 14]],
            'zombie_2': ['people', [18, 15]],
            'ghost': ['people', [9, 11]],
            'santa': ['people', [0, 1]],
            'snowflake': ['nature', [7, 12], globals.BULLET_SCALE],
            'penguin': ['nature', [9,8]],
            'snowman_1': ['nature', [3,12]],
            'snowman_2': ['nature', [12,10]],
            'cloud': ['nature', [12, 9]],
            'fish': ['nature', [9,0], globals.BULLET_SCALE],
            'present': ['objects', [0,1]],
            'football': ['activity', [4,5]],
            'paint_pallet': ['activity', [0,2]],
            'socks': ['people', [4, 18]],
            'book': ['objects', [0, 7]],
            'racecar': ['travel', [4,1]]
        }

        # add cars:
        for i in range(8):
            self.image_name_dict['car_{}'.format(i)] = ['travel', (i, 8)]


    def get_image(self, sheet, position, scale=globals.ENEMY_SCALE):
        if sheet in self.sprite_sheets:
            img = self.sprite_sheets[sheet].image_at(position)
            return pygame.transform.smoothscale(img, scale)
        else:
            return None

    def get_image_name(self, name, scale=globals.ENEMY_SCALE):

        if 'parrot' in name:
            return self.load_party_parrot_image(name)

        if '_ship' in name:
            return self.load_player_image(name)

        if name in self.image_name_dict:
            sheet = self.image_name_dict[name][0]
            pos = self.image_name_dict[name][1]
            if len(self.image_name_dict[name]) > 2:
                scl = self.image_name_dict[name][2]
            else:
                scl = scale
            return self.get_image(sheet, pos, scl)
        else:
            raise KeyError('Key "{}" not found in SpriteMaster name dictionary'.format(name))

    def load_player_image(self, player_frame):
        # load_base_ship
        ship_image = self.get_image('travel', (0, 7), globals.NORMAL_SCALE)
        ship_image = pygame.transform.rotate(ship_image, 45)

        # add bullet for color
        if player_frame == 'p1_ship':
            bullet = self.get_image_name('p1_bullet')
        elif player_frame == 'p2_ship':
            bullet = self.get_image_name('p2_bullet')
        else:
            bullet = self.get_image_name('p3_bullet')
        ship_image.blit(source=bullet, dest=(21, 15))
        return ship_image

    def load_party_parrot_image(self, parrot_frame):
        path = os.path.join(globals.IMAGE_DIR, '{}.png'.format(parrot_frame))
        img = load_image(path).convert()
        img.set_colorkey(colors.TRANSPARENT)
        return pygame.transform.smoothscale(img, (25,25))


def load_image(filename):
    try:
        if not os.path.exists(filename):
            print(os.listdir(os.path.split(filename)[0]))
        img = pygame.image.load(filename)
        img.set_colorkey(colors.TRANSPARENT)
        return img

    except pygame.error as e:
        print('Unable to load spritesheet image: {}'.format(filename))
        print(e)
        raise SystemExit