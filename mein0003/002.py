import pyxel

ball1_x,ball1_y = 40,30
ball1_dx,ball1_dy =2,1

ball2_x,ball2_y = 80,60
ball2_dx,ball2_dy = -1,2

ball3_x,ball3_y = 120,90
ball3_dx,ball3_dy = 1,-1

def update():
    global ball1_x,ball1_y,ball1_dx,ball1_dy
    global ball2_x,ball2_y,ball2_dx,ball2_dy
    global ball3_x,ball3_y,ball3_dx,ball3_dy

    ball1_x +=ball1_dx
    ball1_y +=ball1_dy

    if ball1_x <= 0 or ball1_x >= 160: ball1_dx = -ball1_dx
    if ball1_y <= 0 or ball1_y >= 120: ball1_dy = -ball1_dy
    