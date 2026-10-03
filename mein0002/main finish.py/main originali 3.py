import pyxel
import math

# オブジェクト管理
falling_objects = []
current_mode = "rain"
spawn_timer = 0

# モード設定
modes = {
    "rain": {"spawn_rate": 3, "types": {"raindrop": 100}},
    "snow": {"spawn_rate": 2, "types": {"snowflake": 100}},
    "meteor": {"spawn_rate": 10, "types": {"meteor": 80, "ufo": 20}},
    "mixed": {"spawn_rate": 2, "types": {"raindrop": 40, "snowflake": 30, "meteor": 25, "ufo": 5}}
}

pyxel.init(160, 120)

# ──────────────────────────────────────────
# ユーティリティ
# ──────────────────────────────────────────

def weighted_choice(types_dict):
    """重み付きランダム選択。types_dict = {"name": weight, ...}"""
    total = sum(types_dict.values())
    r = pyxel.rndi(0, total - 1)
    cumulative = 0
    for name, weight in types_dict.items():
        cumulative += weight
        if r < cumulative:
            return name
    return list(types_dict.keys())[-1]

# ──────────────────────────────────────────
# オブジェクト生成
# ──────────────────────────────────────────

def spawn_random_object():
    """現在のモードに基づいてランダムオブジェクトを生成"""
    mode_config = modes[current_mode]
    object_type = weighted_choice(mode_config["types"])
    x = pyxel.rndi(0, 159)

    if object_type == "raindrop":
        create_raindrop(x)
    elif object_type == "snowflake":
        create_snowflake(x)
    elif object_type == "meteor":
        create_meteor(x)
    elif object_type == "ufo":
        create_ufo(x)

def create_raindrop(x):
    falling_objects.append({
        "type": "raindrop",
        "x": x, "y": -5,
        "speed": pyxel.rndf(3.0, 6.0),
        "color": 12,
        "length": pyxel.rndi(3, 7)
    })

def create_snowflake(x):
    falling_objects.append({
        "type": "snowflake",
        "x": x, "y": -5,
        "speed": pyxel.rndf(0.5, 2.0),
        "sway": pyxel.rndf(0.02, 0.05),
        "time": 0,
        "color": 7,
        "size": pyxel.rndi(2, 4)
    })

def create_meteor(x):
    falling_objects.append({
        "type": "meteor",
        "x": x, "y": -10,
        "velocity_x": pyxel.rndf(-2.0, 2.0),
        "velocity_y": pyxel.rndf(2.0, 5.0),
        "color": 8,
        "size": pyxel.rndi(4, 8),
        "trail": []
    })

def create_ufo(x):
    falling_objects.append({
        "type": "ufo",
        "x": x, "y": -10,
        "speed": pyxel.rndf(0.5, 1.5),
        "hover_amplitude": pyxel.rndf(10, 20),
        "hover_frequency": pyxel.rndf(0.03, 0.08),
        "time": 0,
        "color": 11
    })

# ──────────────────────────────────────────
# 水しぶき生成
# ──────────────────────────────────────────

def create_splash_effect(x, y):
    for _ in range(8):
        falling_objects.append({
            "type": "particle",
            "x": x + pyxel.rndf(-1.0, 1.0),
            "y": y,
            "velocity_x": pyxel.rndf(-2.0, 2.0),
            "velocity_y": pyxel.rndf(-3.5, -1.0),
            "life": pyxel.rndi(10, 20),
            "color": 12
        })

# ──────────────────────────────────────────
# オブジェクト更新
# ──────────────────────────────────────────

def update_all_objects():
    for obj in falling_objects:
        if obj["type"] == "raindrop":
            update_raindrop(obj)
        elif obj["type"] == "snowflake":
            update_snowflake(obj)
        elif obj["type"] == "meteor":
            update_meteor(obj)
        elif obj["type"] == "ufo":
            update_ufo(obj)
        elif obj["type"] == "particle":
            update_particle(obj)

def update_raindrop(obj):
    obj["y"] += obj["speed"]

def update_snowflake(obj):
    obj["time"] += 1
    obj["y"] += obj["speed"]
    obj["x"] += math.sin(obj["time"] * obj["sway"]) * 0.5

def update_meteor(obj):
    obj["x"] += obj["velocity_x"]
    obj["y"] += obj["velocity_y"]
    obj["trail"].append((obj["x"], obj["y"]))
    if len(obj["trail"]) > 8:
        obj["trail"].pop(0)

