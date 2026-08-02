import pyxel
import math
import random

# 画面サイズ
W, H = 256, 192

class TankGame:
    def __init__(self):
        # Pyxel初期化
        pyxel.init(W, H, title="Simple 2D Tank", fps=30)
        pyxel.mouse(True)

        # サウンド設定 (0番: 発砲音)
        pyxel.sounds[0].set("c3c2", "n", "72", "f", 4)

        # プレイヤー戦車データ
        self.x = W // 2
        self.y = H // 2
        self.speed = 1.5
        self.hull_angle = 0.0     # 車体の向き（ラジアン）
        self.turret_angle = 0.0   # 砲塔の向き（ラジアン）
        
        # リロード時間管理 (15フレーム = 0.5秒)
        self.reload_timer = 0
        self.max_reload_time = 15

        # 弾・エフェクトリスト
        self.bullets = []
        self.particles = []

        pyxel.run(self.update, self.draw)

    def update(self):
        # 1. 戦車の操縦 (A/D or LEFT/RIGHT: 旋回, W/S or UP/DOWN: 前進・後退)
        # 旋回 (A/D)
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            self.hull_angle -= 0.08  # 左旋回
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.hull_angle += 0.08  # 右旋回

        # 前進・後退 (W/S)
        move_dir = 0
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            move_dir += 1   # 前進
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            move_dir -= 1   # 後退

        if move_dir != 0:
            # 速度 (前進は通常速度、後退は少し遅め)
            current_speed = self.speed if move_dir > 0 else self.speed * 0.6
            
            # 位置の更新
            self.x += math.cos(self.hull_angle) * current_speed * move_dir
            self.y += math.sin(self.hull_angle) * current_speed * move_dir

            # 画面外に出ないよう制限
            self.x = max(10, min(W - 10, self.x))
            self.y = max(10, min(H - 10, self.y))

            # 排気煙エフェクト (走行中のみ発生)
            if pyxel.frame_count % 3 == 0:
                back_x = self.x - math.cos(self.hull_angle) * 8
                back_y = self.y - math.sin(self.hull_angle) * 8
                self.particles.append({
                    "x": back_x, "y": back_y,
                    "vx": random.uniform(-0.3, 0.3), "vy": random.uniform(-0.3, 0.3),
                    "color": 5, "life": 10
                })

        # 2. 砲塔の照準 (マウスカーソルへの旋回)
        self.turret_angle = math.atan2(pyxel.mouse_y - self.y, pyxel.mouse_x - self.x)

        # 3. リロードタイマーの更新
        if self.reload_timer > 0:
            self.reload_timer -= 1

        # 4. 主砲発射 (マウス左クリック長押し対応 & リロード完了時)
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.reload_timer == 0:
            self.reload_timer = self.max_reload_time  # リロード開始

            barrel_len = 10
            bx = self.x + math.cos(self.turret_angle) * barrel_len
            by = self.y + math.sin(self.turret_angle) * barrel_len
            
            # 弾を追加
            self.bullets.append({
                "x": bx, "y": by,
                "vx": math.cos(self.turret_angle) * 5.0,
                "vy": math.sin(self.turret_angle) * 5.0,
                "life": 60
            })

            # 発砲火花エフェクト
            for _ in range(6):
                ang = self.turret_angle + random.uniform(-0.4, 0.4)
                sp = random.uniform(1.0, 3.0)
                self.particles.append({
                    "x": bx, "y": by,
                    "vx": math.cos(ang) * sp, "vy": math.sin(ang) * sp,
                    "color": random.choice([7, 10, 9]), "life": 6
                })

            # 効果音再生
            pyxel.play(0, 0)

        # 5. 弾の移動 & 消滅処理
        for b in self.bullets[:]:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
            b["life"] -= 1
            if b["life"] <= 0 or b["x"] < 0 or b["x"] > W or b["y"] < 0 or b["y"] > H:
                self.bullets.remove(b)

        # 6. パーティクルの更新
        for p in self.particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
            if p["life"] <= 0:
                self.particles.remove(p)

    def draw(self):
        # 背景クリア (ダークブルー/グレー)
        pyxel.cls(1)

        # グリッド線の描画 (背景装飾)
        for x in range(0, W, 16):
            pyxel.line(x, 0, x, H, 5)
        for y in range(0, H, 16):
            pyxel.line(0, y, W, y, 5)

        # パーティクルの描画
        for p in self.particles:
            pyxel.pset(p["x"], p["y"], p["color"])

        # 弾の描画
        for b in self.bullets:
            pyxel.circ(b["x"], b["y"], 2, 10)
            pyxel.circb(b["x"], b["y"], 2, 0)

        # 戦車本体 (緑色の回転体表現)
        # キャタピラ (左右)
        cos_h = math.cos(self.hull_angle)
        sin_h = math.sin(self.hull_angle)

        for side in [-5, 5]:
            tx1 = self.x + side * (-sin_h) - 6 * cos_h
            ty1 = self.y + side * (cos_h) - 6 * sin_h
            tx2 = self.x + side * (-sin_h) + 6 * cos_h
            ty2 = self.y + side * (cos_h) + 6 * sin_h
            pyxel.line(tx1, ty1, tx2, ty2, 0)

        # 車体中央部
        pyxel.circ(self.x, self.y, 6, 11)
        pyxel.circb(self.x, self.y, 6, 3)

        # 砲塔 & 砲身 (マウス向き)
        barrel_x = self.x + math.cos(self.turret_angle) * 10
        barrel_y = self.y + math.sin(self.turret_angle) * 10
        pyxel.line(self.x, self.y, barrel_x, barrel_y, 0)
        pyxel.circ(self.x, self.y, 3, 10)
        pyxel.circb(self.x, self.y, 3, 0)

        # 照準カーソル
        pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, 4, 10)
        pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, 8)

        # 上部 UI バー
        pyxel.rect(0, 0, W, 12, 0)
        pyxel.text(5, 3, "W/S: FWD/BWD  A/D: TURN  MOUSE: AIM", 7)

        # リロードインジケーター / メーター表示
        if self.reload_timer > 0:
            progress = (self.max_reload_time - self.reload_timer) / self.max_reload_time
            pyxel.text(175, 3, "RELOAD", 9)
            pyxel.rect(205, 4, 40, 4, 8)
            pyxel.rect(205, 4, int(40 * progress), 4, 10)
        else:
            pyxel.text(175, 3, "READY", 11)
            pyxel.rect(205, 4, 40, 4, 11)

if __name__ == "__main__":
    TankGame()

