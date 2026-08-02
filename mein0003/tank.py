import os
import pyxel

player_x = 80
player_y = 60


pyxel.init(160, 120)
pyxel.load("tank.pyxres")


def update():
    global player_x, player_y

    if pyxel.btn(pyxel.KEY_UP):
        player_y -= 2
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += 2
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2

def draw():
    pyxel.cls(0)
    pyxel.blt(player_x, player_y, 0, 0, 0, 18, 18)


pyxel.run(update, draw)
