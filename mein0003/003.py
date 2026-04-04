import pyxel

player_x = 80
player_y = 60
jump_timer = 0
color = 8

pyxel.init(160,120)

def update():
    global player_x,player_y, player_color, player_size

    base_speed = 2
    turbo_speed = 4
    dx = 0
    dy = 0

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= base_speed
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += base_speed
    if pyxel.btn(pyxel.KEY_UP):
        player_y -= base_speed
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += base_speed

    if pyxel.btn(pyxel.KEY_A):
        player_x -= turbo_speed
    if pyxel.btn(pyxel.KEY_D):
        player_x += turbo_speed
    if pyxel.btn(pyxel.KEY_W):
        player_y -= turbo_speed
    if pyxel.btn(pyxel.KEY_S):
        player_y += turbo_speed
    
    #if pyxel.btnp(pyxel.KEY_SPACE):
     #   jump_timer = 10

    #if jump_timer > 0:
      #  jump_timer -= 1
    
    player_x = max(0, min(player_x, 160))
    player_y = max(0, min(player_y, 120))

def draw():
    pyxel.cls(1)

    y = player_y - jump_count
    pyxel.circ(player_x, y, 8, color)

pyxel.run(update,draw)