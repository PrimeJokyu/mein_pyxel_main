import pyxel

ball_x = 80
ball_y = 60
dx = 2
dy = 1

pyxel.init(160, 120)
def update():

    global ball_x, ball_y 
    ball_x = ball_x + 1
    ball_x += dx
    ball_y += dy

def draw():
    pyxel.cls(1)
    pyxel.circ(ball_x, ball_y, 8, 10)

pyxel.run(update, draw)