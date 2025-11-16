import pyxel
pyxel.init (160,120)
def updete():
    pass
def draw():
    pyxel.cls(3)
    pyxel.rect(30,40,40,30,8)
    pyxel.circ(100,70,15,12)
    pyxel.tri(120,30,130,50,140,30,10)
    pyxel.text(10,10,"yamamoto",7)
pyxel.run(updete,draw)