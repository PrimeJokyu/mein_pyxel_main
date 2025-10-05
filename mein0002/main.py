import pyxel
# グローバル変数（プログラム全体で使える変数）
ball_x = 50  # ボールのX座標
ball_y = 60  # ボールのY座標

import math

# ボールの初期位置と移動量
ball1_x, ball1_y = 30, 60
ball1_dx = 2  # 左右移動のみ

ball2_x, ball2_y = 80, 30
ball2_dy = 3  # 上下移動のみ

ball3_x, ball3_y = 130, 90
ball3_dx, ball3_dy = -1, -2  # 斜め移動

pyxel.init(160, 120)


def update():
    global ball1_x, ball1_dx

    ball1_x += ball1_dx
    
# update()関数内に追加
    global ball2_y, ball2_dy

    ball2_y += ball2_dy
    
# update()関数内に追加
    global ball3_x, ball3_y, ball3_dx, ball3_dy

    ball3_x += ball3_dx
    ball3_y += ball3_dy

def draw():
    pyxel.cls(1)  # 背景色    
    pyxel.circ(ball1_x, ball1_y, 8, 8)   # 赤、大きい
    pyxel.circ(ball2_x, ball2_y, 6, 10)  # 黄色、中くらい
    pyxel.circ(ball3_x, ball3_y, 4, 12)  # 青、小さい
    if ball1_x <= 0 or ball1_x >= 160:
        ball1_dx = -ball1_dx
        
    if ball2_y <= 0 or ball2_y >= 120:
        ball2_dy = -ball2_dy
        
    if ball3_x <= 0 or ball3_x >= 160:
        ball3_dx = -ball3_dx
    if ball3_y <= 0 or ball3_y >= 120:
        ball3_dy = -ball3_dy

pyxel.run(update, draw)