import pyxel
import math
import random
import ctypes
import os

# 画面サイズ
W, H = 256, 192

def start_bgm(filename="Pixel_Sprint.mp3"):
    """WindowsのMCI機能を利用してMP3音楽をループ再生する"""
    abs_path = os.path.abspath(filename)
    ctypes.windll.winmm.mciSendStringW(f'open "{abs_path}" type mpegvideo alias bgm', None, 0, 0)
    ctypes.windll.winmm.mciSendStringW('play bgm repeat', None, 0, 0)

def stop_bgm():
    """BGM再生を停止してリソースを解放する"""
    ctypes.windll.winmm.mciSendStringW('stop bgm', None, 0, 0)
    ctypes.windll.winmm.mciSendStringW('close bgm', None, 0, 0)

def check_wall_collision(walls, x, y, r):
    """壁との衝突判定"""
    for w in walls:
        closest_x = max(w["x"], min(x, w["x"] + w["w"]))
        closest_y = max(w["y"], min(y, w["y"] + w["h"]))
        dist_x = x - closest_x
        dist_y = y - closest_y
        dist_sq = dist_x * dist_x + dist_y * dist_y
        if dist_sq < r * r:
            return True
    return False

def has_line_of_sight(walls, x1, y1, x2, y2):
    """(x1, y1)から(x2, y2)までの間に壁がないか（視線が通っているか）判定する"""
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if dist < 1:
        return True
    
    steps = int(dist / 4)
    if steps <= 1:
        return True

    for i in range(1, steps):
        t = i / steps
        rx = x1 + (x2 - x1) * t
        ry = y1 + (y2 - y1) * t
        for w in walls:
            if w["x"] <= rx <= w["x"] + w["w"] and w["y"] <= ry <= w["y"] + w["h"]:
                return False  # 壁に遮られている
    return True

def create_enemy(ex, ey, etype):
    """敵戦車のデータを生成する"""
    if etype == "light":
        hp = 1
        speed = 1.1
        shoot_interval = 60
        radius = 5
        color = 9
        score_value = 50
        sight_range = 140
    elif etype == "heavy":
        hp = 4
        speed = 0.35
        shoot_interval = 130
        radius = 8
        color = 2
        score_value = 250
        sight_range = 110
    else:  # normal
        hp = 2
        speed = 0.6
        shoot_interval = 90
        radius = 6
        color = 8
        score_value = 100
        sight_range = 125

    patrol_angle = random.uniform(0, math.pi * 2)

    return {
        "x": ex,
        "y": ey,
        "type": etype,
        "hull_angle": patrol_angle,
        "turret_angle": patrol_angle,
        "speed": speed,
        "hp": hp,
        "max_hp": hp,
        "shoot_timer": random.randint(20, shoot_interval),
        "shoot_interval": shoot_interval,
        "radius": radius,
        "color": color,
        "score_value": score_value,
        # 徘徊・探知関連
        "state": "patrol",          # "patrol" (徘徊) または "chase" (追撃)
        "patrol_angle": patrol_angle,
        "patrol_timer": random.randint(30, 90),
        "sight_range": sight_range
    }

