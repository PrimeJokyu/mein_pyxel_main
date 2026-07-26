import pyxel

player_x = 80
player_y = 60
jump_timer = 0
player_color = 8



def update():
    global player_x, player_y, player_color, jump_timer

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
    
    if pyxel.btnp(pyxel.KEY_SPACE):
        jump_timer = 15

    if jump_timer > 0:
        jump_timer -= 1

    if pyxel.btnp(pyxel.KEY_R):
        player_x = 80
        player_y = 60
        jump_timer = 0
        player_color = 8

    if pyxel.btnp(pyxel.KEY_1):
        player_color = 1
    if pyxel.btnp(pyxel.KEY_2):
        player_color = 2
    if pyxel.btnp(pyxel.KEY_3):
        player_color = 3
    if pyxel.btnp(pyxel.KEY_4):
        player_color = 4
    if pyxel.btnp(pyxel.KEY_5):
        player_color = 5
    if pyxel.btnp(pyxel.KEY_6):
        player_color = 6
    if pyxel.btnp(pyxel.KEY_7):
        player_color = 7
    if pyxel.btnp(pyxel.KEY_8):
        player_color = 8
    if pyxel.btnp(pyxel.KEY_9):
        player_color = 9
    if pyxel.btnp(pyxel.KEY_0):
        player_color = 0

    player_x = max(8, player_x)
    player_x = min(player_x, 152)
    player_y = max(8, player_y)
    player_y = min(player_y, 112) 

def draw():
    pyxel.cls(1)

    y = player_y - jump_timer
    pyxel.circ(player_x, y, 8, player_color)


    pyxel.text(5, 5, "Arrow: Move(2)", 7)
    pyxel.text(5, 15, "WASD: Fast(4)", 7)
    pyxel.text(5, 25, "Space: Jump", 7)
    pyxel.text(5, 35, "R: Reset", 7)
    pyxel.text(5, 45, "1-9: Color", 7)

    pyxel.text(5, 65, f"X:{player_x} Y:{player_y}", 7)
    pyxel.text(5, 75, f"Color:{player_color}", 7)
    if jump_timer > 0:
        pyxel.text(5, 85, "JUMPING!", 10)

pyxel.init(160,120, title="Character Control Master")
pyxel.run(update,draw)