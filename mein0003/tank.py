import pyxel


state = {
    "player_x": 80,
    "player_y": 60,
    "bullet_x": 0,
    "bullet_y": 0,
    "bullet_vx": 0,
    "bullet_vy": -4,
    "bullet_visible": False,
    "player_dir_x": 1,  # 1: 右向き, -1: 左向き（反転）
    "player_dir_y": 1,  # 1: 通常, -1: 上下反転

}

pyxel.init(160, 120)
pyxel.load("tank.pyxres")


def update():
    # スピード
    speed = 2
    if pyxel.btn(pyxel.KEY_SHIFT):
        speed = 5

    # プレイヤーの移動と向き
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        state["player_y"] -= speed
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        state["player_y"] += speed
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        state["player_x"] -= speed
        state["player_dir_x"] = -1  # 左向きにする
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        state["player_x"] += speed
        state["player_dir_x"] = 1   # 右向きにする

    # スペースキーで弾を発射（弾が出ていないときのみ）
    if pyxel.btn(pyxel.KEY_SPACE) and not state["bullet_visible"]:
        state["bullet_x"] = state["player_x"] + 8
        state["bullet_y"] = state["player_y"] + 8
        # 向きに合わせて弾の発射方向を決める
        state["bullet_vx"] = 4 * state["player_dir_x"]
        state["bullet_vy"] = 0
        state["bullet_visible"] = True

    # 弾の移動と画面外判定
    if state["bullet_visible"]:
        state["bullet_x"] += state["bullet_vx"]
        state["bullet_y"] += state["bullet_vy"]
        # 画面外に出たらリセット
        if (
            state["bullet_x"] < 0
            or state["bullet_x"] > 160
            or state["bullet_y"] < 0
            or state["bullet_y"] > 120
        ):
            state["bullet_visible"] = False


def draw():
    pyxel.cls(0)
    # 幅(w)と高さ(h)を向きに応じて反転させます
    w = 18 * state["player_dir_x"]
    h = 18 * state["player_dir_y"]
    pyxel.blt(state["player_x"], state["player_y"], 0, 0, 0, w, h)

    if state["bullet_visible"]:
        pyxel.circ(state["bullet_x"], state["bullet_y"], 2, 10)


pyxel.run(update, draw)
