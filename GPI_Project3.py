import sys
import math
import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Demo")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 24)

floor_y = HEIGHT - 50
gravity = 0.3

# 바닥 물 상태
water_level = 0.0         # 고인 물의 양
time_since_rain = 0.0     # 비가 안 온 시간(증발용)
RAIN_DECAY_TIME = 5.0     # 비 안 올 경우 5초 후부터 천천히 증발 시작
EVAPORATION_RATE = 0.01   # 증발 속도(프레임당)

rain_enabled = False

class PlayerSpawnPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.size = 10

    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (int(self.x), int(self.y)), self.size)

class Projectile:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.speed = 10
        dx = target_x - start_x
        dy = target_y - start_y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0:
            dist = 1
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed
        self.size = 5

    def update(self):
        # 중력 미적용, 직진
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.999
        self.vy *= 0.999

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.size)

    def is_off_screen(self):
        return (self.x < -50 or self.x > WIDTH+50 or self.y < -50 or self.y > HEIGHT+100)

    def hit_floor(self):
        return self.y >= floor_y

class RigidBodyObject:
    def __init__(self, x, y, width, height, mass=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.angular_velocity = 0
        self.I = (1.0/12.0)*self.mass*(self.width**2 + self.height**2)

    def get_points(self):
        hw = self.width/2
        hh = self.height/2
        cosA = math.cos(self.angle)
        sinA = math.sin(self.angle)
        points = [
            (self.x + (-hw*cosA + hh*sinA), self.y + (-hw*sinA - hh*cosA)),  # top-left
            (self.x + ( hw*cosA + hh*sinA), self.y + ( hw*sinA - hh*cosA)),  # top-right
            (self.x + ( hw*cosA - hh*sinA), self.y + ( hw*sinA + hh*cosA)),  # bottom-right
            (self.x + (-hw*cosA - hh*sinA), self.y + (-hw*sinA + hh*cosA))   # bottom-left
        ]
        return points

    def apply_impulse(self, ix, iy, px=None, py=None):
        if px is None or py is None:
            self.vx += ix / self.mass
            self.vy += iy / self.mass
        else:
            rx = px - self.x
            ry = py - self.y
            self.vx += ix / self.mass
            self.vy += iy / self.mass
            torque = rx * iy - ry * ix
            self.angular_velocity += torque / self.I

    def update(self):
        global water_level

        self.vy += gravity
        self.x += self.vx
        self.y += self.vy
        self.angle += self.angular_velocity

        # 공기저항
        self.vx *= 0.99
        self.vy *= 0.99
        self.angular_velocity *= 0.99

        # 회전 및 바닥 처리
        points = self.get_points()
        max_y = max(p[1] for p in points)
        if max_y > floor_y:
            diff = max_y - floor_y
            self.y -= diff
            self.vy = 0
            # 바닥 마찰: 물이 많을수록 마찰 감소
            # dry friction: vx *= 0.95, wet: vx *= closer to 1.0
            # water_level 높을수록 감쇠율 감소
            friction_factor = 0.95 + 0.05*(1/(1+water_level)) # 물 많을수록 조금씩 1에 가까워짐
            # 반대로 1/(1+water_level)는 물 많을수록 작아짐, 0.95+0.05*(작은값) ~0.95초반
            # 여기서는 water_level 높을수록 마찰 줄이기 위해 역관계로 조정
            # 더 단순히: 감쇠율 = 0.95 - min(0.4, water_level*0.01) 이런식으로 해도 됨
            # 여기서는 예시로:
            # water_level이 0이면 감쇠율=0.95
            # water_level이 커지면 감쇠율 약간 커짐 -> 덜 감쇠(더 미끄러짐)
            # 여기서는 단순히 감쇠율을 줄이자:
            base_friction = 0.95
            # water_level이 0일때 0.95, water_level이 100일때 0.55 등
            friction = max(0.55, base_friction - water_level*0.004)
            self.vx *= friction
            self.angular_velocity *= friction

            if abs(self.angular_velocity) < 0.05:
                self.angular_velocity = 0
            else:
                self.angular_velocity *= 0.9

        # 화면 밖 이탈 방지
        half_diag = max(self.width, self.height)
        self.x = max(half_diag/2, min(self.x, WIDTH - half_diag/2))
        self.y = min(self.y, HEIGHT - half_diag/2)

    def draw(self, surface):
        rect_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rect_surf.fill((0,0,255))
        rotated = pygame.transform.rotate(rect_surf, -math.degrees(self.angle))
        w, h = rotated.get_size()
        blit_x = int(self.x - w/2)
        blit_y = int(self.y - h/2)
        surface.blit(rotated, (blit_x, blit_y))

    def aabb(self):
        points = self.get_points()
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return min(xs), min(ys), max(xs), max(ys)

    def inside_aabb(self, px, py):
        x1,y1,x2,y2 = self.aabb()
        return (px >= x1 and px <= x2 and py >= y1 and py <= y2)

class Particle:
    def __init__(self, x, y, vx, vy, size=3, life=120):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.size = size

    def update(self):
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vx *= 0.99
        self.vy *= 0.99

    def is_dead(self):
        return self.life <= 0

    def hit_floor(self):
        return self.y >= floor_y

    def draw(self, surface):
        pygame.draw.circle(surface, (0,0,255), (int(self.x), int(self.y)), self.size)

wind_directions = [
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1)
]
direction_names = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
wind_direction_index = 0
wind_strength = 0
wind_enabled = False

