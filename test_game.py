import unittest
from GPI_Project3 import Player, Gun, Bullet

class TestPlayerMovement(unittest.TestCase):
    def setUp(self):
        self.player = Player(x=100, y=100, speed=5)

    def test_initial_position(self):
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 100)

    def test_move_right(self):
        self.player.move(1, 0)
        self.assertEqual(self.player.x, 105)
        self.assertEqual(self.player.y, 100)

    def test_move_left(self):
        self.player.move(-1, 0)
        self.assertEqual(self.player.x, 95)
        self.assertEqual(self.player.y, 100)

    def test_move_up(self):
        self.player.move(0, -1)
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 95)

    def test_move_down(self):
        self.player.move(0, 1)
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 105)

class TestGun(unittest.TestCase):
    def setUp(self):
        self.gun = Gun(x=50, y=50, ammo=3, recoil_amount=5)

    def test_initial_ammo(self):
        self.assertEqual(self.gun.ammo, 3)

    def test_fire_bullet(self):
        bullet = self.gun.fire()
        self.assertIsInstance(bullet, Bullet)
        self.assertEqual(self.gun.ammo, 2)  # 탄약 감소 확인

    def test_recoil(self):
        old_x = self.gun.x
        self.gun.fire()
        self.assertEqual(self.gun.x, old_x - 5)  # 반동으로 x좌표 감소 확인

    def test_no_ammo_fire(self):
        self.gun.ammo = 0
        bullet = self.gun.fire()
        self.assertIsNone(bullet)  # 탄환 발사 불가시 None 반환 확인


if __name__ == '__main__':
    unittest.main()
