import pyxel
import math
import random

# ゲームの状態管理用辞書 (classやglobalは不使用)
state = {
    "phase": "START",      # START, AIM_ANGLE, AIM_POWER, FLYING, RESULT
    "angle": 45.0,         # 発射角度 (15~75度)
    "angle_speed": 1.5,    # 角度のスイング速度
    "power": 0.0,          # 発射パワー (0~100)
    "power_speed": 3.0,    # パワーゲージの増加速度
    "gnome_x": 30.0,       # ノームのX位置
    "gnome_y": 120.0,      # ノームのY位置 (地面はy=130)
    "vx": 0.0,             # X方向速度
    "vy": 0.0,             # Y方向速度
    "rotation": 0.0,       # 飛行中の回転角度
    "camera_x": 0.0,       # カメラ位置
    "distance": 0.0,       # 現在の飛距離 (m)
    "high_score": 0.0,     # ハイスコア (m)
    "mushrooms": [],       # 大ジャンプキノコの配置Xリスト
    "flowers": [],         # ダッシュ花壇の配置Xリスト
    "effect_text": "",     # 演出用メッセージ (BOOST! など)
    "effect_timer": 0      # メッセージ表示タイマー
}

GROUND_Y = 130.0
LAUNCH_X = 30.0
LAUNCH_Y = 115.0

# アイテム（キノコや花）の自動生成関数
def generate_field():
    state["mushrooms"] = []
    state["flowers"] = []
    # 50m〜1000mの間にランダム配置
    for x in range(100, 3000, 70):
        r = random.random()
        if r < 0.35:
            state["mushrooms"].append(float(x + random.randint(-15, 15)))
        elif r < 0.65:
            state["flowers"].append(float(x + random.randint(-15, 15)))

# ゲームのリセット関数
def reset_game():
    state["phase"] = "AIM_ANGLE"
    state["angle"] = 45.0
    state["angle_speed"] = 1.5
    state["power"] = 0.0
    state["power_speed"] = 3.0
    state["gnome_x"] = LAUNCH_X
    state["gnome_y"] = LAUNCH_Y
    state["vx"] = 0.0
    state["vy"] = 0.0
    state["rotation"] = 0.0
    state["camera_x"] = 0.0
    state["distance"] = 0.0
    state["effect_text"] = ""
    state["effect_timer"] = 0
    generate_field()

# 発射処理
def launch_gnome():
    rad = math.radians(state["angle"])
    # パワーに応じて速度を決定 (最大速度 14.0)
    speed = (state["power"] / 100.0) * 11.0 + 3.0
    state["vx"] = math.cos(rad) * speed
    state["vy"] = -math.sin(rad) * speed
    state["phase"] = "FLYING"

