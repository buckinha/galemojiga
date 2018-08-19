import unittest
from galemojiga.game_objects.Bullets import Bullet
import galemojiga.globals as globals


class TestBulletCreate(unittest.TestCase):
    def setUp(self):
        pass

    def test_assign_integer_speed(self):
        speed = 10
        bullet_down = Bullet(game_context=None,
                             position=[0,0],
                             speed=speed,
                             launched_by='test',
                             strength=1)
        self.assertEqual(bullet_down.speed_horizontal, 0)
        self.assertEqual(bullet_down.speed_vertical, speed)


class TestBulletDismissal(unittest.TestCase):
    def setUp(self):
        self.bullet = Bullet(game_context=None,
                             position=[0,0],
                             speed=10,
                             launched_by='test',
                             strength=1)

    def tearDown(self):
        pass

    def test_dismissal_down(self):
        self.bullet.dead = False
        self.bullet.position=[-1000,-1000]
        self.bullet.update()
        self.assertTrue(self.bullet.dead)

    def test_dismissal_up(self):
        self.bullet.dead = False
        self.bullet.position=[1000,1000]
        self.bullet.update()
        self.assertTrue(self.bullet.dead)