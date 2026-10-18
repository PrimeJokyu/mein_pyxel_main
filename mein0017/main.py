import pyxel

# 変数は一番上に書く！
name = "GUNYA KAZUKI"
age = 12
hobby = "game"
favorite_food = "udon"
favorite_subject = "math"
favorite_color = "blue"

# ▶️ ゲーム開始
pyxel.init(160, 160)

# 🔄 更新処理（ゲームのルール・動きを管理）
def update():
    pass # 何もしない

# 🎨 描画処理（画面に絵を描く）
def draw():
    pyxel.cls(1) 
    pyxel.rectb(2,2,156,156,7)
    pyxel.line(10,100,150,100,7)  # 線
    pyxel.circ(130,130,20,15)      # 顔
    pyxel.circb(130,130,20,0)      # 顔の輪郭
    pyxel.circ(123,125,3,0)        # 左目
    pyxel.circ(137,125,3,0)        # 右目
    pyxel.line(123,138,137,138,8)  # 口
    pyxel.text(5,15,"My Profile Card",7)
    pyxel.text(8,35,  f"name:  {name}",7)
    pyxel.text(8,45,  f"Age:   {age}",7)
    pyxel.text(8,55,  f"Hobby:  {hobby}",7)
    pyxel.text(8,65,  f"favorite_food:{favorite_food}",7)
    pyxel.text(8,75,  f"favorite_subject:{favorite_subject}",7)
    pyxel.text(8,85,  f"favorite_color:{favorite_color}",7)



pyxel.run(update, draw)