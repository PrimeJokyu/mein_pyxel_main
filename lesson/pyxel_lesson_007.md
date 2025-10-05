# 第 7 回：ランダム要素とオブジェクト生成システム

**～予測不可能な楽しさを作り出そう！ランダムな世界の創造～**

## 🎯 今日のゴール

- 動的なオブジェクト生成・削除システムを実装できる
- ランダムを使ったゲーム要素を作れる
- 「スカイフォール・シミュレーター」を作成する

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

### 2-2. オブジェクトプールの実装

```python
# パフォーマンス最適化のためのオブジェクトプール（クラス未使用・関数ベース）
object_pool_active = []
object_pool_inactive = []
object_pool_max = 100

def pool_create_empty_object():
    return {
        "x": 0, "y": 0, "active": False,
        "speed": 0, "color": 0, "size": 0, "type": ""
    }

def pool_init(max_objects=100):
    """プールを初期化（事前確保）"""
    global object_pool_max
    object_pool_max = max_objects
    object_pool_active.clear()
    object_pool_inactive.clear()
    for _ in range(max_objects):
        object_pool_inactive.append(pool_create_empty_object())

def pool_spawn(x, y, object_type):
    """オブジェクトをプールから取得して有効化"""
    if object_pool_inactive:
        obj = object_pool_inactive.pop()
        obj.update({
            "x": x, "y": y, "active": True,
            "speed": pyxel.rndf(1.0, 4.0),
            "color": pyxel.rndi(8, 15),
            "size": pyxel.rndi(3, 8),
            "type": object_type
        })
        object_pool_active.append(obj)
        return obj
    return None

def pool_despawn(obj):
    """オブジェクトを無効化してプールに戻す"""
    if obj in object_pool_active:
        obj["active"] = False
        object_pool_active.remove(obj)
        object_pool_inactive.append(obj)

def pool_update():
    """全アクティブオブジェクトの更新"""
    to_remove = []
    for obj in object_pool_active:
        obj["y"] += obj["speed"]
        if obj["y"] > 130:  # 画面外に出た
            to_remove.append(obj)

    # 画面外オブジェクトをプールに戻す
    for obj in to_remove:
        pool_despawn(obj)

# 使用例
pool_init(100)

def spawn_random_object():
    x = pyxel.rndi(0, 160)
    object_type = weighted_choice({"star": 60, "heart": 30, "diamond": 10})
    pool_spawn(x, -10, object_type)
```

#### ステップで理解する

1. 事前確保（プリウォーム）
   - `max_objects` 分の空オブジェクトを `inactive_objects` に用意します。
2. 取得（spawn）
   - 使い回し可能なオブジェクトを `inactive` から `pop()` し、値を上書きして `active` に移動。
3. 更新（update）
   - 位置や状態を更新し、画面外などで役目が終われば回収対象にします。
4. 返却（despawn）
   - `active` から取り除き、`inactive` に戻して再利用します。
5. 上限管理
   - `inactive` が空なら新規生成せずスキップするなど、上限を超えない設計に。

#### ポイント

- 毎フレームの `dict` 生成/破棄を抑え、GC 負荷と断片化を軽減できます。
- オブジェクトのキー構成を固定し、`update()` 時の分岐や欠損を減らします。
- `append/pop` 中心で O(1) 操作に寄せるとスケールしやすい。
- プール枯渇時の挙動（生成スキップ、古いものの優先回収など）を決めておくと安定します。

---

## 🌧️ 3. 落下・移動

### 3-1. 重力による落下

```python
def create_physics_object(x, y):
    return {
        "x": x, "y": y,
        "velocity_x": pyxel.rndf(-2.0, 2.0),  # 横方向の初期速度
        "velocity_y": 0,                       # 縦方向の初期速度
        "gravity": 0.2,                       # 重力加速度
        "bounce": 0.7,                        # 跳ね返り係数
        "friction": 0.98                      # 空気抵抗
    }

def update_physics_object(obj):
    # 重力を適用
    obj["velocity_y"] += obj["gravity"]

    # 空気抵抗を適用
    obj["velocity_x"] *= obj["friction"]

    # 位置を更新
    obj["x"] += obj["velocity_x"]
    obj["y"] += obj["velocity_y"]

    # 地面との当たり判定
    if obj["y"] > 110:  # 地面の高さ
        obj["y"] = 110
        obj["velocity_y"] = -obj["velocity_y"] * obj["bounce"]  # 跳ね返り

    # 左右の壁との当たり判定
    if obj["x"] < 0 or obj["x"] > 160:
        obj["velocity_x"] = -obj["velocity_x"] * obj["bounce"]
        obj["x"] = max(0, min(obj["x"], 160))
```

