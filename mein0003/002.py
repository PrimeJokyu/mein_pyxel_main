import pyxel

ball1_x,ball1_y = 30,60
ball1_dx = 2

ball2_x,ball2_y = 80,30
ball2_dy = 3

ball3_x,ball3_y = 130,90
ball3_dx,ball3_dy = -1,-2

pyxel.init(160,120)

def update():
    global ball1_x,ball1_dx
    global ball2_y,ball2_dy
    global ball3_x,ball3_y,ball3_dx,ball3_dy

    ball1_x += ball1_dx
    ball2_y += ball2_dy
    ball3_x += ball3_dx
    ball3_y += ball3_dy

    if ball1_x <= 0 or ball1_x >= 160:
        ball1_dx = -ball1_dx
    if ball2_y <= 0 or ball2_y >= 120:
        ball2_dy = -ball2_dy
    if ball3_x <= 0 or ball3_x >= 160:
        ball3_dx = -ball3_dx
    if ball3_y <= 0 or ball3_y >= 120:
        ball3_dy = -ball3_dy


def draw():
    pyxel.cls(0)
    pyxel.circ(ball1_x,ball1_y,8,8)
    pyxel.circ(ball2_x,ball2_y,6,10)
    pyxel.circ(ball3_x,ball3_y,4,12)

pyxel.run(update, draw)