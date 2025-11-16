import pyxel

ball_x = 80
ball_y = 60
dx = 1
dy = 2

pyxel.init(160,120)

def update():
    global ball_y

    time = pyxel.frame_count

    if (time % 120) < 60:
        ball_y += 1
    else:
        ball_y -= 1
    
def draw():
    pyxel.cls(1)
    pyxel.circ(ball_x,ball_y,8,10)

pyxel.run(update,draw)

import math
def update():
    global ball_x,ball_y

    time = pyxel.frame_count * 0.1

    ball_x =80 + math.cos(time) * 50
    ball_y =60 + math.sin(time) * 30
