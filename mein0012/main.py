# Version: 1.0.3 (Ultra Small Tiles)
import pyxel
import random
import math

# Constants
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
TILE_SIZE = 2  # Ultra small!
GRID_W = SCREEN_WIDTH // TILE_SIZE
GRID_H = SCREEN_HEIGHT // TILE_SIZE

# Colors
COL_BG = 0
COL_WALL = 13
COL_WALL_LOW = 5
COL_BASE = 11
COL_ENEMY = 8
COL_TURRET = 12
COL_SHOT = 10
COL_TEXT = 7
COL_HOVER = 5
COL_DAMAGE = 8

# Block Types
TYPE_NONE = 0
TYPE_WALL = 1
TYPE_TURRET = 2
TYPE_BASE = 9

# Costs
COST_WALL = 1
COST_TURRET = 5 # Increased relative cost

# Game States
STATE_TITLE = 0
STATE_BUILD = 1
STATE_DEFEND = 2
STATE_GAMEOVER = 3

class Block:
    def __init__(self, btype):
        self.type = btype
        self.flash_timer = 0
        if btype == TYPE_WALL:
            self.hp = 3
            self.max_hp = 3
        elif btype == TYPE_TURRET:
            self.hp = 2
            self.max_hp = 2
        else:
            self.hp = 20
            self.max_hp = 20

