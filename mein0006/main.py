import pyxel
pyxel.init(160, 120)
def draw():
    pyxel.cls(13)
    pyxel.circb(80, 60, 60, 3)     # 枠だけ（bはborder）
def update():
    pass
pyxel.run(update, draw)
pyxel.cls(0)

import pyxel

# 変数の定義
bg_color = 1        # 背景色
face_x = 80         # 顔のX座標
face_y = 60         # 顔のY座標
face_color = 15     # 顔の色

pyxel.init(160, 120)

def update():
    pass

def draw():
    pyxel.cls(bg_color)  # 変数を使って背景色を設定

    # 変数を使って顔を描画
    pyxel.circfill(face_x, face_y, 20, face_color)
    pyxel.circb(face_x, face_y, 20, 0)



name = "悪魔"
age = 12
score = 1250
def draw():
pyxel.text(10, 10, f"名前: {name}", 1)
pyxel.text(10, 20, f"年齢: {age}歳", 1)
pyxel.text(10, 30, f"スコア: {score}点", 1)

