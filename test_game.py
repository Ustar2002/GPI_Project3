import unittest
from GPI_Project3 import Player

class TestPlayerMovement(unittest.TestCase):
    def setUp(self):
        # 각 테스트마다 새로운 플레이어 인스턴스 생성
        self.player = Player(x=100, y=100, speed=5)

    def test_initial_position(self):
        # 플레이어 초기 위치 테스트
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 100)

    def test_move_right(self):
        # 오른쪽 이동 테스트
        self.player.move(1, 0)  # dx=1, dy=0
        self.assertEqual(self.player.x, 100 + 5)
        self.assertEqual(self.player.y, 100)

    def test_move_left(self):
        # 왼쪽 이동 테스트
        self.player.move(-1, 0)
        self.assertEqual(self.player.x, 100 - 5)
        self.assertEqual(self.player.y, 100)

    def test_move_up(self):
        # 위쪽 이동 테스트
        self.player.move(0, -1)
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 100 - 5)

    def test_move_down(self):
        # 아래쪽 이동 테스트
        self.player.move(0, 1)
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 100 + 5)


if __name__ == '__main__':
    unittest.main()