class Enemy:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 0.3
        self.hp = 3
        self.alive = True
        self.attack_cooldown = 0

    def update(self, app):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            return

        gx = int(self.x // TILE_SIZE)
        gy = int(self.y // TILE_SIZE)
        
        target_block = None
        if 0 <= gx < GRID_W and 0 <= gy < GRID_H:
             if app.grid[gy][gx] is not None:
                  target_block = app.grid[gy][gx]

        if target_block:
            self.attack_cooldown = 30
            target_block.hp -= 1
            target_block.flash_timer = 5
            if target_block.hp <= 0:
                if target_block.type == TYPE_BASE:
                    app.state = STATE_GAMEOVER
                app.grid[gy][gx] = None
            return

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self):
        # Draw enemy even smaller - just a pixel
        pyxel.pset(self.x, self.y, COL_ENEMY)

class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 2.0
        self.alive = True

    def update(self):
        if not self.target.alive:
            self.alive = False
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist < self.speed:
            self.x = self.target.x
            self.y = self.target.y
            self.target.hp -= 1
            if self.target.hp <= 0:
                self.target.alive = False
            self.alive = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self):
        pyxel.pset(self.x, self.y, COL_SHOT)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Block Defense", fps=60)
        pyxel.mouse(True)
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.state = STATE_TITLE
        self.blocks = 100 # Lots of blocks for small size
        self.grid = [[None for _ in range(GRID_W)] for _ in range(GRID_H)]
        self.enemies = []
        self.projectiles = []
        self.wave = 1
        self.spawn_timer = 0
        self.base_x = GRID_W // 2
        self.base_y = GRID_H // 2
        self.selected_type = TYPE_WALL
        
        # Place 2x2 base
        for dy in range(2):
            for dx in range(2):
                if 0 <= self.base_y + dy < GRID_H and 0 <= self.base_x + dx < GRID_W:
                    self.grid[self.base_y + dy][self.base_x + dx] = Block(TYPE_BASE)

    def update(self):
        if self.state == STATE_TITLE:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = STATE_BUILD
        
        elif self.state == STATE_BUILD:
            if pyxel.btnp(pyxel.KEY_1): self.selected_type = TYPE_WALL
            if pyxel.btnp(pyxel.KEY_2): self.selected_type = TYPE_TURRET

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT): # Allow drag-placing
                mx, my = pyxel.mouse_x // TILE_SIZE, pyxel.mouse_y // TILE_SIZE
                if 0 <= mx < GRID_W and 0 <= my < GRID_H:
                    current = self.grid[my][mx]
                    if current is None:
                        cost = COST_WALL if self.selected_type == TYPE_WALL else COST_TURRET
                        if self.blocks >= cost:
                            self.grid[my][mx] = Block(self.selected_type)
                            self.blocks -= cost
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT): # Right click to remove
                mx, my = pyxel.mouse_x // TILE_SIZE, pyxel.mouse_y // TILE_SIZE
                if 0 <= mx < GRID_W and 0 <= my < GRID_H:
                    current = self.grid[my][mx]
                    if current and current.type != TYPE_BASE:
                        refund = COST_WALL if current.type == TYPE_WALL else COST_TURRET
                        self.blocks += refund
                        self.grid[my][mx] = None
            
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = STATE_DEFEND
                self.spawn_timer = 0
                self.enemies_to_spawn = 10 + self.wave * 5

        elif self.state == STATE_DEFEND:
            if self.enemies_to_spawn > 0:
                self.spawn_timer += 1
                if self.spawn_timer > 30: # Faster spawn for more enemies
                    self.spawn_enemy()
                    self.enemies_to_spawn -= 1
                    self.spawn_timer = 0
            
            if self.enemies_to_spawn == 0 and not self.enemies:
                self.wave += 1
                self.blocks += 30
                self.state = STATE_BUILD
                return

            for enemy in self.enemies:
                enemy.update(self)

            for proj in self.projectiles:
                proj.update()

            self.enemies = [e for e in self.enemies if e.alive]
            self.projectiles = [p for p in self.projectiles if p.alive]

            for y in range(GRID_H):
                for x in range(GRID_W):
                    if self.grid[y][x]:
                        if self.grid[y][x].flash_timer > 0:
                             self.grid[y][x].flash_timer -= 1

            if pyxel.frame_count % 30 == 0:
                for y in range(GRID_H):
                    for x in range(GRID_W):
                        blk = self.grid[y][x]
                        if blk and blk.type == TYPE_TURRET:
                            self.fire_turret(x * TILE_SIZE + TILE_SIZE/2, y * TILE_SIZE + TILE_SIZE/2)

        elif self.state == STATE_GAMEOVER:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()

    def spawn_enemy(self):
        side = random.randint(0, 3)
        if side == 0: x, y = random.randint(0, SCREEN_WIDTH), -2
        elif side == 1: x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 2
        elif side == 2: x, y = -2, random.randint(0, SCREEN_HEIGHT)
        else: x, y = SCREEN_WIDTH + 2, random.randint(0, SCREEN_HEIGHT)
        self.enemies.append(Enemy(x, y, self.base_x * TILE_SIZE + 1, self.base_y * TILE_SIZE + 1))

    def fire_turret(self, tx, ty):
        closest, min_dist = None, 30
        for enemy in self.enemies:
            dist = math.hypot(enemy.x - tx, enemy.y - ty)
            if dist < min_dist: min_dist, closest = dist, enemy
        if closest: self.projectiles.append(Projectile(tx, ty, closest))

    def draw(self):
        pyxel.cls(COL_BG)
        if self.state == STATE_TITLE:
            pyxel.text(55, 50, "DEFENSE", COL_TEXT)
            pyxel.text(45, 70, "PRESS SPACE", COL_TEXT)
            return

        for y in range(GRID_H):
            for x in range(GRID_W):
                blk = self.grid[y][x]
                if blk:
                    color = COL_WALL
                    if blk.type == TYPE_WALL and blk.hp <= 1: color = COL_WALL_LOW
                    elif blk.type == TYPE_TURRET: color = COL_TURRET
                    elif blk.type == TYPE_BASE: color = COL_BASE
                    if blk.flash_timer > 0: color = COL_DAMAGE
                    pyxel.rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, color)

        if self.state == STATE_BUILD:
            pyxel.text(2, 2, f"M:{self.blocks} W:{self.wave}", COL_TEXT)
            sel_text = "WALL(1)" if self.selected_type == TYPE_WALL else "TURRET(2)"
            pyxel.text(60, 2, sel_text, COL_WALL if self.selected_type == TYPE_WALL else COL_TURRET)
            pyxel.text(120, 2, "ENTER:GO", COL_TEXT)
            mx, my = pyxel.mouse_x // TILE_SIZE, pyxel.mouse_y // TILE_SIZE
            if 0 <= mx < GRID_W and 0 <= my < GRID_H:
                 pyxel.rectb(mx * TILE_SIZE, my * TILE_SIZE, TILE_SIZE, TILE_SIZE, COL_HOVER)
        elif self.state == STATE_DEFEND:
            pyxel.text(2, 2, f"WAVE: {self.wave}", COL_TEXT)
            for e in self.enemies: e.draw()
            for p in self.projectiles: p.draw()
        elif self.state == STATE_GAMEOVER:
            pyxel.text(60, 50, "GAME OVER", 8)
            pyxel.text(50, 70, "PRESS SPACE", 7)

App()
