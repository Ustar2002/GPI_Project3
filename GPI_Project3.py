# game.py
import pygame
import sys
import math

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GPI_Project3_2022105744")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 플레이어 클래스
class Player:
    def __init__(self):
        self.position = pygame.math.Vector2(WIDTH//2, HEIGHT//2)
        self.speed = 5
        self.image = pygame.Surface((50, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=self.position)
        self.alive = True
        self.disabled_limbs = []

    def move(self, direction):
        if direction == 'left':
            self.position.x -= self.speed
        elif direction == 'right':
            self.position.x += self.speed
        elif direction == 'up':
            self.position.y -= self.speed
        elif direction == 'down':
            self.position.y += self.speed
        self.rect.center = self.position

    def hit(self, limb):
        self.disabled_limbs.append(limb)
        return f"{limb.capitalize()} disabled"

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# 총알 클래스
class Bullet:
    def __init__(self, position, direction):
        self.position = pygame.math.Vector2(position)
        self.direction = pygame.math.Vector2(direction).normalize()
        self.speed = 10
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.position += self.direction * self.speed
        self.rect.center = self.position

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# 게임 클래스
class Game:
    def __init__(self):
        self.player = Player()
        self.bullets = []

    def check_collision(self, bullet, player):
        return bullet.rect.colliderect(player.rect)

    def run(self):
        running = True
        while running:
            screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # 총알 발사
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        mouse_pos = pygame.mouse.get_pos()
                        direction = pygame.math.Vector2(mouse_pos) - self.player.position
                        bullet = Bullet(self.player.position, direction)
                        self.bullets.append(bullet)

            # 플레이어 움직임
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.move('left')
            if keys[pygame.K_d]:
                self.player.move('right')
            if keys[pygame.K_w]:
                self.player.move('up')
            if keys[pygame.K_s]:
                self.player.move('down')

            # 총알 업데이트 및 충돌 체크
            for bullet in self.bullets[:]:
                bullet.update()
                bullet.draw(screen)
                if self.check_collision(bullet, self.player):
                    self.player.hit('foot')
                    self.bullets.remove(bullet)

            self.player.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
