import pyxel

player_x = 80
player_y = 60
jump_count = 0
color = 8

pyxel.init(160,120)

def update():
    global player_x,player_y

    speed = 3

    dx = 0
    dy = 0
    
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        player_x -= speed
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        player_x += speed
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        player_y -= speed
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        player_y += speed
    if pyxel.btnp(pyxel.KEY_C):
        color = (color+1) % 16

    player_x += dx
    player_y += dy

def draw():
    pyxel.cls(1)

    y = player_y - jump_count
    pyxel.circ(player_x, y, 8, color)

pyxel.run(update,draw)