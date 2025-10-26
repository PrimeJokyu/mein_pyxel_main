
import pyxel

# 画面サイズとプレイヤー設定
WIDTH, HEIGHT = 160, 120
SIZE = 10                 # 四角形の一辺
HALF = SIZE // 2          # 半辺
SPEED = 2                 # 移動速度

# 初期位置（中央）
player_x = WIDTH // 2
player_y = HEIGHT // 2

pyxel.init(WIDTH, HEIGHT, title="Arrow Move & Reset")

def update():
    global player_x, player_y

    # 矢印キーで移動
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= SPEED
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += SPEED
    if pyxel.btn(pyxel.KEY_UP):
        player_y -= SPEED
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += SPEED

    # 境界制限（中心座標を半辺でクリップ）
    player_x = max(HALF, min(player_x, WIDTH - HALF))
    player_y = max(HALF, min(player_y, HEIGHT - HALF))

    # Rキーで中央にリセット（押した瞬間）
    if pyxel.btnp(pyxel.KEY_R):
        player_x = WIDTH // 2
        player_y = HEIGHT // 2

def draw():
    pyxel.cls(12)  # 背景（青）
    # 四角形は左上座標指定なので中心→左上に変換
    pyxel.rect(player_x - HALF, player_y - HALF, SIZE, SIZE, 8)  # 赤

pyxel.run(update, draw)
