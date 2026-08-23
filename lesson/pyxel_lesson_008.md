# 第 8 回：当たり判定とゲーム状態管理

**～本格的なゲームの核心へ！インタラクションと状態遷移をマスターしよう～**

## 🎯 今日のゴール

- 多様な当たり判定アルゴリズムを実装できる
- ゲーム状態遷移システムを設計できる
- ゲームオーバー処理とリスタート機能を実装できる

---

## 🎯 1. 多様な当たり判定アルゴリズム

### 1-1. 矩形当たり判定

#### 基本的な実装

```python
def rect_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    """矩形同士の当たり判定（AABB: Axis-Aligned Bounding Box）"""
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)

# 使用例
player_rect = {"x": 80, "y": 60, "w": 16, "h": 16}
enemy_rect = {"x": 90, "y": 65, "w": 12, "h": 12}

if rect_collision(player_rect["x"], player_rect["y"], player_rect["w"], player_rect["h"],
                  enemy_rect["x"], enemy_rect["y"], enemy_rect["w"], enemy_rect["h"]):
    print("衝突!")
```

#### 辞書＋関数での実装（クラス不使用）

```python
import pyxel

def make_object(x, y, w, h):
    return {"x": x, "y": y, "w": w, "h": h}

def get_rect(obj):
    return (obj["x"], obj["y"], obj["w"], obj["h"])

def collides(obj_a, obj_b):
    x1, y1, w1, h1 = get_rect(obj_a)
    x2, y2, w2, h2 = get_rect(obj_b)
    return rect_collision(x1, y1, w1, h1, x2, y2, w2, h2)

def draw_debug_rect(obj, color=8):
    pyxel.rectb(obj["x"], obj["y"], obj["w"], obj["h"], color)

# 使用例
player = make_object(80, 60, 16, 16)
enemy = make_object(90, 65, 12, 12)

if collides(player, enemy):
    print("衝突検出！")
```

### 1-2. 円形当たり判定

#### 距離計算による実装

```python
import math

def circle_collision(x1, y1, r1, x2, y2, r2):
    """円同士の当たり判定"""
    # 中心間の距離を計算
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx * dx + dy * dy)

    # 半径の合計と比較
    return distance < (r1 + r2)

# 最適化版（平方根計算を避ける）
def circle_collision_optimized(x1, y1, r1, x2, y2, r2):
    """最適化された円形当たり判定"""
    dx = x2 - x1
    dy = y2 - y1
    distance_squared = dx * dx + dy * dy
    radius_sum_squared = (r1 + r2) * (r1 + r2)

    return distance_squared < radius_sum_squared

# 使用例
def update():
    # プレイヤー（円）と敵（円）の当たり判定
    if circle_collision(player_x, player_y, player_radius,
                       enemy_x, enemy_y, enemy_radius):
        # 衝突処理
        handle_collision()
```

### 1-3. 点と矩形の当たり判定

```python
def point_in_rect(px, py, rx, ry, rw, rh):
    """点が矩形内にあるかの判定"""
    return (rx <= px <= rx + rw and
            ry <= py <= ry + rh)

# マウスクリック判定での使用例
def update():
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y

        # ボタンがクリックされたか判定
        for button in ui_buttons:
            if point_in_rect(mouse_x, mouse_y,
                            button["x"], button["y"],
                            button["w"], button["h"]):
                button["action"]()  # ボタンのアクション実行
```

### 1-4. 高度な当たり判定：複合形状（クラス不使用）

```python
import pyxel

def make_complex_collider(x, y):
    return {
        "x": x,
        "y": y,
        "hit_boxes": [
            {"x": 0, "y": 0, "w": 16, "h": 8},   # 頭部
            {"x": 2, "y": 8, "w": 12, "h": 16},  # 胴体
            {"x": 4, "y": 24, "w": 8, "h": 8},   # 足部
        ],
    }

def collider_collides_point(col, px, py):
    for box in col["hit_boxes"]:
        abs_x = col["x"] + box["x"]
        abs_y = col["y"] + box["y"]
        if point_in_rect(px, py, abs_x, abs_y, box["w"], box["h"]):
            return True
    return False

def collider_collides_rect(col, rx, ry, rw, rh):
    for box in col["hit_boxes"]:
        abs_x = col["x"] + box["x"]
        abs_y = col["y"] + box["y"]
        if rect_collision(abs_x, abs_y, box["w"], box["h"], rx, ry, rw, rh):
            return True
    return False

def draw_collider_debug(col):
    for box in col["hit_boxes"]:
        abs_x = col["x"] + box["x"]
        abs_y = col["y"] + box["y"]
        pyxel.rectb(abs_x, abs_y, box["w"], box["h"], 8)
```

