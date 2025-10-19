
import pyxel

# 初期化
pyxel.init(160, 120, title="Move + Jump Example")

# プレイヤー情報
player_x = 80
player_y = 100
color = 9

def update():
    global player_x, player_y

    base_speed = 2
    turbo_speed = 5

    # シフトキーで高速移動
    if pyxel.btn(pyxel.KEY_SHIFT):
        speed = turbo_speed
    else:
        speed = base_speed

    # 4方向移動
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= speed
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += speed
    if pyxel.btn(pyxel.KEY_UP):
        player_y -= speed
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += speed

def draw():
    pyxel.cls(0)
    pyxel.rect(player_x - 4, player_y - 4, 8, 8, color)

pyxel.run(update, draw)
