import pyxel
pyxel.init(160, 120)
pyxel.load("my_game.pyxres")

def update():
    pass

def draw():
    pyxel.cls(1)

    pyxel.blt(
        50, 50,  # 描画位置
        0,       # 画像バンク(IMAGE 0)
        0, 0,    # リソース内の座標
        16, 16,  # スプライトサイズ
        0        # 透明色(0=黒)
    )

pyxel.run(update, draw)
