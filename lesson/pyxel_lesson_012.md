# 【第 12 回】敵の動きパターン制作

## 🤖 今日の目標

敵キャラクターに色々な動き方をさせて、ゲームを面白くしよう！

- 敵キャラを作る
- プレイヤーを追いかける敵を実装する
- 複数の敵を同時に管理する

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

## 🎯 実習課題：「色んな敵テスト」を作ろう

### 作るもの

- 3 種類の異なる動きをする敵を配置
- プレイヤー（矢印キーで操作）
- プレイヤーを追いかける敵
- 一定時間で動きパターンが変わる敵
- 敵とプレイヤーの距離を画面に表示

### 完成コード例

import pyxel
import math

player = {"x": 100, "y": 75, "speed": 2}
enemy1 = {"x": 50, "y": 30, "dx": 1, "dy": 0}
enemy2 = {"x": 150, "y": 120, "speed": 0.7}
enemy3 = {"x": 30, "y": 100, "dx": 0, "dy": 1, "timer": 0, "pattern": 0}
distances = []

def init():
pyxel.init(200, 150, title="Enemy Pattern Test")
pyxel.run(update, draw)

def update():
global distances # player
if pyxel.btn(pyxel.KEY_LEFT):
player["x"] -= player["speed"]
if pyxel.btn(pyxel.KEY_RIGHT):
player["x"] += player["speed"]
if pyxel.btn(pyxel.KEY_UP):
player["y"] -= player["speed"]
if pyxel.btn(pyxel.KEY_DOWN):
player["y"] += player["speed"]
player["x"] = max(5, min(195, player["x"]))
player["y"] = max(5, min(145, player["y"]))

    # enemy1 bounce
    enemy1["x"] += enemy1["dx"]
    if enemy1["x"] <= 10 or enemy1["x"] >= 190:
        enemy1["dx"] = -enemy1["dx"]

    # enemy2 chase
    dx = player["x"] - enemy2["x"]
    dy = player["y"] - enemy2["y"]
    distance = math.sqrt(dx * dx + dy * dy)
    if distance > 0:
        enemy2["x"] += (dx / distance) * enemy2["speed"]
        enemy2["y"] += (dy / distance) * enemy2["speed"]

    # enemy3 pattern change
    enemy3["timer"] += 1
    if enemy3["timer"] >= 120:
        enemy3["timer"] = 0
        enemy3["pattern"] = (enemy3["pattern"] + 1) % 3
        if enemy3["pattern"] == 0:
            enemy3["dx"], enemy3["dy"] = 0, 1
        elif enemy3["pattern"] == 1:
            enemy3["dx"], enemy3["dy"] = 1, 0
        else:
            enemy3["dx"], enemy3["dy"] = 1, 1
    enemy3["x"] += enemy3["dx"]
    enemy3["y"] += enemy3["dy"]
    if enemy3["x"] <= 5 or enemy3["x"] >= 195:
        enemy3["dx"] = -enemy3["dx"]
    if enemy3["y"] <= 5 or enemy3["y"] >= 145:
        enemy3["dy"] = -enemy3["dy"]

    # distances
    distances = []
    for e in (enemy1, enemy2, enemy3):
        dx = player["x"] - e["x"]; dy = player["y"] - e["y"]
        distances.append(int(math.sqrt(dx * dx + dy * dy)))

def draw():
pyxel.cls(1)
pyxel.rect(player["x"] - 5, player["y"] - 5, 10, 10, 7)
pyxel.rect(enemy1["x"] - 6, enemy1["y"] - 6, 12, 12, 8)
pyxel.circ(enemy2["x"], enemy2["y"], 7, 10)
pyxel.tri(enemy3["x"], enemy3["y"] - 6, enemy3["x"] - 6, enemy3["y"] + 6, enemy3["x"] + 6, enemy3["y"] + 6, 12)

    pyxel.text(5, 5, "Enemy Pattern Test", 7)
    pyxel.text(5, 15, "Use arrow keys to move", 13)
    pyxel.text(5, 130, f"Distances:", 7)
    for i, dist in enumerate(distances):
        pyxel.text(5, 140 + i * 8, f"Enemy{i+1}: {dist}", 7)
    pyxel.text(120, 5, "Red: Bounce", 8)
    pyxel.text(120, 15, "Pink: Chase", 10)
    pyxel.text(120, 25, "Light Blue: Pattern", 12)

init()

```

### チャレンジ課題

1. **ガード AI**: プレイヤーの前に回り込む敵
2. **群れ行動**: 複数の敵が協力して動く
3. **難易度調整**: 時間とともに敵の速度や数が増加
4. **特殊攻撃**: 一定距離に近づくと特別な行動をする敵

---

## 💡 今日のポイント

### 敵の動きパターンの基本

- **まっすぐ移動**: 一定方向に進む
- **往復移動**: 画面端で跳ね返る
- **ランダム移動**: 不規則な動き
```
