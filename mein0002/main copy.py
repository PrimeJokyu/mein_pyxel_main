#pyxel edit ./mein0002/my_game.pyxres
import pyxel
import math

# 初期設定
pyxel.init(160, 120, fps=30)
pyxel.load("my_game.pyxres")
pyxel.playm(0, loop=True)

character = {
    "x": 80,
    "y": 60,
    "direction": 16,
    "animation_frame": 0,
    "animation_speed": 10,
    "current_animation": "idle",
    "is_attacking": False,  
    "animations": {
        "idle": [(0, 0), (16, 0)],
        "attack": [(0, 48), (16, 48), (32, 48)]
    }
}

# 敵の情報生成
def make_enemy(x, y, hp, enemy_type, sprite_index):
    enemy = {
        "x": x,
        "y": y,
        "hp": hp,
        "max_hp": hp,
        "type": enemy_type,
        "u": sprite_index,
        "state": "alive",
        "timer": 0
    }
    if enemy_type == "bat":
        enemy["cx"] = x
        enemy["cy"] = y
    return enemy

enemies = [
    make_enemy(30, 80, 30, "slime", 0),
    make_enemy(130, 40, 50, "goblin", 1),
    make_enemy(60, 20, 20, "bat", 2),
]

# 敵の動き
def update_enemy_ai(enemy):

    c = character

    if enemy["type"] == "slime":
        enemy["x"] += pyxel.rndi(-2, 2)
        enemy["y"] += pyxel.rndi(-2, 2)

    elif enemy["type"] == "goblin":
        if enemy["x"] < c["x"]:
            enemy["x"] += 1
        elif enemy["x"] > c["x"]:
            enemy["x"] -= 1

        if enemy["y"] < c["y"]:
            enemy["y"] += 1
        elif enemy["y"] > c["y"]:
            enemy["y"] -= 1

    elif enemy["type"] == "bat":
        a = (pyxel.frame_count + enemy["u"] * 30) * 0.1
        enemy["x"] = enemy["cx"] + math.cos(a) * 30
        enemy["y"] = enemy["cy"] + math.sin(a) * 20

    # bat以外だけ画面内制限
    if enemy["type"] != "bat":
        enemy["x"] = max(0, min(160 - 16, enemy["x"]))
        enemy["y"] = max(0, min(120 - 16, enemy["y"]))

# 敵の状態
def update_enemy_state(enemy):
    if enemy["state"] == "alive" and enemy["hp"] <= 0:
        enemy["state"] = "dying"
        enemy["timer"] = 30

    if enemy["state"] == "dying":
        enemy["timer"] -= 1
        if enemy["timer"] <= 0:
            enemy["state"] = "dead"

def update_character():
    c = character

    c["animation_frame"] += 1

    # 移動
    if pyxel.btn(pyxel.KEY_LEFT):
        c["x"] -= 2
        c["direction"] = -16

    elif pyxel.btn(pyxel.KEY_RIGHT):
        c["x"] += 2
        c["direction"] = 16

    # 攻撃開始
    if pyxel.btnp(pyxel.KEY_SPACE) and not c["is_attacking"]:
        c["is_attacking"] = True
        c["current_animation"] = "attack"
        c["animation_frame"] = 0

    # 攻撃中処理
    if c["is_attacking"]:
        frames = c["animations"]["attack"]
        frame_index = (c["animation_frame"] // c["animation_speed"])

        # 2フレーム目で当たり判定
        if frame_index == 1:
            for enemy in enemies:
                if enemy["state"] != "alive":
                    continue

                dx = enemy["x"] - c["x"]
                dy = enemy["y"] - c["y"]

                hit = False

                if c["direction"] == 16:
                    hit = 0 < dx < 16 and abs(dy) < 12
                elif c["direction"] == -16:
                    hit = -16 < dx < 0 and abs(dy) < 12

                if hit:
                    enemy["hp"] -= 5

        # アニメーション終了
        if frame_index >= len(frames):
            c["is_attacking"] = False
            c["current_animation"] = "idle"
            c["animation_frame"] = 0

    else:
        c["current_animation"] = "idle"

def draw_character():
    c = character
    # 現在のアニメーションフレームを取得
    frames = c["animations"][c["current_animation"]]
    frame_index = (c["animation_frame"] // c["animation_speed"]) % len(frames)
    sprite_x, sprite_y = frames[frame_index]
    pyxel.blt(c["x"], c["y"], 0, sprite_x, sprite_y, c["direction"], 16, 1)


# 敵更新
def update_enemy():
    for enemy in enemies:
        if enemy["state"] == "alive":
            update_enemy_ai(enemy)
        update_enemy_state(enemy)

def draw_enemy():
    for enemy in enemies:
        if enemy["state"] == "dead":
            continue

        v = 16 if enemy["state"] == "dying" else 0
        pyxel.blt(enemy["x"], enemy["y"], 1, enemy["u"] * 16, v, 16, 16, 1)

        # HPバー
        if enemy["state"] == "alive":
            w = int(16 * enemy["hp"] / enemy["max_hp"])
            y = max(enemy["y"] - 4, 0)
            pyxel.rect(enemy["x"], y, w, 2, 8)

# 更新
def update():
    update_character()
    update_enemy()

def draw():
    pyxel.cls(12)
    draw_character()
    draw_enemy()


# 実行
pyxel.run(update, draw)