# 更新処理
def update():
    phase = state["phase"]

    if phase == "START":
        if pyxel.btnp(pyxel.KEY_SPACE):
            reset_game()

    elif phase == "AIM_ANGLE":
        # 角度の振り子アニメーション (15度 〜 75度)
        state["angle"] += state["angle_speed"]
        if state["angle"] >= 75.0 or state["angle"] <= 15.0:
            state["angle_speed"] *= -1

        if pyxel.btnp(pyxel.KEY_SPACE):
            state["phase"] = "AIM_POWER"

    elif phase == "AIM_POWER":
        # パワーゲージのアニメーション (0 〜 100)
        state["power"] += state["power_speed"]
        if state["power"] >= 100.0 or state["power"] <= 0.0:
            state["power_speed"] *= -1

        if pyxel.btnp(pyxel.KEY_SPACE):
            launch_gnome()

    elif phase == "FLYING":
        # 物理移動と重力
        state["gnome_x"] += state["vx"]
        state["gnome_y"] += state["vy"]
        state["vy"] += 0.18  # 重力加速度
        state["vx"] *= 0.995 # 空気抵抗
        state["rotation"] += state["vx"] * 10  # 回転

        # カメラのスクロール（ノームを中心に画面追従）
        target_cam_x = state["gnome_x"] - 60.0
        if target_cam_x > state["camera_x"]:
            state["camera_x"] = target_cam_x

        # 飛距離の更新（1ピクセル＝約0.2メートル換算）
        current_dist = max(0.0, (state["gnome_x"] - LAUNCH_X) * 0.2)
        state["distance"] = current_dist

        # キノコ（大ジャンプ）との判定
        gnome_x = state["gnome_x"]
        gnome_y = state["gnome_y"]
        hit_item = False
        if gnome_y >= GROUND_Y - 8:
            for mx in state["mushrooms"]:
                if abs(gnome_x - mx) < 12:
                    state["vy"] = -6.5  # 大バウンド！
                    state["vx"] += 1.0  # 少し加速
                    state["effect_text"] = "MUSHROOM BINGO! +JUMP"
                    state["effect_timer"] = 30
                    hit_item = True
                    break

            if not hit_item:
                # 花壇（ダッシュ）との判定
                for fx in state["flowers"]:
                    if abs(gnome_x - fx) < 12:
                        state["vx"] += 3.5  # ダッシュ加速！
                        state["vy"] = -2.0
                        state["effect_text"] = "FLOWER BOOST! >>"
                        state["effect_timer"] = 30
                        hit_item = True
                        break

        # 地面との着地・バウンド判定（アイテムヒット時はスキップ）
        if not hit_item and state["gnome_y"] >= GROUND_Y - 4:
            state["gnome_y"] = GROUND_Y - 4
            if abs(state["vy"]) > 1.0:
                state["vy"] = -state["vy"] * 0.5  # 反発バウンド
                state["vx"] *= 0.8
            else:
                state["vy"] = 0.0
                state["vx"] *= 0.85  # 地面すべり摩擦

                # 完全停止でリザルトへ
                if abs(state["vx"]) < 0.08:
                    state["vx"] = 0.0
                    state["phase"] = "RESULT"
                    if state["distance"] > state["high_score"]:
                        state["high_score"] = state["distance"]

        # 演出メッセージタイマー
        if state["effect_timer"] > 0:
            state["effect_timer"] -= 1

    elif phase == "RESULT":
        if pyxel.btnp(pyxel.KEY_SPACE):
            reset_game()

