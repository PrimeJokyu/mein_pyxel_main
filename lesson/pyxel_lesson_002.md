# 第 2 回：座標変数と自動アニメーション

**～静止画から動画へ！時間で変化する魔法の世界～**

## 🎯 今日のゴール

- 座標を変数で管理して図形を動かせるようになる
- 画面の更新をマスターする
- 自動で動くオブジェクトをつくれるようになる

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

     ⏰ 4. 時間を使った表現

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

## 🎨 7. 実習課題：「動くボールワールド」を作ろう！

### 課題内容

異なる動きをする 3 つのボールが同時に動くプログラムを作成しましょう。

### 必須要素

1. **ボール 1**: 左右に跳ね返りながら移動
2. **ボール 2**: 上下に跳ね返りながら移動
3. **ボール 3**: 4 方向に跳ね返りながら移動
4. **各ボールの特徴**:
   - 異なる色
   - 異なる速度
   - 異なるサイズ

### 実装のヒント

#### ステップ 1: 基本構造

```python
import pyxel

# ボールの初期位置と移動量
ball1_x, ball1_y = 30, 60
ball1_dx = 2  # 左右移動のみ

ball2_x, ball2_y = 80, 30
ball2_dy = 3  # 上下移動のみ

ball3_x, ball3_y = 130, 90
ball3_dx, ball3_dy = -1, -2  # 斜め移動

pyxel.init(160, 120)

def update():
    # ここに各ボールの更新処理を書く
    pass

def draw():
    pyxel.cls(1)  # 背景色
    # ここに各ボールの描画処理を書く
    pass

pyxel.run(update, draw)
```

#### ステップ 2: 各ボールの動きを実装

**ボール 1（左右移動）**

```python
def update():
    global ball1_x, ball1_dx

    ball1_x += ball1_dx

    # 左右の境界で跳ね返り
    if ball1_x <= 0 or ball1_x >= 160:
        ball1_dx = -ball1_dx
```

**ボール 2（上下移動）**

```python
# update()関数内に追加
global ball2_y, ball2_dy

ball2_y += ball2_dy

# 上下の境界で跳ね返り
if ball2_y <= 0 or ball2_y >= 120:
    ball2_dy = -ball2_dy
```

**ボール 3（4 方向移動）**

```python
# update()関数内に追加
global ball3_x, ball3_y, ball3_dx, ball3_dy

ball3_x += ball3_dx
ball3_y += ball3_dy

# 4方向の境界で跳ね返り
if ball3_x <= 0 or ball3_x >= 160:
    ball3_dx = -ball3_dx
if ball3_y <= 0 or ball3_y >= 120:
    ball3_dy = -ball3_dy
```

#### ステップ 3: 描画処理

```python
def draw():
    pyxel.cls(1)  # 背景色

    # 各ボールを異なる色・サイズで描画
    pyxel.circ(ball1_x, ball1_y, 8, 8)   # 赤、大きい
    pyxel.circ(ball2_x, ball2_y, 6, 10)  # 黄色、中くらい
    pyxel.circ(ball3_x, ball3_y, 4, 12)  # 青、小さい
```

### 応用チャレンジ

基本課題ができたら、以下にも挑戦してみよう！

1. **速度変化**: 時間とともに速度が変わる
2. **色変化**: 壁に当たると色が変わる
3. **軌跡**: ボールが通った道を薄く表示
4. **音効果**: 壁に当たると音が鳴る
5. **重力**: 下向きの力が常に働く

---

## 📊 8. デバッグとテストのコツ

### 8-1. 座標の確認方法

```python
def draw():
    pyxel.cls(0)

    # ボールの描画
    pyxel.circfill(ball_x, ball_y, 5, 8)

    # デバッグ情報の表示
    pyxel.text(5, 5, f"X: {ball_x}", 7)
    pyxel.text(5, 15, f"Y: {ball_y}", 7)
    pyxel.text(5, 25, f"DX: {dx}", 7)
    pyxel.text(5, 35, f"DY: {dy}", 7)
```

### 8-2. よくあるバグと対処法

#### バグ 1: ボールが画面から消える

**原因**: 境界判定の不備

```python
# ❌ 間違い
if ball_x > 160:  # 境界を超えてから判定

# ✅ 正解
if ball_x >= 160:  # 境界に到達した時点で判定
```

#### バグ 2: ボールが壁に埋まる

**原因**: ボールの半径を考慮していない

```python
# ❌ 間違い
if ball_x <= 0 or ball_x >= 160:

# ✅ 正解（半径8の場合）
if ball_x <= 8 or ball_x >= 160-8:
```

#### バグ 3: 動きがカクカクする

**原因**: 移動量が大きすぎる

```python
# ❌ 動きが粗い
dx = 10

# ✅ 滑らかな動き
dx = 2
```

---

## 🎯 9. チェックポイント

### ✅ 基本動作チェック

- [ ] プログラムが正常に動作する
- [ ] 3 つのボールが画面に表示される
- [ ] 各ボールが異なる動きをしている
- [ ] 画面端で適切に跳ね返る

### ✅ 技術要素チェック

- [ ] グローバル変数を正しく使用している
- [ ] update()関数で座標を更新している
- [ ] 境界判定が正しく実装されている
- [ ] 各ボールが異なる色・サイズになっている

### ✅ 応用要素チェック

- [ ] 動きの速度が適切に調整されている
- [ ] 視覚的に面白い動きになっている
- [ ] デバッグ情報を活用している

---

## 🔬 10. 発展学習：物理シミュレーション

時間があったら挑戦してみよう！

### 重力のある世界

```python
ball_x, ball_y = 80, 20
dx, dy = 2, 0
gravity = 0.2  # 重力の強さ

def update():
    global ball_x, ball_y, dx, dy

    # 重力の適用
    dy += gravity  # 下向きの加速度

    # 位置更新
    ball_x += dx
    ball_y += dy

    # 地面で跳ね返り（エネルギー減衰）
    if ball_y >= 110:
        ball_y = 110
        dy = -dy * 0.8  # 跳ね返りで速度減衰

    # 左右の壁
    if ball_x <= 0 or ball_x >= 160:
        dx = -dx * 0.9  # 摩擦
```

### 複数ボールの相互作用

```python
# ボール同士の距離計算
import math

def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# 2つのボールが近づいたら色が変わる
distance = get_distance(ball1_x, ball1_y, ball2_x, ball2_y)
color = 14 if distance < 30 else 8  # 近いとピンク、遠いと赤
```

---

## 📝 11. まとめ

### 今日学んだこと

- `update()`関数での座標管理
- グローバル変数の使い方
- 移動量（速度）による動き制御
- 境界処理の種類（跳ね返り、ループ、停止）
- 複数オブジェクトの管理方法

### 重要なポイント

- **分離の原則**: update()で計算、draw()で表示
- **状態管理**: グローバル変数で状態を保持
- **フレームベース**: 60FPS での滑らかな動き

お疲れ様でした！動くボールワールドで物理の世界を体験できましたか？次回はついにユーザーが操作できるインタラクティブなプログラムに挑戦します！ 🚀✨
