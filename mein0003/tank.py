import pyxel


state = {
    "player_x": 80,
    "player_y": 60,
    "bullet_x": 0,
    "bullet_y": 0,
    "bullet_visible": False,
}

pyxel.init(160, 120)
pyxel.load("tank.pyxres")


def update():
    #スピード
    speed = 3
    speedLv2 = 6

    # プレイヤーの移動
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        state["player_y"] -= speed
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        state["player_y"] += speed
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        state["player_x"] -= speed
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        state["player_x"] += speed
    

    # スペースキーで弾を発射（弾が出ていないときのみ）
    if pyxel.btn(pyxel.KEY_SPACE) and not state["bullet_visible"]:
        state["bullet_x"] = state["player_x"] + 8
        state["bullet_y"] = state["player_y"] + 2
        state["bullet_visible"] = True

    # 弾の移動と画面外判定
    if state["bullet_visible"]:
        state["bullet_y"] -= 4
        if state["bullet_y"] < 0:  # 画面の上に消えたらリセット
            state["bullet_visible"] = False


def draw():
    pyxel.cls(0)
    pyxel.blt(state["player_x"], state["player_y"], 0, 0, 0, 18, 18)

    if state["bullet_visible"]:
        pyxel.circ(state["bullet_x"], state["bullet_y"], 2, 10)


pyxel.run(update, draw)