def reset_game():
    global player_spawn, projectiles, bus, particles, wind_enabled, wind_direction_index, wind_strength, water_level, time_since_rain, rain_enabled
    player_spawn = PlayerSpawnPoint(WIDTH//2, HEIGHT//2)
    projectiles = []
    bus = RigidBodyObject(WIDTH//2, HEIGHT//2, 50, 30, mass=20)
    particles = []
    wind_enabled = False
    wind_direction_index = 0
    wind_strength = 0
    water_level = 0.0
    time_since_rain = 0.0
    rain_enabled = False
    screen.fill((30,30,30))
    pygame.display.flip()
    return player_spawn, projectiles, bus, particles

player_spawn, projectiles, bus, particles = reset_game()

running = True
last_time = pygame.time.get_ticks()

while running:
    dt = clock.tick(60)/1000.0
    # dt: delta time(초 단위)
    # time_since_rain으로 증발 처리에 활용
    time_since_rain += dt

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_spawn, projectiles, bus, particles = reset_game()
            if event.key == pygame.K_w:
                wind_enabled = not wind_enabled
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
            if event.key == pygame.K_9:
                wind_strength += 1
            elif event.key == pygame.K_0:
                wind_strength = max(0, wind_strength - 1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 우클릭으로 비 토글
            if event.button == 3:
                rain_enabled = not rain_enabled
                if rain_enabled:
                    time_since_rain = 0.0

            # 좌클릭으로 탄환 발사(기존 그대로)
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                projectiles.append(Projectile(player_spawn.x, player_spawn.y, mx, my))

    player_spawn.handle_input(keys)

    # 비 파티클 생성 로직
    if rain_enabled:
        # 비가 내리는 동안 time_since_rain=0으로 초기화
        time_since_rain = 0.0
        # 매 프레임 약간의 확률로 여러 방울 생성
        # 예: 매 프레임 3~5개 정도 생성
        for i in range(random.randint(3,5)):
            x_pos = random.uniform(0, WIDTH)
            # 약간의 초기 속도와 크기 변화를 줌
            vy_init = random.uniform(5,8) # 빠르게 떨어지는 빗방울
            size = random.randint(2,4)
            particles.append(Particle(x_pos, 0, 0, vy_init, size=size))

    # 탄환 업데이트
    for p in projectiles:
        p.update()
    projectiles = [p for p in projectiles if not p.hit_floor() and not p.is_off_screen()]

    # 파티클 업데이트
    for pa in particles:
        pa.update()
    # 파티클 바닥 처리:
    # 바닥에 닿으면 파티클 소멸, water_level += 약간 증가
    # 버스 충돌 시 소멸(증발)
    survived_particles = []
    for pa in particles:
        if pa.hit_floor():
            # 바닥 도달 -> 물 축적
            water_level += 0.1
        elif pa.is_dead() or bus.inside_aabb(pa.x, pa.y):
            # 수명 만료 or 버스 충돌시 제거
            pass
        else:
            survived_particles.append(pa)
    particles = survived_particles

    bus.update()

    # 탄환-버스 충돌
    for p in projectiles:
        px1, py1 = p.x - p.size, p.y - p.size
        px2, py2 = p.x + p.size, p.y + p.size
        bx1, by1, bx2, by2 = bus.aabb()
        if (px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1):
            ix = p.vx * 2
            iy = p.vy * 2
            bus.apply_impulse(ix, iy, p.x, p.y)
            projectiles.remove(p)
            break

    # 바람 적용
    if wind_enabled and wind_strength > 0:
        wx, wy = wind_directions[wind_direction_index]
        force_x = wx * wind_strength * 0.05
        force_y = wy * wind_strength * 0.05
        bus.apply_impulse(force_x*bus.mass, force_y*bus.mass)
        for p in projectiles:
            p.vx += force_x
            p.vy += force_y
        for pa in particles:
            pa.vx += force_x*0.1
            pa.vy += force_y*0.1

    # 물 증발 로직
    # 비가 안온 지 RAIN_DECAY_TIME초 지나면 증발 시작
    if not rain_enabled and time_since_rain > RAIN_DECAY_TIME:
        water_level = max(0, water_level - EVAPORATION_RATE)

    # 렌더링
    screen.fill((30, 30, 30))
    player_spawn.draw(screen)
    for p in projectiles:
        p.draw(screen)
    bus.draw(screen)
    for pa in particles:
        pa.draw(screen)

    # 바닥 및 물 웅덩이 시각화
    pygame.draw.line(screen, (100,50,0), (0, floor_y), (WIDTH, floor_y), 5)

    if water_level > 0:
        # water_level이 클수록 더 높은 물 레이어 표현 가능
        # 여기서는 단순히 floor_y 부근에 얇은 파란 레이어
        # water_level이 커질수록 height 증가 혹은 투명도 변경
        water_height = min(20, water_level*0.5) # 최대 20픽셀 높이
        surf = pygame.Surface((WIDTH, water_height), pygame.SRCALPHA)
        alpha = min(200, int(20+water_level*5)) # 물 많을수록 불투명
        surf.fill((0,0,255, alpha))
        screen.blit(surf, (0, floor_y - water_height))

    direction_text = direction_names[wind_direction_index]
    info_text = FONT.render(
        "[Arrows/WASD]Move | L-Click:Straight Bullet | R-Click:Toggle Rain | W:WindToggle | 1~8:Dir={} | 9/0:WindStr={} | R:Reset | water_level={:.2f}".format(direction_text, wind_strength, water_level),
        True, (255,255,255))
    screen.blit(info_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