---

## 🎮 2. ゲーム状態管理システム

### 2-1. 基本的な状態管理（global不使用）

ゲームの進行（タイトル、プレイ中、一時停止、ゲームオーバーなど）を「状態（ステート）」として管理します。
Pythonの `global` キーワードを使わず、状態をひとつの**辞書（dict）**にまとめて管理するのが Pyxel でのおすすめの方法です。

```python
import pyxel

# ゲーム状態の定義（定数）
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3
STATE_RESULT = 4

# ゲーム全体の状態を辞書で管理
game_state = {
    "current": STATE_TITLE,
    "timer": 0
}

def update():
    game_state["timer"] += 1

    if game_state["current"] == STATE_TITLE:
        update_title()
    elif game_state["current"] == STATE_PLAYING:
        update_playing()
    elif game_state["current"] == STATE_PAUSED:
        update_paused()
    elif game_state["current"] == STATE_GAME_OVER:
        update_game_over()
    elif game_state["current"] == STATE_RESULT:
        update_result()

def draw():
    if game_state["current"] == STATE_TITLE:
        draw_title()
    elif game_state["current"] == STATE_PLAYING:
        draw_playing()
    elif game_state["current"] == STATE_PAUSED:
        draw_paused()
    elif game_state["current"] == STATE_GAME_OVER:
        draw_game_over()
    elif game_state["current"] == STATE_RESULT:
        draw_result()

def change_state(new_state):
    """状態を変更する関数"""
    game_state["current"] = new_state
    game_state["timer"] = 0  # タイマーリセット
```

### 2-2. 各状態の実装

#### タイトル画面

```python
def update_title():
    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        change_state(STATE_PLAYING)
        initialize_game()  # ゲーム初期化

def draw_title():
    pyxel.cls(1)

    # タイトルロゴ
    title_text = "COLLECTOR CHALLENGE"
    text_width = len(title_text) * 4
    x = (160 - text_width) // 2
    pyxel.text(x, 40, title_text, 14)

    # 点滅する開始指示（timerを利用）
    if (game_state["timer"] // 30) % 2:  # 0.5秒ごとに点滅
        pyxel.text(45, 80, "PRESS SPACE TO START", 7)

    # 背景の演出
    for i in range(10):
        x = (game_state["timer"] + i * 16) % 180 - 10
        y = 20 + i * 8
        pyxel.pix(x, y, 12)
```

#### ゲームプレイ画面

```python
# ゲームデータも辞書で管理
game_data = {
    "player": {"x": 80, "y": 100, "w": 12, "h": 12, "score": 0, "lives": 3},
    "items": [],
    "enemies": []
}

def initialize_game():
    """ゲーム開始時の初期化"""
    game_data["player"] = {"x": 80, "y": 100, "w": 12, "h": 12, "score": 0, "lives": 3}
    game_data["items"].clear()
    game_data["enemies"].clear()

def update_playing():
    player = game_data["player"]

    # プレイヤー操作
    if pyxel.btn(pyxel.KEY_LEFT) and player["x"] > 0:
        player["x"] -= 2
    if pyxel.btn(pyxel.KEY_RIGHT) and player["x"] < 148:
        player["x"] += 2
    if pyxel.btn(pyxel.KEY_UP) and player["y"] > 0:
        player["y"] -= 2
    if pyxel.btn(pyxel.KEY_DOWN) and player["y"] < 108:
        player["y"] += 2

    # ポーズ機能
    if pyxel.btnp(pyxel.KEY_P):
        change_state(STATE_PAUSED)

    # アイテムと敵の定期生成
    if game_state["timer"] % 60 == 0:  # 1秒ごと
        spawn_item()
    if game_state["timer"] % 90 == 0:  # 1.5秒ごと
        spawn_enemy()

    # オブジェクト更新と当たり判定
    update_game_objects()

    # ゲームオーバー判定
    if player["lives"] <= 0:
        change_state(STATE_GAME_OVER)

def draw_playing():
    pyxel.cls(0)
    player = game_data["player"]

    # プレイヤー描画
    pyxel.rect(player["x"], player["y"], player["w"], player["h"], 11)

    # アイテム描画
    for item in game_data["items"]:
        pyxel.circ(item["x"], item["y"], item["r"], item["color"])

    # 敵描画
    for enemy in game_data["enemies"]:
        pyxel.rect(enemy["x"], enemy["y"], enemy["w"], enemy["h"], 8)

    # UI描画
    pyxel.text(5, 5, f"Score: {player['score']}", 7)
    pyxel.text(5, 15, f"Lives: {player['lives']}", 7)
    pyxel.text(120, 5, "P: Pause", 6)
```

