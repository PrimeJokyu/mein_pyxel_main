import pyxel

ball_x = 80
ball_y = 60
dx = 2
dy = 1

pyxel.init(160,120)

def update():
    global ball_x,ball_y

    ball_x += dx
    
    if ball_x > 160:
        ball_x = 0
    if ball_x < 0 :
        ball_x = 0

def draw():
    pyxel.cls(1)
    pyxel.circ(ball_x,ball_y,8,90)

pyxel.run(update,draw)

