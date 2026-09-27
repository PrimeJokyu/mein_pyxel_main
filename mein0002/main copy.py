import pyxel

# ゲームの状態（globalを使わない辞書）
state = {
    # ターゲット（四角形）
    "rect": {
        "x": pyxel.rndi(10, 140),
        "y": pyxel.rndi(10, 100),
        "w": 10,
        "h": 10
    },
    "hit_rect": False
}

def update():
    rect = state["rect"]
    mx, my = pyxel.mouse_x, pyxel.mouse_y

    # マウスカーソル（点）がターゲット（四角形）の中にあるか判定
    state["hit_rect"] = (rect["x"] <= mx <= rect["x"] + rect["w"] and
                         rect["y"] <= my <= rect["y"] + rect["h"])

    # ターゲットの上で左クリックしたときの処理
    if state["hit_rect"] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        # ランダムな位置にターゲットを移動
        rect["x"] = pyxel.rndi(10, 140)
        rect["y"] = pyxel.rndi(10, 100)

def draw():
    pyxel.cls(0)
    rect = state["rect"]

    # ターゲットの描画（マウスが乗っている時は黄色:10、離れている時は赤:8）
    color = 10 if state["hit_rect"] else 8
    pyxel.rect(rect["x"], rect["y"], rect["w"], rect["h"], color)


# 初期化と実行
pyxel.init(160, 120, title="Target Clicker Game")
pyxel.mouse(True)
pyxel.run(update, draw)