#### ポーズ画面

```python
def update_paused():
    if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_SPACE):
        change_state(STATE_PLAYING)

    if pyxel.btnp(pyxel.KEY_Q):  # タイトルへ戻る
        change_state(STATE_TITLE)

def draw_paused():
    # プレイ画面の上に重ねて表示
    draw_playing()

    # 枠付きメッセージボックス
    pyxel.rect(40, 45, 80, 30, 0)
    pyxel.rectb(40, 45, 80, 30, 7)

    pyxel.text(65, 52, "PAUSED", 14)
    pyxel.text(45, 63, "P: Resume  Q: Quit", 7)
```

#### ゲームオーバー画面

```python
def update_game_over():
    # 切り替わってから少し待って操作を受け付ける（誤操作防止）
    if game_state["timer"] > 60:
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.KEY_SPACE):
            initialize_game()
            change_state(STATE_PLAYING)
        elif pyxel.btnp(pyxel.KEY_Q):
            change_state(STATE_TITLE)

def draw_game_over():
    pyxel.cls(8)  # 赤色の背景

    player = game_data["player"]

    # 文字の表示
    pyxel.text(60, 40, "GAME OVER", 7)
    pyxel.text(50, 55, f"Final Score: {player['score']}", 7)

    if game_state["timer"] > 60:
        if (game_state["timer"] // 30) % 2:
            pyxel.text(35, 80, "PRESS R TO RESTART", 10)
            pyxel.text(45, 92, "PRESS Q TO QUIT", 6)
```

---

## 🤖 AI活用Tips：当たり判定と状態遷移をAIに相談しよう！

> **AIに聞いてみよう！**
>
> プログラミングで迷ったら、ChatGPTなどのAIに以下のように質問してみよう！
>
> 💬 **質問プロンプト例：**
> - 「Pyxelで円と四角の当たり判定をする関数を `class` や `global` を使わずに書く方法を教えて！」
> - 「ゲームオーバー画面からタイトル画面に戻る時の変数の初期化のコツを教えて！」
> - 「ヒットボックス（当たり判定の範囲）を可視化して画面に表示するデバッグ機能のアイデアを出して！」

---

## 🕹️ 3. 実践：当たり判定と状態遷移を合わせたミニゲーム

ここまで学んだ「矩形当たり判定」と「状態遷移」を組み合わせた、完全に動くプログラム例です。

