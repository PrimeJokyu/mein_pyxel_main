# 第7回（2/3）：落とす、投げる

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 物を上から下へ落とす
- 下向きの速さを少しずつ増やす
- 投げた物が弧を描く

前回のファイル: `pyxel_lesson_007_1.md`

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

## 余裕があれば：オブジェクトプール

落下と、投げた動きが動いてから読みます。難しかったら、この節は後で戻ってきます。

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

---

## この回の確認

- 落ちる物が1つ以上見える
- 下へ行くほど速くなるか、弧を描く
- エラーで止まらない

次回は「スカイフォール」です。ファイルは `pyxel_lesson_007_3.md` です。

### AI に聞いてみよう

「毎フレーム、下向きの速さに重力を足してyを動かす書き方を教えて」と聞いてみよう。
