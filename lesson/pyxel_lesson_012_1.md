# 第12回（1/3）：敵の基本の動き

**全3回の1回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- まっすぐ進む敵を出す
- 往復する敵を出す
- ランダムに動く敵を出す

---

## 📚 学習内容

### 1. 基本的な敵の動きパターン

#### まっすぐ移動する敵

```python
import pyxel

enemy = {"x": 80, "y": 60, "dx": 1, "dy": 0.5}

def init():
    pyxel.init(160, 120, title="Straight Enemy Test")
    pyxel.run(update, draw)

def update():
    enemy["x"] += enemy["dx"]
    enemy["y"] += enemy["dy"]

    # 画面外→反対側から出現
    if enemy["x"] < -10:
        enemy["x"] = 170
    elif enemy["x"] > 170:
        enemy["x"] = -10

    if enemy["y"] < -10:
        enemy["y"] = 130
    elif enemy["y"] > 130:
        enemy["y"] = -10

def draw():
    pyxel.cls(0)
    pyxel.circ(enemy["x"], enemy["y"], 5, 8)
    pyxel.text(10, 10, "Straight moving enemy", 7)

init()
```

#### 往復移動する敵

```python
import pyxel

enemy = {"x": 80, "y": 60, "dx": 2, "dy": 1}

def init():
    pyxel.init(160, 120, title="Bouncing Enemy Test")
    pyxel.run(update, draw)

def update():
    enemy["x"] += enemy["dx"]
    enemy["y"] += enemy["dy"]

    if enemy["x"] <= 5 or enemy["x"] >= 155:
        enemy["dx"] = -enemy["dx"]
    if enemy["y"] <= 5 or enemy["y"] >= 115:
        enemy["dy"] = -enemy["dy"]

def draw():
    pyxel.cls(0)
    pyxel.rect(enemy["x"] - 5, enemy["y"] - 5, 10, 10, 9)
    pyxel.text(10, 10, "Bouncing enemy", 7)

init()
```

#### ランダムに動く敵

```python
import pyxel

enemy = {"x": 80, "y": 60, "dx": 0.0, "dy": 0.0, "timer": 0, "max_speed": 2}

def init():
    pyxel.init(160, 120, title="Random Enemy Test")
    pyxel.run(update, draw)

def update():
    enemy["timer"] += 1
    if enemy["timer"] >= 60:
        enemy["dx"] = pyxel.rndf(-enemy["max_speed"], enemy["max_speed"])
        enemy["dy"] = pyxel.rndf(-enemy["max_speed"], enemy["max_speed"])
        enemy["timer"] = 0

    enemy["x"] += enemy["dx"]
    enemy["y"] += enemy["dy"]
    enemy["x"] = max(5, min(155, enemy["x"]))
    enemy["y"] = max(5, min(115, enemy["y"]))

def draw():
    pyxel.cls(0)
    pyxel.tri(enemy["x"], enemy["y"] - 5, enemy["x"] - 5, enemy["y"] + 5, enemy["x"] + 5, enemy["y"] + 5, 11)
    pyxel.text(10, 10, "Random moving enemy", 7)

init()
```

---

## この回の確認

- まっすぐ進む敵がいる
- 端で往復する敵がいる
- 動きがランダムな敵がいる

次回は「追跡と、複数の敵」です。ファイルは `pyxel_lesson_012_2.md` です。

### AI に聞いてみよう

「敵が画面の端で進む向きを反対にする書き方を教えて」と聞いてみよう。
