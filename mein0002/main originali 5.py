#python -m pyxel edit ./mein0002/my_game2.pyxres
import pyxel
pyxel.init(160, 120)
pyxel.load("my_game2.pyxres")

screen = 1
looks_x = 0
looks_y = 0
looks_slippage_y = 0
player_x = 80
player_y = 60
def update_waiting():
    global screen,player_x,player_y,looks_x,looks_y,looks_slippage_y
    if pyxel.btn(pyxel.KEY_UP):
        player_y -= 2
        looks_x =0
        looks_y =0

    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += 2
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2

def update_battle():
    pass

def draw_waiting():
    pyxel.blt(player_x, player_y, 0, 0, 0, 16, 16,1)
    

def draw_battle():
    pass

def update():
    if screen == 1:
        update_waiting()
    elif screen == 2:
        update_battle()

def draw():
    pyxel.cls(0)
    if screen == 1:
        draw_waiting()
    elif screen == 2:
        draw_battle()


pyxel.run(update, draw)