def load_stage(state, stage_num):
    """指定したステージ番号のマップと敵データをロードする"""
    state["stage"] = stage_num
    state["x"] = W // 2
    state["y"] = H // 2
    state["speed"] = 1.5
    state["hull_angle"] = 0.0     # 車体の向き（ラジアン）
    state["turret_angle"] = 0.0   # 砲塔の向き（ラジアン）
    state["hp"] = 5
    
    state["is_gameover"] = False
    state["is_cleared"] = False
    
    state["reload_timer"] = 0
    state["max_reload_time"] = 15

    state["bullets"] = []
    state["particles"] = []

    # ステージごとのマップ（壁）と敵の配置設定
    if stage_num % 3 == 1:
        # ステージ1（基本パターン）
        state["walls"] = [
            {"x": 70, "y": 30, "w": 16, "h": 50},   # 左上縦壁
            {"x": 170, "y": 30, "w": 16, "h": 50},  # 右上縦壁
            {"x": 70, "y": 112, "w": 16, "h": 50},  # 左下縦壁
            {"x": 170, "y": 112, "w": 16, "h": 50}, # 右下縦壁
            {"x": 118, "y": 45, "w": 20, "h": 16},  # 中央上横壁
            {"x": 118, "y": 130, "w": 20, "h": 16}, # 中央下横壁
        ]
        enemy_configs = [
            (30, 30, "light"),
            (W - 30, 30, "light"),
            (30, H - 30, "normal"),
            (W - 30, H - 30, "normal"),
        ]
    elif stage_num % 3 == 2:
        # ステージ2（十字型エリアと広めの中央）
        state["walls"] = [
            {"x": 118, "y": 30, "w": 20, "h": 50},  # 中央上
            {"x": 118, "y": 112, "w": 20, "h": 50}, # 中央下
            {"x": 30, "y": 88, "w": 50, "h": 16},   # 左中央
            {"x": 176, "y": 88, "w": 50, "h": 16},  # 右中央
        ]
        enemy_configs = [
            (30, 30, "light"),
            (W - 30, 30, "normal"),
            (30, H - 30, "heavy"),
            (W - 30, H - 30, "heavy"),
        ]
    else:
        # ステージ3（四隅の壁と複数敵）
        state["walls"] = [
            {"x": 50, "y": 40, "w": 156, "h": 14},  # 上横壁
            {"x": 50, "y": 138, "w": 156, "h": 14}, # 下横壁
            {"x": 50, "y": 70, "w": 14, "h": 52},   # 左縦壁
            {"x": 192, "y": 70, "w": 14, "h": 52},  # 右縦壁
        ]
        enemy_configs = [
            (30, 25, "light"),
            (W - 30, 25, "light"),
            (W // 2, 25, "heavy"),
            (30, H - 25, "normal"),
            (W - 30, H - 25, "normal"),
        ]

    state["enemies"] = [create_enemy(ex, ey, etype) for ex, ey, etype in enemy_configs]

def reset_game_state(state):
    """ゲーム全体の初期化（ゲームオーバー時の再スタート）"""
    state["score"] = 0
    load_stage(state, 1)

def next_stage(state):
    """次のステージへ進む（スコアは引き継ぐ）"""
    load_stage(state, state.get("stage", 1) + 1)

def create_game_state():
    """初期ゲーム状態の辞書を生成する"""
    state = {}
    reset_game_state(state)
    return state

def move_enemy_smoothly(state, e, target_angle, move_speed):
    """
    敵の滑らかな移動と壁回避処理
    """
    # 1. 旋回処理
    angle_diff = (target_angle - e["hull_angle"] + math.pi) % (math.pi * 2) - math.pi
    e["hull_angle"] += max(-0.08, min(0.08, angle_diff))

    # 2. 前進処理と予測衝突判定
    dx = math.cos(e["hull_angle"]) * move_speed
    dy = math.sin(e["hull_angle"]) * move_speed

    next_x = e["x"] + dx
    next_y = e["y"] + dy

    # 予測位置での壁・画面端との衝突チェック (少し大きめのマージン)
    margin = e["radius"] + 2
    hit_x = check_wall_collision(state["walls"], next_x, e["y"], margin) or next_x < 12 or next_x > W - 12
    hit_y = check_wall_collision(state["walls"], e["x"], next_y, margin) or next_y < 12 or next_y > H - 12

    if not hit_x:
        e["x"] = next_x
    else:
        # X軸方向の障害物回避：進行方向をランダムに大きくそらす
        turn_dir = random.choice([1, -1])
        e["hull_angle"] += (math.pi / 2) * turn_dir
        e["patrol_angle"] = e["hull_angle"]
        e["patrol_timer"] = random.randint(40, 90)

    if not hit_y:
        e["y"] = next_y
    else:
        # Y軸方向の障害物回避
        turn_dir = random.choice([1, -1])
        e["hull_angle"] += (math.pi / 2) * turn_dir
        e["patrol_angle"] = e["hull_angle"]
        e["patrol_timer"] = random.randint(40, 90)

def update_game(state):
    """ゲーム状態の更新処理"""
    # ゲームオーバーまたはクリア時のキー入力処理
    if state["is_gameover"]:
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            reset_game_state(state)
        return

    if state["is_cleared"]:
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            next_stage(state)
        return

    # 1. 戦車の操縦 (生存時のみ)
    if state["hp"] > 0:
        # 旋回 (A/D)
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            state["hull_angle"] -= 0.08  # 左旋回
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            state["hull_angle"] += 0.08  # 右旋回

        # 前進・後退 (W/S)
        move_dir = 0
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            move_dir += 1   # 前進
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            move_dir -= 1   # 後退

        if move_dir != 0:
            current_speed = state["speed"] if move_dir > 0 else state["speed"] * 0.6
            
            dx = math.cos(state["hull_angle"]) * current_speed * move_dir
            dy = math.sin(state["hull_angle"]) * current_speed * move_dir

            state["x"] += dx
            state["x"] = max(10, min(W - 10, state["x"]))
            if check_wall_collision(state["walls"], state["x"], state["y"], 6):
                state["x"] -= dx

            state["y"] += dy
            state["y"] = max(10, min(H - 10, state["y"]))
            if check_wall_collision(state["walls"], state["x"], state["y"], 6):
                state["y"] -= dy

            # 排気煙エフェクト
            if pyxel.frame_count % 3 == 0:
                back_x = state["x"] - math.cos(state["hull_angle"]) * 8
                back_y = state["y"] - math.sin(state["hull_angle"]) * 8
                state["particles"].append({
                    "x": back_x, "y": back_y,
                    "vx": random.uniform(-0.3, 0.3), "vy": random.uniform(-0.3, 0.3),
                    "color": 5, "life": 10
                })

        # 2. 砲塔の照準
        state["turret_angle"] = math.atan2(pyxel.mouse_y - state["y"], pyxel.mouse_x - state["x"])

        # 3. リロードタイマーの更新
        if state["reload_timer"] > 0:
            state["reload_timer"] -= 1

        # 4. 主砲発射
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and state["reload_timer"] == 0:
            state["reload_timer"] = state["max_reload_time"]

            barrel_len = 10
            bx = state["x"] + math.cos(state["turret_angle"]) * barrel_len
            by = state["y"] + math.sin(state["turret_angle"]) * barrel_len
            
            state["bullets"].append({
                "x": bx, "y": by,
                "vx": math.cos(state["turret_angle"]) * 5.0,
                "vy": math.sin(state["turret_angle"]) * 5.0,
                "life": 60,
                "owner": "player",
                "radius": 2,
                "damage": 1
            })

            # 発砲火花エフェクト
            for _ in range(6):
                ang = state["turret_angle"] + random.uniform(-0.4, 0.4)
                sp = random.uniform(1.0, 3.0)
                state["particles"].append({
                    "x": bx, "y": by,
                    "vx": math.cos(ang) * sp, "vy": math.sin(ang) * sp,
                    "color": random.choice([7, 10, 9]), "life": 6
                })

            # 効果音再生
            pyxel.play(0, 0)

    # 5. 敵のAI更新 (徘徊 & 視線探知)
    if state["hp"] > 0:
        for e in state["enemies"]:
            dx = state["x"] - e["x"]
            dy = state["y"] - e["y"]
            dist = math.sqrt(dx * dx + dy * dy)

            # 視線チェック: 探知距離以内で壁に遮られていなければ発見
            can_see_player = (
                dist <= e["sight_range"] and
                has_line_of_sight(state["walls"], e["x"], e["y"], state["x"], state["y"])
            )

            if can_see_player:
                e["state"] = "chase"
            else:
                if e["state"] == "chase":
                    e["state"] = "patrol"
                    e["patrol_angle"] = e["hull_angle"]
                    e["patrol_timer"] = random.randint(30, 90)

            if e["state"] == "chase":
                # --- 発見中 (追撃・攻撃モード) ---
                e["turret_angle"] = math.atan2(dy, dx)
                target_hull_angle = math.atan2(dy, dx)

                # プレイヤーへ向けて移動 (距離50以上離れている場合)
                if dist > 50:
                    move_enemy_smoothly(state, e, target_hull_angle, e["speed"])
                    if pyxel.frame_count % 5 == 0:
                        back_x = e["x"] - math.cos(e["hull_angle"]) * 8
                        back_y = e["y"] - math.sin(e["hull_angle"]) * 8
                        state["particles"].append({
                            "x": back_x, "y": back_y,
                            "vx": random.uniform(-0.2, 0.2), "vy": random.uniform(-0.2, 0.2),
                            "color": 13, "life": 8
                        })

                # 射撃処理
                if e["shoot_timer"] > 0:
                    e["shoot_timer"] -= 1
                else:
                    e["shoot_timer"] = e["shoot_interval"] + random.randint(-15, 15)
                    barrel_len = e["radius"] + 4
                    ebx = e["x"] + math.cos(e["turret_angle"]) * barrel_len
                    eby = e["y"] + math.sin(e["turret_angle"]) * barrel_len

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

                    state["bullets"].append({
                        "x": ebx, "y": eby,
                        "vx": math.cos(e["turret_angle"]) * bullet_speed,
                        "vy": math.sin(e["turret_angle"]) * bullet_speed,
                        "life": 70,
                        "owner": "enemy",
                        "radius": bullet_radius,
                        "damage": bullet_damage
                    })

                    for _ in range(4):
                        ang = e["turret_angle"] + random.uniform(-0.4, 0.4)
                        sp = random.uniform(1.0, 2.5)
                        state["particles"].append({
                            "x": ebx, "y": eby,
                            "vx": math.cos(ang) * sp, "vy": math.sin(ang) * sp,
                            "color": random.choice([7, 8, 14]), "life": 5
                        })
                    pyxel.play(0, 0)

            else:
                # --- 徘徊モード ---
                e["patrol_timer"] -= 1
                if e["patrol_timer"] <= 0:
                    e["patrol_angle"] += random.uniform(-math.pi / 2, math.pi / 2)
                    e["patrol_timer"] = random.randint(40, 100)

                # 徘徊移動
                move_enemy_smoothly(state, e, e["patrol_angle"], e["speed"] * 0.7)
                e["turret_angle"] = e["hull_angle"]

                if pyxel.frame_count % 8 == 0:
                    back_x = e["x"] - math.cos(e["hull_angle"]) * 8
                    back_y = e["y"] - math.sin(e["hull_angle"]) * 8
                    state["particles"].append({
                        "x": back_x, "y": back_y,
                        "vx": random.uniform(-0.1, 0.1), "vy": random.uniform(-0.1, 0.1),
                        "color": 13, "life": 6
                    })

    # 6. 弾の移動 & 衝突判定処理
    for b in state["bullets"][:]:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        b["life"] -= 1

        if b["life"] <= 0 or b["x"] < 0 or b["x"] > W or b["y"] < 0 or b["y"] > H:
            if b in state["bullets"]:
                state["bullets"].remove(b)
            continue

        if check_wall_collision(state["walls"], b["x"], b["y"], b.get("radius", 2)):
            if b in state["bullets"]:
                state["bullets"].remove(b)
            for _ in range(4):
                state["particles"].append({
                    "x": b["x"], "y": b["y"],
                    "vx": random.uniform(-1.2, 1.2), "vy": random.uniform(-1.2, 1.2),
                    "color": random.choice([7, 13, 5]), "life": 6
                })
            continue

        if b["owner"] == "player":
            hit_enemy = False
            for e in state["enemies"][:]:
                edx = b["x"] - e["x"]
                edy = b["y"] - e["y"]
                edist = math.sqrt(edx * edx + edy * edy)
                if edist < (e["radius"] + b.get("radius", 2)):
                    e["hp"] -= 1
                    hit_enemy = True
                    
                    for _ in range(5):
                        state["particles"].append({
                            "x": b["x"], "y": b["y"],
                            "vx": random.uniform(-1.5, 1.5), "vy": random.uniform(-1.5, 1.5),
                            "color": random.choice([8, 9, 10]), "life": 8
                        })

                    if e["hp"] <= 0:
                        state["enemies"].remove(e)
                        state["score"] += e.get("score_value", 100)
                        pyxel.play(1, 1)

                        for _ in range(20):
                            state["particles"].append({
                                "x": e["x"], "y": e["y"],
                                "vx": random.uniform(-3.0, 3.0), "vy": random.uniform(-3.0, 3.0),
                                "color": random.choice([7, 8, 9, 10, 14]), "life": 15
                            })
                    break
            if hit_enemy:
                if b in state["bullets"]:
                    state["bullets"].remove(b)
        
        elif b["owner"] == "enemy":
            if state["hp"] > 0:
                pdx = b["x"] - state["x"]
                pdy = b["y"] - state["y"]
                pdist = math.sqrt(pdx * pdx + pdy * pdy)
                if pdist < (6 + b.get("radius", 2)):
                    state["hp"] -= b.get("damage", 1)
                    if b in state["bullets"]:
                        state["bullets"].remove(b)
                    
                    for _ in range(8):
                        state["particles"].append({
                            "x": b["x"], "y": b["y"],
                            "vx": random.uniform(-2.0, 2.0), "vy": random.uniform(-2.0, 2.0),
                            "color": random.choice([8, 11, 12]), "life": 10
                        })
                    
                    if state["hp"] <= 0:
                        state["hp"] = 0
                        state["is_gameover"] = True
                        pyxel.play(1, 1)
                        
                        for _ in range(30):
                            state["particles"].append({
                                "x": state["x"], "y": state["y"],
                                "vx": random.uniform(-4.0, 4.0), "vy": random.uniform(-4.0, 4.0),
                                "color": random.choice([7, 8, 9, 10, 14]), "life": 20
                            })

    # ステージクリア判定
    if len(state["enemies"]) == 0 and not state["is_gameover"]:
        state["is_cleared"] = True

    # 7. パーティクルの更新
    for p in state["particles"][:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1
        if p["life"] <= 0:
            state["particles"].remove(p)

def draw_game(state):
    """ゲーム描画処理"""
    pyxel.cls(1)

    # グリッド線
    for x in range(0, W, 16):
        pyxel.line(x, 0, x, H, 5)
    for y in range(0, H, 16):
        pyxel.line(0, y, W, y, 5)

    # 壁
    for w in state["walls"]:
        pyxel.rect(w["x"], w["y"], w["w"], w["h"], 5)
        pyxel.rectb(w["x"], w["y"], w["w"], w["h"], 13)

    # パーティクル
    for p in state["particles"]:
        pyxel.pset(p["x"], p["y"], p["color"])

    # 弾
    for b in state["bullets"]:
        color = 10 if b["owner"] == "player" else 8
        radius = b.get("radius", 2)
        pyxel.circ(b["x"], b["y"], radius, color)
        pyxel.circb(b["x"], b["y"], radius, 0)

    # 敵戦車
    for e in state["enemies"]:
        cos_e = math.cos(e["hull_angle"])
        sin_e = math.sin(e["hull_angle"])

        side_dist = e["radius"] - 1
        len_dist = e["radius"]
        for side in [-side_dist, side_dist]:
            tx1 = e["x"] + side * (-sin_e) - len_dist * cos_e
            ty1 = e["y"] + side * (cos_e) - len_dist * sin_e
            tx2 = e["x"] + side * (-sin_e) + len_dist * cos_e
            ty2 = e["y"] + side * (cos_e) + len_dist * sin_e
            pyxel.line(tx1, ty1, tx2, ty2, 0)

        pyxel.circ(e["x"], e["y"], e["radius"], e["color"])
        pyxel.circb(e["x"], e["y"], e["radius"], 2 if e["type"] == "heavy" else 0)

        barrel_len = e["radius"] + 4
        barrel_x = e["x"] + math.cos(e["turret_angle"]) * barrel_len
        barrel_y = e["y"] + math.sin(e["turret_angle"]) * barrel_len
        pyxel.line(e["x"], e["y"], barrel_x, barrel_y, 0)
        
        turret_color = 10 if e["type"] == "light" else (9 if e["type"] == "normal" else 14)
        turret_r = max(2.5, e["radius"] * 0.5)
        pyxel.circ(e["x"], e["y"], turret_r, turret_color)
        pyxel.circb(e["x"], e["y"], turret_r, 0)

        # 追撃状態（発見時）には感嘆符 '!' を頭上に表示
        if e["state"] == "chase":
            pyxel.text(int(e["x"]) - 1, int(e["y"] - e["radius"] - 10), "!", 8)

        # HPゲージ
        bar_w = e["radius"] * 2
        bar_h = 2
        bx = e["x"] - bar_w // 2
        by = e["y"] - e["radius"] - 4
        pyxel.rect(bx, by, bar_w, bar_h, 0)
        hp_w = int(bar_w * (e["hp"] / e["max_hp"]))
        pyxel.rect(bx, by, hp_w, bar_h, 8)

    # プレイヤー戦車 (生存時のみ)
    if state["hp"] > 0:
        cos_h = math.cos(state["hull_angle"])
        sin_h = math.sin(state["hull_angle"])

        for side in [-5, 5]:
            tx1 = state["x"] + side * (-sin_h) - 6 * cos_h
            ty1 = state["y"] + side * (cos_h) - 6 * sin_h
            tx2 = state["x"] + side * (-sin_h) + 6 * cos_h
            ty2 = state["y"] + side * (cos_h) + 6 * sin_h
            pyxel.line(tx1, ty1, tx2, ty2, 0)

        pyxel.circ(state["x"], state["y"], 6, 11)
        pyxel.circb(state["x"], state["y"], 6, 3)

        barrel_x = state["x"] + math.cos(state["turret_angle"]) * 10
        barrel_y = state["y"] + math.sin(state["turret_angle"]) * 10
        pyxel.line(state["x"], state["y"], barrel_x, barrel_y, 0)
        pyxel.circ(state["x"], state["y"], 3, 10)
        pyxel.circb(state["x"], state["y"], 3, 0)

        pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, 4, 10)
        pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, 8)

    # 上部 UI バー
    pyxel.rect(0, 0, W, 12, 0)
    
    stage_str = f"ST:{state.get('stage', 1)}"
    hp_str = "HP:" + "♥" * state["hp"] + "♡" * (5 - state["hp"])
    score_str = f"SC:{state['score']}"
    pyxel.text(5, 3, f"{stage_str} {hp_str} {score_str}", 7)

    if state["hp"] > 0:
        if state["reload_timer"] > 0:
            progress = (state["max_reload_time"] - state["reload_timer"]) / state["max_reload_time"]
            pyxel.text(175, 3, "RELOAD", 9)
            pyxel.rect(205, 4, 40, 4, 8)
            pyxel.rect(205, 4, int(40 * progress), 4, 10)
        else:
            pyxel.text(175, 3, "READY", 11)
            pyxel.rect(205, 4, 40, 4, 11)

    # ゲームオーバー・クリア画面表示
    if state["is_gameover"]:
        pyxel.rect(W // 2 - 65, H // 2 - 22, 130, 44, 0)
        pyxel.rectb(W // 2 - 65, H // 2 - 22, 130, 44, 8)
        pyxel.text(W // 2 - 27, H // 2 - 12, "GAME OVER", 8)
        pyxel.text(W // 2 - 45, H // 2 + 2, f"FINAL SCORE: {state['score']}", 10)
        pyxel.text(W // 2 - 50, H // 2 + 12, "PRESS ENTER TO RETRY", 7)
    
    elif state["is_cleared"]:
        pyxel.rect(W // 2 - 70, H // 2 - 22, 140, 44, 0)
        pyxel.rectb(W // 2 - 70, H // 2 - 22, 140, 44, 11)
        pyxel.text(W // 2 - 32, H // 2 - 12, "STAGE CLEAR!", 11)
        pyxel.text(W // 2 - 45, H // 2 + 2, f"STAGE {state.get('stage', 1)} COMPLETED", 10)
        pyxel.text(W // 2 - 55, H // 2 + 12, "PRESS ENTER FOR NEXT", 7)

def main():
    # Pyxel初期化
    pyxel.init(W, H, title="Simple 2D Tank", fps=30)
    pyxel.mouse(True)

    # サウンド設定 (0番: 発砲音, 1番: 爆発音)
    pyxel.sounds[0].set("c3c2", "n", "72", "f", 4)
    pyxel.sounds[1].set("c1c2g1c1", "s", "7474", "f", 8)

    # MP3 BGMの再生開始
    start_bgm("Pixel_Sprint.mp3")

    state = create_game_state()

    def update():
        update_game(state)

    def draw():
        draw_game(state)

    pyxel.run(update, draw)

if __name__ == "__main__":
    main()
