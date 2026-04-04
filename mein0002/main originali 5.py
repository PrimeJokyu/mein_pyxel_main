import pyxel
test = 0

player_x = 40
player_y = 80
player_size = 8
eye_x = 4

base_speed = 2
turbo_speed = 3

vy = 0            # 縦方向のスピード（下に+、上に-）
gravity = 0.3     # 重力の強さ
ground_y = 80     # 地面の高さ (= 立ってるときのY)

tree_x = 120
tree2_x = 130

pyxel.init(160, 120)

def update():
    global player_x, player_y, vy,base_speed,turbo_speed,eye_x,tree_x,test,tree2_x
    
    #テスト用
    if pyxel.btnp(pyxel.KEY_W):
        test += 1

    if pyxel.btnp(pyxel.KEY_Q):
        test -= 1

    #スペースで速度を変える
    if pyxel.btn(pyxel.KEY_SHIFT):
        speed = turbo_speed
    else:
        speed = base_speed

    # ← →
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        tree_x -= speed
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        tree_x += speed

    #画面端のワープ
    if tree_x <= -10 :
        tree_x = 169
        pass

    if tree_x >= 170 :
        tree_x = 0
        pass

    # ← →
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        tree2_x -= speed*1.5
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        tree2_x += speed*1.5

    #画面端のワープ
    if tree2_x <= -10 :
        tree2_x = 219
        pass

    if tree2_x >= 220 :
        tree2_x = 0
        pass

    # スペースでジャンプ開始
    # 条件: 地面にいるときだけジャンプできる（2段ジャンプ防止）
    if pyxel.btnp(pyxel.KEY_SPACE):
        if player_y >= ground_y:
            vy = -5      # 上向きに初速を与える（マイナス方向が上）
    
    # 重力を速度に足す（落ちるほど速くなる）
    vy += gravity

    # 位置を更新
    player_y += vy

    # 地面より下に落ちたら、地面で止める
    if player_y > ground_y:
        player_y = ground_y
        vy = 0  # 着地したので停止
    
    #目の位置を揃える
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        eye_x = 4
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        eye_x = 2

def draw():
    pyxel.cls(0)

    # プレイヤーを描画（四角）
    pyxel.rect(player_x, player_y, player_size,player_size,3)
    # プレイヤーを描画（目）
    pyxel.rect(player_x+eye_x, player_y+1, 1,3,6)
    pyxel.rect(player_x+eye_x+2, player_y+1, 1,3,6)

    # 地面のライン
    pyxel.line(0, ground_y + 8, 160, ground_y + 8, 7)

    pyxel.rect(tree_x,68, 4,20,4)
    pyxel.circ(tree_x+1,60, 10,11)
    
    pyxel.rect(tree2_x,75, 2,13,4)
    pyxel.circ(tree2_x,70, 5,11)
    
    pyxel.rect(tree2_x-50,75, 2,13,4)
    pyxel.circ(tree2_x-50,70, 5,11)
    
pyxel.run(update, draw)
