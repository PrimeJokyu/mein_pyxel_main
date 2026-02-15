import pyxel
import math

# 初期設定
pyxel.init(160, 120, fps=30)
pyxel.load("my_game.pyxres")
pyxel.playm(0, loop=True)

# プレイヤー情報
player_x = 80
player_y = 60
facing = 0
state = 0
counter = 0

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
    if enemy["type"] == "slime":
        enemy["x"] += pyxel.rndi(-2, 2)
        enemy["y"] += pyxel.rndi(-2, 2)

    elif enemy["type"] == "goblin":
        if enemy["x"] < player_x:
            enemy["x"] += 1
        elif enemy["x"] > player_x:
            enemy["x"] -= 1

        if enemy["y"] < player_y:
            enemy["y"] += 1
        elif enemy["y"] > player_y:
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

# 更新
def update():
    global player_x, player_y, facing, state, counter

    # プレイヤー移動
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
        facing = 0
    elif pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2
        facing = 1
    elif pyxel.btn(pyxel.KEY_UP):
        player_y -= 2
        facing = 2
    elif pyxel.btn(pyxel.KEY_DOWN):
        player_y += 2
        facing = 3

    # 画面内制限
    player_x = max(0, min(160 - 16, player_x))
    player_y = max(0, min(120 - 16, player_y))

    # アニメーション
    counter += 1
    if counter >= 15:
        counter = 0
        state = 16 if state == 0 else 0

    # 敵更新
    for enemy in enemies:
        if enemy["state"] == "alive":
            update_enemy_ai(enemy)
        update_enemy_state(enemy)

    # 攻撃
    if pyxel.btnp(pyxel.KEY_A):
        for enemy in enemies:
            if enemy["state"] != "alive" or enemy["hp"] <= 0:
                continue

            dx = enemy["x"] - player_x
            dy = enemy["y"] - player_y

            hit = False
            if facing == 0:   # 左
                hit = -16 < dx < 0 and abs(dy) < 12
            elif facing == 1: # 右
                hit = 0 < dx < 16 and abs(dy) < 12
            elif facing == 2: # 上
                hit = -16 < dy < 0 and abs(dx) < 12
            elif facing == 3: # 下
                hit = 0 < dy < 16 and abs(dx) < 12

            if hit:
                enemy["hp"] -= 5
                break

# 描画
def draw():
    pyxel.cls(12)

    # プレイヤー
    if facing == 0:
        pyxel.blt(player_x, player_y, 0, state, 0, -16, 16, 1)
    elif facing == 1:
        pyxel.blt(player_x, player_y, 0, state, 0, 16, 16, 1)
    elif facing == 2:
        pyxel.blt(player_x, player_y, 0, state, 16, 16, 16, 1)
    elif facing == 3:
        pyxel.blt(player_x, player_y, 0, state, 32, 16, 16, 1)

    # 敵
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

# 実行
pyxel.run(update, draw)
