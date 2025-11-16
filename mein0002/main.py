import pyxel

player_x = 80
player_y = 80
speed = 2
player_size = 8
player_color = 1

base_speed = 2
turbo_speed = 5

vy = 0            # 縦方向のスピード（下に+、上に-）
gravity = 0.3     # 重力の強さ
ground_y = 80     # 地面の高さ (= 立ってるときのY)

pyxel.init(160, 120)

def update():
    global player_x, player_y, vy,base_speed,turbo_speed,player_color
    
    if pyxel.btnp(pyxel.KEY_C):
        player_color += 1
    
    if player_color == 12:
        player_color = 0

    if pyxel.btnp(pyxel.KEY_R):
        player_x = 80
        player_y = ground_y  # = 80 と同じ。地面に戻す
        vy = 0          

    if pyxel.btn(pyxel.KEY_SHIFT):
        speed = turbo_speed
    else:
        speed = base_speed

    # ← →
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        player_x += speed
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        player_x -= speed

    # スペースでジャンプ開始
    # 条件: 地面にいるときだけジャンプできる（2段ジャンプ防止）
    if pyxel.btnp(pyxel.KEY_SPACE):
        if player_y >= ground_y:
            vy = -5      # 上向きに初速を与える（マイナス方向が上）
    
    # 重力を速度に足す（落ちるほど速くなる）
    vy += gravity

    # 位置を更新
    player_y += vy

    # 地面より下に落ちたら、地面で止める
    if player_y > ground_y:
        player_y = ground_y
        vy = 0  # 着地したので停止

    # X座標の制限：左端(0)と右端(160)でチェック
    
    player_x = max(player_size, min(player_x, 160 - player_size))
    player_y = max(player_size, min(player_y, 120 - player_size))
def draw():
    pyxel.cls(0)

    # プレイヤーを描画（丸）
    pyxel.circ(player_x, player_y, player_size,player_color)

    # 地面の目安ライン（見やすくする用）
    pyxel.line(0, ground_y + 8, 160, ground_y + 8, 7)

pyxel.run(update, draw)
