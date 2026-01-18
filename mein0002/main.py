import pyxel
player_x = 80
player_y = 60
facing = 0
state = 0
counter = 0

enemies = [
    {"x": 30, "y": 80, "hp": 30, "type": "slime", "death": 0},
    {"x": 130, "y": 40, "hp": 50, "type": "goblin", "death": 0},
    {"x": 60, "y": 20, "hp": 20, "type": "bat", "death": 0}
]

pyxel.init(160, 120, fps=30)
pyxel.load("my_game.pyxres")

def update():
    global player_x, facing,player_y,counter, state

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

    counter += 1
    if counter >= 15:          # fps=1 なので 1フレーム=1秒
        counter = 0
        state = 16 if state == 0 else 0

    for enemy in enemies:
        # 敵の種類に応じた行動
        if enemy["type"] == "slime":
            # スライムは左右に移動
            enemy["x"] += pyxel.rndi(-1, 1)
            if enemy["hp"] == 0:
                enemy["death"] = 16

        elif enemy["type"] == "goblin":
            # ゴブリンはプレイヤーに近づく
            if enemy["x"] < player_x:
                enemy["x"] += 1
            elif enemy["x"] > player_x:
                enemy["x"] -= 1
            if enemy["hp"] == 0:
                enemy["death"] = 16

        elif enemy["type"] == "bat":
            # コウモリは円運動
            import math
            angle = pyxel.frame_count * 0.1
            enemy["x"] = 80 + math.cos(angle) * 30
            enemy["y"] = 60 + math.sin(angle) * 20
            if enemy["hp"] == 0:
                enemy["death"] = 16


    # A を押したら、プレイヤーに近い敵の HP を 5 減らす（連打防止で1押し1回）
    if pyxel.btnp(pyxel.KEY_A):
        hit_range = 16  # 当たり判定の距離（ピクセル）
        for enemy in enemies:
            dx = enemy["x"] - player_x
            dy = enemy["y"] - player_y
            if dx * dx + dy * dy <= hit_range * hit_range:
                enemy["hp"] -= 5
                if enemy["hp"] <= 0:
                    enemy["hp"] = 0
                break  # 1回の攻撃で1体だけ削る



def draw():
    pyxel.cls(12)
    # 向きに応じてスプライトを反転
    
    if facing == 0:
        pyxel.blt(player_x, player_y, 0, state, 0, -16, 16, 1)
    elif facing == 1:
        pyxel.blt(player_x, player_y, 0, state, 0, 16, 16, 1)  # 幅を負数で反転
    elif facing == 2:
        pyxel.blt(player_x, player_y, 0, state, 16, 16, 16, 1)  # 高さを負数で反転
    elif facing == 3:
        pyxel.blt(player_x, player_y, 0, state, 32, 16, 16, 1)  # 幅と高さを負数で反転



    for enemy in enemies:
        # 敵の種類に応じたスプライト表示
        if enemy["type"] == "slime":
            pyxel.blt(enemy["x"], enemy["y"], 1, 0, enemy["death"], 16, 16, 0)
        elif enemy["type"] == "goblin":
            pyxel.blt(enemy["x"], enemy["y"], 1, 16, enemy["death"], 16, 16, 0)
        elif enemy["type"] == "bat":
            pyxel.blt(enemy["x"], enemy["y"], 1, 32, enemy["death"], 16, 16, 0)

        # HPバーの表示
        bar_width = enemy["hp"] // 5
        pyxel.rect(enemy["x"], enemy["y"] - 5, bar_width, 2, 8)


pyxel.playm(0, loop=True)  # MUSIC 0 をループ再生
pyxel.run(update, draw)