### 3-2. ものを投げた時の動き

```python
import math

def create_projectile(start_x, start_y, target_x, target_y, flight_time=60):
    """指定された時間で目標地点に到達する放物線軌道"""
    dx = target_x - start_x
    dy = target_y - start_y

    # 初期速度を計算
    velocity_x = dx / flight_time
    velocity_y = dy / flight_time - 0.5 * 0.2 * flight_time  # 重力を考慮

    return {
        "x": start_x, "y": start_y,
        "velocity_x": velocity_x,
        "velocity_y": velocity_y,
        "gravity": 0.2,
        "time": 0
    }

def update_projectile(proj):
    proj["time"] += 1

    # 物理計算
    proj["x"] += proj["velocity_x"]
    proj["y"] += proj["velocity_y"]
    proj["velocity_y"] += proj["gravity"]
```

---

## 🎨 4. 実習課題：「スカイフォール・シミュレーター」を作ろう！

### 課題内容

空からランダムに様々なオブジェクトが落下するシミュレーションプログラムを作成しましょう。

### 必須要素

1. **多様なオブジェクト**: 雨、雪、流れ星、UFO など
2. **異なる落下パターン**: 直線落下、波型軌道、放物線など
3. **確率的出現**: レアオブジェクトが低確率で出現
4. **背景インタラクション**: クリックでオブジェクト種類変更

### 実装のヒント

#### ステップ 1: 基本構造

```python
import pyxel
import math

# オブジェクト管理
falling_objects = []
current_mode = "rain"
spawn_timer = 0

# モード設定
modes = {
    "rain": {"spawn_rate": 3, "types": {"raindrop": 100}},
    "snow": {"spawn_rate": 2, "types": {"snowflake": 100}},
    "meteor": {"spawn_rate": 10, "types": {"meteor": 80, "ufo": 20}},
    "mixed": {"spawn_rate": 2, "types": {"raindrop": 40, "snowflake": 30, "meteor": 25, "ufo": 5}}
}

pyxel.init(160, 120)

def update():
    global spawn_timer, current_mode

    # モード切り替え（クリック）
    if pyxel.btnp(pyxel.KEY_SPACE):
        mode_list = list(modes.keys())
        current_index = mode_list.index(current_mode)
        current_mode = mode_list[(current_index + 1) % len(mode_list)]

    # オブジェクト生成
    spawn_timer += 1
    if spawn_timer >= modes[current_mode]["spawn_rate"]:
        spawn_timer = 0
        spawn_random_object()

    # オブジェクト更新
    update_all_objects()

    # 画面外オブジェクトの削除
    cleanup_objects()

def draw():
    # 背景色をモードに応じて変更
    bg_colors = {"rain": 13, "snow": 6, "meteor": 1, "mixed": 5}
    pyxel.cls(bg_colors.get(current_mode, 1))

    # 全オブジェクト描画
    draw_all_objects()

    # UI表示
    pyxel.text(5, 5, f"Mode: {current_mode.upper()}", 7)
    pyxel.text(5, 15, f"Objects: {len(falling_objects)}", 7)
    pyxel.text(5, 105, "SPACE: Change Mode", 7)

pyxel.run(update, draw)
```

#### ステップ 2: オブジェクト生成システム

