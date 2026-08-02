import pyxel
#あいうえお
pyxel.init(100,100)
def update():
    pass
def draw():
    pyxel.cls(8)
    pyxel.rect(10,10,5,5,9)
    pyxel.rectb(10,10,5,5,9)
    pyxel.circ(10,10,5,9)
    pyxel.circb(10,10,5,9)
    pyxel.tri(20,20,20,20,20,20,5)
    pyxel.trib(20,20,20,20,20,20,5)
    

pyxel.run(update,draw)
