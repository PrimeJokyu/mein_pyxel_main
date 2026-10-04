# ==========================================
# 🥷 ハイパー忍者ダッシュ (Hyper Ninja Dash)
# （Pyxel / class・global 完全不使用）
# ==========================================
import math
import random
import pyxel

# 画面定数
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
TILE_SIZE = 16

# ------------------------------------------
# 🎨 初期状態の生成関数
# ------------------------------------------
def create_initial_state():
    return {
        "ninja": {
            "x": 32.0,
            "y": 176.0,
            "vx": 0.0,
            "vy": 0.0,
            "facing": 1,        # 1: 右, -1: 左
            "is_ground": False,
            "anim_frame": 0,
            "status": "PLAYING", # PLAYING, DEAD, GOAL
            "afterimages": [],   # [{x, y, timer}] 残像
        },
        "wire": {
            "active": False,
            "hx": 0.0,          # フック位置 X
            "hy": 0.0,          # フック位置 Y
            "length": 0.0,       # 現在のロープ長
            "max_length": 140.0, # 最大伸長
        },
        "camera_x": 0.0,
        "score": 0,
        "scrolls_collected": 0,
        "total_scrolls": 0,
        "time_frames": 0,
        "game_state": "TITLE", # TITLE, PLAY, GAMEOVER, CLEAR
        "particles": [],       # [{x, y, vx, vy, color, timer, max_timer}]
        "enemies": [],         # [{x, y, vx, start_x, end_x, facing}]
        "items": [],           # [{x, y, collected}]
        "spikes": [],          # [{x, y}]
        "map": [],
        "map_width": 0,
        "map_height": 0,
        "goal": {"x": 0, "y": 0},
    }

# ------------------------------------------
# 🗺️ マップデータ (ASCIIデザイン)
# G: 硬い壁/地面, W: ワイヤーフック可能な木枠
# S: 危険なトゲ, C: 秘伝の巻物, E: 敵忍者
# P: 忍者初期位置, F: ゴールの鳥居
# ------------------------------------------
RAW_MAP = [
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "G                                                                                                        G",
    "G                                                                                                        G",
    "G      WWWW              WWWW              WWWW              WWWW              WWWW              WWWW    G",
    "G                                                                                                        G",
    "G                                     C                                                                  G",
    "G               C                 GGGGGGGG                C                                C             G",
    "G            GGGGGG                                    GGGGGG                           GGGGGG           G",
    "G                                                                                                        G",
    "G                                                                     C                                  G",
    "G    WWWW              WWWW              WWWW            GGGGGGGGGGGGGGGG            WWWW                G",
    "G                                                                                                        G",
    "G                                            E                                                           G",
    "G             C               S S        GGGGGGGG                         S S                            G",
    "G          GGGGGG            GGGGGG                                      GGGGGG                          G",
    "G                                                                                                       FG",
    "G                                                                                                       FG",
    "G  P             E           SSSSSS                  E                  SSSSSS                         FFG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
]

# ------------------------------------------
# 🔊 音声のイニシャライズ (音符はc0〜b4の範囲)
# ------------------------------------------
def setup_sounds():
    # 0: ジャンプ
    pyxel.sounds[0].set("a2c3", "p", "7", "v", 5)
    # 1: ワイヤー射出・接続
    pyxel.sounds[1].set("c3e3g3", "n", "7", "f", 4)
    # 2: 巻物ゲット
    pyxel.sounds[2].set("g3c4", "p", "6", "v", 6)
    # 3: ゴールファンファーレ
    pyxel.sounds[3].set("c3e3g3c4 e3g3c4c4", "p", "6", "v", 10)
    # 4: 痛恨のミス
    pyxel.sounds[4].set("c3f2c2a1", "n", "7", "s", 12)

