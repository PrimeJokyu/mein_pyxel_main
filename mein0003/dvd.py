import pyxel

# 初期位置
ball_x = 80
ball_y = 60

# 移動量
dx = 2
dy = 1

pyxel.init(160, 120)

def update():
    global ball_x, ball_y, dx, dy

    ball_x += dx
    ball_y += dy

    # 画面の端で跳ね返る処理
    if ball_x < 0 or ball_x > 160:
        dx = -dx
    if ball_y < 0 or ball_y > 120:
        dy = -dy

def draw():
    pyxel.cls(1)
    pyxel.circ(ball_x, ball_y, 8, 10)

pyxel.run(update, draw)
