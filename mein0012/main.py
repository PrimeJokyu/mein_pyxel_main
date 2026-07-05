import pyxel
import math
import random

# --- 定数定義 ---
SCREEN_W = 160
SCREEN_H = 120
GRID_SIZE = 8
MAP_COLS = 60
MAP_ROWS = 60
MAP_W = MAP_COLS * GRID_SIZE
MAP_H = MAP_ROWS * GRID_SIZE

# タイル状態
TILE_EMPTY = 0
TILE_WALL = 1
TILE_PLAYER_INK = 2
TILE_ENEMY_INK = 3

# チーム定義
TEAM_BLUE = 1   # プレイヤー側 (青)
TEAM_ORANGE = 2 # 敵側 (オレンジ)

# 色定義
COLOR_BG = 7           # 白 (床)
COLOR_WALL = 5         # 暗いグレー (壁)
COLOR_BLUE_INK = 12    # 青 (プレイヤーチームのインク)
COLOR_ORANGE_INK = 9   # オレンジ (敵チームのインク)
COLOR_BLUE_HERO = 11   # 水色 (プレイヤーのヒト状態)
COLOR_BLUE_SQUID = 3   # 緑がかった青 (プレイヤーのイカ状態)
COLOR_ORANGE_HERO = 10 # 黄色 (敵のヒト状態)
COLOR_ORANGE_SQUID = 8 # 赤みがかったオレンジ (敵のイカ状態)

# ゲーム状態
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_RESULT = 2

# --- スプライトデータ (8x8ドット) ---
SPRITE_DATA = {
    # 青ヒト (水色=11, 青=12, 黒=0, 透明=c)
    (0, 0): [
        "cccc11cc",
        "ccc1111c",
        "cc111211",
        "cc111111",
        "cc011110",
        "ccc111cc",
        "cc11c11c",
        "cc11c11c"
    ],
    # 青イカ (水色=11, 青=12, 白=7, 黒=0)
    (8, 0): [
        "ccc11ccc",
        "cc1111cc",
        "c171171c",
        "c101101c",
        "11111111",
        "11111111",
        "1c1cc1c1",
        "1c1cc1c1"
    ],
    # オレンジヒト (黄色=10, オレンジ=9, 黒=0, 透明=c)
    (16, 0): [
        "ccccaacc",
        "cccaaaac",
        "ccaacaaa",
        "ccaaaaaa",
        "cc0aaaa0",
        "cccaaacc",
        "ccaacaac",
        "ccaacaac"
    ],
    # オレンジイカ (黄色=10, オレンジ=9, 白=7, 黒=0)
    (24, 0): [
        "cccaaccc",
        "ccaaaacc",
        "ca7aa7ac",
        "ca0aa0ac",
        "aaaaaaaa",
        "aaaaaaaa",
        "acaacaac",
        "acaacaac"
    ]
}

# --- 音声の定義 ---
def init_sounds():
    # 0: プレイヤー射撃音 (短く高いプチプチ音)
    pyxel.sounds[0].set("r", "p", "3", "n", 3)
    
    # 1: 敵射撃音 (少し低い音)
    pyxel.sounds[1].set("r", "p", "2", "n", 3)

    # 2: イカ潜水・泳ぎ音 (ピチャピチャ)
    pyxel.sounds[2].set("r", "t", "2", "n", 4)
    
    # 3: 被弾音 (濁った爆発音風)
    pyxel.sounds[3].set("g2", "n", "6", "f", 6)

    # 4: BGM メロディライン
    pyxel.sounds[4].set(
        "c3e3g3c4 e3g3c4e4 g3c4e4g4 c4e4g4c4",
        "p",
        "5",
        "vffvvffvvffvvffv",
        15
    )
    # 5: BGM ベースライン
    pyxel.sounds[5].set(
        "c2c2e2e2 g2g2c3c3 e2e2g2g2 c3c3e3e3",
        "s",
        "4",
        "n",
        15
    )

# --- クラス定義 ---

