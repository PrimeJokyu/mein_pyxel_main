import pyxel
import math
import random

TILE_SIZE = 8
FIELD_WIDTH = 50
FIELD_HEIGHT = 50

class SplatoonCursorBomb:
    def __init__(self):
        pyxel.init(160, 120, title="カーソル爆発ボム")
        self.x = FIELD_WIDTH * TILE_SIZE // 2
        self.y = FIELD_HEIGHT * TILE_SIZE // 2
        self.angle = 0
        self.hp = 3
        self.alive = True
        self.bomb_cooldown = 0
        self.explosions = []

        self.enemies = [
            {"x": 100, "y": 100, "hp": 3, "alive": True},
            {"x": 250, "y": 180, "hp": 3, "alive": True}
        ]

        self.ink_particles = []
        self.field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.frame_count = 0

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.frame_count += 1
        if not self.alive:
            return

        dx = pyxel.mouse_x - pyxel.width // 2
        dy = pyxel.mouse_y - pyxel.height // 2
        self.angle = math.atan2(dy, dx)

        speed = 2
        move_x = move_y = 0
        if pyxel.btn(pyxel.KEY_W):
            move_x += math.cos(self.angle) * speed
            move_y += math.sin(self.angle) * speed
        if pyxel.btn(pyxel.KEY_S):
            move_x -= math.cos(self.angle) * speed
            move_y -= math.sin(self.angle) * speed
        if pyxel.btn(pyxel.KEY_A):
            move_x += math.cos(self.angle - math.pi / 2) * speed
            move_y += math.sin(self.angle - math.pi / 2) * speed
        if pyxel.btn(pyxel.KEY_D):
            move_x += math.cos(self.angle + math.pi / 2) * speed
            move_y += math.sin(self.angle + math.pi / 2) * speed

        self.x = max(0, min(self.x + move_x, FIELD_WIDTH * TILE_SIZE - 1))
        self.y = max(0, min(self.y + move_y, FIELD_HEIGHT * TILE_SIZE - 1))

        if pyxel.btn(pyxel.KEY_SPACE) and self.frame_count % 3 == 0:
            self.shoot_ink(self.x, self.y, self.angle, 9, "player")

        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1
        if pyxel.btnp(pyxel.KEY_Q) and self.bomb_cooldown == 0:
            self.shoot_cursor_bomb()
            self.bomb_cooldown = 180

        for enemy in self.enemies:
            if enemy["alive"] and self.frame_count % 60 == 0:
                angle = math.atan2(self.y - enemy["y"], self.x - enemy["x"])
                self.shoot_ink(enemy["x"], enemy["y"], angle, 8, "enemy")

        new_particles = []
        for p in self.ink_particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["life"] -= 1

            tx = int(p["x"]) // TILE_SIZE
            ty = int(p["y"]) // TILE_SIZE
            if 0 <= tx < FIELD_WIDTH and 0 <= ty < FIELD_HEIGHT:
                self.field[ty][tx] = p["color"]

            if p["owner"] == "player":
                hit = False
                for enemy in self.enemies:
                    if enemy["alive"] and math.hypot(p["x"] - enemy["x"], p["y"] - enemy["y"]) < 6:
                        enemy["hp"] -= 1
                        if enemy["hp"] <= 0:
                            enemy["alive"] = False
                        hit = True
                        break
                if not hit and p["life"] > 0:
                    new_particles.append(p)
            elif p["owner"] == "enemy":
                if math.hypot(p["x"] - self.x, p["y"] - self.y) < 6:
                    self.hp -= 1
                    if self.hp <= 0:
                        self.alive = False
                elif p["life"] > 0:
                    new_particles.append(p)
        self.ink_particles = new_particles

        # 爆発エフェクトの寿命処理
        self.explosions = [e for e in self.explosions if e["life"] > 0]
        for e in self.explosions:
            e["life"] -= 1

    def shoot_ink(self, x, y, angle, color, owner):
        for _ in range(10):
            spread = random.uniform(-0.1, 0.1)
            dx = math.cos(angle + spread) * random.uniform(2.0, 2.8)
            dy = math.sin(angle + spread) * random.uniform(2.0, 2.8)
            self.ink_particles.append({
                "x": x + math.cos(angle) * 4,
                "y": y + math.sin(angle) * 4,
                "dx": dx,
                "dy": dy,
                "life": 20,
                "color": color,
                "owner": owner
            })

    def shoot_cursor_bomb(self):
        cx = self.x - pyxel.width // 2 + pyxel.mouse_x
        cy = self.y - pyxel.height // 2 + pyxel.mouse_y

        # フィールド塗り
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                tx = x * TILE_SIZE + TILE_SIZE // 2
                ty = y * TILE_SIZE + TILE_SIZE // 2
                if math.hypot(cx - tx, cy - ty) < 24:
                    self.field[y][x] = 10

        # 敵ダメージ
        for enemy in self.enemies:
            if enemy["alive"] and math.hypot(cx - enemy["x"], cy - enemy["y"]) < 24:
                enemy["alive"] = False

        # 爆発演出を登録
        self.explosions.append({
            "x": cx,
            "y": cy,
            "life": 20
        })

    def draw(self):
        pyxel.cls(0)
        offset_x = int(self.x) - pyxel.width // 2
        offset_y = int(self.y) - pyxel.height // 2

        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                c = self.field[y][x]
                if c != 0:
                    px = x * TILE_SIZE - offset_x
                    py = y * TILE_SIZE - offset_y
                    if 0 <= px < pyxel.width and 0 <= py < pyxel.height:
                        pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, c)

        # プレイヤー
        px, py = pyxel.width // 2, pyxel.height // 2
        pyxel.circ(px, py, 4, 7)
        pyxel.line(px, py, px + math.cos(self.angle) * 6, py + math.sin(self.angle) * 6, 10)

        # 敵
        for enemy in self.enemies:
            if enemy["alive"]:
                ex = enemy["x"] - offset_x
                ey = enemy["y"] - offset_y
                pyxel.circ(ex, ey, 4, 8)
                angle = math.atan2(self.y - enemy["y"], self.x - enemy["x"])
                pyxel.line(ex, ey, ex + math.cos(angle) * 6, ey + math.sin(angle) * 6, 11)

        # 爆発エフェクト
        for e in self.explosions:
            ex = e["x"] - offset_x
            ey = e["y"] - offset_y
            r = e["life"]
            pyxel.circ(ex, ey, r // 2 + 6, 10)
            pyxel.circ(ex, ey, r // 3 + 4, 8)

        pyxel.text(2, 5, f"HP: {self.hp}", 7)
        pyxel.text(2, 115, "SPACE: Ink  Q: Bomb", 6)
        if not self.alive:
            pyxel.text(55, 60, "GAME OVER", 8)

SplatoonCursorBomb()
