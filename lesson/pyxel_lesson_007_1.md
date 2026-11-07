# 第7回（1/3）：ランダムとリスト

**全3回の1回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- rndiでバラバラの数を出す
- 確率で何かが起きる
- リストに物体を追加して消す

---

## 🎲 1. ランダム関数の戦略的活用

### 1-1. Pyxel のランダム関数

```python
import pyxel

# 整数のランダム値
random_int = pyxel.rndi(0, 10)      # 0から10の整数
random_color = pyxel.rndi(1, 15)    # 1から15の色番号

# 小数のランダム値
random_float = pyxel.rndf(0.0, 1.0) # 0.0から1.0の小数
random_speed = pyxel.rndf(0.5, 3.0) # 0.5から3.0の速度

# よく使うパターン
random_bool = pyxel.rndi(0, 1)      # 0 or 1 (True/False)
random_sign = pyxel.rndi(0, 1) * 2 - 1  # -1 or 1
```

### 1-2. 確率イベント

#### 基本的な確率判定

```python
def random_event():
    # 10%の確率で特別なイベント
    if pyxel.rndi(0, 99) < 10:  # 0-9 (10個) / 100個 = 10%
        return "special"
    else:
        return "normal"

# 使用例
def update():
    if pyxel.rndi(0, 99) < 5:  # 5%の確率
        # レアアイテムが出現
        spawn_rare_item()
```

#### 重み付き確率システム

```python
# アイテム出現の重み設定
item_weights = {
    "common": 70,    # 70%
    "uncommon": 20,  # 20%
    "rare": 8,       # 8%
    "epic": 2        # 2%
}

def weighted_random_item():
    roll = pyxel.rndi(0, 99)  # 0-99の乱数

    if roll < 70:
        return "common"
    elif roll < 90:      # 70-89
        return "uncommon"
    elif roll < 98:      # 90-97
        return "rare"
    else:                # 98-99
        return "epic"

```

### 1-3. シード値を使った再現可能なランダム性

```python
# 同じシード値で同じランダム結果を得る
def generate_level(seed):
    pyxel.rseed(seed)  # シード値を設定

    # これで毎回同じマップが生成される
    obstacles = []
    for i in range(10):
        x = pyxel.rndi(0, 160)
        y = pyxel.rndi(0, 120)
        obstacles.append({"x": x, "y": y})

    return obstacles

# プレイヤーが選んだレベル番号で固定マップ生成
level_1_obstacles = generate_level(12345)  # 常に同じ配置
level_2_obstacles = generate_level(67890)  # 別の固定配置
```

---

## 📦 2. 動的オブジェクト管理システム

ゲーム中に生まれて、動いて、消えていく「動的オブジェクト」を効率よく扱う仕組みを作ります。

- **動的オブジェクトとは**: プログラムで生成するオブジェクト（例: 雨粒、雪、流れ星、UFO）。

### 2-1. リストを使った基本的な管理

```python
import pyxel

# オブジェクトリスト
falling_objects = []

def spawn_object():
    """新しいオブジェクトを生成"""
    new_object = {
        "x": pyxel.rndi(0, 160),
        "y": -10,  # 画面上部から開始
        "speed": pyxel.rndf(1.0, 4.0),
        "color": pyxel.rndi(8, 15),
        "size": pyxel.rndi(3, 8),
        "type": weighted_choice({"star": 60, "heart": 30, "diamond": 10})
    }
    falling_objects.append(new_object)

def update_objects():
    """全オブジェクトの更新"""
    for obj in falling_objects:
        obj["y"] += obj["speed"]

    # 画面外のオブジェクトを削除
    falling_objects[:] = [obj for obj in falling_objects if obj["y"] < 130]

def draw_objects():
    """全オブジェクトの描画"""
    for obj in falling_objects:
        if obj["type"] == "star":
            draw_star(obj["x"], obj["y"], obj["size"], obj["color"])
        elif obj["type"] == "heart":
            draw_heart(obj["x"], obj["y"], obj["size"], obj["color"])
        elif obj["type"] == "diamond":
            draw_diamond(obj["x"], obj["y"], obj["size"], obj["color"])

def draw_star(x, y, size, color):
    """星の描画"""
    pyxel.circ(x, y, size, color)
    pyxel.line(x-size, y, x+size, y, 7)
    pyxel.line(x, y-size, x, y+size, 7)

def draw_heart(x, y, size, color):
    """ハートの描画"""
    pyxel.circ(x-size//2, y-size//2, size//2, color)
    pyxel.circ(x+size//2, y-size//2, size//2, color)
    pyxel.tri(x-size, y, x, y+size, x+size, y, color)

def draw_diamond(x, y, size, color):
    """ダイヤの描画"""
    pyxel.tri(x, y-size, x-size, y, x+size, y, color)
    pyxel.tri(x-size, y, x, y+size, x+size, y, color)
```

#### ステップで理解する

1. コンテナの用意
   - 可変長の `falling_objects` リストに辞書型オブジェクトを格納します。
2. 生成（spawn）
   - `spawn_object()` で `x/y`、`speed`、`color`、`size`、`type` を持つ辞書を作り、リストへ `append`。
3. 更新（update）
   - `update_objects()` で各 `obj` の `y` を `speed` 分だけ増やし、落下を表現します。
4. 削除（cleanup）
   - 画面外に出た要素を内包表記でフィルタし、`falling_objects[:] = [...]` で同じリストを置換（参照先を保つ）。
5. 描画（draw）
   - `type` に応じて専用の描画関数へ振り分け、見た目を分けます。

#### ポイント

- 反復中に同じリストを `pop()` で変更しない。削除は内包表記や逆順走査で安全に。
- `falling_objects[:] = [...]` は参照維持のため有効（他の箇所が同じリストを持っていても破綻しない）。
- `type` ごとの描画/更新は関数分割し、責務を明確化すると拡張しやすい。
- ランダム範囲は画面サイズと整合させて、端での不自然な出現を避ける。

---

## この回の確認

- 実行するたびに位置か色が変わる
- リストに物体を追加できる
- 画面の外に出たものを消している

次回は「落とす、投げる」です。ファイルは `pyxel_lesson_007_2.md` です。

### AI に聞いてみよう

「pyxel.rndiの使い方と、画面の外に出た要素をリストから除く書き方を教えて」と聞いてみよう。
