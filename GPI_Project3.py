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

# 비, 바람 관련 전역변수
water_level = 0.0
time_since_rain = 0.0
RAIN_DECAY_TIME = 5.0
EVAPORATION_RATE = 0.01
rain_enabled = False

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
        # 직선 운동, 중력X
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

class Fragment:
    # 수류탄 폭발 파편
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.pi*2)
        speed = random.uniform(5,12)
        self.vx = math.cos(angle)*speed
        self.vy = math.sin(angle)*speed
        self.life = 60

    def update(self):
        self.vx *= 0.99
        self.vy *= 0.99
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, (255,255,0), (int(self.x), int(self.y)), 3)

    def is_dead(self):
        return self.life <= 0 or self.x < 0 or self.x>WIDTH or self.y<0 or self.y>HEIGHT

    def check_bus_collision(self, bus):
        # 파편은 점으로 간주, bus AABB와 충돌 시 파편 제거 & 버스에 임펄스
        bx1,by1,bx2,by2 = bus.aabb()
        if self.x > bx1 and self.x < bx2 and self.y > by1 and self.y < by2:
            # 충돌
            # 버스에 약간의 임펄스 적용
            ix = self.vx * 0.5
            iy = self.vy * 0.5
            bus.apply_impulse(ix, iy, self.x, self.y)
            return True
        return False

