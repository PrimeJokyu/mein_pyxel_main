#python -m pyxel edit ./mein0002/my_game.pyxres
import pyxel

pyxel.init(160, 120, fps=30)
pyxel.load("my_game.pyxres")

ball_speed = 3

player1_x = 0
player1_y = 0
player1_looks = 0
player1_looks_x = 0
player1_looks_y = 0

player1_ball_false = 0
player1_ball_x = 0
player1_ball_y = 0
player1_ballspped_x = 0
player1_ballspped_y = 0
player1_ball_look = 9
player1_ballcount = 0

player2_x = 80
player2_y = 50
player2_looks = 0
player2_looks_x = 0
player2_looks_y = 0

player2_ball_false = 0
player2_ball_x = 0
player2_ball_y = 0
player2_ballspped_x = 0
player2_ballspped_y = 0
player2_ball_look = 9
player2_ballcount = 0

text = ""



# 更新
def player1_update():
    global player1_x, player1_y, player1_looks_x, player1_looks_y,player1_looks
  
    if pyxel.btn(pyxel.KEY_D):
        player1_x += 1
        player1_looks = 0
        player1_looks_x = 0
        player1_looks_y = 0

    if pyxel.btn(pyxel.KEY_A):
        player1_x -= 1
        player1_looks = 1
        player1_looks_x = 16
        player1_looks_y = 0
        
    if pyxel.btn(pyxel.KEY_W):
        player1_y -= 1
        player1_looks = 2
        player1_looks_x = 0
        player1_looks_y = 16
        
    if pyxel.btn(pyxel.KEY_S):
        player1_y += 1
        player1_looks = 3
        player1_looks_x = 16
        player1_looks_y = 16

    if pyxel.btn(pyxel.KEY_D)and pyxel.btn(pyxel.KEY_W):
        player1_looks = 4
        player1_looks_x = 32
        player1_looks_y = 0

    if pyxel.btn(pyxel.KEY_D)and pyxel.btn(pyxel.KEY_S):
        player1_looks = 5
        player1_looks_x = 48
        player1_looks_y = 0

    if pyxel.btn(pyxel.KEY_A)and pyxel.btn(pyxel.KEY_W):
        player1_looks = 6
        player1_looks_x = 32
        player1_looks_y = 16

    if pyxel.btn(pyxel.KEY_A)and pyxel.btn(pyxel.KEY_S):
        player1_looks = 7
        player1_looks_x = 48
        player1_looks_y = 16

    if player1_x > 144 :
        player1_x = 144

    if player1_y > 104 :
        player1_y = 104

    if player1_y < 0:
        player1_y = 0

    if player1_x < 0:
        player1_x = 0
        
def player1_ball_update():
    global player1_ball_x, player1_ball_y, player1_looks, player2_x, player2_y,text
    global player1_ballspped_x, player1_ballspped_y, player1_ball_look, player1_ball_false, player1_ballcount

    if pyxel.btnp(pyxel.KEY_SPACE):
        if player1_ball_false == 0:
            player1_ball_x = player1_x + 7
            player1_ball_y = player1_y + 7
            player1_ball_look = 0  
            player1_ball_false = 1     
            player1_ballcount = 0
            
            if player1_looks == 0:    
                player1_ballspped_x = ball_speed
                player1_ballspped_y = 0
            elif player1_looks == 1:  
                player1_ballspped_x = -ball_speed
                player1_ballspped_y = 0
            elif player1_looks == 2:  
                player1_ballspped_x = 0
                player1_ballspped_y = -ball_speed
            elif player1_looks == 3:   
                player1_ballspped_x = 0
                player1_ballspped_y = ball_speed
                
            elif player1_looks == 4:  
                player1_ballspped_x = ball_speed
                player1_ballspped_y = -ball_speed
            elif player1_looks == 5:  
                player1_ballspped_x = ball_speed
                player1_ballspped_y = ball_speed
            elif player1_looks == 6:   
                player1_ballspped_x = -ball_speed
                player1_ballspped_y = -ball_speed
            elif player1_looks == 7:   
                player1_ballspped_x = -ball_speed
                player1_ballspped_y = ball_speed

    if player1_ball_false == 1:
        player1_ball_x += player1_ballspped_x
        player1_ball_y += player1_ballspped_y
        player1_ballcount += 1

        # 壁での跳ね返り判定（めり込み対策として進行方向もチェック）
        if player1_ball_x > 160 and player1_ballspped_x > 0:
            player1_ballspped_x *= -1
        elif player1_ball_x < 0 and player1_ballspped_x < 0:
            player1_ballspped_x *= -1

        if player1_ball_y > 120 and player1_ballspped_y > 0:
            player1_ballspped_y *= -1
        elif player1_ball_y < 0 and player1_ballspped_y < 0:
            player1_ballspped_y *= -1

        # プレイヤー2への当たり判定
        if abs(player1_ball_x - (player2_x + 8)) < 8 and abs(player1_ball_y - (player2_y + 8)) < 8:
            player1_ball_false = 0
            player1_ball_look = 9
            text="WIN"

        # 90フレーム経過したら消滅させる
        if player1_ballcount >= 90:
            player1_ball_false = 0
            player1_ball_look = 9

