import pyxel
import math
import random

# --- Constants ---
SCREEN_W = 160
SCREEN_H = 120
GRID = 8
COLS = 100
ROWS = 100

MODE_COMBAT = 0
MODE_BUILD = 1

EMPTY = 0
TERRAIN = 1
CORE = 2
WALL_WOOD = 3
WALL_BRICK = 4
WALL_METAL = 5

MAT_HP = {
    WALL_WOOD: 200,
    WALL_BRICK: 500,
    WALL_METAL: 1000
}

MAT_COLOR = {
    WALL_WOOD: 4,   # Brown
    WALL_BRICK: 9,  # Orange
    WALL_METAL: 13  # Gray
}

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = 60

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 30
        self.speed = 0.5
        self.attack_cooldown = 0
        self.damage = 10

class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, fps=30, title="Save The Core")
        pyxel.mouse(True)
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.map_grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.grid_hp = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.wall_orientations = {} # (gx, gy) -> 'H' or 'V'
        
        self.core_x = COLS // 2
        self.core_y = ROWS // 2
        self.core_hp = 1000
        self.core_max_hp = 1000
        
        # コアの配置 (3x3)
        for cy in range(self.core_y - 1, self.core_y + 2):
            for cx in range(self.core_x - 1, self.core_x + 2):
                self.map_grid[cy][cx] = CORE
        
        # 地形（TERRAIN）の配置
        for _ in range(150):
            rx = random.randint(2, COLS - 5)
            ry = random.randint(2, ROWS - 5)
            w = random.randint(2, 4)
            h = random.randint(2, 4)
            # コア付近には生成しない
            if math.hypot(rx - self.core_x, ry - self.core_y) > 10:
                for dy in range(h):
                    for dx in range(w):
                        if self.map_grid[ry+dy][rx+dx] == EMPTY:
                            self.map_grid[ry+dy][rx+dx] = TERRAIN

        self.player_x = self.core_x * GRID
        self.player_y = (self.core_y + 4) * GRID
        self.player_speed = 2
        
        self.mode = MODE_COMBAT
        
        # 0: Wood, 1: Brick, 2: Metal
        self.materials = [1000, 1000, 1000]
        self.selected_mat = 0
        
        self.bullets = []
        self.enemies = []
        
        self.frame_count = 0
        self.game_over = False
        
        self.build_gx = 0
        self.build_gy = 0

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        self.frame_count += 1
        
        # カメラとマウス位置の計算
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        camera_x = self.player_x - SCREEN_W // 2
        camera_y = self.player_y - SCREEN_H // 2
        
        world_mx = mx + camera_x
        world_my = my + camera_y
        
        angle = math.atan2(world_my - self.player_y, world_mx - self.player_x)
        
        # プレイヤーの移動 (向いている方向を基準にWASD)
        dx, dy = 0, 0
        if pyxel.btn(pyxel.KEY_W):
            dx += math.cos(angle)
            dy += math.sin(angle)
        if pyxel.btn(pyxel.KEY_S):
            dx -= math.cos(angle)
            dy -= math.sin(angle)
        if pyxel.btn(pyxel.KEY_A):
            dx += math.cos(angle - math.pi/2)
            dy += math.sin(angle - math.pi/2)
        if pyxel.btn(pyxel.KEY_D):
            dx += math.cos(angle + math.pi/2)
            dy += math.sin(angle + math.pi/2)
        
        if dx != 0 or dy != 0:
            move_angle = math.atan2(dy, dx)
            new_x = self.player_x + math.cos(move_angle) * self.player_speed
            new_y = self.player_y + math.sin(move_angle) * self.player_speed
            
            # 地形コリジョン（プレイヤーが地形を通れないようにする簡易判定）
            gx = int(new_x // GRID)
            gy = int(new_y // GRID)
            if 0 <= gx < COLS and 0 <= gy < ROWS:
                if self.map_grid[gy][gx] not in [TERRAIN, CORE, WALL_WOOD, WALL_BRICK, WALL_METAL]:
                    self.player_x = new_x
                    self.player_y = new_y

        self.player_x = max(0, min(COLS*GRID-1, self.player_x))
        self.player_y = max(0, min(ROWS*GRID-1, self.player_y))
        
        # モードと資材の切り替え
        if pyxel.btnp(pyxel.KEY_B) or pyxel.btnp(pyxel.KEY_Q):
            self.mode = MODE_BUILD if self.mode == MODE_COMBAT else MODE_COMBAT
            
        if pyxel.btnp(pyxel.KEY_1): self.selected_mat = 0
        if pyxel.btnp(pyxel.KEY_2): self.selected_mat = 1
        if pyxel.btnp(pyxel.KEY_3): self.selected_mat = 2
        
        # 建築ターゲットの計算（目の前のグリッドにスナップ）
        build_dist = GRID * 1.5
        target_x = self.player_x + math.cos(angle) * build_dist
        target_y = self.player_y + math.sin(angle) * build_dist
        self.build_gx = int(target_x // GRID)
        self.build_gy = int(target_y // GRID)
            
        # アクション
        if self.mode == MODE_COMBAT:
            # 射撃
            if self.frame_count % 5 == 0 and (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.KEY_SPACE)):
                speed = 6
                bx = math.cos(angle) * speed
                by = math.sin(angle) * speed
                self.bullets.append(Bullet(self.player_x, self.player_y, bx, by))
        elif self.mode == MODE_BUILD and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            # ターボ建築（押しっぱなしで建築）
            gx = self.build_gx
            gy = self.build_gy
            if 0 <= gx < COLS and 0 <= gy < ROWS:
                if self.map_grid[gy][gx] == EMPTY and self.materials[self.selected_mat] >= 10:
                    dist = math.hypot(self.player_x - gx*GRID - GRID/2, self.player_y - gy*GRID - GRID/2)
                    if dist > GRID/2: # プレイヤーの立ち位置には置けない
                        self.materials[self.selected_mat] -= 10
                        cell_type = [WALL_WOOD, WALL_BRICK, WALL_METAL][self.selected_mat]
                        self.map_grid[gy][gx] = cell_type
                        self.grid_hp[gy][gx] = MAT_HP[cell_type]
                        # 向きの記録 (向いている方向に対して垂直になるように)
                        is_horiz = abs(math.sin(angle)) > abs(math.cos(angle))
                        self.wall_orientations[(gx, gy)] = 'H' if is_horiz else 'V'

        self.update_bullets()
        self.spawn_enemies()
        self.update_enemies()

    def update_bullets(self):
        for b in self.bullets[:]:
            b.x += b.dx
            b.y += b.dy
            b.life -= 1
            if b.life <= 0:
                if b in self.bullets: self.bullets.remove(b)
                continue
                
            gx = int(b.x // GRID)
            gy = int(b.y // GRID)
            
            # グリッドとの当たり判定（壁は攻撃で壊せる）
            if 0 <= gx < COLS and 0 <= gy < ROWS:
                cell = self.map_grid[gy][gx]
                if cell in [WALL_WOOD, WALL_BRICK, WALL_METAL]:
                    self.grid_hp[gy][gx] -= 10
                    if self.grid_hp[gy][gx] <= 0:
                        self.map_grid[gy][gx] = EMPTY
                        if (gx, gy) in self.wall_orientations:
                            del self.wall_orientations[(gx, gy)]
                    if b in self.bullets: self.bullets.remove(b)
                    continue
                elif cell == TERRAIN:
                    # 地形には弾が消える
                    if b in self.bullets: self.bullets.remove(b)
                    continue
            
            # 敵との当たり判定
            for e in self.enemies:
                if abs(b.x - e.x) < 6 and abs(b.y - e.y) < 6:
                    e.hp -= 15
                    if b in self.bullets: self.bullets.remove(b)
                    break

    def spawn_enemies(self):
        # 時間経過でスポーン頻度上昇
        spawn_rate = max(10, 60 - self.frame_count // 150)
        if self.frame_count % spawn_rate == 0:
            side = random.randint(0, 3)
            if side == 0: # 上
                ex, ey = random.randint(0, COLS*GRID), 0
            elif side == 1: # 下
                ex, ey = random.randint(0, COLS*GRID), ROWS*GRID
            elif side == 2: # 左
                ex, ey = 0, random.randint(0, ROWS*GRID)
            else: # 右
                ex, ey = COLS*GRID, random.randint(0, ROWS*GRID)
            self.enemies.append(Enemy(ex, ey))

    def update_enemies(self):
        target_x = self.core_x * GRID + GRID/2
        target_y = self.core_y * GRID + GRID/2
        
        for e in self.enemies[:]:
            if e.hp <= 0:
                self.enemies.remove(e)
                continue
                
            # コアへ向かって移動
            ang = math.atan2(target_y - e.y, target_x - e.x)
            next_x = e.x + math.cos(ang) * e.speed
            next_y = e.y + math.sin(ang) * e.speed
            
            gx = int(next_x // GRID)
            gy = int(next_y // GRID)
            
            can_move = True
            if 0 <= gx < COLS and 0 <= gy < ROWS:
                cell = self.map_grid[gy][gx]
                if cell in [WALL_WOOD, WALL_BRICK, WALL_METAL, CORE]:
                    can_move = False
                    if e.attack_cooldown <= 0:
                        e.attack_cooldown = 30
                        if cell == CORE:
                            self.core_hp -= e.damage
                            if self.core_hp <= 0:
                                self.game_over = True
                        else:
                            self.grid_hp[gy][gx] -= e.damage
                            if self.grid_hp[gy][gx] <= 0:
                                self.map_grid[gy][gx] = EMPTY
                                if (gx, gy) in self.wall_orientations:
                                    del self.wall_orientations[(gx, gy)]
                elif cell == TERRAIN:
                    # 地形を避ける簡単な挙動（ランダムに迂回）
                    can_move = False
                    e.x += random.choice([-1, 1])
                    e.y += random.choice([-1, 1])
                            
            if can_move:
                e.x = next_x
                e.y = next_y
            
            if e.attack_cooldown > 0:
                e.attack_cooldown -= 1

    def draw_battery(self, x, y, value, is_selected):
        # 小さめの電池枠 (17x5)
        col = 10 if is_selected else 5
        pyxel.rectb(x, y, 17, 5, col)
        pyxel.rect(x+17, y+1, 1, 3, col)
        
        # 閾値
        thresholds = [10, 50, 100, 500, 1000]
        segments = sum(1 for t in thresholds if value >= t)
                
        # メモリの描画
        for i in range(segments):
            mem_col = 11 if value >= 500 else (9 if value >= 100 else 8)
            pyxel.rect(x + 1 + i * 3, y + 1, 2, 3, mem_col)

    def draw(self):
        pyxel.cls(3) # 背景（緑）
        
        camera_x = int(self.player_x - SCREEN_W // 2)
        camera_y = int(self.player_y - SCREEN_H // 2)

        start_col = max(0, camera_x // GRID)
        end_col = min(COLS, (camera_x + SCREEN_W) // GRID + 1)
        start_row = max(0, camera_y // GRID)
        end_row = min(ROWS, (camera_y + SCREEN_H) // GRID + 1)

        # マップ描画
        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                cell = self.map_grid[y][x]
                draw_x = x * GRID - camera_x
                draw_y = y * GRID - camera_y
                
                if cell == EMPTY:
                    if (x * 7 + y * 13) % 5 == 0:
                        pyxel.pset(draw_x + 2, draw_y + 2, 11)
                elif cell == TERRAIN:
                    pyxel.rect(draw_x, draw_y, GRID, GRID, 1) # 深い紺色（通れない崖）
                    pyxel.pset(draw_x+2, draw_y+2, 5)
                elif cell in [WALL_WOOD, WALL_BRICK, WALL_METAL]:
                    col = MAT_COLOR[cell]
                    ori = self.wall_orientations.get((x, y), 'H')
                    
                    # 板として描画（厚さ2）
                    if ori == 'H':
                        pyxel.rect(draw_x, draw_y + GRID//2 - 1, GRID, 2, col)
                    else:
                        pyxel.rect(draw_x + GRID//2 - 1, draw_y, 2, GRID, col)
                    
                    hp_ratio = self.grid_hp[y][x] / MAT_HP[cell]
                    if hp_ratio < 0.5:
                        # ダメージインジケーター
                        if ori == 'H':
                            pyxel.pset(draw_x + GRID//2, draw_y + GRID//2 - 1, 0)
                        else:
                            pyxel.pset(draw_x + GRID//2 - 1, draw_y + GRID//2, 0)
                            
                elif cell == CORE:
                    pyxel.rect(draw_x, draw_y, GRID, GRID, 12)
                    pyxel.circ(draw_x+4, draw_y+4, 2, 7)

        # 敵描画
        for e in self.enemies:
            draw_x = e.x - camera_x
            draw_y = e.y - camera_y
            pyxel.circ(draw_x, draw_y, 3, 8)
            pyxel.circ(draw_x-1, draw_y-1, 1, 0)

        # 弾描画
        for b in self.bullets:
            pyxel.circ(b.x - camera_x, b.y - camera_y, 1, 10)

        # プレイヤー描画 (小さくする)
        player_draw_x = self.player_x - camera_x
        player_draw_y = self.player_y - camera_y
        pyxel.circ(player_draw_x, player_draw_y, 2, 9)
        
        # プレイヤーの照準方向
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        world_mx = mx + camera_x
        world_my = my + camera_y
        angle = math.atan2(world_my - self.player_y, world_mx - self.player_x)
        line_ex = player_draw_x + math.cos(angle) * 5
        line_ey = player_draw_y + math.sin(angle) * 5
        pyxel.line(player_draw_x, player_draw_y, line_ex, line_ey, 0)

        # 建築モードのプレビュー
        if self.mode == MODE_BUILD:
            gx = self.build_gx
            gy = self.build_gy
            if 0 <= gx < COLS and 0 <= gy < ROWS and self.map_grid[gy][gx] == EMPTY:
                draw_x = gx * GRID - camera_x
                draw_y = gy * GRID - camera_y
                prev_col = [4, 9, 13][self.selected_mat]
                is_horiz = abs(math.sin(angle)) > abs(math.cos(angle))
                
                if is_horiz:
                    pyxel.rect(draw_x, draw_y + GRID//2 - 1, GRID, 2, prev_col)
                else:
                    pyxel.rect(draw_x + GRID//2 - 1, draw_y, 2, GRID, prev_col)

        # UI描画
        # 左上: コアHPなど
        pyxel.rect(0, 0, 70, 10, 0)
        pyxel.text(2, 2, f"CORE: {self.core_hp}/{self.core_max_hp}", 7 if self.core_hp > 300 else 8)
        
        mode_text = "BUILD MODE" if self.mode == MODE_BUILD else "COMBAT MODE"
        mode_color = 10 if self.mode == MODE_BUILD else 8
        pyxel.rect(SCREEN_W//2 - 20, 0, 40, 10, 0)
        pyxel.text(SCREEN_W//2 - 18, 2, mode_text, mode_color)

        # 右下: インベントリ（小さくした電池風UI）
        bx = SCREEN_W - 30
        by = SCREEN_H - 22
        labels = ["W", "B", "M"]
        for i in range(3):
            self.draw_battery(bx + 8, by + i * 7, self.materials[i], self.selected_mat == i)
            pyxel.text(bx, by + i * 7, labels[i], 7)

        # ゲームオーバー画面
        if self.game_over:
            pyxel.rect(SCREEN_W//2 - 30, SCREEN_H//2 - 10, 60, 20, 0)
            pyxel.text(SCREEN_W//2 - 18, SCREEN_H//2 - 6, "GAME OVER", 8)
            pyxel.text(SCREEN_W//2 - 24, SCREEN_H//2 + 2, "PRESS R RETRY", 7)

if __name__ == "__main__":
    App()
