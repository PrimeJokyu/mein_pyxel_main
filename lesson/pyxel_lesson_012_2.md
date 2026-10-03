# 第12回（2/3）：追跡と、複数の敵

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- プレイヤーに近づく敵を出す
- 種類の違う敵をリストで持つ
- プレイヤーをキーで動かす

前回のファイル: `pyxel_lesson_012_1.md`

---

### 2. AI で追跡する敵を作ろう！

#### 基本的な追跡 AI

```python
import pyxel
import math

player = {"x": 80, "y": 60, "speed": 2}
enemy = {"x": 20, "y": 20, "speed": 0.8}

def init():
    pyxel.init(160, 120, title="Chasing Enemy Test")
    pyxel.run(update, draw)

def update():
    # プレイヤー移動
    if pyxel.btn(pyxel.KEY_LEFT):
        player["x"] -= player["speed"]
    if pyxel.btn(pyxel.KEY_RIGHT):
        player["x"] += player["speed"]
    if pyxel.btn(pyxel.KEY_UP):
        player["y"] -= player["speed"]
    if pyxel.btn(pyxel.KEY_DOWN):
        player["y"] += player["speed"]

    player["x"] = max(5, min(155, player["x"]))
    player["y"] = max(5, min(115, player["y"]))

    # 追跡
    dx = player["x"] - enemy["x"]
    dy = player["y"] - enemy["y"]
    dist = math.sqrt(dx * dx + dy * dy)
    if dist > 0:
        enemy["x"] += (dx / dist) * enemy["speed"]
        enemy["y"] += (dy / dist) * enemy["speed"]

def draw():
    pyxel.cls(0)
    pyxel.rect(player["x"] - 5, player["y"] - 5, 10, 10, 7)
    pyxel.circ(enemy["x"], enemy["y"], 6, 8)
    pyxel.pix(enemy["x"] - 2, enemy["y"] - 2, 0)
    pyxel.pix(enemy["x"] + 2, enemy["y"] - 2, 0)
    pyxel.text(10, 10, "Use arrows to move", 7)
    pyxel.text(10, 20, "Enemy chases you!", 8)

init()
```

### 3. 複数の敵の管理

#### 異なるタイプの敵を同時に管理

```python
import pyxel
import math

player = {"x": 80, "y": 60, "speed": 2}
enemies = [
    {"type": "straight", "x": 10, "y": 30, "dx": 1, "dy": 0},
    {"type": "bounce",   "x": 140, "y": 90, "dx": -1.5, "dy": 1},
    {"type": "random",   "x": 50, "y": 20, "dx": 0.0, "dy": 0.0, "timer": 0, "max_speed": 2},
    {"type": "chase",    "x": 120, "y": 30, "speed": 0.8},
]

def init():
    pyxel.init(160, 120, title="Multiple Enemies")
    pyxel.run(update, draw)

def update():
    # player
    if pyxel.btn(pyxel.KEY_LEFT):
        player["x"] -= player["speed"]
    if pyxel.btn(pyxel.KEY_RIGHT):
        player["x"] += player["speed"]
    if pyxel.btn(pyxel.KEY_UP):
        player["y"] -= player["speed"]
    if pyxel.btn(pyxel.KEY_DOWN):
        player["y"] += player["speed"]
    player["x"] = max(5, min(155, player["x"]))
    player["y"] = max(5, min(115, player["y"]))

    # enemies
    for e in enemies:
        if e["type"] == "straight":
            e["x"] += e["dx"]; e["y"] += e["dy"]
            if e["x"] < -10: e["x"] = 170
            elif e["x"] > 170: e["x"] = -10
            if e["y"] < -10: e["y"] = 130
            elif e["y"] > 130: e["y"] = -10
        elif e["type"] == "bounce":
            e["x"] += e["dx"]; e["y"] += e["dy"]
            if e["x"] <= 5 or e["x"] >= 155: e["dx"] = -e["dx"]
            if e["y"] <= 5 or e["y"] >= 115: e["dy"] = -e["dy"]
        elif e["type"] == "random":
            e["timer"] += 1
            if e["timer"] >= 60:
                e["dx"] = pyxel.rndf(-e["max_speed"], e["max_speed"])
                e["dy"] = pyxel.rndf(-e["max_speed"], e["max_speed"])
                e["timer"] = 0
            e["x"] += e["dx"]; e["y"] += e["dy"]
            e["x"] = max(5, min(155, e["x"]))
            e["y"] = max(5, min(115, e["y"]))
        elif e["type"] == "chase":
            dx = player["x"] - e["x"]; dy = player["y"] - e["y"]
            d = math.sqrt(dx * dx + dy * dy)
            if d > 0:
                e["x"] += (dx / d) * e["speed"]; e["y"] += (dy / d) * e["speed"]

def draw():
    pyxel.cls(0)
    pyxel.rect(player["x"] - 5, player["y"] - 5, 10, 10, 7)
    for e in enemies:
        if e["type"] == "straight":
            pyxel.circ(e["x"], e["y"], 5, 8)
        elif e["type"] == "bounce":
            pyxel.rect(e["x"] - 5, e["y"] - 5, 10, 10, 9)
        elif e["type"] == "random":
            pyxel.tri(e["x"], e["y"] - 5, e["x"] - 5, e["y"] + 5, e["x"] + 5, e["y"] + 5, 11)
        elif e["type"] == "chase":
            pyxel.circ(e["x"], e["y"], 6, 10)
    pyxel.text(5, 5, "Player vs Multiple Enemies", 7)
    pyxel.text(5, 110, "Use arrow keys to move", 13)

init()
```

---

---

## この回の確認

- 敵がプレイヤーの方へ動く
- 敵が2体以上いる
- 種類で色か形が違う

次回は「色んな敵を1つにまとめる」です。ファイルは `pyxel_lesson_012_3.md` です。
