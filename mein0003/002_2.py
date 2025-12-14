import pyxel

ball1_x,ball1_y = 30,60
ball1_dx = 2

ball2_x,ball2_y = 60,80
ball2_dy = 4

ball3_x,ball3_y = 10,30
ball3_dx,ball3_dy = 3,6

pyxel.init(160,120)

def update():

    global ball1_x, ball1_dx
    global ball2_y, ball2_dy
    global ball3_x, ball3_y, ball3_dx, ball3_dy


    ball1_x += ball1_dx
    ball2_y += ball2_dy
    ball3_x,ball3_y += ball3_dx,ball3_dy

    if ball1_x <= 0 or ball1_x >=160:
        dx = -dx
    if ball2_y <= 0 or ball2_y >=120:
        dy = -dy
    if ball3_x <= 0 or ball3_x >=160:
        dx = -dx
    if ball3_y <= 0 or ball3_y >=120:
        dy = -dy


def draw():
  pyxel.cls(1)
  pyxel.circ(ball1_x,ball1_y,10,2)
  pyxel.circ(ball2_x,ball2_y,20,4)
  pyxel.circ(ball3_x,ball3_y,30,6)

  


pyxel.run(update,draw)

