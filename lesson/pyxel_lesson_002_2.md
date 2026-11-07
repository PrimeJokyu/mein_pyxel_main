# 第2回（2/3）：時間の動きと、複数のボール

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- フレーム数で上下する動きを出す
- リストと辞書でボールをまとめる
- 端の処理を1種類動かす

前回のファイル: `pyxel_lesson_002_1.md`

---

## ⏰ 4. 時間を使った表現

### 4-1. フレーム数を使った周期的変化

```python
def update():
    global ball_y

    # pyxel.frame_countは起動からのフレーム数
    # 60フレーム = 1秒
    time = pyxel.frame_count

    # 120フレーム（2秒）周期で上下移動
    if (time % 120) < 60:
        ball_y += 1  # 1秒間下に移動
    else:
        ball_y -= 1  # 1秒間上に移動
```

### 4-2. 三角関数を使った自然な動き

```python
import math

def update():
    global ball_x, ball_y

    time = pyxel.frame_count * 0.1  # 時間の調整

    # 波のような動き
    ball_x = 80 + math.cos(time) * 50  # 中心80、振幅50
    ball_y = 60 + math.sin(time) * 30  # 中心60、振幅30
```

#### sin/cos の使い分け

- **sin（サイン）**: 波のような上下動
- **cos（コサイン）**: 波のような左右動
- **両方**: 円や楕円の動き

---

## 🎪 5. 複数のオブジェクトを管理しよう

### 5-1. 複数のボールを独立して動かす

```python
# 3つのボールの情報
ball1_x, ball1_y = 40, 30
ball1_dx, ball1_dy = 2, 1

ball2_x, ball2_y = 80, 60
ball2_dx, ball2_dy = -1, 2

ball3_x, ball3_y = 120, 90
ball3_dx, ball3_dy = 1, -1

def update():
    global ball1_x, ball1_y, ball1_dx, ball1_dy
    global ball2_x, ball2_y, ball2_dx, ball2_dy
    global ball3_x, ball3_y, ball3_dx, ball3_dy

    # ボール1の更新
    ball1_x += ball1_dx
    ball1_y += ball1_dy
    if ball1_x <= 0 or ball1_x >= 160: ball1_dx = -ball1_dx
    if ball1_y <= 0 or ball1_y >= 120: ball1_dy = -ball1_dy

    # ボール2の更新（同様の処理）
    # ボール3の更新（同様の処理）

def draw():
    pyxel.cls(0)
    pyxel.circ(ball1_x, ball1_y, 6, 8)   # 赤いボール
    pyxel.circ(ball2_x, ball2_y, 8, 12)  # 青いボール
    pyxel.circ(ball3_x, ball3_y, 4, 10)  # 黄色いボール
```

### 5-2. リストを使ったスマートな管理

#### 📚 Python の配列（リスト）を理解しよう

リストを使った管理方法を学ぶ前に、まずは Python の配列（リスト）について基本から学びましょう！

##### 🎒 リストって何？

リストは「複数のものを順番に入れておける箱」のようなものです。

```python
# 基本的なリストの作り方
numbers = [1, 2, 3, 4, 5]        # 数字のリスト
colors = ["赤", "青", "緑"]       # 文字のリスト
positions = [10, 20, 30, 40]    # 座標のリスト
```

##### 📦 辞書型（ディクショナリ）も覚えよう

辞書型は「名前を付けて整理できる箱」です。

```python
# 1つのボールの情報を辞書型で管理
ball = {
    "x": 50,        # X座標
    "y": 30,        # Y座標
    "dx": 2,        # X方向の速度
    "dy": 1,        # Y方向の速度
    "color": 8      # 色
}

# 辞書の中身を使う方法
print(ball["x"])    # 50が表示される
ball["x"] = 100     # X座標を100に変更
```

##### 🎯 リストと辞書を組み合わせよう

複数のボールを管理するには、辞書をリストに入れます：

```python
# 3つのボールをリストで管理
balls = [
    {"x": 40, "y": 30, "dx": 2, "dy": 1, "color": 8},   # 1個目のボール
    {"x": 80, "y": 60, "dx": -1, "dy": 2, "color": 12}, # 2個目のボール
    {"x": 120, "y": 90, "dx": 1, "dy": -1, "color": 10} # 3個目のボール
]

# 個別のボールにアクセスする方法
first_ball = balls[0]        # 最初のボール（0番目）
second_ball = balls[1]       # 2番目のボール（1番目）
third_ball = balls[2]        # 3番目のボール（2番目）

# 特定のボールの座標を変更
balls[0]["x"] = 50          # 1個目のボールのX座標を50に変更
balls[1]["color"] = 15      # 2個目のボールの色を15に変更
```

```python
# リストで複数のボールを管理
balls = [
    {"x": 40, "y": 30, "dx": 2, "dy": 1, "color": 8, "size": 6},
    {"x": 80, "y": 60, "dx": -1, "dy": 2, "color": 12, "size": 8},
    {"x": 120, "y": 90, "dx": 1, "dy": -1, "color": 10, "size": 4}
]

def update():
    for ball in balls:
        # 位置更新
        ball["x"] += ball["dx"]
        ball["y"] += ball["dy"]

        # 跳ね返り判定
        if ball["x"] <= 0 or ball["x"] >= 160:
            ball["dx"] = -ball["dx"]
        if ball["y"] <= 0 or ball["y"] >= 120:
            ball["dy"] = -ball["dy"]

def draw():
    pyxel.cls(0)
    for ball in balls:
        pyxel.circ(ball["x"], ball["y"], ball["size"], ball["color"])
```

#### 💡 `for ball in balls`の仕組みを理解しよう

`for ball in balls:`という文について詳しく説明します：

**基本的な動作**

- `balls`というリスト（配列）から、要素を 1 つずつ取り出します
- 取り出した要素を`ball`という変数に入れます
- リストの要素がなくなるまで、この処理を繰り返します

**具体例で理解**

```python
# ballsリストの中身
balls = [
    {"x": 40, "y": 30, "dx": 2, "dy": 1},
    {"x": 80, "y": 60, "dx": -1, "dy": 2},
    {"x": 120, "y": 90, "dx": 1, "dy": -1}
]

# for文の動作
for ball in balls:
    print(ball)
    # 1回目: {"x": 40, "y": 30, "dx": 2, "dy": 1}
    # 2回目: {"x": 80, "y": 60, "dx": -1, "dy": 2}
    # 3回目: {"x": 120, "y": 90, "dx": 1, "dy": -1}
```

---

## 🚧 6. いろいろな境界処理

### 6-1. 跳ね返り（反転）

```python
# 前述の例と同じ
if ball_x <= 0 or ball_x >= 160:
    dx = -dx
```

### 6-2. ループ（端から端へ）

```python
def update():
    global ball_x

    ball_x += 2

    # 右端を超えたら左端に戻る
    if ball_x > 160:
        ball_x = 0

    # 左端を超えたら右端に戻る
    if ball_x < 0:
        ball_x = 160
```

### 6-3. 停止（境界で止まる）

```python
def update():
    global ball_x

    ball_x += 2

    # 境界を超えないようにクランプ（制限）
    if ball_x > 160:
        ball_x = 160
    if ball_x < 0:
        ball_x = 0
```

---

---

## この回の確認

- ボールが2つ以上動く
- for文でまとめて更新している
- 端で跳ねる、戻る、止まるのどれかができる

次回は「動くボールワールド」です。ファイルは `pyxel_lesson_002_3.md` です。

### AI に聞いてみよう

「リストの中の辞書で、ボールのxとyを動かす例を教えて」と聞いてみよう。