def update_ufo(obj):
    obj["time"] += 1
    obj["y"] += obj["speed"]
    obj["x"] += math.sin(obj["time"] * obj["hover_frequency"]) * obj["hover_amplitude"] * 0.1

def update_particle(obj):
    obj["x"] += obj["velocity_x"]
    obj["y"] += obj["velocity_y"]
    obj["velocity_y"] += 0.2
    obj["life"] -= 1

# ──────────────────────────────────────────
# 地面との衝突
# ──────────────────────────────────────────

def check_ground_collision(obj):
    if obj["y"] > 110:
        if obj["type"] == "raindrop":
            create_splash_effect(obj["x"], 110)
        return True
    return False

# ──────────────────────────────────────────
# 画面外オブジェクトの削除
# ──────────────────────────────────────────

def cleanup_objects():
    falling_objects[:] = [
        obj for obj in falling_objects
        if obj["y"] < 130 and -20 < obj["x"] < 180
    ]

# ──────────────────────────────────────────
# 描画
# ──────────────────────────────────────────

def draw_all_objects():
    for obj in falling_objects:
        if obj["type"] == "raindrop":
            draw_raindrop(obj)
        elif obj["type"] == "snowflake":
            draw_snowflake(obj)
        elif obj["type"] == "meteor":
            draw_meteor(obj)
        elif obj["type"] == "ufo":
            draw_ufo(obj)
        elif obj["type"] == "particle":
            draw_particle(obj)

def draw_raindrop(obj):
    pyxel.line(
        int(obj["x"]),
        int(obj["y"]),
        int(obj["x"]),
        int(obj["y"] + obj["length"]),
        obj["color"]
    )

def draw_snowflake(obj):
    x, y, size = int(obj["x"]), int(obj["y"]), obj["size"]
    pyxel.circ(x, y, size, obj["color"])
    pyxel.line(x - size, y, x + size, y, obj["color"])
    pyxel.line(x, y - size, x, y + size, obj["color"])

def draw_meteor(obj):
    x, y, size = int(obj["x"]), int(obj["y"]), obj["size"]
    pyxel.circ(x, y, size, obj["color"])

    for i, (tx, ty) in enumerate(obj["trail"]):
        alpha = i / len(obj["trail"])
        if alpha > 0.3:
            pyxel.rect(int(tx), int(ty), 1, 1, 9)

def draw_ufo(obj):
    x, y = int(obj["x"]), int(obj["y"])
    pyxel.circ(x, y, 6, obj["color"])
    pyxel.rect(x - 8, y - 2, 16, 4, obj["color"])

    if (pyxel.frame_count // 10) % 2:
        pyxel.rect(x - 4, y, 1, 1, 10)
        pyxel.rect(x + 4, y, 1, 1, 10)

def draw_particle(obj):
    pyxel.rect(
        int(obj["x"]),
        int(obj["y"]),
        2, 2,
        obj["color"]
    )

# ──────────────────────────────────────────
# メインループ
# ──────────────────────────────────────────

def update():
    global spawn_timer, current_mode

    # モード切り替え（スペースキー）
    if pyxel.btnp(pyxel.KEY_SPACE):
        mode_list = list(modes.keys())
        current_index = mode_list.index(current_mode)
        current_mode = mode_list[(current_index + 1) % len(mode_list)]

    # オブジェクト生成
    spawn_timer += 1
    if spawn_timer >= modes[current_mode]["spawn_rate"]:
        spawn_timer = 0
        spawn_random_object()

    # オブジェクト更新
    update_all_objects()

    # 地面との衝突チェック
    for obj in falling_objects[:]:
        if obj["type"] in ["raindrop", "meteor"]:
            if check_ground_collision(obj):
                falling_objects.remove(obj)

    # 水しぶきの寿命が切れたら削除
    falling_objects[:] = [
        obj for obj in falling_objects
        if obj["type"] != "particle" or obj["life"] > 0
    ]

    # 画面外オブジェクトの削除
    cleanup_objects()

def draw():
    # 背景色をモードに応じて変更
    bg_colors = {
        "rain": 13,
        "snow": 6,
        "meteor": 1,
        "mixed": 5
    }

    pyxel.cls(bg_colors.get(current_mode, 1))

    # 地面
    pyxel.line(0, 110, 159, 110, 3)

    # 全オブジェクト描画
    draw_all_objects()

    # UI表示
    pyxel.text(5, 5, f"Mode: {current_mode.upper()}", 7)
    pyxel.text(5, 15, f"Objects: {len(falling_objects)}", 7)
    pyxel.text(5, 105, "SPACE: Change Mode", 7)

pyxel.run(update, draw)