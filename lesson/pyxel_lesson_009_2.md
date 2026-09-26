# 第9回（2/3）：ランダム生成と当たり判定

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 前半で、ランダムに図形を出す
- 後半で、取るとスコアが増える動きを作る
- プレイヤーをキーで動かす

前回のファイル: `pyxel_lesson_009_1.md`

---

前半は課題Aです。課題Aが動いてから課題Bに進みます。

## 💻 Part 2: プログラミング実技検定（45 分）

### 課題 A: ランダム生成システム（15 分）

#### 課題内容

ランダムな位置に図形が定期的に出現し、画面に一定数まで表示されるシステムを作成してください。

#### 必須要素

1. **定期生成**: 3 秒（180 フレーム）ごとに円を出す
2. **ランダム**: 位置と色はランダム
3. **上限**: 同時に最大 3 個まで

#### 実装のヒント

```python
import pyxel

circles = []
spawn_timer = 0
MAX_CIRCLES = 3

pyxel.init(160, 120)

def update():
    global spawn_timer

    spawn_timer += 1

    # 3秒ごとに新しい円を生成
    if spawn_timer >= 180:
        spawn_timer = 0
        spawn_circle()

    # 円の数が上限を超えたら古いものを削除
    while len(circles) > MAX_CIRCLES:
        circles.pop(0)  # 最初の要素（最古）を削除

def spawn_circle():
    circle = {
        "x": pyxel.rndi(10, 150),
        "y": pyxel.rndi(10, 110),
        "color": pyxel.rndi(8, 15),
        "size": pyxel.rndi(5, 15)
    }
    circles.append(circle)

def draw():
    pyxel.cls(1)

    # 全ての円を描画
    for circle in circles:
        pyxel.circ(circle["x"], circle["y"], circle["size"], circle["color"])

    # 情報表示
    pyxel.text(5, 5, f"Circles: {len(circles)}", 7)
    pyxel.text(5, 15, f"Timer: {spawn_timer}", 7)

pyxel.run(update, draw)
```

#### チェックポイント

- [ ] 180 フレームごとに円が出る
- [ ] 位置と色がランダム
- [ ] 同時に 3 個まで

#### AI Tip

- 「AI に『ランダムな位置に図形を出す方法（Pyxel）』を聞いてみよう」

---

### 課題 B: 当たり判定ミニゲーム（15 分）

#### 課題内容

プレイヤーキャラクターがアイテムを収集するシンプルなゲームシステムを作成してください。

#### 必須要素

1. **プレイヤー**: 矢印キーで動く四角形
2. **アイテム**: 定期的に生成されて上から落ちる円
3. **当たり判定**: 取ったらスコア+1（表示は任意）

#### 実装のヒント

```python
import pyxel

# プレイヤー
player = {"x": 80, "y": 100, "w": 12, "h": 12}

# ゲーム状態
items = []
score = 0
spawn_timer = 0

pyxel.init(160, 120)

def update():
    global spawn_timer, score

    # プレイヤー移動
    if pyxel.btn(pyxel.KEY_LEFT) and player["x"] > 0:
        player["x"] -= 2
    if pyxel.btn(pyxel.KEY_RIGHT) and player["x"] < 148:
        player["x"] += 2
    if pyxel.btn(pyxel.KEY_UP) and player["y"] > 0:
        player["y"] -= 2
    if pyxel.btn(pyxel.KEY_DOWN) and player["y"] < 108:
        player["y"] += 2

    # アイテム生成
    spawn_timer += 1
    if spawn_timer >= 60:  # 1秒ごと
        spawn_timer = 0
        spawn_item()

    # アイテム更新
    for item in items[:]:
        item["y"] += item["speed"]
        if item["y"] > 120:
            items.remove(item)

    # 当たり判定
    check_collisions()

def spawn_item():
    item = {
        "x": pyxel.rndi(5, 155),
        "y": -5,
        "radius": 6,
        "speed": pyxel.rndf(1, 3),
        "color": pyxel.rndi(9, 15)
    }
    items.append(item)

def check_collisions():
    global score

    player_center_x = player["x"] + player["w"] // 2
    player_center_y = player["y"] + player["h"] // 2

    for item in items[:]:
        # 距離計算（円と矩形の簡易当たり判定）
        dx = abs(item["x"] - player_center_x)
        dy = abs(item["y"] - player_center_y)

        if dx < player["w"]//2 + item["radius"] and dy < player["h"]//2 + item["radius"]:
            score += 1
            items.remove(item)

def draw():
    pyxel.cls(0)

    # プレイヤー描画
    pyxel.rect(player["x"], player["y"], player["w"], player["h"], 11)

    # アイテム描画
    for item in items:
        pyxel.circ(item["x"], item["y"], item["radius"], item["color"])

    # スコア表示
    pyxel.text(5, 5, f"Score: {score}", 7)

pyxel.run(update, draw)
```

#### チェックポイント

- [ ] 矢印キーでプレイヤーが動く
- [ ] アイテムが落ちてくる
- [ ] 取るとスコアが増える

#### AI Tip

- 「AI に『四角形と円の当たり判定を簡単にする方法』を聞いてみよう」

---

---

## この回の確認

- 課題Aで円がランダムに出る
- 課題Bでアイテムを取れる
- スコアの数字が変わる

次回は「画面の切り替え」です。ファイルは `pyxel_lesson_009_3.md` です。