```python
def spawn_random_object():
    """現在のモードに基づいてランダムオブジェクトを生成"""
    mode_config = modes[current_mode]
    object_type = weighted_choice(mode_config["types"])

    x = pyxel.rndi(0, 160)

    if object_type == "raindrop":
        create_raindrop(x)
    elif object_type == "snowflake":
        create_snowflake(x)
    elif object_type == "meteor":
        create_meteor(x)
    elif object_type == "ufo":
        create_ufo(x)

def create_raindrop(x):
    obj = {
        "type": "raindrop",
        "x": x, "y": -5,
        "speed": pyxel.rndf(3.0, 6.0),
        "color": 12,
        "length": pyxel.rndi(3, 7)
    }
    falling_objects.append(obj)

def create_snowflake(x):
    obj = {
        "type": "snowflake",
        "x": x, "y": -5,
        "speed": pyxel.rndf(0.5, 2.0),
        "sway": pyxel.rndf(0.02, 0.05),  # 横揺れの強さ
        "time": 0,
        "color": 7,
        "size": pyxel.rndi(2, 4)
    }
    falling_objects.append(obj)

def create_meteor(x):
    obj = {
        "type": "meteor",
        "x": x, "y": -10,
        "velocity_x": pyxel.rndf(-2.0, 2.0),
        "velocity_y": pyxel.rndf(2.0, 5.0),
        "color": 8,
        "size": pyxel.rndi(4, 8),
        "trail": []  # 軌跡記録用
    }
    falling_objects.append(obj)

def create_ufo(x):
    obj = {
        "type": "ufo",
        "x": x, "y": -10,
        "speed": pyxel.rndf(0.5, 1.5),
        "hover_amplitude": pyxel.rndf(10, 20),
        "hover_frequency": pyxel.rndf(0.03, 0.08),
        "time": 0,
        "color": 11
    }
    falling_objects.append(obj)
```

#### ステップ 3: 個別オブジェクト更新

```python
def update_all_objects():
    for obj in falling_objects:
        if obj["type"] == "raindrop":
            update_raindrop(obj)
        elif obj["type"] == "snowflake":
            update_snowflake(obj)
        elif obj["type"] == "meteor":
            update_meteor(obj)
        elif obj["type"] == "ufo":
            update_ufo(obj)

def update_raindrop(obj):
    obj["y"] += obj["speed"]

def update_snowflake(obj):
    obj["time"] += 1
    obj["y"] += obj["speed"]
    # 横にふらつく動き
    obj["x"] += math.sin(obj["time"] * obj["sway"]) * 0.5

def update_meteor(obj):
    obj["x"] += obj["velocity_x"]
    obj["y"] += obj["velocity_y"]

    # 軌跡を記録
    obj["trail"].append((obj["x"], obj["y"]))
    if len(obj["trail"]) > 8:
        obj["trail"].pop(0)

def update_ufo(obj):
    obj["time"] += 1
    obj["y"] += obj["speed"]

    # ホバリング動作
    obj["x"] += math.sin(obj["time"] * obj["hover_frequency"]) * obj["hover_amplitude"] * 0.1
```

#### ステップ 5: 描画システム

```python
def draw_all_objects():
    for obj in falling_objects:
        if obj["type"] == "raindrop":
            draw_raindrop(obj)
        elif obj["type"] == "snowflake":
            draw_snowflake(obj)
        elif obj["type"] == "meteor":
            draw_meteor(obj)
        elif obj["type"] == "ufo":
            draw_ufo(obj)

def draw_raindrop(obj):
    # 雨粒を線で表現
    pyxel.line(obj["x"], obj["y"], obj["x"], obj["y"] + obj["length"], obj["color"])

def draw_snowflake(obj):
    # 雪の結晶
    x, y, size = int(obj["x"]), int(obj["y"]), obj["size"]
    pyxel.circ(x, y, size, obj["color"])

    # 十字の装飾
    pyxel.line(x - size, y, x + size, y, obj["color"])
    pyxel.line(x, y - size, x, y + size, obj["color"])

def draw_meteor(obj):
    # 流れ星本体
    x, y, size = int(obj["x"]), int(obj["y"]), obj["size"]
    pyxel.circ(x, y, size, obj["color"])

    # 軌跡
    for i, (tx, ty) in enumerate(obj["trail"]):
        alpha = i / len(obj["trail"])  # 徐々に薄く
        if alpha > 0.3:  # 一定以上の濃さのみ描画
            pyxel.pix(int(tx), int(ty), 9)

def draw_ufo(obj):
    # UFOの形
    x, y = int(obj["x"]), int(obj["y"])

    # 本体
    pyxel.circ(x, y, 6, obj["color"])
    pyxel.rect(x - 8, y - 2, 16, 4, obj["color"])

    # 点滅ライト
    if (pyxel.frame_count // 10) % 2:
        pyxel.pix(x - 4, y, 10)
        pyxel.pix(x + 4, y, 10)
```

