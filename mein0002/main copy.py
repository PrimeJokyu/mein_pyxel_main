import pyxel

# ゲーム状態
STATE_TITLE = 0
STATE_GAME = 1

current_state = STATE_TITLE
player_x = 80
player_y = 60

pyxel.init(160, 120)

def update():
    global current_state

    if current_state == STATE_TITLE:
        update_title()
    elif current_state == STATE_GAME:
        update_game()

def draw():
    if current_state == STATE_TITLE:
        draw_title()
    elif current_state == STATE_GAME:
        draw_game()

def update_title():
    global current_state, player_x, player_y

    if pyxel.btnp(pyxel.KEY_SPACE):
        current_state = STATE_GAME
        # ゲーム開始時にプレイヤー位置をリセット
        player_x = 80
        player_y = 60

def update_game():
    global current_state, player_x, player_y

    # プレイヤー移動
    if pyxel.btn(pyxel.KEY_LEFT) and player_x > 0:
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT) and player_x < 144:
        player_x += 2
    if pyxel.btn(pyxel.KEY_UP) and player_y > 0:
        player_y -= 2
    if pyxel.btn(pyxel.KEY_DOWN) and player_y < 104:
        player_y += 2

    # タイトル画面に戻る
    if pyxel.btnp(pyxel.KEY_R):
        current_state = STATE_TITLE

def draw_title():
    pyxel.cls(1)

    # タイトル
    pyxel.text(60, 40, "MINI GAME", 14)

    # 開始指示
    pyxel.text(35, 80, "Press SPACE to Start", 7)

def draw_game():
    pyxel.cls(0)

    # プレイヤー
    pyxel.rect(player_x, player_y, 16, 16, 10)

    # 操作説明
    pyxel.text(5, 5, "Arrow keys: Move", 7)
    pyxel.text(5, 15, "R: Return to Title", 7)

pyxel.run(update, draw)