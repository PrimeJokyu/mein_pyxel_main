import pyxel


player_x = 80
player_y = 60
player_color = 8
jump_timer = 0

pyxel.init(160, 120, title="Character Control Master")

def update():
    global player_x, player_y, player_color, jump_timer

    # 基本移動（矢印キー - 速度2）
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2
    if pyxel.btn(pyxel.KEY_UP):
        player_y -= 2
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += 2

    # WASD高速移動（速度4）
    if pyxel.btn(pyxel.KEY_A):
        player_x -= 4
    if pyxel.btn(pyxel.KEY_D):
        player_x += 4
    if pyxel.btn(pyxel.KEY_W):
        player_y -= 4
    if pyxel.btn(pyxel.KEY_S):
        player_y += 4

    # スペースキーでジャンプ
    if pyxel.btnp(pyxel.KEY_SPACE):
        jump_timer = 15

    # ジャンプ処理
    if jump_timer > 0:
        jump_timer -= 1

    # Rキーでリセット
    if pyxel.btnp(pyxel.KEY_R):
        player_x = 80
        player_y = 60
        player_color = 8
        jump_timer = 0

    # 数字キー1-9で色変更
    if pyxel.btnp(pyxel.KEY_1):
        player_color = 1
    if pyxel.btnp(pyxel.KEY_2):
        player_color = 2
    if pyxel.btnp(pyxel.KEY_3):
        player_color = 3
    if pyxel.btnp(pyxel.KEY_4):
        player_color = 4
    if pyxel.btnp(pyxel.KEY_5):
        player_color = 5
    if pyxel.btnp(pyxel.KEY_6):
        player_color = 6
    if pyxel.btnp(pyxel.KEY_7):
        player_color = 7
    if pyxel.btnp(pyxel.KEY_8):
        player_color = 8
    if pyxel.btnp(pyxel.KEY_9):
        player_color = 9

    # 画面端制限
    player_x = max(8, player_x)      # 左端制限
    player_x = min(player_x, 152)    # 右端制限
    player_y = max(8, player_y)      # 上端制限
    player_y = min(player_y, 112)    # 下端制限

def draw():
    pyxel.cls(1)  # 背景

    # ジャンプ中の表示調整
    y = player_y - jump_timer * 2
    pyxel.circfill(player_x, y, 8, player_color)

    # 操作説明
    pyxel.text(5, 5, "Arrow: Move(2)", 7)
    pyxel.text(5, 15, "WASD: Fast(4)", 7)
    pyxel.text(5, 25, "Space: Jump", 7)
    pyxel.text(5, 35, "R: Reset", 7)
    pyxel.text(5, 45, "1-9: Color", 7)

    # 現在の情報表示
    pyxel.text(5, 65, f"X:{player_x} Y:{player_y}", 7)
    pyxel.text(5, 75, f"Color:{player_color}", 7)
    if jump_timer > 0:
        pyxel.text(5, 85, "JUMPING!", 10)

pyxel.run(update, draw)