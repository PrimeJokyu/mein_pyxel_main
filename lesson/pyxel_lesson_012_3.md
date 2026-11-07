# 第12回（3/3）：色んな敵を1つにまとめる

**全3回の3回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 前の動きを1つのプログラムにまとめる
- プレイヤーが避けられる
- 種類が画面で分かる

前回のファイル: `pyxel_lesson_012_2.md`

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

---

## この回の確認

- 敵が複数動く
- プレイヤーが動く
- 種類が2つ以上分かる

次回は「距離でスコアを増やす」です。ファイルは `pyxel_lesson_013_1.md` です。