def player2_update():
    global player2_x, player2_y, player2_looks_x, player2_looks_y, player2_looks
  
    if pyxel.btn(pyxel.KEY_RIGHT):
        player2_x += 1
        player2_looks = 0
        player2_looks_x = 0
        player2_looks_y = 0

    if pyxel.btn(pyxel.KEY_LEFT):
        player2_x -= 1
        player2_looks = 1
        player2_looks_x = 16
        player2_looks_y = 0
        
    if pyxel.btn(pyxel.KEY_UP):
        player2_y -= 1
        player2_looks = 2
        player2_looks_x = 0
        player2_looks_y = 16
        
    if pyxel.btn(pyxel.KEY_DOWN):
        player2_y += 1
        player2_looks = 3
        player2_looks_x = 16
        player2_looks_y = 16

    if pyxel.btn(pyxel.KEY_RIGHT) and pyxel.btn(pyxel.KEY_UP):
        player2_looks = 4
        player2_looks_x = 32
        player2_looks_y = 0

    if pyxel.btn(pyxel.KEY_RIGHT) and pyxel.btn(pyxel.KEY_DOWN):
        player2_looks = 5
        player2_looks_x = 48
        player2_looks_y = 0

    if pyxel.btn(pyxel.KEY_LEFT) and pyxel.btn(pyxel.KEY_UP):
        player2_looks = 6
        player2_looks_x = 32
        player2_looks_y = 16

    if pyxel.btn(pyxel.KEY_LEFT) and pyxel.btn(pyxel.KEY_DOWN):
        player2_looks = 7
        player2_looks_x = 48
        player2_looks_y = 16

    if player2_x > 144:
        player2_x = 144

    if player2_y > 104:
        player2_y = 104

    if player2_y < 0:
        player2_y = 0

    if player2_x < 0:
        player2_x = 0

def player2_ball_update():
    global player2_ball_x, player2_ball_y, player2_looks,player1_x,player1_y,text
    global player2_ballspped_x, player2_ballspped_y, player2_ball_look, player2_ball_false, player2_ballcount

    if pyxel.btnp(pyxel.KEY_RETURN):
        if player2_ball_false == 0:
            player2_ball_x = player2_x + 7
            player2_ball_y = player2_y + 7
            player2_ball_look = 0  
            player2_ball_false = 1     
            player2_ballcount = 0
            
            if player2_looks == 0:    
                player2_ballspped_x = ball_speed
                player2_ballspped_y = 0
            elif player2_looks == 1:  
                player2_ballspped_x = -ball_speed
                player2_ballspped_y = 0
            elif player2_looks == 2:  
                player2_ballspped_x = 0
                player2_ballspped_y = -ball_speed
            elif player2_looks == 3:   
                player2_ballspped_x = 0
                player2_ballspped_y = ball_speed
                
            elif player2_looks == 4:  
                player2_ballspped_x = ball_speed
                player2_ballspped_y = -ball_speed
            elif player2_looks == 5:  
                player2_ballspped_x = ball_speed
                player2_ballspped_y = ball_speed
            elif player2_looks == 6:   
                player2_ballspped_x = -ball_speed
                player2_ballspped_y = -ball_speed
            elif player2_looks == 7:   
                player2_ballspped_x = -ball_speed
                player2_ballspped_y = ball_speed

    if player2_ball_false == 1:
        player2_ball_x += player2_ballspped_x
        player2_ball_y += player2_ballspped_y
        player2_ballcount += 1

        # 壁での跳ね返り判定
        if player2_ball_x > 160 and player2_ballspped_x > 0:
            player2_ballspped_x *= -1
        elif player2_ball_x < 0 and player2_ballspped_x < 0:
            player2_ballspped_x *= -1

        if player2_ball_y > 120 and player2_ballspped_y > 0:
            player2_ballspped_y *= -1
        elif player2_ball_y < 0 and player2_ballspped_y < 0:
            player2_ballspped_y *= -1

        # 90フレーム経過したら消滅させる
        if player2_ballcount >= 90:
            player2_ball_false = 0
            player2_ball_look = 9

    #当たり判定
    if player2_ball_false == 1:
        if abs(player2_ball_x - (player1_x + 8)) < 8 and abs(player2_ball_y - (player1_y + 8)) < 8:
            player2_ball_false = 0
            player2_ball_look = 9
            text="LOSE"
            
def update():
    player1_update()
    player1_ball_update()
    player2_update()
    player2_ball_update()

# 描画
def draw():
    pyxel.cls(9)
    # プレイヤー1と弾の描画
    pyxel.blt(player1_x, player1_y, 2, player1_looks_x, player1_looks_y, 16, 16, 1)
    pyxel.circ(player1_ball_x, player1_ball_y, 1, player1_ball_look)
    
    # プレイヤー2と弾の描画
    pyxel.blt(player2_x, player2_y, 2, player2_looks_x, player2_looks_y, 16, 16, 1)
    pyxel.circ(player2_ball_x, player2_ball_y, 1, player2_ball_look)
    pyxel.text(0,0,text,0)

# 実行
pyxel.run(update, draw)
