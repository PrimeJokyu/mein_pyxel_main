# 第8回（1/3）：当たったかを判定する

**全3回の1回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 四角同士が重なったか調べる
- 円の距離で当たったか調べる
- 重なったら色を変える

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

---

## この回の確認

- 重なると何かが変わる
- 離れると元に戻る
- 座標を変えても判定が壊れない

次回は「タイトルとプレイ」です。ファイルは `pyxel_lesson_008_2.md` です。

### AI に聞いてみよう

「2つの四角が重なっているかを、ifで書く式を教えて」と聞いてみよう。
