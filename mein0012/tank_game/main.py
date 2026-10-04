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
        # プレイヤー戦車データ (16pxグリッドに合わせて中央に配置)
        self.x = W // 2
        self.y = 96   # ちょうどプレイエリア (16~176) の中央
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

        # スタミナ & ダッシュ (Shiftキー)
        self.stamina = 100.0
        self.max_stamina = 100.0
        self.is_dashing = False

        # 地雷 (右クリック)
        self.mines = []
        self.mine_cooldown = 0
        self.max_mine_cooldown = 45  # 1.5秒

        # 操作のコツ (ヘルプ画面表示)
        self.show_help = False

        # 弾・エフェクトリスト
        self.bullets = []
        self.particles = []

        # 壁データ (すべて 16px グリッドの倍数にきれいに整列)
        self.walls = [
            {"x": 64, "y": 32, "w": 16, "h": 48},   # 左上縦壁 (col 4, row 2~4)
            {"x": 176, "y": 32, "w": 16, "h": 48},  # 右上縦壁 (col 11, row 2~4)
            {"x": 64, "y": 112, "w": 16, "h": 48},  # 左下縦壁 (col 4, row 7~9)
            {"x": 176, "y": 112, "w": 16, "h": 48}, # 右下縦壁 (col 11, row 7~9)
            {"x": 112, "y": 48, "w": 32, "h": 16},  # 中央上横壁 (col 7~8, row 3)
            {"x": 112, "y": 128, "w": 32, "h": 16}, # 中央下横壁 (col 7~8, row 8)
        ]

        # 敵戦車データ
        self.enemies = []
        # プレイヤーから離れた位置に敵を配置 (x, y, type) - 16pxグリッド位置
        enemy_configs = [
            (32, 40, "light"),
            (W - 32, 40, "light"),
            (32, 152, "heavy"),
            (W - 32, 152, "normal"),
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
        # 操作のコツ / ヘルプ画面のトグル (Hキー)
        if pyxel.btnp(pyxel.KEY_H):
            self.show_help = not self.show_help

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

            # ダッシュ判定 (Shiftキー) - スタミナ管理
            is_shift = pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.KEY_LSHIFT) or pyxel.btn(pyxel.KEY_RSHIFT)
            if is_shift and self.stamina > 5:
                self.is_dashing = True
                self.stamina = max(0.0, self.stamina - 2.0)
            else:
                self.is_dashing = False
                self.stamina = min(self.max_stamina, self.stamina + 0.8)

            # 前進・後退 (W/S)
            move_dir = 0
            if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
                move_dir += 1   # 前進
            if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
                move_dir -= 1   # 後退

            if move_dir != 0:
                # 速度 (ダッシュ時は1.8倍)
                speed_mult = 1.8 if self.is_dashing else 1.0
                base_speed = self.speed if move_dir > 0 else self.speed * 0.6
                current_speed = base_speed * speed_mult
                
                # 位置の更新 (壁衝突時のスライド移動のため個別に更新)
                dx = math.cos(self.hull_angle) * current_speed * move_dir
                dy = math.sin(self.hull_angle) * current_speed * move_dir

                self.x += dx
                self.x = max(6, min(W - 6, self.x))
                if self.check_wall_collision(self.x, self.y, 6):  # プレイヤー半径6
                    self.x -= dx

                self.y += dy
                # 上部UIバー(0~16px)と下部ガイドバー(176~192px)を侵犯しないよう y: 22~170 (16+6 ~ 176-6) に制限
                self.y = max(22, min(170, self.y))
                if self.check_wall_collision(self.x, self.y, 6):
                    self.y -= dy

                # 排気煙エフェクト (ダッシュ時は強力に発生)
                smoke_freq = 1 if self.is_dashing else 3
                if pyxel.frame_count % smoke_freq == 0:
                    back_x = self.x - math.cos(self.hull_angle) * 8
                    back_y = self.y - math.sin(self.hull_angle) * 8
                    smoke_color = random.choice([7, 10]) if self.is_dashing else 5
                    self.particles.append({
                        "x": back_x, "y": back_y,
                        "vx": random.uniform(-0.4, 0.4), "vy": random.uniform(-0.4, 0.4),
                        "color": smoke_color, "life": 12 if self.is_dashing else 10
                    })

            # 2. 砲塔の照準 (マウスカーソルへの旋回)
            self.turret_angle = math.atan2(pyxel.mouse_y - self.y, pyxel.mouse_x - self.x)

            # 3. リロードタイマー & 地雷クールダウンの更新
            if self.reload_timer > 0:
                self.reload_timer -= 1
            if self.mine_cooldown > 0:
                self.mine_cooldown -= 1

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

            # 4.5. 地雷設置 (右クリック & クールダウン完了時)
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and self.mine_cooldown == 0:
                self.mine_cooldown = self.max_mine_cooldown
                self.mines.append({
                    "x": self.x,
                    "y": self.y,
                    "arm_timer": 15,  # 設置後0.5秒で有効化
                    "radius": 16,
                    "damage": 3
                })
                # 設置時の火花
                for _ in range(6):
                    self.particles.append({
                        "x": self.x, "y": self.y,
                        "vx": random.uniform(-1.0, 1.0), "vy": random.uniform(-1.0, 1.0),
                        "color": 10, "life": 8
                    })
                pyxel.play(0, 0)

        # 5. 敵のAI更新 (プレイヤーが生存時のみ - 壁回避AI搭載)
        if self.hp > 0:
            for e in self.enemies:
                # 回避用変数の初期化
                if "avoid_timer" not in e:
                    e["avoid_timer"] = 0
                    e["avoid_dir"] = 1

                # プレイヤーへの角度と距離を計算
                dx = self.x - e["x"]
                dy = self.y - e["y"]
                dist = math.sqrt(dx*dx + dy*dy)

                # 砲塔は常にプレイヤーを狙う
                e["turret_angle"] = math.atan2(dy, dx)

                # 基本目標角度 (プレイヤーの方向)
                direct_angle = math.atan2(dy, dx)
                target_hull_angle = direct_angle

                # 前方障害物探知センサー (18px先)
                sensor_dist = 18
                front_x = e["x"] + math.cos(direct_angle) * sensor_dist
                front_y = e["y"] + math.sin(direct_angle) * sensor_dist

                # 直進前方に壁があるかチェック
                if self.check_wall_collision(front_x, front_y, e["radius"]):
                    if e["avoid_timer"] == 0:
                        e["avoid_timer"] = 25  # 回避行動フレーム
                        # 左右のセンサーで壁の少ない方向へ迂回
                        left_x = e["x"] + math.cos(direct_angle - math.pi / 3) * sensor_dist
                        left_y = e["y"] + math.sin(direct_angle - math.pi / 3) * sensor_dist
                        left_hit = self.check_wall_collision(left_x, left_y, e["radius"])
                        e["avoid_dir"] = 1 if left_hit else -1

                # 回避モード発動中の角度調整
                if e["avoid_timer"] > 0:
                    e["avoid_timer"] -= 1
                    target_hull_angle = direct_angle + (math.pi / 2.2) * e["avoid_dir"]

                # 車体の向きをスムーズに合わせる
                angle_diff = (target_hull_angle - e["hull_angle"] + math.pi) % (math.pi * 2) - math.pi
                e["hull_angle"] += max(-0.1, min(0.1, angle_diff))

                # 一定の距離より遠ければ前進
                if dist > 50:
                    edx = math.cos(e["hull_angle"]) * e["speed"]
                    edy = math.sin(e["hull_angle"]) * e["speed"]

                    # X軸移動 & 衝突回避
                    e["x"] += edx
                    e["x"] = max(e["radius"], min(W - e["radius"], e["x"]))
                    if self.check_wall_collision(e["x"], e["y"], e["radius"]):
                        e["x"] -= edx
                        e["avoid_timer"] = 20
                        e["avoid_dir"] = random.choice([1, -1])

                    # Y軸移動 & 衝突回避
                    e["y"] += edy
                    e["y"] = max(16 + e["radius"], min(176 - e["radius"], e["y"]))
                    if self.check_wall_collision(e["x"], e["y"], e["radius"]):
                        e["y"] -= edy
                        e["avoid_timer"] = 20
                        e["avoid_dir"] = random.choice([1, -1])

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

            # 画面外（UIバー/ガイドバー境界含む）または寿命切れで消滅
            if b["life"] <= 0 or b["x"] <= 0 or b["x"] >= W or b["y"] <= 16 or b["y"] >= 176:
                if b in self.bullets:
                    self.bullets.remove(b)
                # 境界へのヒット火花
                for _ in range(3):
                    self.particles.append({
                        "x": b["x"], "y": b["y"],
                        "vx": random.uniform(-1.0, 1.0), "vy": random.uniform(-1.0, 1.0),
                        "color": random.choice([7, 13, 5]), "life": 5
                    })
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

        # 6.5. 地雷の更新 & 起爆判定
        for m in self.mines[:]:
            if m["arm_timer"] > 0:
                m["arm_timer"] -= 1

            # 起爆チェック (敵との接近判定)
            if m["arm_timer"] == 0:
                triggered = False
                for e in self.enemies:
                    mdx = e["x"] - m["x"]
                    mdy = e["y"] - m["y"]
                    mdist = math.sqrt(mdx * mdx + mdy * mdy)
                    if mdist < (m["radius"] + e["radius"]):
                        triggered = True
                        break

                if triggered:
                    # 地雷爆発！ 爆風範囲内のすべての敵にダメージ
                    for e in self.enemies[:]:
                        mdx = e["x"] - m["x"]
                        mdy = e["y"] - m["y"]
                        mdist = math.sqrt(mdx * mdx + mdy * mdy)
                        if mdist < (m["radius"] + 12):
                            e["hp"] -= m["damage"]
                            for _ in range(8):
                                self.particles.append({
                                    "x": e["x"], "y": e["y"],
                                    "vx": random.uniform(-2.5, 2.5), "vy": random.uniform(-2.5, 2.5),
                                    "color": random.choice([8, 9, 10]), "life": 12
                                })
                            if e["hp"] <= 0 and e in self.enemies:
                                self.enemies.remove(e)
                                self.score += e.get("score_value", 100)
                                pyxel.play(1, 1)
                                for _ in range(25):
                                    self.particles.append({
                                        "x": e["x"], "y": e["y"],
                                        "vx": random.uniform(-3.5, 3.5), "vy": random.uniform(-3.5, 3.5),
                                        "color": random.choice([7, 8, 9, 10, 14]), "life": 16
                                    })

                    # 地雷自身の爆発エフェクト
                    for _ in range(30):
                        ang = random.uniform(0, math.pi * 2)
                        sp = random.uniform(0.5, 4.0)
                        self.particles.append({
                            "x": m["x"], "y": m["y"],
                            "vx": math.cos(ang) * sp, "vy": math.sin(ang) * sp,
                            "color": random.choice([7, 8, 9, 10]), "life": 15
                        })
                    pyxel.play(1, 1)
                    if m in self.mines:
                        self.mines.remove(m)

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
        # 背景クリア (ダークブルー)
        pyxel.cls(1)

        # 均一な1pxグリッド線の描画 (画面全体に16px間隔で正確に描画)
        for x in range(0, W + 1, 16):
            pyxel.line(x, 0, x, H, 5)
        for y in range(0, H + 1, 16):
            pyxel.line(0, y, W, y, 5)

        # 壁の描画 (グリッド線と重なって線が太くならないよう、マス目の内側に均一描画)
        for w in self.walls:
            # マス目の内側を壁の本体色(5:暗いグレー)で塗り潰し
            pyxel.rect(w["x"] + 1, w["y"] + 1, w["w"] - 1, w["h"] - 1, 5)
            # マス目の内側境界に枠線(13:明るいグレー)を描画して線の太さを完全均一(1px)化
            pyxel.rectb(w["x"] + 1, w["y"] + 1, w["w"] - 1, w["h"] - 1, 13)

        # パーティクルの描画
        for p in self.particles:
            pyxel.pset(p["x"], p["y"], p["color"])

        # 地雷の描画
        for m in self.mines:
            if m["arm_timer"] > 0:
                # 起爆準備中 (点滅)
                col = 5 if pyxel.frame_count % 4 < 2 else 13
                pyxel.circb(m["x"], m["y"], 3, col)
            else:
                # 起爆準備完了 (赤/橙の点滅リング)
                col = 8 if pyxel.frame_count % 6 < 3 else 9
                pyxel.circ(m["x"], m["y"], 3, col)
                pyxel.circb(m["x"], m["y"], 5, 8)
                pyxel.pset(m["x"], m["y"], 7)

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

            # 車体中央部 (ダッシュ時は輝く)
            body_color = 10 if self.is_dashing else 11
            pyxel.circ(self.x, self.y, 6, body_color)
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

        # 上部 UI バー (高さ 16px: y = 0 ~ 16)
        pyxel.rect(0, 0, W, 16, 0)
        pyxel.line(0, 16, W, 16, 13)

        # UI 1: HP & SCORE
        hp_str = "HP:" + "♥" * self.hp + "♡" * (5 - self.hp)
        score_str = f"SCORE:{self.score:04d}"
        pyxel.text(4, 5, hp_str, 8 if self.hp <= 1 else 7)
        pyxel.text(68, 5, score_str, 7)

        if self.hp > 0:
            # UI 2: DASH Gauge (Shift)
            pyxel.text(125, 5, "DASH", 10 if self.is_dashing else 7)
            stamina_w = int(20 * (self.stamina / self.max_stamina))
            stamina_col = 10 if self.stamina > 30 else 8
            pyxel.rect(145, 6, 20, 4, 5)
            pyxel.rect(145, 6, stamina_w, 4, stamina_col)

            # UI 3: MINE Cool (R-Click)
            if self.mine_cooldown > 0:
                m_prog = (self.max_mine_cooldown - self.mine_cooldown) / self.max_mine_cooldown
                pyxel.text(172, 5, "MINE", 9)
                pyxel.rect(192, 6, 16, 4, 5)
                pyxel.rect(192, 6, int(16 * m_prog), 4, 9)
            else:
                pyxel.text(172, 5, "MINE", 11)
                pyxel.rect(192, 6, 16, 4, 11)

            # UI 4: SHOOT (L-Click)
            if self.reload_timer > 0:
                r_prog = (self.max_reload_time - self.reload_timer) / self.max_reload_time
                pyxel.text(214, 5, "SHOT", 9)
                pyxel.rect(234, 6, 18, 4, 5)
                pyxel.rect(234, 6, int(18 * r_prog), 4, 10)
            else:
                pyxel.text(214, 5, "SHOT", 11)
                pyxel.rect(234, 6, 18, 4, 11)

        # 画面最下部: 操作ガイドバー (高さ 16px: y = 176 ~ 192)
        pyxel.rect(0, 176, W, 16, 0)
        pyxel.line(0, 176, W, 176, 5)
        pyxel.text(4, 181, "[H] Tips | WASD:Move  Shift:Dash  L-Click:Shot  R-Click:Mine", 6)

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

        # 操作のコツ ポップアップ (Hキーで表示切替)
        if self.show_help:
            bx, by = 10, 20
            bw, bh = 236, 155
            pyxel.rect(bx, by, bw, bh, 0)
            pyxel.rectb(bx, by, bw, bh, 10)
            pyxel.rectb(bx + 1, by + 1, bw - 2, bh - 2, 7)

            pyxel.text(bx + 35, by + 6, "--- TIPS FOR SMOOTH PLAY ---", 10)

            # コツ 1: 移動と照準を切り離す
            pyxel.text(bx + 8, by + 22, "1. Separate Move & Aim (Twin-stick)", 11)
            pyxel.text(bx + 14, by + 32, "WASD for Move, Mouse for Aiming.", 7)
            pyxel.text(bx + 14, by + 42, "Shoot backward while running away!", 7)

            # コツ 2: ダッシュの管理
            pyxel.text(bx + 8, by + 58, "2. Manage Dash (Shift Key)", 11)
            pyxel.text(bx + 14, by + 68, "Use Dash to dodge bullets & gain advantage.", 7)
            pyxel.text(bx + 14, by + 78, "Watch your stamina bar carefully!", 7)

            # コツ 3: 地雷の設置
            pyxel.text(bx + 8, by + 94, "3. Mine Timing (Right Click)", 11)
            pyxel.text(bx + 14, by + 104, "Place mines in escape paths to easily kill", 7)
            pyxel.text(bx + 14, by + 114, "chasing enemy tanks!", 7)

            pyxel.text(bx + 60, by + 138, "[ Press H to Close ]", 9)

if __name__ == "__main__":
    TankGame()

