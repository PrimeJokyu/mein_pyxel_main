# 第2回（1/3）：図形を動かして跳ね返す

**全3回の1回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- updateで座標を変える
- ボールを横に動かす
- 端で進む向きを逆にする

---

## 🔄 1. update()関数の秘密

前回は`update()`という関数を作ったのを覚えていますか？
今回は`update()`関数を使ってものに動きを付けていきます。

### update()と draw()の違い

| 関数         | 役割            | ゲームでの例え | 主な処理                                   |
| ------------ | --------------- | -------------- | ------------------------------------------ |
| **update()** | 🧠 ゲームの頭脳 | 「考える人」   | 座標計算、キー入力、当たり判定、ルール処理 |
| **draw()**   | 🎨 ゲームの表現 | 「絵を描く人」 | 画面クリア、図形描画、文字表示、エフェクト |

---

## 🎯 2. 座標変数で図形を動かそう

### 基本的な動きの仕組み

```python
import pyxel

# グローバル変数（プログラム全体で使える変数）
ball_x = 50  # ボールのX座標
ball_y = 60  # ボールのY座標

pyxel.init(160, 120)

def update():
    global ball_x  # グローバル変数を使うための宣言

    # 💡 グローバル変数について詳しく知りたい場合は、AIに「Pythonのグローバル変数について教えてわかりやすく教えて」と聞いてみよう！

    ball_x = ball_x + 1  # または ball_x += 1
    # 毎フレーム（1/60秒）ごとにX座標を1ずつ増やす

def draw():
    pyxel.cls(1)  # 背景をクリア
    pyxel.circ(ball_x, ball_y, 8, 10)  # 動くボール

pyxel.run(update, draw)
```

### 🚀 速度を使った制御

```python
# より柔軟な動きの制御
ball_x = 80
ball_y = 60
dx = 2      # X方向の移動量（速度）
dy = 1      # Y方向の移動量（速度）

def update():
    global ball_x, ball_y

    ball_x += dx  # X座標を移動量分移動
    ball_y += dy  # Y座標を移動量分移動
```

---

## 🏀 3. いろんな動きパターンを覚えよう

### 3-1. 基本的な移動パターン

#### 右方向への等速移動

```python
def update():
    global ball_x
    ball_x += 2  # 右に2ピクセルずつ移動
```

#### 斜め移動

```python
def update():
    global ball_x, ball_y
    ball_x += 1  # 右に移動
    ball_y += 1  # 下に移動（斜め下に進む）
```

### 3-2. 往復移動（跳ね返り）

#### 水平方向の往復

```python
ball_x = 50
dx = 2  # 移動方向と速度

def update():
    global ball_x, dx

    ball_x += dx

    # 画面端に到達したら方向を反転
    if ball_x <= 0 or ball_x >= 160:
        dx = -dx  # 移動方向を逆にする
```

#### 完全な跳ね返り（4 方向）

```python
ball_x = 80
ball_y = 60
dx = 3
dy = 2

def update():
    global ball_x, ball_y, dx, dy

    ball_x += dx
    ball_y += dy

    # 左右の壁で跳ね返り
    if ball_x <= 0 or ball_x >= 160:
        dx = -dx

    # 上下の壁で跳ね返り
    if ball_y <= 0 or ball_y >= 120:
        dy = -dy
```

---

---

## この回の確認

- ボールが止まらず動く
- 画面の端で折り返す
- 速度の数字を変えると速さが変わる

次回は「時間の動きと、複数のボール」です。ファイルは `pyxel_lesson_002_2.md` です。
