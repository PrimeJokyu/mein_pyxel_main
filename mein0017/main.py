import pyxel
#コメントができる
pyxel.init(200,200)


def update():
    pass

def draw():
    pyxel.cls(0)
    pyxel.text(24,24,"Hello! My name is kazuki",7)
pyxel.run(update,draw)