class Bullet:
    def __init__(self, x, y, angle, team, is_player=False):
        self.x = x
        self.y = y
        self.team = team
        self.is_player = is_player
        
        # 射撃のブレ（敵は命中率を下げるために大きくブレさせる）
        spread_deg = 8 if (team == TEAM_BLUE) else 18
        spread = math.radians(random.uniform(-spread_deg, spread_deg))
        self.angle = angle + spread
        
        # 初速と射程 (敵の弾は遅く、避けやすくする)
        speed_min = 4.5 if (team == TEAM_BLUE) else 2.5
        speed_max = 5.5 if (team == TEAM_BLUE) else 3.5
        self.speed = random.uniform(speed_min, speed_max)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        
        self.life = random.randint(12, 18)  # 弾の寿命
        self.damage = 15 if (team == TEAM_BLUE) else 8  # 敵の弾のダメージを8に弱体化
        
        # 描画サイズ用
        self.size = random.uniform(2.0, 3.5)

    def update(self, map_grid):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        
        if random.random() < 0.4:
            self.paint(map_grid, radius=1)
            
        if self.x < 0 or self.x >= MAP_W or self.y < 0 or self.y >= MAP_H:
            self.life = 0
            return False
            
        gx, gy = int(self.x // GRID_SIZE), int(self.y // GRID_SIZE)
        if 0 <= gx < MAP_COLS and 0 <= gy < MAP_ROWS:
            if map_grid[gy][gx] == TILE_WALL:
                self.paint(map_grid, radius=2)
                self.life = 0
                return False
                
        return self.life > 0

    def paint(self, map_grid, radius=2.0):
        gx_center = int(self.x // GRID_SIZE)
        gy_center = int(self.y // GRID_SIZE)
        
        ink_type = TILE_PLAYER_INK if self.team == TEAM_BLUE else TILE_ENEMY_INK
        
        r_grid = int(radius)
        for dy in range(-r_grid, r_grid + 1):
            for dx in range(-r_grid, r_grid + 1):
                if dx*dx + dy*dy <= radius*radius:
                    gx = gx_center + dx
                    gy = gy_center + dy
                    if 0 <= gx < MAP_COLS and 0 <= gy < MAP_ROWS:
                        if map_grid[gy][gx] != TILE_WALL:
                            map_grid[gy][gx] = ink_type

    def draw(self, camera_x, camera_y):
        color = COLOR_BLUE_INK if self.team == TEAM_BLUE else COLOR_ORANGE_INK
        pyxel.circ(self.x - camera_x, self.y - camera_y, self.size, color)


class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, size=None, life=None):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx if vx is not None else random.uniform(-1.5, 1.5)
        self.vy = vy if vy is not None else random.uniform(-1.5, 1.5)
        self.size = size if size is not None else random.randint(1, 3)
        self.life = life if life is not None else random.randint(5, 12)
        self.max_life = self.life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.9
        self.vy *= 0.9
        self.life -= 1
        return self.life > 0

    def draw(self, camera_x, camera_y):
        r = max(1, int(self.size * (self.life / self.max_life)))
        pyxel.circ(self.x - camera_x, self.y - camera_y, r, self.color)


class Actor:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        
        # 敵AIはHPを 60 に弱体化 (プレイヤー側は 100)
        self.max_hp = 100 if team == TEAM_BLUE else 60
        self.hp = self.max_hp
        self.max_ink = 100
        self.ink = 100
        
        self.is_squid = False
        self.angle = 0.0
        
        self.shoot_cooldown = 0
        self.damage_overlay = 0
        self.respawn_timer = 0
        
        self.radius = 3.5

    def is_alive(self):
        return self.respawn_timer == 0

    def take_damage(self, amount, app):
        if not self.is_alive():
            return
        self.hp -= amount
        self.damage_overlay = 8
        if self.hp <= 0:
            self.hp = 0
            self.respawn_timer = 90
            color = COLOR_BLUE_INK if self.team == TEAM_BLUE else COLOR_ORANGE_INK
            for _ in range(25):
                app.particles.append(Particle(self.x, self.y, color, 
                                              vx=random.uniform(-3, 3), 
                                              vy=random.uniform(-3, 3), 
                                              size=random.randint(2, 4), 
                                              life=random.randint(15, 25)))
            pyxel.play(3, 3)

    def respawn(self, spawn_points):
        pt = spawn_points[self.team]
        self.x = pt[0]
        self.y = pt[1]
        self.hp = self.max_hp
        self.ink = self.max_ink
        self.is_squid = False
        self.respawn_timer = 0

    def update_status(self, map_grid, app):
        if not self.is_alive():
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.respawn(app.spawn_points)
            return

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.damage_overlay > 0:
            self.damage_overlay -= 1

        gx = int(self.x // GRID_SIZE)
        gy = int(self.y // GRID_SIZE)
        
        on_my_ink = False
        on_enemy_ink = False
        
        if 0 <= gx < MAP_COLS and 0 <= gy < MAP_ROWS:
            tile = map_grid[gy][gx]
            if self.team == TEAM_BLUE:
                on_my_ink = (tile == TILE_PLAYER_INK)
                on_enemy_ink = (tile == TILE_ENEMY_INK)
            else:
                on_my_ink = (tile == TILE_ENEMY_INK)
                on_enemy_ink = (tile == TILE_PLAYER_INK)

        if self.is_squid:
            if on_my_ink:
                self.ink = min(self.max_ink, self.ink + 1.5)
                self.hp = min(self.max_hp, self.hp + 1.0)
            else:
                self.hp = min(self.max_hp, self.hp + 0.1)
        else:
            self.ink = min(self.max_ink, self.ink + 0.3)
            self.hp = min(self.max_hp, self.hp + 0.2)

        if on_enemy_ink:
            self.hp = max(0, self.hp - 0.5)
            if self.hp <= 0:
                self.take_damage(0, app)
            if random.random() < 0.15:
                color = COLOR_ORANGE_INK if self.team == TEAM_BLUE else COLOR_BLUE_INK
                app.particles.append(Particle(self.x, self.y, color, size=1, life=6))

    def move_with_collision(self, dx, dy, map_grid):
        new_x = self.x + dx
        if not self.check_wall_collision(new_x, self.y, map_grid):
            self.x = new_x
        else:
            for offset in [-2, 2]:
                if not self.check_wall_collision(new_x, self.y + offset, map_grid):
                    self.y += offset * 0.5
                    self.x = new_x
                    break
        
        new_y = self.y + dy
        if not self.check_wall_collision(self.x, new_y, map_grid):
            self.y = new_y
        else:
            for offset in [-2, 2]:
                if not self.check_wall_collision(self.x + offset, new_y, map_grid):
                    self.x += offset * 0.5
                    self.y = new_y
                    break

        self.x = max(self.radius, min(MAP_W - self.radius, self.x))
        self.y = max(self.radius, min(MAP_H - self.radius, self.y))

    def check_wall_collision(self, px, py, map_grid):
        check_points = [
            (px, py),
            (px - self.radius, py),
            (px + self.radius, py),
            (px, py - self.radius),
            (px, py + self.radius),
            (px - self.radius * 0.7, py - self.radius * 0.7),
            (px + self.radius * 0.7, py - self.radius * 0.7),
            (px - self.radius * 0.7, py + self.radius * 0.7),
            (px + self.radius * 0.7, py + self.radius * 0.7),
        ]
        
        for cx, cy in check_points:
            gx = int(cx // GRID_SIZE)
            gy = int(cy // GRID_SIZE)
            if 0 <= gx < MAP_COLS and 0 <= gy < MAP_ROWS:
                if map_grid[gy][gx] == TILE_WALL:
                    return True
            else:
                return True
        return False

    def draw(self, camera_x, camera_y):
        if not self.is_alive():
            return
            
        if self.damage_overlay > 0 and pyxel.frame_count % 2 == 0:
            pyxel.circ(self.x - camera_x, self.y - camera_y, self.radius + 1, 7)
            return

        u = 0
        if self.team == TEAM_BLUE:
            u = 8 if self.is_squid else 0
        else:
            u = 24 if self.is_squid else 16
            
        w_dir = 8 if math.cos(self.angle) >= 0 else -8
        pyxel.blt(self.x - camera_x - 4, self.y - camera_y - 4, 0, u, 0, w_dir, 8, 12)


class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, TEAM_BLUE)

    def update(self, map_grid, app):
        self.update_status(map_grid, app)
        if not self.is_alive():
            return

        camera_x = app.camera_x
        camera_y = app.camera_y
        world_mx = pyxel.mouse_x + camera_x
        world_my = pyxel.mouse_y + camera_y
        self.angle = math.atan2(world_my - self.y, world_mx - self.x)

        want_squid = pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_SHIFT)
        is_shooting = pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
        if is_shooting:
            want_squid = False
            
        self.is_squid = want_squid

        gx = int(self.x // GRID_SIZE)
        gy = int(self.y // GRID_SIZE)
        on_my_ink = False
        on_enemy_ink = False
        if 0 <= gx < MAP_COLS and 0 <= gy < MAP_ROWS:
            tile = map_grid[gy][gx]
            on_my_ink = (tile == TILE_PLAYER_INK)
            on_enemy_ink = (tile == TILE_ENEMY_INK)

        if self.is_squid:
            if on_my_ink:
                speed = 3.2
                if pyxel.btn(pyxel.KEY_W): # W移動中のみエフェクト
                    if pyxel.frame_count % 3 == 0:
                        app.particles.append(Particle(self.x, self.y, COLOR_BLUE_INK, size=2, life=10))
                        if pyxel.frame_count % 6 == 0:
                            pyxel.play(2, 2)
            else:
                speed = 0.8
        else:
            if on_enemy_ink:
                speed = 0.5
            elif is_shooting:
                speed = 1.0
            else:
                speed = 1.6

        # Wキーを押したときのみマウスカーソルの方向に進む (ASDは無効化)
        dx, dy = 0, 0
        if pyxel.btn(pyxel.KEY_W):
            dx = math.cos(self.angle) * speed
            dy = math.sin(self.angle) * speed
        
        if dx != 0 or dy != 0:
            self.move_with_collision(dx, dy, map_grid)
            
            if not self.is_squid and pyxel.frame_count % 8 == 0:
                app.particles.append(Particle(self.x, self.y, 13, vx=-dx*0.2, vy=-dy*0.2, size=1, life=6))

        if is_shooting and self.shoot_cooldown == 0 and not self.is_squid:
            if self.ink >= 2.0:
                self.ink -= 2.0
                self.shoot_cooldown = 4
                
                bx = self.x + math.cos(self.angle) * 4
                by = self.y + math.sin(self.angle) * 4
                app.bullets.append(Bullet(bx, by, self.angle, TEAM_BLUE, is_player=True))
                
                app.particles.append(Particle(bx, by, COLOR_BLUE_INK, 
                                              vx=math.cos(self.angle)*2 + random.uniform(-1,1),
                                              vy=math.sin(self.angle)*2 + random.uniform(-1,1),
                                              size=random.randint(1,2), life=8))
                pyxel.play(0, 0)


class AICharacter(Actor):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.target_x = x
        self.target_y = y
        self.ai_state_timer = 0
        self.ai_state = "wander"
        self.shoot_target = None

    def update(self, map_grid, app):
        self.update_status(map_grid, app)
        if not self.is_alive():
            return

        self.ai_state_timer -= 1
        
        opposing_team = TEAM_ORANGE if self.team == TEAM_BLUE else TEAM_BLUE
        enemies = [a for a in app.actors if a.team == opposing_team and a.is_alive()]
        
        if self.team == TEAM_ORANGE and app.player.is_alive():
            enemies.append(app.player)
            
        closest_enemy = None
        closest_dist = 9999.0
        for e in enemies:
            d = math.hypot(e.x - self.x, e.y - self.y)
            if d < closest_dist:
                closest_dist = d
                closest_enemy = e

        if self.ink < 25 and self.ai_state != "retreat":
            self.ai_state = "retreat"
            self.ai_state_timer = random.randint(45, 90)
        elif self.ai_state == "retreat" and self.ink > 85:
            self.ai_state = "wander"
            self.ai_state_timer = 0
            
        if self.ai_state != "retreat":
            if closest_enemy and closest_dist < 80:
                self.ai_state = "chase"
                self.shoot_target = closest_enemy
            else:
                if self.ai_state_timer <= 0:
                    self.ai_state = "wander"
                    self.target_x = random.uniform(20, MAP_W - 20)
                    self.target_y = random.uniform(20, MAP_H - 20)
                    self.ai_state_timer = random.randint(60, 150)
                self.shoot_target = None

        gx = int(self.x // GRID_SIZE)
        gy = int(self.y // GRID_SIZE)
        on_my_ink = False
        on_enemy_ink = False
        if 0 <= gx < MAP_COLS and 0 <= gy < MAP_ROWS:
            tile = map_grid[gy][gx]
            if self.team == TEAM_BLUE:
                on_my_ink = (tile == TILE_PLAYER_INK)
                on_enemy_ink = (tile == TILE_ENEMY_INK)
            else:
                on_my_ink = (tile == TILE_ENEMY_INK)
                on_enemy_ink = (tile == TILE_PLAYER_INK)

        want_squid = False
        if self.ai_state == "retreat":
            want_squid = True
        elif on_my_ink and self.ai_state == "chase" and closest_dist > 40:
            want_squid = True
            
        self.is_squid = want_squid

        # 敵AIは移動速度を弱体化
        if self.is_squid:
            squid_speed = 3.2 if (self.team == TEAM_BLUE) else 2.0
            speed = squid_speed if on_my_ink else 0.8
            if (self.x != self.target_x or self.y != self.target_y) and pyxel.frame_count % 4 == 0 and on_my_ink:
                color = COLOR_BLUE_INK if self.team == TEAM_BLUE else COLOR_ORANGE_INK
                app.particles.append(Particle(self.x, self.y, color, size=2, life=8))
        else:
            human_speed = 1.2 if (self.team == TEAM_BLUE) else 0.8
            speed = human_speed
            if on_enemy_ink:
                speed = 0.5 if (self.team == TEAM_BLUE) else 0.3

        dx, dy = 0, 0
        if self.ai_state == "retreat":
            if closest_enemy:
                dx = self.x - closest_enemy.x
                dy = self.y - closest_enemy.y
            else:
                dx = self.target_x - self.x
                dy = self.target_y - self.y
        elif self.ai_state == "chase" and self.shoot_target:
            dx = self.shoot_target.x - self.x
            dy = self.shoot_target.y - self.y
            
            dist = math.hypot(dx, dy)
            if dist < 35:
                dx, dy = -dy, dx
        else:
            dx = self.target_x - self.x
            dy = self.target_y - self.y

        dist_to_target = math.hypot(dx, dy)
        if dist_to_target > 2:
            dx = (dx / dist_to_target) * speed
            dy = (dy / dist_to_target) * speed
            self.move_with_collision(dx, dy, map_grid)
            
            if not self.is_squid:
                self.angle = math.atan2(dy, dx)

        if self.ai_state == "chase" and self.shoot_target and not self.is_squid:
            self.angle = math.atan2(self.shoot_target.y - self.y, self.shoot_target.x - self.x)
            
            if self.shoot_cooldown == 0 and self.ink >= 2.0:
                self.ink -= 2.0
                # 敵AIは攻撃の頻度を大きく低下 (18フレームの間隔。味方AIは6フレーム)
                self.shoot_cooldown = 6 if (self.team == TEAM_BLUE) else 18
                
                bx = self.x + math.cos(self.angle) * 4
                by = self.y + math.sin(self.angle) * 4
                app.bullets.append(Bullet(bx, by, self.angle, self.team))
                
                color = COLOR_BLUE_INK if self.team == TEAM_BLUE else COLOR_ORANGE_INK
                app.particles.append(Particle(bx, by, color, 
                                              vx=math.cos(self.angle)*2 + random.uniform(-1,1),
                                              vy=math.sin(self.angle)*2 + random.uniform(-1,1),
                                              size=1, life=6))
                if app.is_on_screen(self.x, self.y):
                    pyxel.play(1, 1)


class App:
    def __init__(self):
        # 160 x 120 解像度で初期化
        pyxel.init(SCREEN_W, SCREEN_H, title="SplatPyxel - Paint Battle", fps=30)
        pyxel.mouse(True)
        
        init_sounds()
        
        for (col, row), data in SPRITE_DATA.items():
            for dy, line in enumerate(data):
                for dx, char in enumerate(line):
                    color_idx = int(char, 16) if char != 'c' else 12
                    if char == 'c':
                        pyxel.images[0].pset(col + dx, row + dy, 12)
                    else:
                        pyxel.images[0].pset(col + dx, row + dy, color_idx)

        self.state = STATE_TITLE
        
        self.camera_x = 0
        self.camera_y = 0
        
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.map_grid = [[TILE_EMPTY for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]
        
        for y in range(MAP_ROWS):
            for x in range(MAP_COLS):
                if x == 0 or x == MAP_COLS - 1 or y == 0 or y == MAP_ROWS - 1:
                    self.map_grid[y][x] = TILE_WALL

        num_blocks = 20
        for _ in range(num_blocks):
            bx = random.randint(4, MAP_COLS // 2 - 2)
            by = random.randint(4, MAP_ROWS - 5)
            bw = random.randint(2, 4)
            bh = random.randint(2, 4)
            
            for dy in range(bh):
                for dx in range(bw):
                    gx1, gy1 = bx + dx, by + dy
                    gx2, gy2 = (MAP_COLS - 1) - gx1, (MAP_ROWS - 1) - gy1
                    
                    if math.hypot(gx1 - 5, gy1 - 5) > 6 and math.hypot(gx2 - 5, gy2 - 5) > 6:
                        if gx1 < MAP_COLS and gy1 < MAP_ROWS:
                            self.map_grid[gy1][gx1] = TILE_WALL
                        if gx2 < MAP_COLS and gy2 < MAP_ROWS:
                            self.map_grid[gy2][gx2] = TILE_WALL

        self.spawn_points = {
            TEAM_BLUE: (40, 40),
            TEAM_ORANGE: (MAP_W - 40, MAP_H - 40)
        }

        px, py = self.spawn_points[TEAM_BLUE]
        self.player = Player(px, py)
        
        self.actors = []
        
        ax, ay = self.spawn_points[TEAM_BLUE]
        self.actors.append(AICharacter(ax + 16, ay + 16, TEAM_BLUE))
        
        # 敵AI (2体)
        ex1, ey1 = self.spawn_points[TEAM_ORANGE]
        self.actors.append(AICharacter(ex1 - 16, ey1, TEAM_ORANGE))
        self.actors.append(AICharacter(ex1, ey1 - 16, TEAM_ORANGE))

        self.bullets = []
        self.particles = []

        self.total_time = 60
        self.game_timer = self.total_time * 30
        
        self.blue_percent = 0.0
        self.orange_percent = 0.0
        self.empty_percent = 100.0
        
        pyxel.play(0, 4, loop=True)
        pyxel.play(1, 5, loop=True)

    def is_on_screen(self, x, y):
        return (self.camera_x - 16 <= x <= self.camera_x + SCREEN_W + 16 and
                self.camera_y - 16 <= y <= self.camera_y + SCREEN_H + 16)

    def update(self):
        if self.state == STATE_TITLE:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.reset_game()
                self.state = STATE_PLAYING
        
        elif self.state == STATE_PLAYING:
            self.game_timer -= 1
            if self.game_timer <= 0:
                self.game_timer = 0
                self.calculate_result()
                pyxel.stop()
                self.state = STATE_RESULT
                return

            self.player.update(self.map_grid, self)
            for actor in self.actors:
                actor.update(self.map_grid, self)

            all_actors = [self.player] + self.actors
            for b in self.bullets[:]:
                is_alive = b.update(self.map_grid)
                if not is_alive:
                    self.bullets.remove(b)
                    continue
                
                for actor in all_actors:
                    if actor.is_alive() and b.team != actor.team:
                        dist = math.hypot(actor.x - b.x, actor.y - b.y)
                        if dist < actor.radius + b.size:
                            actor.take_damage(b.damage, self)
                            
                            color = COLOR_BLUE_INK if b.team == TEAM_BLUE else COLOR_ORANGE_INK
                            for _ in range(5):
                                self.particles.append(Particle(actor.x, actor.y, color, life=6))
                                
                            b.paint(self.map_grid, radius=2)
                            if b in self.bullets:
                                self.bullets.remove(b)
                            break

            for p in self.particles[:]:
                if not p.update():
                    self.particles.remove(p)

            # カメラをプレイヤー中心に追従
            self.camera_x = self.player.x - SCREEN_W // 2
            self.camera_y = self.player.y - SCREEN_H // 2
            self.camera_x = max(0, min(MAP_W - SCREEN_W, self.camera_x))
            self.camera_y = max(0, min(MAP_H - SCREEN_H, self.camera_y))

        elif self.state == STATE_RESULT:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
                self.state = STATE_PLAYING
            elif pyxel.btnp(pyxel.KEY_Q):
                self.state = STATE_TITLE

    def calculate_result(self):
        blue_cnt = 0
        orange_cnt = 0
        total_floor = 0
        
        for y in range(MAP_ROWS):
            for x in range(MAP_COLS):
                if self.map_grid[y][x] != TILE_WALL:
                    total_floor += 1
                    if self.map_grid[y][x] == TILE_PLAYER_INK:
                        blue_cnt += 1
                    elif self.map_grid[y][x] == TILE_ENEMY_INK:
                        orange_cnt += 1
                        
        if total_floor > 0:
            self.blue_percent = (blue_cnt / total_floor) * 100
            self.orange_percent = (orange_cnt / total_floor) * 100
            self.empty_percent = 100.0 - self.blue_percent - self.orange_percent

    def draw(self):
        pyxel.cls(0)
        
        if self.state == STATE_TITLE:
            self.draw_title()
        elif self.state == STATE_PLAYING:
            self.draw_game()
        elif self.state == STATE_RESULT:
            self.draw_result()

    def draw_title(self):
        pyxel.cls(5) # 暗いグレー背景
        
        # 160 x 120 用に座標調整
        pyxel.text(46, 20, "S P L A T P Y X E L", COLOR_BLUE_INK)
        pyxel.text(48, 22, "S P L A T P Y X E L", COLOR_ORANGE_INK)
        pyxel.text(47, 21, "S P L A T P Y X E L", 7)
        
        pyxel.rect(10, 45, 140, 60, 1)
        pyxel.rectb(10, 45, 140, 60, 7)
        
        pyxel.text(15, 50, "CONTROLS:", 10)
        pyxel.text(15, 60, "- MOVE:  W KEY (To mouse direction)", 7)
        pyxel.text(15, 70, "- SHOOT: MOUSE LEFT CLICK", 7)
        pyxel.text(15, 80, "- SQUID: SPACE / SHIFT (in Ink)", 7)
        pyxel.text(15, 90, "- GOAL:  Paint the most turf in 60s!", 7)
        
        pyxel.text(25, 110, "PRESS ENTER TO START BATTLE!", pyxel.frame_count % 30 < 15 and 7 or 13)

    def draw_game(self):
        start_col = max(0, int(self.camera_x // GRID_SIZE))
        end_col = min(MAP_COLS, int((self.camera_x + SCREEN_W) // GRID_SIZE) + 1)
        start_row = max(0, int(self.camera_y // GRID_SIZE))
        end_row = min(MAP_ROWS, int((self.camera_y + SCREEN_H) // GRID_SIZE) + 1)
        
        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                tile = self.map_grid[y][x]
                screen_x = x * GRID_SIZE - self.camera_x
                screen_y = y * GRID_SIZE - self.camera_y
                
                if tile == TILE_WALL:
                    pyxel.rect(screen_x, screen_y, GRID_SIZE, GRID_SIZE, COLOR_WALL)
                    pyxel.rectb(screen_x, screen_y, GRID_SIZE, GRID_SIZE, 0) # 壁の輪郭線は黒
                elif tile == TILE_PLAYER_INK:
                    pyxel.rect(screen_x, screen_y, GRID_SIZE, GRID_SIZE, COLOR_BLUE_INK)
                elif tile == TILE_ENEMY_INK:
                    pyxel.rect(screen_x, screen_y, GRID_SIZE, GRID_SIZE, COLOR_ORANGE_INK)
                else:
                    pyxel.rect(screen_x, screen_y, GRID_SIZE, GRID_SIZE, COLOR_BG)
                    # 白い床にライトグレー(6)の細い枠を描く
                    if (x + y) % 2 == 0:
                        pyxel.rectb(screen_x, screen_y, GRID_SIZE, GRID_SIZE, 6)

        for b in self.bullets:
            b.draw(self.camera_x, self.camera_y)

        self.player.draw(self.camera_x, self.camera_y)
        for actor in self.actors:
            actor.draw(self.camera_x, self.camera_y)

        for p in self.particles:
            p.draw(self.camera_x, self.camera_y)

        self.draw_ui()

    def draw_ui(self):
        # 160 x 120 画面用にUI座標を完全調整
        seconds = self.game_timer // 30
        time_color = 7
        if seconds <= 10:
            time_color = 8
            if pyxel.frame_count % 10 < 5:
                time_color = 7
        pyxel.rect(55, 2, 50, 12, 0)
        pyxel.rectb(55, 2, 50, 12, time_color)
        pyxel.text(67, 5, f"TIME:{seconds:02d}s", time_color)

        # インクタンク (コンパクト化)
        gauge_w = 40
        gauge_h = 5
        gx = SCREEN_W - gauge_w - 6
        gy = SCREEN_H - gauge_h - 6
        
        pyxel.rect(gx - 2, gy - 2, gauge_w + 4, gauge_h + 4, 0)
        pyxel.rectb(gx - 2, gy - 2, gauge_w + 4, gauge_h + 4, 7)
        fill_w = int(gauge_w * (self.player.ink / self.player.max_ink))
        if fill_w > 0:
            pyxel.rect(gx, gy, fill_w, gauge_h, COLOR_BLUE_INK)
        pyxel.line(gx + int(gauge_w * 0.4), gy, gx + int(gauge_w * 0.4), gy + gauge_h - 1, 7)
        pyxel.text(gx - 20, gy, "INK", 7)

        # HPゲージ (コンパクト化)
        hx = 22
        hy = SCREEN_H - 11
        pyxel.rect(hx - 2, hy - 2, 44, 9, 0)
        pyxel.rectb(hx - 2, hy - 2, 44, 9, 7)
        
        hp_w = int(40 * (self.player.hp / self.player.max_hp))
        if hp_w > 0:
            hp_color = 11 if self.player.hp > 20 else 8
            pyxel.rect(hx, hy, hp_w, 5, hp_color)
        pyxel.text(hx - 16, hy + 1, "HP", 7)
        
        if self.player.ink < 10 and pyxel.frame_count % 20 < 10:
            pyxel.text(SCREEN_W // 2 - 24, SCREEN_H // 2 + 15, "LOW INK!", 8)

        # ミニマップ (右上)
        mx = SCREEN_W - 33
        my = 2
        pyxel.rect(mx - 1, my - 1, 32, 32, 0)
        pyxel.rectb(mx - 1, my - 1, 32, 32, 7)
        
        for y in range(0, MAP_ROWS, 2):
            for x in range(0, MAP_COLS, 2):
                tile = self.map_grid[y][x]
                if tile == TILE_WALL:
                    color = COLOR_WALL
                elif tile == TILE_PLAYER_INK:
                    color = COLOR_BLUE_INK
                elif tile == TILE_ENEMY_INK:
                    color = COLOR_ORANGE_INK
                else:
                    color = COLOR_BG
                pyxel.pset(mx + x//2, my + y//2, color)
                
        m_px = mx + int(self.player.x // (GRID_SIZE * 2))
        m_py = my + int(self.player.y // (GRID_SIZE * 2))
        if pyxel.frame_count % 10 < 5:
            pyxel.pset(m_px, m_py, 7)

        if not self.player.is_alive():
            seconds_left = math.ceil(self.player.respawn_timer / 30)
            pyxel.text(SCREEN_W // 2 - 40, SCREEN_H // 2 - 5, f"RESPAWNING IN {seconds_left}", 8)

    def draw_result(self):
        pyxel.cls(0)
        
        # 160 x 120 用に座標調整
        y_bar = 60
        bar_h = 16
        bar_max_w = SCREEN_W - 40
        
        blue_w = int(bar_max_w * (self.blue_percent / 100))
        orange_w = int(bar_max_w * (self.orange_percent / 100))
        
        pyxel.rect(20, y_bar, blue_w, bar_h, COLOR_BLUE_INK)
        pyxel.rect(20 + blue_w, y_bar, bar_max_w - blue_w, bar_h, COLOR_BG)
        pyxel.rect(SCREEN_W - 20 - orange_w, y_bar, orange_w, bar_h, COLOR_ORANGE_INK)
        pyxel.rectb(20, y_bar, bar_max_w, bar_h, 7)
        
        pyxel.text(20, y_bar - 10, f"BLUE: {self.blue_percent:.1f}%", COLOR_BLUE_INK)
        pyxel.text(SCREEN_W - 75, y_bar - 10, f"ORANGE: {self.orange_percent:.1f}%", COLOR_ORANGE_INK)
        
        if self.blue_percent > self.orange_percent:
            pyxel.text(SCREEN_W // 2 - 20, y_bar + 25, "VICTORY!", COLOR_BLUE_HERO)
        elif self.blue_percent < self.orange_percent:
            pyxel.text(SCREEN_W // 2 - 20, y_bar + 25, "DEFEAT...", COLOR_ORANGE_HERO)
        else:
            pyxel.text(SCREEN_W // 2 - 10, y_bar + 25, "DRAW!", 7)
            
        pyxel.text(35, SCREEN_H - 22, "PRESS R TO PLAY AGAIN", 7)
        pyxel.text(35, SCREEN_H - 12, "PRESS Q TO GO TO TITLE", 13)

# 起動
if __name__ == "__main__":
    App()