# ------------------------------------------
# 🛠️ マップ構築＆エンティティ読み込み
# ------------------------------------------
def load_map_data(state):
    grid = []
    enemies = []
    items = []
    spikes = []
    start_x, start_y = 32.0, 176.0
    goal_x, goal_y = 0, 0
    total_scrolls = 0

    height = len(RAW_MAP)
    width = len(RAW_MAP[0])

    for r in range(height):
        row = []
        for c in range(width):
            ch = RAW_MAP[r][c]
            x_pos = c * TILE_SIZE
            y_pos = r * TILE_SIZE

            if ch == 'P':
                start_x, start_y = float(x_pos), float(y_pos)
                row.append(' ')
            elif ch == 'E':
                enemies.append({
                    "x": float(x_pos),
                    "y": float(y_pos),
                    "vx": -0.8,
                    "start_x": float(x_pos - 32),
                    "end_x": float(x_pos + 32),
                    "facing": -1
                })
                row.append(' ')
            elif ch == 'C':
                items.append({"x": float(x_pos + 4), "y": float(y_pos + 4), "collected": False})
                total_scrolls += 1
                row.append(' ')
            elif ch == 'S':
                spikes.append({"x": float(x_pos), "y": float(y_pos)})
                row.append('S')
            elif ch == 'F':
                goal_x, goal_y = x_pos, y_pos
                row.append('F')
            else:
                row.append(ch)
        grid.append(row)

    state["map"] = grid
    state["map_width"] = width * TILE_SIZE
    state["map_height"] = height * TILE_SIZE
    state["ninja"]["x"] = start_x
    state["ninja"]["y"] = start_y
    state["enemies"] = enemies
    state["items"] = items
    state["spikes"] = spikes
    state["goal"] = {"x": goal_x, "y": goal_y}
    state["total_scrolls"] = total_scrolls

# ------------------------------------------
# 💥 パーティクル生成ヘルパー
# ------------------------------------------
def add_particles(state, x, y, count=5, color=10):
    for _ in range(count):
        vx = random.uniform(-1.0, 1.0) * 2.5
        vy = random.uniform(-2.0, 0.5) * 2.0
        timer = random.randint(10, 20)
        state["particles"].append({
            "x": x, "y": y,
            "vx": vx, "vy": vy,
            "color": color,
            "timer": timer,
            "max_timer": timer
        })

