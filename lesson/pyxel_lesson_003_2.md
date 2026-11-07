# 第3回（2/3）：4方向移動と画面の端

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 上下左右に動かす
- 画面の外に出ないようにする
- maxとminで端を止める

前回のファイル: `pyxel_lesson_003_1.md`

---

## 🏃‍♂️ 3. 基本的な移動制御パターン

### 3-1. 4 方向移動

```python
def update():
    global player_x, player_y

    speed = 3  # 移動速度

    if pyxel.btn(pyxel.KEY_UP):
        player_y -= speed
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += speed
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= speed
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += speed
```

### 3-2. 8 方向移動（斜め移動対応）

```python
def update():
    global player_x, player_y

    speed = 2

    # 縦横の移動量を計算
    dx = 0
    dy = 0

    if pyxel.btn(pyxel.KEY_LEFT):
        dx -= speed
    if pyxel.btn(pyxel.KEY_RIGHT):
        dx += speed
    if pyxel.btn(pyxel.KEY_UP):
        dy -= speed
    if pyxel.btn(pyxel.KEY_DOWN):
        dy += speed

    player_x += dx
    player_y += dy
```

### 3-3. 複数キーセットの対応

```python
def update():
    global player_x, player_y

    speed = 2

    # 矢印キー OR WASDキー
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        player_x -= speed
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        player_x += speed
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        player_y -= speed
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        player_y += speed
```

---

## 🚧 4. 画面端での制御をマスターしよう

### 4-1. 基本的な画面端での制限

```python
def update():
    global player_x, player_y

    # 移動処理
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2

    # X座標の制限：左端(0)と右端(160)でチェック
    player_x = max(0, player_x)      # 左端制限：0より小さくならない
    player_x = min(player_x, 160)    # 右端制限：160より大きくならない

    # Y座標の制限：上端(0)と下端(120)でチェック
    player_y = max(0, player_y)      # 上端制限：0より小さくならない
    player_y = min(player_y, 120)    # 下端制限：120より大きくならない
```

#### 🤔 なぜこれで画面端制限ができるの？

**まずは`min`と`max`関数を理解しよう！**

##### `min`関数：「小さい方を選ぶ」

```python
# 例：2つの数字のうち小さい方を選ぶ
result = min(50, 160)  # 結果は50
result = min(200, 160) # 結果は160
```

- `min(50, 160)` → 50 と 160 を比べて小さい方の 50 を返す
- `min(200, 160)` → 200 と 160 を比べて小さい方の 160 を返す

##### `max`関数：「大きい方を選ぶ」

```python
# 例：2つの数字のうち大きい方を選ぶ
result = max(0, 50)   # 結果は50
result = max(0, -10)  # 結果は0
```

- `max(0, 50)` → 0 と 50 を比べて大きい方の 50 を返す
- `max(0, -10)` → 0 と-10 を比べて大きい方の 0 を返す

##### 実際の画面端制限の仕組み（二段階方式）

今回使っている方法を詳しく見てみましょう：

**ステップ 1：下限制限（左端/上端制限）**

```python
# X座標の左端制限
player_x = max(0, player_x)
# もし player_x が -10 なら → max(0, -10) = 0（左端でストップ）
# もし player_x が 50 なら → max(0, 50) = 50（そのまま）
```

**ステップ 2：上限制限（右端/下端制限）**

```python
# X座標の右端制限
player_x = min(player_x, 160)
# もし player_x が 180 なら → min(180, 160) = 160（右端でストップ）
# もし player_x が 50 なら → min(50, 160) = 50（そのまま）
```

##### 📊 具体例で理解しよう

キャラクターの位置が変化する様子：

| 元の位置 | `max(0, player_x)` | `min(結果, 160)`    | 最終位置 | 説明                 |
| -------- | ------------------ | ------------------- | -------- | -------------------- |
| -30      | max(0, -30) = 0    | min(0, 160) = 0     | 0        | 左端でストップ       |
| 50       | max(0, 50) = 50    | min(50, 160) = 50   | 50       | 画面内なのでそのまま |
| 180      | max(0, 180) = 180  | min(180, 160) = 160 | 160      | 右端でストップ       |

##### 💡 豆知識：一行で書く方法

実は、以下のように一行で書くこともできます：

```python
# 一行で書く方法（上級者向け）
player_x = max(0, min(player_x, 160))
player_y = max(0, min(player_y, 120))

# 今回学んだ二段階方法（初心者向け・分かりやすい）
player_x = max(0, player_x)      # 左端制限
player_x = min(player_x, 160)    # 右端制限
player_y = max(0, player_y)      # 上端制限
player_y = min(player_y, 120)    # 下端制限
```

一行で書く方法は短くて便利ですが、二段階方法の方が「何をしているか」が分かりやすいので、最初は二段階方法で練習しましょう！

##### 🎯 覚え方のコツ

「ガードレール」で覚えよう！

- 左のガードレール（0）: `max(0, player_x)` で左に出ないように
- 右のガードレール（160）: `min(player_x, 160)` で右に出ないように
- 道路の真ん中を安全に走れる！

### 4-2. オブジェクトサイズを考慮した画面端制限

```python
def update():
    global player_x, player_y

    player_size = 8  # キャラクターの半径

    # 移動処理
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2

    # サイズを考慮した画面端制限
    player_x = max(player_size, min(player_x, 160 - player_size))
    player_y = max(player_size, min(player_y, 120 - player_size))
```

### 4-3. 段階的な画面端制限

```python
def update():
    global player_x, player_y

    new_x = player_x
    new_y = player_y

    # 新しい位置を計算
    if pyxel.btn(pyxel.KEY_LEFT):
        new_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        new_x += 2

    # 画面端チェックしてから適用
    if 0 <= new_x <= 160:
        player_x = new_x
    if 0 <= new_y <= 120:
        player_y = new_y
```

---

---

## この回の確認

- 4方向に動く
- 端で止まる
- 斜めに動かしても画面の外に出ない

次回は「操作感とキャラクター操作」です。ファイルは `pyxel_lesson_003_3.md` です。

### AI に聞いてみよう

「maxとminで、座標を0から160の間に収める書き方を教えて」と聞いてみよう。
