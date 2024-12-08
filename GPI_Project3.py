import pygame
import sys

class Player:
    def __init__(self, x=0, y=0, speed=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Bullet:
    def __init__(self, x, y, speed=10):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 5
        self.height = 5
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        # 탄환은 단순히 오른쪽으로 이동한다고 가정
        self.x += self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Gun:
    def __init__(self, x=0, y=0, ammo=10, recoil_amount=5):
        self.x = x
        self.y = y
        self.ammo = ammo
        self.recoil_amount = recoil_amount

    def fire(self):
        """
        총 발사:
        - 탄약이 0보다 크면 발사 가능
        - 탄환 생성 및 반환
        - 반동으로 총의 x 위치가 recoil_amount 만큼 왼쪽으로 이동
        - 탄약 감소
        """
        if self.ammo > 0:
            bullet = Bullet(self.x, self.y)
            self.ammo -= 1
            self.x -= self.recoil_amount  # 간단한 반동 처리
            return bullet
        else:
            return None

def run_simulation():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("GPI Project 3 Simulation")

    clock = pygame.time.Clock()
    player = Player(x=screen_width//2, y=screen_height//2, speed=5)
    gun = Gun(x=player.x + player.width//2, y=player.y + player.height//2, ammo=5)
    bullets = []

    running = True
    while running:
        clock.tick(60)  # FPS 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = gun.fire()
                    if bullet:
                        bullets.append(bullet)

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

        # 총 위치를 플레이어 중앙으로 맞춰준다(단순 구현)
        gun.x = player.x + player.width//2
        gun.y = player.y + player.height//2

        # 탄환 업데이트
        for b in bullets:
            b.update()

        screen.fill((0, 0, 0))
        player.draw(screen)

        for b in bullets:
            b.draw(screen)

        # 총을 가시화(여기서는 플레이어 위치 위에 작은 박스로 표시)
        pygame.draw.rect(screen, (0,255,0), (gun.x, gun.y, 10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_simulation()
