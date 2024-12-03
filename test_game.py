# test_game.py
import unittest
from unittest.mock import Mock, patch
from GPI_Project3 import Game, Player, Bullet

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player = Player()
        self.bullet = Bullet()

    def test_player_movement(self):
        initial_position = self.player.position.copy()
        self.player.move('right')
        self.assertNotEqual(initial_position, self.player.position)

    def test_bullet_collision(self):
        self.bullet.position = self.player.position
        collision = self.game.check_collision(self.bullet, self.player)
        self.assertTrue(collision)

    @patch('game.Player')
    def test_reaction_on_hit(self, MockPlayer):
        mock_player = MockPlayer()
        mock_player.hit.return_value = 'Foot disabled'
        result = mock_player.hit('foot')
        self.assertEqual(result, 'Foot disabled')

if __name__ == '__main__':
    unittest.main()
