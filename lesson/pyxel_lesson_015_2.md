# 第15回（2/3）：遊べるところまで動かす

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- タイトルからプレイへ進める
- 動く敵を1体出す
- 音かスコアを1つ入れる

前回のファイル: `pyxel_lesson_015_1.md`

---

サンプルは全部を写さなくてよいです。自分のテーマに必要な部分だけ使います。

## 🛠️ 実装サンプル：基本ゲーム構造

### ゲーム状態管理

```python
import pyxel
import random
import math

state = "title"  # "title", "game", "gameover"
player_x, player_y, player_life = 80, 60, 3
score, timer = 0, 1800
enemies, items = [], []

pyxel.init(160, 120, title="My Mini Game")
pyxel.sound(0).set("c3e3g3c4", "t", "7", "n", 10)
pyxel.sound(1).set("f2d2a2f2", "s", "6", "n", 20)

def spawn_enemy():
    enemies.append({
        'x': random.randint(0, 160),
        'y': random.randint(0, 60),
        'dx': random.choice([-1, 1]),
        'dy': random.randint(1, 2),
        'type': random.choice(['chaser', 'patrol'])
    })

def reset_game():
    global player_x, player_y, player_life, score, timer, enemies, items
    player_x, player_y, player_life = 80, 60, 3
    score, timer = 0, 1800
    enemies, items = [], []
    for _ in range(3):
        spawn_enemy()

def update():
    global state, player_x, player_y, player_life, score, timer
    if state == "title":
        if pyxel.btnp(pyxel.KEY_SPACE):
            state = "game"
            reset_game()
        return

    if state == "game":
        # player move
        if pyxel.btn(pyxel.KEY_LEFT):
            player_x = max(8, player_x - 2)
        if pyxel.btn(pyxel.KEY_RIGHT):
            player_x = min(152, player_x + 2)
        if pyxel.btn(pyxel.KEY_UP):
            player_y = max(8, player_y - 2)
        if pyxel.btn(pyxel.KEY_DOWN):
            player_y = min(112, player_y + 2)

        update_enemies()
        update_items()
        check_collisions()

        timer -= 1
        if timer <= 0 or player_life <= 0:
            state = "gameover"
        return

    if state == "gameover":
        if pyxel.btnp(pyxel.KEY_SPACE):
            state = "title"

def draw():
    pyxel.cls(1)
    if state == "title":
        pyxel.text(60, 40, "MY MINI GAME", 7)
        pyxel.text(55, 60, "Press SPACE to Start", 6)
        pyxel.text(45, 80, "Arrow Keys: Move", 5)
        pyxel.text(45, 90, "Avoid enemies, Get items!", 5)
        return

    if state == "game":
        pyxel.circfill(player_x, player_y, 6, 12)
        pyxel.circ(player_x, player_y, 6, 1)
        for enemy in enemies:
            color = 8 if enemy['type'] == 'chaser' else 4
            pyxel.circfill(int(enemy['x']), int(enemy['y']), 5, color)
        for item in items:
            if item['type'] == 'coin':
                pyxel.circfill(int(item['x']), int(item['y']), 3, 10)
            elif item['type'] == 'gem':
                pyxel.rectfill(int(item['x'])-2, int(item['y'])-2, 4, 4, 14)
            elif item['type'] == 'star':
                pyxel.pset(int(item['x']), int(item['y'])-3, 7)
                pyxel.pset(int(item['x'])-2, int(item['y'])+1, 7)
                pyxel.pset(int(item['x'])+2, int(item['y'])+1, 7)
        pyxel.text(5, 5, f"Score: {score}", 7)
        pyxel.text(5, 15, f"Life: {player_life}", 7)
        pyxel.text(100, 5, f"Time: {timer//60}", 7)
        return

    if state == "gameover":
        pyxel.text(65, 40, "GAME OVER", 8)
        pyxel.text(55, 60, f"Final Score: {score}", 7)
        pyxel.text(50, 80, "Press SPACE to Return", 6)

pyxel.run(update, draw)
```

---

## 🎵 サウンド実装のコツ

### 効果音パターン

```python
# アイテム取得音（明るい音）
pyxel.sound(0).set("c4e4g4c5", "t", "7", "n", 10)

# ダメージ音（低い音）
pyxel.sound(1).set("f2d2a1f2", "s", "6", "n", 20)

# ゲームオーバー音（悲しい音）
pyxel.sound(2).set("c4a3f3d3", "t", "5", "n", 30)

# レベルクリア音（華やかな音）
pyxel.sound(3).set("c4d4e4f4g4a4b4c5", "t", "7", "n", 5)
```

### BGM 実装例

```python
# シンプルなループBGM
pyxel.sound(0).set("c3c3g3g3a3a3g3f3f3e3e3d3d3c3", "t", "6", "n", 8)

def update():
    # BGMのループ再生
    if not pyxel.play_pos(0):  # チャンネル0で何も再生していない場合
        pyxel.play(0, 0, loop=True)
```

---

## 👾 敵の動きパターン集

### 基本パターン

```python
# 1. 直線移動
enemy['x'] += enemy['dx']
enemy['y'] += enemy['dy']

# 2. 跳ね返り移動
enemy['x'] += enemy['dx']
if enemy['x'] <= 0 or enemy['x'] >= 160:
    enemy['dx'] = -enemy['dx']

# 3. プレイヤー追跡
if enemy['x'] < player_x:
    enemy['x'] += 1
elif enemy['x'] > player_x:
    enemy['x'] -= 1

# 4. ランダム移動
if random.randint(1, 30) == 1:  # 1/30の確率で方向変更
    enemy['dx'] = random.choice([-2, -1, 0, 1, 2])
    enemy['dy'] = random.choice([-2, -1, 0, 1, 2])

# 5. 円運動
enemy['angle'] += 0.1
enemy['x'] = center_x + math.cos(enemy['angle']) * radius
enemy['y'] = center_y + math.sin(enemy['angle']) * radius
```

---

## 📊 データ管理のテクニック

### スコアシステム

```python
score_state = {"score": 0, "multiplier": 1, "combo": 0}

def add_score(points, item_type="normal"):
    s = score_state
    base_points = points * s["multiplier"]
    if item_type == "combo":
        s["combo"] += 1
        base_points *= s["combo"]
    else:
        s["combo"] = 0
    s["score"] += base_points
    if s["score"] > 1000:
        s["multiplier"] = 2
```

### 統計情報

```python
stats = {"items_collected": 0, "enemies_avoided": 0, "time_survived": 0, "max_combo": 0}

def stats_update():
    stats["time_survived"] += 1

def show_results():
    pyxel.text(10, 40, f"Items: {stats['items_collected']}", 7)
    pyxel.text(10, 50, f"Time: {stats['time_survived']//60}s", 7)
    pyxel.text(10, 60, f"Max Combo: {stats['max_combo']}", 7)
```

---

---

## この回の確認

- プレイ画面でキャラが動く
- 敵が1体動く
- 音かスコアのどちらかがある

次回は「整えて発表する」です。ファイルは `pyxel_lesson_015_3.md` です。

### AI に聞いてみよう

「タイトルでスペースを押すとプレイが始まる最小のコードを教えて」と聞いてみよう。
