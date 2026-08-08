import pyxel

player_x = 80
player_y = 60


pyxel.init(160, 120)
pyxel.load("tank.pyxres")


def update():
    global player_x, player_y

    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        player_y -= 2
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        player_y += 2
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        player_x += 2

    if pyxel.btn(pyxel.KEY_SPACE) and not
bullet_visible:
        bullet_x - player_x + 8
        bullet_y - player_y + 2
        bullet_visible = True

    if bullet_visible:
        bullet_ y-= 4

def draw():
    pyxel.cls(0)
    pyxel.blt(player_x, player_y, 0, 0, 0, 18, 18)

    if bullet_visible:
        pyxel.circ(bullet_x, bullet_y, 2, 10)

pyxel.run(update, draw)
