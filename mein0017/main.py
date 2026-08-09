import pyxel

# 変数は一番上に書く！
name = "GUNYA KAZUKI"
age = 12
hobby = "game"

# ▶️ ゲーム開始
pyxel.init(160, 160)

# 🔄 更新処理（ゲームのルール・動きを管理）
def update():
    pass # 何もしない

# 🎨 描画処理（画面に絵を描く）
def draw():
    pyxel.cls(1) 
    pyxel.text(5,15,"My Profile Card",7)
    pyxel.text(8,35,  f"name:  {name}",7)
    pyxel.text(8,45,  f"Age:   {age}",7)
    pyxel.text(8,55,  f"Hobby:  {hobby}",7)
 

pyxel.run(update, draw)