class Grenade:
    def __init__(self, x, y, vx, vy, fuse=3.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = 7
        self.fuse = fuse
        self.time_alive = 0.0
        self.exploded = False

    def update(self, dt, bus):
        if self.exploded:
            return
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.99
        self.vy *= 0.99

        # 바닥 충돌
        if self.y + self.size > floor_y:
            diff = (self.y + self.size) - floor_y
            self.y -= diff
            self.vy = -self.vy * 0.6
            self.vx *= 0.8

        # Bus 충돌 처리 (AABB)
        bx1,by1,bx2,by2 = bus.aabb()
        # 수류탄은 작은 원이라도 점 비슷하게 처리
        if self.x > bx1 and self.x < bx2 and self.y > by1 and self.y < by2:
            # 버스 내부 침투 → 반사 처리
            # 간단히 x방향 반사나 y방향 반사
            # 충돌면을 단순화하기 위해 현재 위치에서 버스 중심을 이용해 반사
            bus_cx = (bx1+bx2)/2
            bus_cy = (by1+by2)/2
            dx = self.x - bus_cx
            dy = self.y - bus_cy
            # 버스 중심 방향 벡터 반사
            # 정규화
            dist = math.sqrt(dx*dx+dy*dy)
            if dist != 0:
                nx = dx/dist
                ny = dy/dist
                # 속도 벡터를 이 방향으로 반사
                dot = self.vx*nx + self.vy*ny
                # 반사 벡터
                self.vx = self.vx - 2*dot*nx
                self.vy = self.vy - 2*dot*ny
                # 약간 밀어냄
                self.x += nx * 5
                self.y += ny * 5
                # 버스에 임펄스
                bus.apply_impulse(self.vx*0.5, self.vy*0.5, self.x, self.y)

        self.time_alive += dt
        if self.time_alive >= self.fuse and not self.exploded:
            self.explode()

    def explode(self):
        self.exploded = True

    def draw(self, surface):
        if self.exploded:
            return
        pygame.draw.circle(surface, (100,100,100), (int(self.x), int(self.y)), self.size)

    def is_exploded(self):
        return self.exploded

    def get_position(self):
        return (self.x, self.y)

def spawn_fragments(x, y):
    frags = []
    count = random.randint(10,20)
    for i in range(count):
        frags.append(Fragment(x, y))
    return frags

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
            (self.x + (-hw*cosA + hh*sinA), self.y + (-hw*sinA - hh*cosA)),
            (self.x + ( hw*cosA + hh*sinA), self.y + ( hw*sinA - hh*cosA)),
            (self.x + ( hw*cosA - hh*sinA), self.y + ( hw*sinA + hh*cosA)),
            (self.x + (-hw*cosA - hh*sinA), self.y + (-hw*sinA + hh*cosA))
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

        self.vx *= 0.99
        self.vy *= 0.99
        self.angular_velocity *= 0.99

        points = self.get_points()
        max_y = max(p[1] for p in points)
        if max_y > floor_y:
            diff = max_y - floor_y
            self.y -= diff
            self.vy = 0
            friction = max(0.55, 0.95 - water_level*0.004)
            self.vx *= friction
            self.angular_velocity *= friction

            if abs(self.angular_velocity) < 0.05:
                self.angular_velocity = 0
            else:
                self.angular_velocity *= 0.9

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

def reset_game():
    global player_spawn, projectiles, bus, particles, fragments, grenades, wind_enabled, wind_direction_index, wind_strength, water_level, time_since_rain, rain_enabled
    player_spawn = PlayerSpawnPoint(WIDTH//2, HEIGHT//2)
    projectiles = []
    bus = RigidBodyObject(WIDTH//2, HEIGHT//2, 50, 30, mass=20)
    particles = []
    fragments = []
    grenades = []
    wind_enabled = False
    wind_direction_index = 0
    wind_strength = 0
    water_level = 0.0
    time_since_rain = 0.0
    rain_enabled = False
    screen.fill((30,30,30))
    pygame.display.flip()
    return player_spawn, projectiles, bus, particles, fragments, grenades

player_spawn, projectiles, bus, particles, fragments, grenades = reset_game()

running = True

while running:
    dt = clock.tick(60)/1000.0
    time_since_rain += dt
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_spawn, projectiles, bus, particles, fragments, grenades = reset_game()
            if event.key == pygame.K_w:
                wind_enabled = not wind_enabled
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                             pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]:
                wind_direction_index = int(event.key) - pygame.K_1
            if event.key == pygame.K_9:
                wind_strength += 1
            elif event.key == pygame.K_0:
                wind_strength = max(0, wind_strength - 1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 우클릭 비 토글
            if event.button == 3:
                rain_enabled = not rain_enabled
                if rain_enabled:
                    time_since_rain = 0.0
            # 좌클릭 탄환
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                projectiles.append(Projectile(player_spawn.x, player_spawn.y, mx, my))
            # 가운데 클릭 수류탄
            if event.button == 2:
                mx, my = pygame.mouse.get_pos()
                dx = mx - player_spawn.x
                dy = my - player_spawn.y
                dist = math.sqrt(dx*dx+dy*dy)
                if dist == 0: dist=1
                speed = 8
                vx = (dx/dist)*speed
                vy = (dy/dist)*speed
                grenades.append(Grenade(player_spawn.x, player_spawn.y, vx, vy, fuse=3.0))

    player_spawn.handle_input(keys)

    # 비 파티클 생성
    if rain_enabled:
        time_since_rain = 0.0
        for i in range(random.randint(3,5)):
            x_pos = random.uniform(0, WIDTH)
            vy_init = random.uniform(5,8)
            size = random.randint(2,4)
            particles.append(Particle(x_pos, 0, 0, vy_init, size=size))

    # 탄환 업데이트
    for p in projectiles:
        p.update()
    projectiles = [p for p in projectiles if not p.hit_floor() and not p.is_off_screen()]

    # 파티클 업데이트
    for pa in particles:
        pa.update()
    survived_particles = []
    for pa in particles:
        if pa.hit_floor():
            water_level += 0.1
        elif pa.is_dead() or bus.inside_aabb(pa.x, pa.y):
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
        for f in fragments:
            f.vx += force_x*0.05
            f.vy += force_y*0.05

    # 물 증발
    if not rain_enabled and time_since_rain > RAIN_DECAY_TIME:
        water_level = max(0, water_level - EVAPORATION_RATE)

    # 수류탄 업데이트
    for g in grenades:
        g.update(dt, bus)

    # 폭발한 수류탄 처리
    exploded_grenades = [g for g in grenades if g.is_exploded()]
    new_frags = []
    for g in exploded_grenades:
        gx, gy = g.get_position()
        new_frags += spawn_fragments(gx, gy)
    fragments += new_frags
    grenades = [g for g in grenades if not g.is_exploded()]

    # 파편 업데이트 & 버스 충돌
    survived_frags = []
    for f in fragments:
        f.update()
        if not f.is_dead():
            if f.check_bus_collision(bus):
                # 버스와 충돌 -> 파편 소멸
                pass
            else:
                survived_frags.append(f)
    fragments = survived_frags

    # 렌더링
    screen.fill((30, 30, 30))
    player_spawn.draw(screen)
    for p in projectiles:
        p.draw(screen)
    bus.draw(screen)
    for pa in particles:
        pa.draw(screen)

    # 물 웅덩이
    pygame.draw.line(screen, (100,50,0), (0, floor_y), (WIDTH, floor_y), 5)
    if water_level > 0:
        water_height = min(20, water_level*0.5)
        surf = pygame.Surface((WIDTH, water_height), pygame.SRCALPHA)
        alpha = min(200, int(20+water_level*5))
        surf.fill((0,0,255, alpha))
        screen.blit(surf, (0, floor_y - water_height))

    # 수류탄, 파편 그리기
    for g in grenades:
        g.draw(screen)
    for f in fragments:
        f.draw(screen)

    direction_text = direction_names[wind_direction_index]
    info_text = FONT.render(
        "[Arrows/WASD]Move | L:Bullet | R:RainToggle | M:Grenade(Mid Click) | W:WindToggle | 1~8:Dir={} | 9/0:WStr={} | R:Reset | water={:.2f}".format(
            direction_text, wind_strength, water_level),
        True, (255,255,255))
    screen.blit(info_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
