from pyxel import cls
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

    pyxel.init(160,120)

def update():
    pass

def drow():
    pyxel.cls(12)#青い背景

    #顔（ピーチ色の円）

    

pyxel.run(update,draw)
