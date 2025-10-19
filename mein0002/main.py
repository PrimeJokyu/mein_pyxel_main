import pyxel

pyxel.init(160, 120)
def update():
    global player_x

    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2  # 右キーを押している間、継続的に移動

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2  # 左キーを押している間、継続的に移動

def draw():
    pyxel.cls(0)

    # ボールの描画
    pyxel.circ(player_x, 5, 8)

pyxel.run(update, draw)