# ------------------------------------------
# 🎯 当たり判定計算（タイルベース）
# ------------------------------------------
def get_tile_at(state, x, y):
    col = int(x // TILE_SIZE)
    row = int(y // TILE_SIZE)
    if row < 0 or row >= len(state["map"]) or col < 0 or col >= len(state["map"][0]):
        return 'G'
    return state["map"][row][col]

def is_solid_tile(ch):
    return ch in ('G', 'W')

# ------------------------------------------
# 🎯 ワイヤー照準＆発射処理
# ------------------------------------------
def try_shoot_wire(state):
    ninja = state["ninja"]
    wire = state["wire"]

    # 照準ベクトルの決定
    dx, dy = 0.0, -1.0
    if pyxel.btn(pyxel.KEY_RIGHT):
        dx = 1.0
    elif pyxel.btn(pyxel.KEY_LEFT):
        dx = -1.0

    if pyxel.btn(pyxel.KEY_UP):
        dy = -1.0
    elif pyxel.btn(pyxel.KEY_DOWN):
        dy = 0.5

    length_dir = math.hypot(dx, dy)
    if length_dir > 0:
        dx /= length_dir
        dy /= length_dir
    else:
        dx = float(ninja["facing"])
        dy = -0.7

    curr_x = ninja["x"] + 6
    curr_y = ninja["y"] + 6
    step = 4.0
    max_dist = wire["max_length"]
    dist = 0.0

    hit = False
    hit_x, hit_y = curr_x, curr_y

    while dist < max_dist:
        curr_x += dx * step
        curr_y += dy * step
        dist += step
        tile = get_tile_at(state, curr_x, curr_y)
        if is_solid_tile(tile):
            hit = True
            hit_x, hit_y = curr_x, curr_y
            break

    if hit:
        wire["active"] = True
        wire["hx"] = hit_x
        wire["hy"] = hit_y
        wire["length"] = math.hypot(hit_x - (ninja["x"] + 6), hit_y - (ninja["y"] + 6))
        pyxel.play(0, 1)
        add_particles(state, hit_x, hit_y, count=6, color=7)

# ------------------------------------------
# 🏃 物理とプレイヤー状態の更新
# ------------------------------------------
def update_player(state):
    ninja = state["ninja"]
    wire = state["wire"]

    if ninja["status"] != "PLAYING":
        return

    accel = 0.35 if ninja["is_ground"] else 0.18
    if pyxel.btn(pyxel.KEY_LEFT):
        ninja["vx"] -= accel
        ninja["facing"] = -1
    if pyxel.btn(pyxel.KEY_RIGHT):
        ninja["vx"] += accel
        ninja["facing"] = 1

    friction = 0.88 if ninja["is_ground"] else 0.97
    ninja["vx"] *= friction

    gravity = 0.30
    ninja["vy"] += gravity

    if wire["active"]:
        px = ninja["x"] + 6
        py = ninja["y"] + 6
        dx = px - wire["hx"]
        dy = py - wire["hy"]
        dist = math.hypot(dx, dy)

        if dist > wire["length"]:
            nx = dx / dist
            ny = dy / dist

            dot = ninja["vx"] * nx + ninja["vy"] * ny
            if dot > 0:
                ninja["vx"] -= dot * nx
                ninja["vy"] -= dot * ny

            ninja["x"] = wire["hx"] + nx * wire["length"] - 6
            ninja["y"] = wire["hy"] + ny * wire["length"] - 6

        if pyxel.btn(pyxel.KEY_UP):
            wire["length"] = max(20.0, wire["length"] - 2.0)
        if pyxel.btn(pyxel.KEY_DOWN):
            wire["length"] = min(wire["max_length"], wire["length"] + 2.0)

        if pyxel.btnp(pyxel.KEY_X):
            wire["active"] = False
            ninja["vy"] -= 1.5

    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z):
        if ninja["is_ground"]:
            ninja["vy"] = -5.2
            ninja["is_ground"] = False
            pyxel.play(0, 0)
            add_particles(state, ninja["x"] + 6, ninja["y"] + 12, count=4, color=9)
        else:
            if wire["active"]:
                wire["active"] = False
            else:
                try_shoot_wire(state)

    new_x = ninja["x"] + ninja["vx"]
    new_y = ninja["y"] + ninja["vy"]

    ninja["is_ground"] = False
    if is_solid_tile(get_tile_at(state, new_x, ninja["y"])) or is_solid_tile(get_tile_at(state, new_x + 12, ninja["y"])) or is_solid_tile(get_tile_at(state, new_x, ninja["y"] + 12)) or is_solid_tile(get_tile_at(state, new_x + 12, ninja["y"] + 12)):
        ninja["vx"] = 0.0
    else:
        ninja["x"] = new_x

    if ninja["vy"] >= 0:
        if is_solid_tile(get_tile_at(state, ninja["x"], new_y + 12)) or is_solid_tile(get_tile_at(state, ninja["x"] + 12, new_y + 12)):
            ninja["y"] = (int((new_y + 12) // TILE_SIZE)) * TILE_SIZE - 12
            ninja["vy"] = 0.0
            ninja["is_ground"] = True
        else:
            ninja["y"] = new_y
    else:
        if is_solid_tile(get_tile_at(state, ninja["x"], new_y)) or is_solid_tile(get_tile_at(state, ninja["x"] + 12, new_y)):
            ninja["y"] = (int(new_y // TILE_SIZE) + 1) * TILE_SIZE
            ninja["vy"] = 0.0
        else:
            ninja["y"] = new_y

    speed = math.hypot(ninja["vx"], ninja["vy"])
    if speed > 3.0:
        ninja["afterimages"].append({"x": ninja["x"], "y": ninja["y"], "timer": 6})

    updated_afterimages = []
    for img in ninja["afterimages"]:
        img["timer"] -= 1
        if img["timer"] > 0:
            updated_afterimages.append(img)
    ninja["afterimages"] = updated_afterimages

    state["camera_x"] = max(0.0, min(ninja["x"] - SCREEN_WIDTH / 3, state["map_width"] - SCREEN_WIDTH))

    if get_tile_at(state, ninja["x"] + 6, ninja["y"] + 6) == 'S':
        trigger_game_over(state)

    for enemy in state["enemies"]:
        if math.hypot((ninja["x"] + 6) - (enemy["x"] + 6), (ninja["y"] + 6) - (enemy["y"] + 6)) < 10.0:
            trigger_game_over(state)

    for item in state["items"]:
        if not item["collected"]:
            if math.hypot((ninja["x"] + 6) - (item["x"] + 4), (ninja["y"] + 6) - (item["y"] + 4)) < 12.0:
                item["collected"] = True
                state["score"] += 500
                state["scrolls_collected"] += 1
                pyxel.play(0, 2)
                add_particles(state, item["x"] + 4, item["y"] + 4, count=8, color=10)

    goal = state["goal"]
    if math.hypot((ninja["x"] + 6) - (goal["x"] + 8), (ninja["y"] + 6) - (goal["y"] + 8)) < 16.0:
        trigger_clear(state)

# ------------------------------------------
# 👾 敵と環境の更新
# ------------------------------------------
def update_enemies(state):
    for enemy in state["enemies"]:
        enemy["x"] += enemy["vx"]
        if enemy["x"] <= enemy["start_x"]:
            enemy["x"] = enemy["start_x"]
            enemy["vx"] = abs(enemy["vx"])
            enemy["facing"] = 1
        elif enemy["x"] >= enemy["end_x"]:
            enemy["x"] = enemy["end_x"]
            enemy["vx"] = -abs(enemy["vx"])
            enemy["facing"] = -1

# ------------------------------------------
# ✨ パーティクルの更新
# ------------------------------------------
def update_particles(state):
    alive_particles = []
    for p in state["particles"]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["timer"] -= 1
        if p["timer"] > 0:
            alive_particles.append(p)
    state["particles"] = alive_particles

# ------------------------------------------
# 💀 ゲームオーバー処理
# ------------------------------------------
def trigger_game_over(state):
    if state["ninja"]["status"] == "PLAYING":
        state["ninja"]["status"] = "DEAD"
        state["game_state"] = "GAMEOVER"
        pyxel.play(0, 4)
        add_particles(state, state["ninja"]["x"] + 6, state["ninja"]["y"] + 6, count=15, color=8)

# ------------------------------------------
# 🏆 クリア処理
# ------------------------------------------
def trigger_clear(state):
    if state["ninja"]["status"] == "PLAYING":
        state["ninja"]["status"] = "GOAL"
        state["game_state"] = "CLEAR"
        pyxel.play(0, 3)
        add_particles(state, state["ninja"]["x"] + 6, state["ninja"]["y"] + 6, count=25, color=10)

# ------------------------------------------
# 🔄 ゲーム全体フレーム更新 (pyxel.update)
# ------------------------------------------
def update():
    state = pyxel.user_state

    if state["game_state"] == "TITLE":
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            state["game_state"] = "PLAY"
            load_map_data(state)
        return

    if state["game_state"] == "PLAY":
        state["time_frames"] += 1
        update_player(state)
        update_enemies(state)
        update_particles(state)

    elif state["game_state"] in ("GAMEOVER", "CLEAR"):
        update_particles(state)
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            new_state = create_initial_state()
            pyxel.user_state = new_state
            load_map_data(pyxel.user_state)
            pyxel.user_state["game_state"] = "PLAY"

# ------------------------------------------
# 🎨 描画処理 (pyxel.draw)
# ------------------------------------------
def draw():
    pyxel.cls(1) # ダークブルー背景
    state = pyxel.user_state
    cam_x = state["camera_x"]

    if state["game_state"] == "TITLE":
        draw_title_screen(state)
        return

    # --- マップ描画 ---
    grid = state["map"]
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            ch = grid[r][c]
            wx = c * TILE_SIZE - cam_x
            wy = r * TILE_SIZE

            if -TILE_SIZE <= wx <= SCREEN_WIDTH:
                if ch == 'G':
                    pyxel.rect(wx, wy, TILE_SIZE, TILE_SIZE, 3)
                    pyxel.rectb(wx, wy, TILE_SIZE, TILE_SIZE, 11)
                elif ch == 'W':
                    pyxel.rect(wx, wy, TILE_SIZE, TILE_SIZE, 4)
                    pyxel.rectb(wx, wy, TILE_SIZE, TILE_SIZE, 9)
                    pyxel.line(wx, wy, wx + TILE_SIZE - 1, wy + TILE_SIZE - 1, 9)
                elif ch == 'S':
                    pyxel.tri(wx, wy + TILE_SIZE, wx + 8, wy, wx + TILE_SIZE, wy + TILE_SIZE, 8)
                elif ch == 'F':
                    pyxel.rect(wx + 2, wy, 4, TILE_SIZE, 8)
                    pyxel.rect(wx + 10, wy, 4, TILE_SIZE, 8)
                    if r % 2 == 0:
                        pyxel.rect(wx, wy, TILE_SIZE, 3, 8)

    # --- 巻物（アイテム）描画 ---
    for item in state["items"]:
        if not item["collected"]:
            ix = item["x"] - cam_x
            iy = item["y"]
            if -8 <= ix <= SCREEN_WIDTH:
                pyxel.rect(ix, iy, 8, 8, 10)
                pyxel.rectb(ix, iy, 8, 8, 7)

    # --- 敵描画 ---
    for enemy in state["enemies"]:
        ex = enemy["x"] - cam_x
        ey = enemy["y"]
        if -16 <= ex <= SCREEN_WIDTH:
            pyxel.rect(ex + 2, ey + 2, 12, 12, 8)
            eye_x = ex + 9 if enemy["facing"] == 1 else ex + 3
            pyxel.pset(eye_x, ey + 5, 7)

    # --- ワイヤー（クナイ）描画 ---
    wire = state["wire"]
    ninja = state["ninja"]
    if wire["active"]:
        px = ninja["x"] + 6 - cam_x
        py = ninja["y"] + 6
        hx = wire["hx"] - cam_x
        hy = wire["hy"]
        pyxel.line(px, py, hx, hy, 7)
        pyxel.circ(hx, hy, 2, 10)

    # --- 残像描画 ---
    for img in ninja["afterimages"]:
        ax = img["x"] - cam_x
        ay = img["y"]
        pyxel.rectb(ax, ay, 12, 12, 12)

    # --- プレイヤー（忍者）描画 ---
    if ninja["status"] != "DEAD":
        nx = ninja["x"] - cam_x
        ny = ninja["y"]
        pyxel.rect(nx + 2, ny + 2, 12, 12, 0)
        pyxel.rect(nx + 4, ny + 4, 8, 8, 2)
        eye_x = nx + 8 if ninja["facing"] == 1 else nx + 3
        pyxel.pset(eye_x, ny + 5, 7)
        muffler_x = nx - 2 if ninja["facing"] == 1 else nx + 12
        pyxel.line(nx + 6, ny + 8, muffler_x, ny + 10, 8)

    # --- パーティクル描画 ---
    for p in state["particles"]:
        px = p["x"] - cam_x
        py = p["y"]
        pyxel.pset(px, py, p["color"])

    # --- UI / スコア表示 ---
    draw_ui(state)

    # --- オーバーレイ表示 ---
    if state["game_state"] == "GAMEOVER":
        pyxel.text(SCREEN_WIDTH // 2 - 36, SCREEN_HEIGHT // 2 - 10, "GAME OVER", 8)
        pyxel.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 10, "PRESS SPACE TO RETRY", 7)
    elif state["game_state"] == "CLEAR":
        clear_time = state["time_frames"] / 30.0
        pyxel.text(SCREEN_WIDTH // 2 - 36, SCREEN_HEIGHT // 2 - 20, "STAGE CLEAR!", 10)
        pyxel.text(SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT // 2 - 5, f"TIME: {clear_time:.2f} sec", 7)
        pyxel.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 15, "PRESS SPACE TO TITLE", 7)

# ------------------------------------------
# 📺 タイトル画面の描画
# ------------------------------------------
def draw_title_screen(state):
    pyxel.cls(1)
    pyxel.text(SCREEN_WIDTH // 2 - 52, 60, "HYPER NINJA DASH", 10)
    pyxel.text(SCREEN_WIDTH // 2 - 40, 80, "WIRED TIME ATTACK", 7)

    pyxel.rect(SCREEN_WIDTH // 2 - 30, 110, 60, 20, 3)
    pyxel.text(SCREEN_WIDTH // 2 - 24, 117, "PRESS SPACE", 7)

    pyxel.text(20, 160, "[LEFT/RIGHT] MOVE", 6)
    pyxel.text(20, 172, "[SPACE/Z] JUMP / SHOOT WIRE", 6)
    pyxel.text(20, 184, "[UP/DOWN] REEL WIRE IN/OUT", 6)
    pyxel.text(20, 196, "[X] RELEASE WIRE & BOOST", 6)

# ------------------------------------------
# 📊 UI表示
# ------------------------------------------
def draw_ui(state):
    seconds = state["time_frames"] // 30
    pyxel.text(8, 8, f"SCORE: {state['score']}", 7)
    pyxel.text(100, 8, f"SCROLL: {state['scrolls_collected']}/{state['total_scrolls']}", 10)
    pyxel.text(200, 8, f"TIME: {seconds}s", 7)

# ------------------------------------------
# 🚀 ゲームメイン起動
# ------------------------------------------
def main():
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hyper Ninja Dash")
    setup_sounds()

    initial_state = create_initial_state()
    load_map_data(initial_state)

    pyxel.user_state = initial_state
    pyxel.run(update, draw)

if __name__ == "__main__":
    main()