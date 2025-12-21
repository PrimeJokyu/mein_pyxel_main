
import pyxel
player_x = 80
player_y = 60
facing = 0

pyxel.init(160, 120)
pyxel.load("my_game.pyxres")

def update():
    global player_x, facing,player_y

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
        facing = 0
    elif pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2
        facing = 1
    elif pyxel.btn(pyxel.KEY_UP):
        player_y -= 2
        facing = 2
    elif pyxel.btn(pyxel.KEY_DOWN):
        player_y += 2
        facing = 3

def draw():
    pyxel.cls(12)
    # 向きに応じてスプライトを反転
    
    if facing == 0:
        pyxel.blt(player_x, player_y, 0, 0, 0, -16, 16, 1)
    elif facing == 1:
        pyxel.blt(player_x, player_y, 0, 0, 0, 16, 16, 1)  # 幅を負数で反転
    elif facing == 2:
        pyxel.blt(player_x, player_y, 0, 0, 16, 16, 16, 1)  # 高さを負数で反転
    elif facing == 3:
        pyxel.blt(player_x, player_y, 0, 0, 32, 16, 16, 1)  # 幅と高さを負数で反転

pyxel.playm(0, loop=True)  # MUSIC 0 をループ再生
pyxel.run(update, draw)