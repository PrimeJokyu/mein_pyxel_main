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

        # サウンド設定 (0番: 発砲音, 1番: 爆発音)
        pyxel.sounds[0].set("c3c2", "n", "72", "f", 4)
        pyxel.sounds[1].set("c1c2g1c1", "s", "7474", "f", 8)

        self.reset_game()

        pyxel.run(self.update, self.draw)

    def check_wall_collision(self, x, y, r):
        for w in self.walls:
            closest_x = max(w["x"], min(x, w["x"] + w["w"]))
            closest_y = max(w["y"], min(y, w["y"] + w["h"]))
            dist_x = x - closest_x
            dist_y = y - closest_y
            dist_sq = dist_x * dist_x + dist_y * dist_y
            if dist_sq < r * r:
                return True
        return False

    def reset_game(self):
        # プレイヤー戦車データ
        self.x = W // 2
        self.y = H // 2
        self.speed = 1.5
        self.hull_angle = 0.0     # 車体の向き（ラジアン）
        self.turret_angle = 0.0   # 砲塔の向き（ラジアン）
        self.hp = 5
        self.score = 0
        
        # ゲーム状態
        self.is_gameover = False
        self.is_cleared = False
        
        # リロード時間管理 (15フレーム = 0.5秒)
        self.reload_timer = 0
        self.max_reload_time = 15

        # 弾・エフェクトリスト
        self.bullets = []
        self.particles = []

        # 壁データ
        self.walls = [
            {"x": 70, "y": 30, "w": 16, "h": 50},   # 左上縦壁
            {"x": 170, "y": 30, "w": 16, "h": 50},  # 右上縦壁
            {"x": 70, "y": 112, "w": 16, "h": 50},  # 左下縦壁
            {"x": 170, "y": 112, "w": 16, "h": 50}, # 右下縦壁
            {"x": 118, "y": 45, "w": 20, "h": 16},  # 中央上横壁
            {"x": 118, "y": 130, "w": 20, "h": 16}, # 中央下横壁
        ]

        # 敵戦車データ
        self.enemies = []
        # プレイヤーから離れた位置に敵を配置 (x, y, type)
        enemy_configs = [
            (30, 30, "light"),
            (W - 30, 30, "light"),
            (30, H - 30, "heavy"),
            (W - 30, H - 30, "normal"),
        ]
        for ex, ey, etype in enemy_configs:
            if etype == "light":
                hp = 1
                speed = 1.1
                shoot_interval = 60
                radius = 5
                color = 9
                score_value = 50
            elif etype == "heavy":
                hp = 4
                speed = 0.35
                shoot_interval = 130
                radius = 8
                color = 2
                score_value = 250
            else: # normal
                hp = 2
                speed = 0.6
                shoot_interval = 90
                radius = 6
                color = 8
                score_value = 100

            self.enemies.append({
                "x": ex,
                "y": ey,
                "type": etype,
                "hull_angle": random.uniform(0, math.pi * 2),
                "turret_angle": 0.0,
                "speed": speed,
                "hp": hp,
                "max_hp": hp,
                "shoot_timer": random.randint(20, shoot_interval),
                "shoot_interval": shoot_interval,
                "radius": radius,
                "color": color,
                "score_value": score_value
            })

    def update(self):
        # ゲームオーバーまたはクリア時のリスタート処理
        if self.is_gameover or self.is_cleared:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
            return

        # 1. 戦車の操縦 (生存時のみ)
        if self.hp > 0:
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
                
                # 位置の更新 (壁衝突時のスライド移動のため個別に更新)
                dx = math.cos(self.hull_angle) * current_speed * move_dir
                dy = math.sin(self.hull_angle) * current_speed * move_dir

                self.x += dx
                self.x = max(10, min(W - 10, self.x))
                if self.check_wall_collision(self.x, self.y, 6):  # プレイヤー半径6
                    self.x -= dx

                self.y += dy
                self.y = max(10, min(H - 10, self.y))
                if self.check_wall_collision(self.x, self.y, 6):
                    self.y -= dy

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
                    "life": 60,
                    "owner": "player",
                    "radius": 2,
                    "damage": 1
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

        # 5. 敵のAI更新 (プレイヤーが生存時のみ)
        if self.hp > 0:
            for e in self.enemies:
                # プレイヤーへの角度と距離を計算
                dx = self.x - e["x"]
                dy = self.y - e["y"]
                dist = math.sqrt(dx*dx + dy*dy)

                # プレイヤーの方向へ砲塔を向ける
                e["turret_angle"] = math.atan2(dy, dx)

                # 車体の向きをゆっくりプレイヤーに合わせる
                target_hull_angle = math.atan2(dy, dx)
                angle_diff = (target_hull_angle - e["hull_angle"] + math.pi) % (math.pi * 2) - math.pi
                e["hull_angle"] += max(-0.05, min(0.05, angle_diff))

                # 一定の距離より遠ければ前進
                if dist > 60:
                    edx = math.cos(e["hull_angle"]) * e["speed"]
                    edy = math.sin(e["hull_angle"]) * e["speed"]

                    e["x"] += edx
                    e["x"] = max(10, min(W - 10, e["x"]))
                    if self.check_wall_collision(e["x"], e["y"], e["radius"]):
                        e["x"] -= edx

                    e["y"] += edy
                    e["y"] = max(10, min(H - 10, e["y"]))
                    if self.check_wall_collision(e["x"], e["y"], e["radius"]):
                        e["y"] -= edy

                    # 敵の排気煙
                    if pyxel.frame_count % 5 == 0:
                        back_x = e["x"] - math.cos(e["hull_angle"]) * 8
                        back_y = e["y"] - math.sin(e["hull_angle"]) * 8
                        self.particles.append({
                            "x": back_x, "y": back_y,
                            "vx": random.uniform(-0.2, 0.2), "vy": random.uniform(-0.2, 0.2),
                            "color": 13, "life": 8
                        })

                # 射撃タイマーの更新
                if e["shoot_timer"] > 0:
                    e["shoot_timer"] -= 1
                else:
                    e["shoot_timer"] = e["shoot_interval"] + random.randint(-15, 15)
                    barrel_len = e["radius"] + 4
                    ebx = e["x"] + math.cos(e["turret_angle"]) * barrel_len
                    eby = e["y"] + math.sin(e["turret_angle"]) * barrel_len

                    # 敵の弾の性能を設定
                    bullet_speed = 3.5
                    bullet_radius = 2
                    bullet_damage = 1
                    
                    if e["type"] == "heavy":
                        bullet_speed = 2.2
                        bullet_radius = 3.5
                        bullet_damage = 2
                    elif e["type"] == "light":
                        bullet_speed = 4.5
                        bullet_radius = 1.5

                    # 敵の弾を追加
                    self.bullets.append({
                        "x": ebx, "y": eby,
                        "vx": math.cos(e["turret_angle"]) * bullet_speed,
                        "vy": math.sin(e["turret_angle"]) * bullet_speed,
                        "life": 70,
                        "owner": "enemy",
                        "radius": bullet_radius,
                        "damage": bullet_damage
                    })

                    # 敵の発砲火花
                    for _ in range(4):
                        ang = e["turret_angle"] + random.uniform(-0.4, 0.4)
                        sp = random.uniform(1.0, 2.5)
                        self.particles.append({
                            "x": ebx, "y": eby,
                            "vx": math.cos(ang) * sp, "vy": math.sin(ang) * sp,
                            "color": random.choice([7, 8, 14]), "life": 5
                        })
                    pyxel.play(0, 0)

        # 6. 弾の移動 & 衝突判定処理
        for b in self.bullets[:]:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
            b["life"] -= 1

            # 画面外または寿命切れで消滅
            if b["life"] <= 0 or b["x"] < 0 or b["x"] > W or b["y"] < 0 or b["y"] > H:
                if b in self.bullets:
                    self.bullets.remove(b)
                continue

            # 壁との衝突判定
            if self.check_wall_collision(b["x"], b["y"], b.get("radius", 2)):
                if b in self.bullets:
                    self.bullets.remove(b)
                # 壁への衝突火花エフェクト
                for _ in range(4):
                    self.particles.append({
                        "x": b["x"], "y": b["y"],
                        "vx": random.uniform(-1.2, 1.2), "vy": random.uniform(-1.2, 1.2),
                        "color": random.choice([7, 13, 5]), "life": 6
                    })
                continue

            # 衝突判定
            if b["owner"] == "player":
                # プレイヤーの弾が敵に当たったか
                hit_enemy = False
                for e in self.enemies[:]:
                    edx = b["x"] - e["x"]
                    edy = b["y"] - e["y"]
                    edist = math.sqrt(edx*edx + edy*edy)
                    if edist < (e["radius"] + b.get("radius", 2)):  # 半径の合計で判定
                        e["hp"] -= 1
                        hit_enemy = True
                        
                        # 火花エフェクト
                        for _ in range(5):
                            self.particles.append({
                                "x": b["x"], "y": b["y"],
                                "vx": random.uniform(-1.5, 1.5), "vy": random.uniform(-1.5, 1.5),
                                "color": random.choice([8, 9, 10]), "life": 8
                            })

                        if e["hp"] <= 0:
                            self.enemies.remove(e)
                            self.score += e.get("score_value", 100)
                            pyxel.play(1, 1)  # 爆発音再生

                            # 敵撃破時の大爆発エフェクト
                            for _ in range(20):
                                self.particles.append({
                                    "x": e["x"], "y": e["y"],
                                    "vx": random.uniform(-3.0, 3.0), "vy": random.uniform(-3.0, 3.0),
                                    "color": random.choice([7, 8, 9, 10, 14]), "life": 15
                                })
                        break
                if hit_enemy:
                    if b in self.bullets:
                        self.bullets.remove(b)
            
            elif b["owner"] == "enemy":
                # 敵の弾がプレイヤーに当たったか
                if self.hp > 0:
                    pdx = b["x"] - self.x
                    pdy = b["y"] - self.y
                    pdist = math.sqrt(pdx*pdx + pdy*pdy)
                    if pdist < (6 + b.get("radius", 2)):  # プレイヤー半径6 + 弾の半径
                        self.hp -= b.get("damage", 1)
                        if b in self.bullets:
                            self.bullets.remove(b)
                        
                        # 被弾エフェクト
                        for _ in range(8):
                            self.particles.append({
                                "x": b["x"], "y": b["y"],
                                "vx": random.uniform(-2.0, 2.0), "vy": random.uniform(-2.0, 2.0),
                                "color": random.choice([8, 11, 12]), "life": 10
                            })
                        
                        if self.hp <= 0:
                            self.hp = 0
                            self.is_gameover = True
                            pyxel.play(1, 1)  # 爆発音再生
                            
                            # プレイヤー撃破時の大爆発エフェクト
                            for _ in range(30):
                                self.particles.append({
                                    "x": self.x, "y": self.y,
                                    "vx": random.uniform(-4.0, 4.0), "vy": random.uniform(-4.0, 4.0),
                                    "color": random.choice([7, 8, 9, 10, 14]), "life": 20
                                })

        # ステージクリア判定
        if len(self.enemies) == 0 and not self.is_gameover:
            self.is_cleared = True

        # 7. パーティクルの更新
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

        # 壁の描画
        for w in self.walls:
            pyxel.rect(w["x"], w["y"], w["w"], w["h"], 5)   # 本体: 暗いグレー(5)
            pyxel.rectb(w["x"], w["y"], w["w"], w["h"], 13) # 枠線: 明るいグレー(13)

        # パーティクルの描画
        for p in self.particles:
            pyxel.pset(p["x"], p["y"], p["color"])

        # 弾の描画
        for b in self.bullets:
            color = 10 if b["owner"] == "player" else 8
            radius = b.get("radius", 2)
            pyxel.circ(b["x"], b["y"], radius, color)
            pyxel.circb(b["x"], b["y"], radius, 0)

        # 敵戦車の描画
        for e in self.enemies:
            cos_e = math.cos(e["hull_angle"])
            sin_e = math.sin(e["hull_angle"])

            # 敵のキャタピラ (左右。サイズに応じて動的に調整)
            side_dist = e["radius"] - 1
            len_dist = e["radius"]
            for side in [-side_dist, side_dist]:
                tx1 = e["x"] + side * (-sin_e) - len_dist * cos_e
                ty1 = e["y"] + side * (cos_e) - len_dist * sin_e
                tx2 = e["x"] + side * (-sin_e) + len_dist * cos_e
                ty2 = e["y"] + side * (cos_e) + len_dist * sin_e
                pyxel.line(tx1, ty1, tx2, ty2, 0)

            # 敵の車体中央部
            pyxel.circ(e["x"], e["y"], e["radius"], e["color"])
            pyxel.circb(e["x"], e["y"], e["radius"], 2 if e["type"] == "heavy" else 0)

            # 敵の砲塔 & 砲身 (プレイヤー向き)
            barrel_len = e["radius"] + 4
            barrel_x = e["x"] + math.cos(e["turret_angle"]) * barrel_len
            barrel_y = e["y"] + math.sin(e["turret_angle"]) * barrel_len
            pyxel.line(e["x"], e["y"], barrel_x, barrel_y, 0)
            
            # 砲塔の色 (少し明るい色)
            turret_color = 10 if e["type"] == "light" else (9 if e["type"] == "normal" else 14)
            turret_r = max(2.5, e["radius"] * 0.5)
            pyxel.circ(e["x"], e["y"], turret_r, turret_color)
            pyxel.circb(e["x"], e["y"], turret_r, 0)

            # 敵のHPゲージ (頭上)
            bar_w = e["radius"] * 2
            bar_h = 2
            bx = e["x"] - bar_w // 2
            by = e["y"] - e["radius"] - 4
            pyxel.rect(bx, by, bar_w, bar_h, 0)
            hp_w = int(bar_w * (e["hp"] / e["max_hp"]))
            pyxel.rect(bx, by, hp_w, bar_h, 8)

        # プレイヤー戦車の描画 (生存時のみ)
        if self.hp > 0:
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
        
        # UI情報の描画 (ハートマークでHP表示)
        hp_str = "HP: " + "♥" * self.hp + "♡" * (5 - self.hp)
        score_str = f"SCORE: {self.score}"
        pyxel.text(5, 3, f"{hp_str}  {score_str}", 7)

        # リロードインジケーター / メーター表示
        if self.hp > 0:
            if self.reload_timer > 0:
                progress = (self.max_reload_time - self.reload_timer) / self.max_reload_time
                pyxel.text(175, 3, "RELOAD", 9)
                pyxel.rect(205, 4, 40, 4, 8)
                pyxel.rect(205, 4, int(40 * progress), 4, 10)
            else:
                pyxel.text(175, 3, "READY", 11)
                pyxel.rect(205, 4, 40, 4, 11)

        # ゲームオーバー・クリア画面表示
        if self.is_gameover:
            pyxel.rect(W // 2 - 60, H // 2 - 20, 120, 40, 0)
            pyxel.rectb(W // 2 - 60, H // 2 - 20, 120, 40, 8)
            pyxel.text(W // 2 - 27, H // 2 - 10, "GAME OVER", 8)
            pyxel.text(W // 2 - 45, H // 2 + 5, "PRESS ENTER TO PLAY", 7)
        
        elif self.is_cleared:
            pyxel.rect(W // 2 - 65, H // 2 - 20, 130, 40, 0)
            pyxel.rectb(W // 2 - 65, H // 2 - 20, 130, 40, 11)
            pyxel.text(W // 2 - 32, H // 2 - 10, "STAGE CLEAR!", 11)
            pyxel.text(W // 2 - 45, H // 2 + 5, "PRESS ENTER TO PLAY", 7)

if __name__ == "__main__":
    TankGame()

