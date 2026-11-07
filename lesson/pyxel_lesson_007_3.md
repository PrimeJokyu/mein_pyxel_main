# 第7回（3/3）：スカイフォール

**全3回の3回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 空から何かが落ちる
- 種類か色をランダムにする
- 画面の外で消す

前回のファイル: `pyxel_lesson_007_2.md`

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

---

## この回の確認

- 落ちてくる物が何度も出る
- 同時に複数見える
- 下に消えたあともプログラムが動く

次回は「当たったかを判定する」です。ファイルは `pyxel_lesson_008_1.md` です。

### AI に聞いてみよう

「一定フレームごとに、リストへ落下物を追加する書き方を教えて」と聞いてみよう。
