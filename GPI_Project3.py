<<<<<<< HEAD
import sys
import math
import random 
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2022105744_project3")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 24)

# ---------------------
# 엔티티 클래스 정의
# ---------------------

class PlayerSpawnPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.size = 10

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # 화면 밖으로 나가지 않도록 제한
        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (int(self.x), int(self.y)), self.size)


class Projectile:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.speed = 10
        # 방향 벡터 계산
        dx = target_x - start_x
        dy = target_y - start_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:
            dist = 1
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed
        self.size = 5

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.size)

    def is_off_screen(self):
        return (self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT)

# 버스, 스틱맨 등 강체 관련 설정
class RigidBodyObject:
    def __init__(self, x, y, width, height, mass=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.vx = 0
        self.vy = 0

    def get_aabb(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    
    def apply_impulse(self, ix, iy):
        self.vx += ix / self.mass
        self.vy += iy / self.mass
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.99
        self.vy *= 0.99

    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,255), (int(self.x), int(self.y), self.width, self.height))

def check_collision_aabb(obj_a, obj_b):
    ax1, ay1, ax2, ay2 = obj_a.get_aabb()
    bx1, by1, bx2, by2 = obj_b.get_aabb()
    return (ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1)

# 물방울 관련 설정
class Particle:
    def __init__(self, x, y, vx, vy, life=60):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.gravity = 0.3

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def is_dead(self):
        return self.life <= 0 or self.y > HEIGHT

    def draw(self, surface):
        pygame.draw.circle(surface, (0,0,255), (int(self.x), int(self.y)), 3)

particles = []

# 바람 관련 설정
# 8방향: N, NE, E, SE, S, SW, W, NW
wind_directions = [
    (0, -1),   # N(1)
    (1, -1),   # NE(2)
    (1, 0),    # E(3)
    (1, 1),    # SE(4)
    (0, 1),    # S(5)
    (-1, 1),   # SW(6)
    (-1, 0),   # W(7)
    (-1, -1)   # NW(8)
]
direction_names = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
wind_direction_index = 0
wind_strength = 0

wind_enabled = False
wind_region = (200, 200, 400, 400)

def in_wind_region(x, y):
    rx, ry, rw, rh = wind_region
    return (x > rx and x < rx+rw and y > ry and y < ry+rh)

def reset_game():
    global player_spawn, projectiles, bus, particles, wind_enabled, wind_direction_index, wind_strength
    # 초기화
    player_spawn = PlayerSpawnPoint(WIDTH//2, HEIGHT//2)
    projectiles = []
    bus = RigidBodyObject(300, 300, 50, 30, mass=20)
    particles = []
    wind_enabled = False
    wind_direction_index = 0
    wind_strength = 0
    screen.fill((30,30,30))
    pygame.display.flip()
    return player_spawn, projectiles, bus, particles

player_spawn, projectiles, bus, particles = reset_game()

running = True
while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # R키로 리셋
            if event.key == pygame.K_r:
                player_spawn, projectiles, bus, particles = reset_game()
            # 바람 On/Off 토글
            if event.key == pygame.K_w:
                wind_enabled = not wind_enabled
            # 바람 방향 변경: 1~8 키
            if event.key == pygame.K_1:
                wind_direction_index = 0
            elif event.key == pygame.K_2:
                wind_direction_index = 1
            elif event.key == pygame.K_3:
                wind_direction_index = 2
            elif event.key == pygame.K_4:
                wind_direction_index = 3
            elif event.key == pygame.K_5:
                wind_direction_index = 4
            elif event.key == pygame.K_6:
                wind_direction_index = 5
            elif event.key == pygame.K_7:
                wind_direction_index = 6
            elif event.key == pygame.K_8:
                wind_direction_index = 7
            # 바람 세기 조절
            if event.key == pygame.K_9:
                wind_strength += 1
            elif event.key == pygame.K_0:
                wind_strength = max(0, wind_strength - 1)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 왼쪽 클릭: 탄환 발사
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                projectiles.append(Projectile(player_spawn.x, player_spawn.y, mx, my))
            # 오른쪽 클릭: 물 파티클 생성
            elif event.button == 3:
                for i in range(10):
                    vx = (random.random() - 0.5)*2
                    vy = -3 + (random.random() - 0.5)
                    particles.append(Particle(player_spawn.x, player_spawn.y, vx, vy))

    # 입력 처리
    player_spawn.handle_input(keys)

    # 업데이트
    for p in projectiles:
        p.update()
    projectiles = [p for p in projectiles if not p.is_off_screen()]

    for pa in particles:
        pa.update()
    particles = [pa for pa in particles if not pa.is_dead()]

    bus.update()

    # 탄환-버스 충돌 체크
    for p in projectiles:
        px1, py1 = p.x - p.size, p.y - p.size
        px2, py2 = p.x + p.size, p.y + p.size
        class TempAABB:
            def __init__(self, x1,y1,x2,y2):
                self.x1, self.y1, self.x2, self.y2 = x1,y1,x2,y2
            def get_aabb(self):
                return (self.x1, self.y1, self.x2, self.y2)
        projectile_aabb = TempAABB(px1, py1, px2, py2)

        if check_collision_aabb(projectile_aabb, bus):
            bus.apply_impulse(p.vx * 2, p.vy * 2)
            projectiles.remove(p)
            break

    # 바람 효과 적용 (wind_strength > 0이고 wind_enabled일 때만)
    if wind_enabled and wind_strength > 0:
        wx, wy = wind_directions[wind_direction_index]
        force_x = wx * wind_strength * 0.5
        force_y = wy * wind_strength * 0.5

        # 버스
        if in_wind_region(bus.x+bus.width/2, bus.y+bus.height/2):
            bus.apply_impulse(force_x*bus.mass, force_y*bus.mass)
        # 탄환
        for p in projectiles:
            if in_wind_region(p.x, p.y):
                p.vx += force_x
                p.vy += force_y
        # 파티클
        for pa in particles:
            if in_wind_region(pa.x, pa.y):
                pa.vx += force_x*0.1
                pa.vy += force_y*0.1

    # 렌더링
    screen.fill((30, 30, 30))
    player_spawn.draw(screen)
    for p in projectiles:
        p.draw(screen)
    bus.draw(screen)
    for pa in particles:
        pa.draw(screen)

    if wind_enabled:
        pygame.draw.rect(screen, (0,255,255), wind_region, 2)

    direction_text = direction_names[wind_direction_index]
    info_text = FONT.render(
        "[Arrow Keys] Move | [Left Click] Shoot | [Right Click] Particles | [W] Wind Toggle | [1~8] Wind Dir={} | [9/0] Wind Strength={} | [R] Reset".format(
            direction_text, wind_strength
        ), True, (255,255,255))
    screen.blit(info_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
=======
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
>>>>>>> affb975 (feat: add player class)
