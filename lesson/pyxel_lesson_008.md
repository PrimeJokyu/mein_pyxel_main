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

### 2-1. 基本的な状態管理

```python
import pyxel

# ゲーム状態の定義
GAME_STATE_TITLE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_PAUSED = 2
GAME_STATE_GAME_OVER = 3
GAME_STATE_RESULT = 4

# 現在の状態
current_state = GAME_STATE_TITLE
state_timer = 0  # 状態に入ってからの経過時間

def update():
    global current_state, state_timer
    state_timer += 1

    if current_state == GAME_STATE_TITLE:
        update_title()
    elif current_state == GAME_STATE_PLAYING:
        update_playing()
    elif current_state == GAME_STATE_PAUSED:
        update_paused()
    elif current_state == GAME_STATE_GAME_OVER:
        update_game_over()
    elif current_state == GAME_STATE_RESULT:
        update_result()

def draw():
    if current_state == GAME_STATE_TITLE:
        draw_title()
    elif current_state == GAME_STATE_PLAYING:
        draw_playing()
    elif current_state == GAME_STATE_PAUSED:
        draw_paused()
    elif current_state == GAME_STATE_GAME_OVER:
        draw_game_over()
    elif current_state == GAME_STATE_RESULT:
        draw_result()

def change_state(new_state):
    """状態を変更する"""
    global current_state, state_timer
    current_state = new_state
    state_timer = 0  # タイマーリセット
```

### 2-2. 各状態の実装

#### タイトル画面

```python
def update_title():
    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        change_state(GAME_STATE_PLAYING)
        initialize_game()  # ゲーム初期化

def draw_title():
    pyxel.cls(1)

    # タイトルロゴ
    title_text = "COLLECTOR CHALLENGE"
    text_width = len(title_text) * 4
    x = (160 - text_width) // 2
    pyxel.text(x, 40, title_text, 14)

    # 点滅する開始指示
    if (state_timer // 30) % 2:  # 0.5秒ごとに点滅
        pyxel.text(45, 80, "PRESS SPACE TO START", 7)

    # 簡単な背景演出
    for i in range(10):
        x = (state_timer + i * 16) % 180 - 10
        y = 20 + i * 8
        pyxel.pix(x, y, 12)
```

#### ゲームプレイ画面

```python
# ゲーム変数
player = {"x": 80, "y": 100, "score": 0, "lives": 3}
items = []
enemies = []

def initialize_game():
    """ゲーム開始時の初期化"""
    global player, items, enemies
    player = {"x": 80, "y": 100, "score": 0, "lives": 3}
    items = []
    enemies = []

def update_playing():
    # プレイヤー操作
    if pyxel.btn(pyxel.KEY_LEFT) and player["x"] > 0:
        player["x"] -= 2
    if pyxel.btn(pyxel.KEY_RIGHT) and player["x"] < 144:
        player["x"] += 2
    if pyxel.btn(pyxel.KEY_UP) and player["y"] > 0:
        player["y"] -= 2
    if pyxel.btn(pyxel.KEY_DOWN) and player["y"] < 104:
        player["y"] += 2

    # ポーズ機能
    if pyxel.btnp(pyxel.KEY_P):
        change_state(GAME_STATE_PAUSED)

    # アイテム生成
    if state_timer % 60 == 0:  # 1秒ごと
        spawn_item()

    # 敵生成
    if state_timer % 90 == 0:  # 1.5秒ごと
        spawn_enemy()

    # オブジェクト更新
    update_items()
    update_enemies()

    # 当たり判定
    check_collisions()

    # ゲームオーバー判定
    if player["lives"] <= 0:
        change_state(GAME_STATE_GAME_OVER)

def draw_playing():
    pyxel.cls(0)

    # プレイヤー描画
    pyxel.rect(player["x"], player["y"], 16, 16, 11)

    # アイテム描画
    for item in items:
        pyxel.circ(item["x"], item["y"], 4, item["color"])

    # 敵描画
    for enemy in enemies:
        pyxel.rect(enemy["x"], enemy["y"], 12, 12, 8)

    # UI描画
    pyxel.text(5, 5, f"Score: {player['score']}", 7)
    pyxel.text(5, 15, f"Lives: {player['lives']}", 7)
    pyxel.text(130, 5, "P: Pause", 6)
```

#### ポーズ画面

```python
def update_paused():
    if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_SPACE):
        change_state(GAME_STATE_PLAYING)

    if pyxel.btnp(pyxel.KEY_Q):  # Quit
        change_state(GAME_STATE_TITLE)

def draw_paused():
    # ゲーム画面を暗くして表示
    draw_playing()

    # オーバーレイ
    pyxel.rect(40, 45, 80, 30, 0)
    pyxel.rectb(40, 45, 80, 30, 7)

    pyxel.text(60, 55, "PAUSED", 14)
    pyxel.text(45, 65, "P: Resume  Q: Quit", 7)
```

#### ゲームオーバー画面

```python
def update_game_over():
    if state_timer > 120:  # 2秒後から操作可能
        if pyxel.btnp(pyxel.KEY_R):
            change_state(GAME_STATE_PLAYING)
            initialize_game()
        if pyxel.btnp(pyxel.KEY_Q):
            change_state(GAME_STATE_TITLE)

def draw_game_over():
    pyxel.cls(8)  # 赤い背景

    # ゲームオーバー文字
    pyxel.text(55, 40, "GAME OVER", 7)
    pyxel.text(45, 55, f"Final Score: {player['score']}", 7)

    if state_timer > 120:
        pyxel
```
