# test_game.py (업데이트)
import unittest
from unittest.mock import Mock, patch
from GPI_Project3 import Game, Player, Bullet

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player = self.game.player
        self.bullet = Bullet(self.player.position, (1, 0))

    def test_player_movement(self):
        initial_position = self.player.position.copy()
        self.player.move('right')
        self.assertNotEqual(initial_position, self.player.position)
        self.assertEqual(self.player.position.x, initial_position.x + self.player.speed)

    def test_bullet_movement(self):
        initial_position = self.bullet.position.copy()
        self.bullet.update()
        self.assertNotEqual(initial_position, self.bullet.position)

    def test_bullet_collision(self):
        self.bullet.rect.center = self.player.rect.center
        collision = self.game.check_collision(self.bullet, self.player)
        self.assertTrue(collision)

    def test_reaction_on_hit(self):
        self.player.hit('foot')
        self.assertIn('foot', self.player.disabled_limbs)

if __name__ == '__main__':
    unittest.main()
