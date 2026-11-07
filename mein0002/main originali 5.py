#python -m pyxel edit ./mein0002/my_game2.pyxres
import pyxel
pyxel.init(160, 120)
pyxel.load("my_game2.pyxres")

enemy_type = {
    1:{
        "name": "スライム",
        "hp": 100,
        "attack": 10,
        "defense": 10,
        "enemy_x": 0,
        "enemy_y": 0,
        "enemy_size": 16
    },
    2:{
        "name": "ドラキー",
        "hp": 150,
        "attack": 15,
        "defense": 5,
        "enemy_x": 16,
        "enemy_y": 0,
        "enemy_size": 16
    },
}
e = 1

frame_counter = 0
screen = 1
looks_x = 0
looks_y = 0
looks_slippage_y = 0
player_x = 80
player_y = 60
work_counter = 0
work_count = pyxel.rndi(150, 200)
topik = 0
damage_caused = 0

screen_paused = 0

choose_x = 0
choose_y = 0

def update_waiting():
    global screen,player_x,player_y,looks_x,looks_y,looks_slippage_y,frame_counter,work_counter

    if frame_counter == 15:
        frame_counter = 0
        if looks_slippage_y == 0:
            looks_slippage_y = 1
        elif looks_slippage_y == 1:
            looks_slippage_y = 0

    if pyxel.btn(pyxel.KEY_UP):
        player_y -= 2
        looks_y =32

    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += 2
        looks_y =48

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
        looks_y =16

    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2
        looks_y =0

    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_DOWN):
        work_counter += 1
        if work_counter == work_count:
            screen = 2
            frame_counter = 0
            work_counter = 0

def update_battle_go():
    global screen,frame_counter,e
    if frame_counter == 50:
        e = pyxel.rndi(1, 2)
        screen = 3
        frame_counter = 0

def update_battle_1():
    global choose_x, choose_y, topik, damage_caused, frame_counter, screen
    # コマンド選択中
    if topik == 0:
        if pyxel.btnp(pyxel.KEY_UP):
            choose_y = 0
        if pyxel.btnp(pyxel.KEY_DOWN):
            choose_y = 16
        if pyxel.btnp(pyxel.KEY_LEFT):
            choose_x = 0
        if pyxel.btnp(pyxel.KEY_RIGHT):
            choose_x = 32

        # 決定（普通のEnterキー、テンキーのEnter、スペースキーのどれでもOK）
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_SPACE):
            if choose_x == 0 and choose_y == 0:
                topik = 1
                damage_caused = pyxel.rndi(30, 50)
                enemy_type[e]["hp"] -= damage_caused
                frame_counter = 0

            elif choose_x == 32 and choose_y == 0:
                pass
            elif choose_x == 0 and choose_y == 16:
                pass
            elif choose_x == 32 and choose_y == 16:
                pass

    # ダメージ表示中：Enterキーかスペースキーを押すとコマンド選択に戻る
    elif topik == 1:
        if frame_counter == 30:
            screen = 4

def update_battle_2():
    pass
    
def draw_paused():

    pyxel.rect(40, 45, 80, 30, 0)
    pyxel.rectb(40, 45, 80, 30, 7)

    pyxel.text(60, 55, "PAUSED", 14)
    pyxel.text(45, 65, "P: Resume  Q: Quit", 7)


def draw_game_over():
    pyxel.cls(8)  # 赤い背景

    # ゲームオーバー文字
    pyxel.text(55, 40, "GAME OVER", 7)

def draw_waiting():
    pyxel.blt(0, 0, 2, 0, 0, 160, 120,)
    pyxel.blt(player_x, player_y, 0, 0, looks_y+looks_slippage_y, 16, 16 ,1)
    
def draw_battle_go():
    pyxel.cls(0)

def draw_battle():
    pyxel.blt(0, 0, 2, 0, 120, 160, 120,)
    pyxel.blt( 72, 48, 1, enemy_type[e]["enemy_x"], enemy_type[e]["enemy_y"], enemy_type[e]["enemy_size"], enemy_type[e]["enemy_size"], 1)

def draw_battle_1():
    if topik == 0:
        pyxel.blt(48, 70, 2, 160, 0, 64, 32, 1,)
        pyxel.blt(48+choose_x, 70+choose_y, 2, 160, 32, 32, 16, 1,)
    elif topik == 1:
        pyxel.text(60, 80, f"Damage: {damage_caused}", 7)

def draw_battle_2():
    pass

def update():
    global frame_counter,screen,screen_paused

    if pyxel.btnp(pyxel.KEY_A):
        screen = -1

    frame_counter += 1
    if pyxel.btnp(pyxel.KEY_P):
        screen_paused = screen
        screen = 0
        
    if screen == 0:
        if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_Q):
            screen = screen_paused
    elif screen == -1:
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_R):
            screen = 1


    if screen == 1:
        update_waiting()
    elif screen == 2:
        update_battle_go()
    elif screen == 3:
        update_battle_1()
    elif screen == 4:
        update_battle_2()

def draw():
    pyxel.cls(0)
    if screen == 1:
        draw_waiting()
    elif screen == 2:
        draw_battle_go()
    elif screen == 3:
        draw_battle()
        draw_battle_1()
    elif screen == 4:
        draw_battle()
        draw_battle_2()
    elif screen == 0:
        draw_paused()
    elif screen == -1:
        draw_game_over()

    print(screen)
    print(frame_counter)
    print(topik)

pyxel.run(update, draw)