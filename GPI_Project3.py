import pygame
import sys

class Player:
    def __init__(self, x=0, y=0, speed=5):
        """
        Player 클래스
        x, y: 플레이어의 초기 위치
        speed: 플레이어 이동 속도
        """
        self.x = x
        self.y = y
        self.speed = speed
        # 플레이어의 크기 및 모양 정의(여기서는 임시 Rect)
        self.width = 50
        self.height = 50
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx, dy):
        """
        플레이어의 위치를 변경한다.
        dx, dy: 이동할 방향 및 거리
        """
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """
        플레이어 상태 업데이트 (간단한 예: 아직 충돌 검사나 중력 없음)
        """
        pass

    def draw(self, screen):
        """
        플레이어를 화면에 그린다.
        """
        pygame.draw.rect(screen, self.color, self.rect)


def run_simulation():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("GPI Project 3 Simulation")

    clock = pygame.time.Clock()
    player = Player(x=screen_width//2, y=screen_height//2, speed=5)

    running = True
    while running:
        clock.tick(60)  # FPS 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        player.move(dx, dy)
        player.update()

        screen.fill((0, 0, 0))
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_simulation()