# 描画処理
def draw():
    pyxel.cls(12)  # 空の色（明るい青）

    cam_x = state["camera_x"]

    # 遠景の雲の描画（パララックス効果）
    for i in range(10):
        cloud_x = (i * 120 - cam_x * 0.3) % 400 - 50
        pyxel.circ(cloud_x, 30 + (i % 3) * 10, 12, 7)
        pyxel.circ(cloud_x + 10, 32 + (i % 3) * 10, 8, 7)

    # 地面（緑と土）
    pyxel.rect(0, int(GROUND_Y), 240, 30, 11)   # 草原 (緑)
    pyxel.rect(0, int(GROUND_Y + 4), 240, 26, 3) # 土 (茶色)

    # フィールドアイテムの描画 (カメラオフセット反映)
    for mx in state["mushrooms"]:
        draw_x = mx - cam_x
        if -10 <= draw_x <= 250:
            # キノコ（赤い笠と白い幹）
            pyxel.rect(int(draw_x) - 2, int(GROUND_Y) - 4, 4, 4, 7)
            pyxel.circ(int(draw_x), int(GROUND_Y) - 5, 5, 8)
            pyxel.pset(int(draw_x) - 1, int(GROUND_Y) - 6, 7)

    for fx in state["flowers"]:
        draw_x = fx - cam_x
        if -10 <= draw_x <= 250:
            # 花壇（黄色とピンクの花）
            pyxel.circ(int(draw_x) - 3, int(GROUND_Y) - 3, 3, 10)
            pyxel.circ(int(draw_x) + 3, int(GROUND_Y) - 3, 3, 14)
            pyxel.circ(int(draw_x), int(GROUND_Y) - 5, 3, 9)

    # 発射台（カタパルト）の描画
    catapult_x = LAUNCH_X - cam_x
    if -30 <= catapult_x <= 250:
        pyxel.line(int(catapult_x) - 10, int(GROUND_Y), int(catapult_x), int(LAUNCH_Y), 4)
        pyxel.line(int(catapult_x) + 10, int(GROUND_Y), int(catapult_x), int(LAUNCH_Y), 4)
        pyxel.rect(int(catapult_x) - 12, int(GROUND_Y) - 2, 24, 4, 4)

        # 角度決定前のガイドライン
        if state["phase"] in ["AIM_ANGLE", "AIM_POWER"]:
            rad = math.radians(state["angle"])
            gx = catapult_x + math.cos(rad) * 25
            gy = LAUNCH_Y - math.sin(rad) * 25
            pyxel.line(int(catapult_x), int(LAUNCH_Y), int(gx), int(gy), 8)

    # ガーデンノーム（ノーム妖精）の描画
    gx = state["gnome_x"] - cam_x
    gy = state["gnome_y"]

    if state["phase"] != "START":
        # 赤い三角帽子
        pyxel.tri(int(gx), int(gy) - 8, int(gx) - 4, int(gy) - 2, int(gx) + 4, int(gy) - 2, 8)
        # 顔と白いお髭
        pyxel.rect(int(gx) - 3, int(gy) - 2, 6, 4, 7)
        # 青い服
        pyxel.rect(int(gx) - 3, int(gy) + 2, 6, 4, 12)

    # UI描画 (カメラ非依存)
    # スコア・ハイスコア表示
    pyxel.rect(5, 5, 100, 20, 0)
    pyxel.rectb(5, 5, 100, 20, 7)
    pyxel.text(10, 9, f"DISTANCE: {state['distance']:.1f} m", 10)
    pyxel.text(10, 16, f"HIGH    : {state['high_score']:.1f} m", 7)

    # 演出テキスト
    if state["effect_timer"] > 0 and state["effect_text"]:
        pyxel.text(70, 40, state["effect_text"], 10)

    # 各フェーズごとのUI表示
    phase = state["phase"]

    if phase == "START":
        pyxel.rect(30, 40, 180, 70, 0)
        pyxel.rectb(30, 40, 180, 70, 10)
        pyxel.text(65, 52, "GOOGLE GARDEN GNOME", 10)
        pyxel.text(50, 68, "Launch gnome as far as you can!", 7)
        pyxel.text(65, 88, "PRESS SPACE TO START", 9)

    elif phase == "AIM_ANGLE":
        # 角度選択UI
        pyxel.rect(70, 135, 100, 18, 0)
        pyxel.rectb(70, 135, 100, 18, 7)
        pyxel.text(76, 141, f"ANGLE: {int(state['angle'])} deg [SPACE]", 10)

    elif phase == "AIM_POWER":
        # パワーメーター選択UI
        pyxel.rect(50, 135, 140, 18, 0)
        pyxel.rectb(50, 135, 140, 18, 7)
        # パワーバー
        bar_w = int(state["power"] * 1.2)
        pyxel.rect(55, 140, bar_w, 8, 8)
        pyxel.rectb(55, 140, 120, 8, 7)
        pyxel.text(60, 142, "POWER! [SPACE]", 7)

    elif phase == "RESULT":
        # リザルト画面
        pyxel.rect(40, 45, 160, 65, 0)
        pyxel.rectb(40, 45, 160, 65, 10)
        pyxel.text(80, 55, "RESULT SCORE", 10)
        pyxel.text(60, 70, f"Distance: {state['distance']:.1f} m", 7)
        pyxel.text(50, 90, "PRESS SPACE TO RESTART", 9)

# ゲームの初期化と実行
pyxel.init(240, 160, title="Google Garden Gnome Launch")
generate_field()
pyxel.run(update, draw)