```python
import pyxel

# 状態定数
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

# ゲーム状態とデータ（辞書で一括管理）
game_state = {"current": STATE_TITLE, "timer": 0}
game_data = {
    "player": {"x": 76, "y": 90, "w": 8, "h": 8, "score": 0, "lives": 3},
    "enemy": {"x": 10, "y": 10, "w": 8, "h": 8, "speed": 1.5},
    "item": {"x": 80, "y": 40, "w": 6, "h": 6}
}

def rect_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    """矩形衝突判定"""
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)

def reset_game():
    """ゲームデータの初期化"""
    game_data["player"]["x"] = 76
    game_data["player"]["y"] = 90
    game_data["player"]["score"] = 0
    game_data["player"]["lives"] = 3
    game_data["enemy"]["x"] = 10
    game_data["enemy"]["y"] = 10

def update():
    game_state["timer"] += 1

    if game_state["current"] == STATE_TITLE:
        if pyxel.btnp(pyxel.KEY_SPACE):
            reset_game()
            game_state["current"] = STATE_PLAYING
            game_state["timer"] = 0

    elif game_state["current"] == STATE_PLAYING:
        p = game_data["player"]
        e = game_data["enemy"]
        i = game_data["item"]

        # プレイヤー移動
        if pyxel.btn(pyxel.KEY_LEFT) and p["x"] > 0: p["x"] -= 2
        if pyxel.btn(pyxel.KEY_RIGHT) and p["x"] < 152: p["x"] += 2
        if pyxel.btn(pyxel.KEY_UP) and p["y"] > 0: p["y"] -= 2
        if pyxel.btn(pyxel.KEY_DOWN) and p["y"] < 112: p["y"] += 2

        # 敵がプレイヤーを追いかける
        if e["x"] < p["x"]: e["x"] += e["speed"]
        elif e["x"] > p["x"]: e["x"] -= e["speed"]
        if e["y"] < p["y"]: e["y"] += e["speed"]
        elif e["y"] > p["y"]: e["y"] -= e["speed"]

        # アイテムゲット判定
        if rect_collision(p["x"], p["y"], p["w"], p["h"], i["x"], i["y"], i["w"], i["h"]):
            p["score"] += 10
            i["x"] = pyxel.rndi(10, 140)
            i["y"] = pyxel.rndi(10, 100)

        # 敵との衝突判定
        if rect_collision(p["x"], p["y"], p["w"], p["h"], e["x"], e["y"], e["w"], e["h"]):
            p["lives"] -= 1
            e["x"] = 10
            e["y"] = 10
            if p["lives"] <= 0:
                game_state["current"] = STATE_GAME_OVER
                game_state["timer"] = 0

    elif game_state["current"] == STATE_GAME_OVER:
        if game_state["timer"] > 30 and pyxel.btnp(pyxel.KEY_SPACE):
            game_state["current"] = STATE_TITLE
            game_state["timer"] = 0

def draw():
    pyxel.cls(0)

    if game_state["current"] == STATE_TITLE:
        pyxel.text(50, 50, "CATCH & DODGE", 10)
        if (game_state["timer"] // 30) % 2:
            pyxel.text(40, 80, "PRESS SPACE TO START", 7)

    elif game_state["current"] == STATE_PLAYING:
        p = game_data["player"]
        e = game_data["enemy"]
        i = game_data["item"]

        pyxel.rect(p["x"], p["y"], p["w"], p["h"], 11)  # プレイヤー（水色）
        pyxel.rect(e["x"], e["y"], e["w"], e["h"], 8)   # 敵（赤）
        pyxel.rect(i["x"], i["y"], i["w"], i["h"], 10)  # アイテム（黄色）

        pyxel.text(4, 4, f"SCORE: {p['score']}", 7)
        pyxel.text(120, 4, f"LIFE: {p['lives']}", 7)

    elif game_state["current"] == STATE_GAME_OVER:
        pyxel.text(60, 45, "GAME OVER", 8)
        pyxel.text(50, 60, f"SCORE: {game_data['player']['score']}", 7)
        if (game_state["timer"] // 30) % 2:
            pyxel.text(35, 85, "PRESS SPACE TO TITLE", 6)

pyxel.init(160, 120, title="State & Collision Demo")
pyxel.run(update, draw)
```

---

## 🏆 4. チェックポイント

### ✅ 当たり判定の確認
- [ ] 矩形（四角）同士の当たり判定ロジックを理解できている
- [ ] 円形や点判定など状況に応じた判定方法を選べる
- [ ] 判定領域（ヒットボックス）の位置を調整できる

### ✅ 状態管理の確認
- [ ] タイトル・プレイ・ゲームオーバーの状態を分けられる
- [ ] `global` キーワードを使わずに辞書で状態を管理できる
- [ ] キー入力や条件に応じてスムーズに画面遷移できる

### ✅ 動作確認
- [ ] タイトル画面でスペースキーを押すとゲームが始まる
- [ ] 敵に当たるとライフが減り、0でゲームオーバーになる
- [ ] ゲームオーバーから再度スタートできる

---

## 📝 5. まとめ

### 今日学んだこと
- **多様な当たり判定**: 矩形（AABB）、円形、点判定の仕組み
- **状態管理（ステートマシン）**: 画面ごとの更新・描画処理の切り替え
- **安全な状態データ更新**: `global` を使わず、辞書 `dict` でデータ・状態を一括管理する方法

### 次回の予告
次回は**第 9 回：ブラインド再現（ブロック崩し編）**です！
これまでに学んだ「グラフィック」「入力」「物理演算」「当たり判定」「状態管理」を総動員して、仕様書だけを頼りにゲームを完成させるチャレンジを行います！

```
