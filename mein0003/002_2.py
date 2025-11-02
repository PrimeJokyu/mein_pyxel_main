import pyxel

ball_x = 80
ball_y = 60
dx = 1
dy = 2

pyxel.init(160,120)

def update():
    global ball_x, dx

    ball_x +=dx
    if ball_x <=0 or ball_x >=160:
        dx = -dx


def draw():
    pyxel.cls(1)
    pyxel.circ(ball_x,ball_y,8,10)

pyxel.run(update,draw)