### 応用チャレンジ

#### 地面との相互作用

```python
def check_ground_collision(obj):
    if obj["y"] > 110:  # 地面に到達
        if obj["type"] == "raindrop":
            # 水しぶき効果
            create_splash_effect(obj["x"], 110)
        elif obj["type"] == "meteor":
            # 爆発効果
            create_explosion_effect(obj["x"], 110)

        return True  # オブジェクト削除のサイン
    return False

def create_splash_effect(x, y):
    for _ in range(5):
        particle = {
            "type": "particle",
            "x": x + pyxel.rndi(-5, 5),
            "y": y,
            "velocity_x": pyxel.rndf(-2, 2),
            "velocity_y": pyxel.rndf(-3, -1),
            "life": 20,
            "color": 12
        }
        falling_objects.append(particle)
```

#### 統計情報表示

```python
stats = {"raindrop": 0, "snowflake": 0, "meteor": 0, "ufo": 0}

def update_stats():
    # オブジェクト種類をカウント
    for key in stats:
        stats[key] = sum(1 for obj in falling_objects if obj["type"] == key)

def draw_stats():
    y_offset = 25
    for obj_type, count in stats.items():
        if count > 0:
            pyxel.text(5, y_offset, f"{obj_type}: {count}", 7)
            y_offset += 10
```

---

## ⚡ 6. パフォーマンス最適化技術

### 6-1. 効率的なオブジェクト削除

```python
def cleanup_objects():
    """効率的なオブジェクト削除"""
    # リスト内包表記を使った高速削除
    falling_objects[:] = [
        obj for obj in falling_objects
        if obj["y"] < 130 and obj.get("life", float('inf')) > 0
    ]

# または、逆順での削除（インデックスがずれない）
def cleanup_objects_reverse():
    for i in range(len(falling_objects) - 1, -1, -1):
        obj = falling_objects[i]
        if obj["y"] > 130 or obj.get("life", float('inf')) <= 0:
            falling_objects.pop(i)
```

### 6-2. フレームレート制御

```python
max_objects = 50
frame_skip = 0

def update():
    global frame_skip

    # フレームスキップでパフォーマンス調整
    frame_skip += 1

    # オブジェクトが多すぎる場合は更新頻度を下げる
    if len(falling_objects) > max_objects:
        if frame_skip % 2 != 0:  # 2フレームに1回更新
            return

    # 通常の更新処理
    update_all_objects()
    cleanup_objects()
```

---

## 🏆 7. チェックポイント

### ✅ 基本機能チェック

- [ ] 複数種類のオブジェクトが落下する
- [ ] ランダムな位置・タイミングで生成される
- [ ] 異なる落下パターンが実装されている
- [ ] レアオブジェクトが低確率で出現する

### ✅ 技術要素チェック

- [ ] ランダム関数を適切に活用している
- [ ] 動的なオブジェクト生成・削除ができている
- [ ] 確率的イベントが正しく動作する
- [ ] パフォーマンスを考慮した設計になっている

### ✅ 表現力チェック

- [ ] 視覚的に美しい動きを実現している
- [ ] 各オブジェクトに個性がある
- [ ] 背景との調和が取れている
- [ ] インタラクティブ要素がある

---

## 📝 8. まとめ

### 今日学んだこと

- **ランダム性の活用**: 確率・重み・シード値を使った予測不可能な表現
- **動的オブジェクト管理**: リスト・プールを使った効率的なシステム
- **物理シミュレーション**: 重力・軌道・相互作用の実装
- **パフォーマンス最適化**: 大量オブジェクトの効率的な処理

### 重要なポイント

- **適度なランダム性**: 完全にランダムではなく、制御されたランダム性
- **メモリ効率**: オブジェクトの適切な生成・削除タイミング
- **視覚的魅力**: 数学的な美しさと直感的な面白さの両立
- **拡張性**: 新しいオブジェクト型を# 第 7 回：ランダム要素とオブジェクト生成システム
  **～予測不可能な楽しさを作り出そう！動的な世界の創造～**

## 🎯 今日のゴール

- ランダム関数を戦略的に活用できるようになる
- 動的なオブジェクトを活用できるようになる
