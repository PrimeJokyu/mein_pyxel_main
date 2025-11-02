# 第 3 回：キーボード入力を制御しよう

**～プレイヤーの意思で動く！リアルタイム操作の世界～**

## 🎯 今日のゴール

- キーボード入力を検出できる
- `pyxel.btn()`と`pyxel.btnp()`の違いを理解する
- 画面端での制御をマスターする

---

## ⌨️ 1. キー入力の基本

### Pyxel で使えるキー

Pyxel では以下のキーを検出できます：

#### 📝 使用可能なキーの例

| カテゴリ               | キー定数              | 説明               | 備考                 |
| ---------------------- | --------------------- | ------------------ | -------------------- |
| **方向キー**           | `pyxel.KEY_UP`        | ↑ キー             | 移動によく使う       |
|                        | `pyxel.KEY_DOWN`      | ↓ キー             |                      |
|                        | `pyxel.KEY_LEFT`      | ← キー             |                      |
|                        | `pyxel.KEY_RIGHT`     | → キー             |                      |
| **文字キー**           | `pyxel.KEY_A`         | A キー             | A〜Z 全て使用可能    |
|                        | `pyxel.KEY_B`         | B キー             |                      |
|                        | `pyxel.KEY_C`         | C キー             |                      |
|                        | `pyxel.KEY_W`         | W キー             | WASD での移動に      |
|                        | `pyxel.KEY_S`         | S キー             |                      |
|                        | `pyxel.KEY_D`         | D キー             |                      |
|                        | `pyxel.KEY_Z`         | Z キー             | アクションによく使う |
|                        | `pyxel.KEY_X`         | X キー             |                      |
| **数字キー**           | `pyxel.KEY_0`         | 0 キー             | 0〜9 全て使用可能    |
|                        | `pyxel.KEY_1`         | 1 キー             |                      |
|                        | `pyxel.KEY_2`         | 2 キー             |                      |
|                        | `pyxel.KEY_3`         | 3 キー             |                      |
|                        | `pyxel.KEY_4`         | 4 キー             |                      |
|                        | `pyxel.KEY_5`         | 5 キー             |                      |
|                        | `pyxel.KEY_6`         | 6 キー             |                      |
|                        | `pyxel.KEY_7`         | 7 キー             |                      |
|                        | `pyxel.KEY_8`         | 8 キー             |                      |
|                        | `pyxel.KEY_9`         | 9 キー             |                      |
| **特殊キー**           | `pyxel.KEY_SPACE`     | スペースキー       | ジャンプ・決定に     |
|                        | `pyxel.KEY_ENTER`     | エンターキー       | 決定・開始に         |
|                        | `pyxel.KEY_ESCAPE`    | エスケープキー     | メニュー・終了に     |
|                        | `pyxel.KEY_TAB`       | タブキー           |                      |
|                        | `pyxel.KEY_BACKSPACE` | バックスペースキー |                      |
| **修飾キー**           | `pyxel.KEY_SHIFT`     | シフトキー         | 高速移動・特殊操作   |
|                        | `pyxel.KEY_CTRL`      | コントロールキー   |                      |
|                        | `pyxel.KEY_ALT`       | オルトキー         |                      |
| **ファンクションキー** | `pyxel.KEY_F1`        | F1 キー            | F1〜F12 全て使用可能 |
|                        | `pyxel.KEY_F2`        | F2 キー            | デバッグ・設定に     |
|                        | `pyxel.KEY_F3`        | F3 キー            |                      |
|                        | `pyxel.KEY_F12`       | F12 キー           |                      |

#### 🧠 豆知識：キー定数の正体

`pyxel.KEY_UP`のようなキー定数は、実は内部では**数字**として扱われています！

- `pyxel.KEY_UP` は実際には数字の `265` です
- `pyxel.KEY_A` は数字の `65` です
- `pyxel.KEY_SPACE` は数字の `32` です

これらの数字は「キーコード」と呼ばれ、コンピューターがキーボードの各キーを区別するために使っています。Pyxel では、この数字を覚えなくても済むように、分かりやすい名前（定数）を用意してくれているのです。

つまり、以下の 2 つの書き方は全く同じ意味になります：

```python
# 分かりやすい書き方（推奨）
if pyxel.btn(pyxel.KEY_UP):

# 数字を直接使う書き方（非推奨）
if pyxel.btn(265):
```

定数を使う方が、後からコードを読み返したときに「あ、これは上キーのことだな」とすぐに分かるので、必ず`pyxel.KEY_UP`のような定数を使いましょう！

#### 💡 AI に聞いてみよう

「Pyxel で使えるキーの種類をもっと詳しく教えて」と AI に質問してみましょう。他にもどんなキーが使えるか、より詳しい情報を教えてくれるかもしれません！

---

## 🎮 2. btn()と btnp()の違いを理解しよう

### 2-1. btn() - 継続的な入力

**「押している間ずっと」反応する**

```python
def update():
    global player_x

    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2  # 右キーを押している間、継続的に移動

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2  # 左キーを押している間、継続的に移動
```

#### 使用場面

- キャラクターの移動
- 連射系の操作
- 滑らかな動作が必要な場面

### 2-2. btnp() - 単発的な入力

**「押した瞬間だけ」反応する**

```python
def update():
    global player_color

    if pyxel.btnp(pyxel.KEY_SPACE):
        player_color += 1  # スペースを押した瞬間だけ色が変わる
        if player_color > 15:
            player_color = 1
```

#### 使用場面

- メニューの選択
- ジャンプ動作
- 一回だけ実行したい処理

### 2-3. 実際の比較例

```python
import pyxel

player_x = 80
player_y = 60
jump_count = 0
color = 8

pyxel.init(160, 120)

def update():
    global player_x, jump_count, color

    # btn(): 滑らかな左右移動
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2

    # btnp(): 一回だけのジャンプと色変更
    if pyxel.btnp(pyxel.KEY_SPACE):
        jump_count = 20  # ジャンプ開始

    if pyxel.btnp(pyxel.KEY_C):
        color = (color + 1) % 16  # 色をサイクル

    # ジャンプ処理
    if jump_count > 0:
        jump_count -= 1

def draw():
    pyxel.cls(1)

    # ジャンプ中は少し上に表示
    y = player_y - jump_count
    pyxel.circ(player_x, y, 8, color)

pyxel.run(update, draw)
```

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

## 🎨 5. 操作感を向上させるテクニック

### 5-1. 🚀 やってみよう：高速移動システムを作成

**課題：シフトキーを押しながら移動すると速くなるシステムを作ってみましょう！**

#### 📝 新しい概念：`and`（そして）

複数のキーが**同時に**押されているかをチェックするには、`and`を使います：

```python
# シフトキー「と」左キーが同時に押されている
if pyxel.btn(pyxel.KEY_SHIFT) and pyxel.btn(pyxel.KEY_LEFT):
    print("高速で左に移動！")

# 普通の左キーだけの場合
if pyxel.btn(pyxel.KEY_LEFT):
    print("普通の速度で左に移動")
```

`and`は「A かつ B」という意味で、両方の条件が満たされた時だけ実行されます。

#### 🎯 作成手順

1. **基本の移動速度を決める**

   - `base_speed = 2` に通常時の速度を設定
   - `turbo_speed = 5` に加速時の速度を設定

2. **シフトキー入力を確認する**

   - `pyxel.btn(pyxel.KEY_SHIFT)` が押されているかチェック
   - 押されていれば高速、そうでなければ通常速度を選ぶ

3. **実際に使う速度を決定する**

   - `if`文で条件に応じて `speed` に値を代入

4. **入力方向に応じて座標を更新する**

   - 左右キー（`KEY_LEFT` / `KEY_RIGHT`）の入力で `player_x` を移動

5. **応用してみよう**
   - 上下移動にも同じ仕組みを適用
   - 画面に現在の速度を表示してみる

#### 💻 完成コード例

```python
def update():
    global player_x, player_y

    base_speed = 2
    turbo_speed = 5

    # シフトキーで高速移動
    if pyxel.btn(pyxel.KEY_SHIFT):
        speed = turbo_speed
    else:
        speed = base_speed

    # 4方向移動
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= speed
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += speed
    if pyxel.btn(pyxel.KEY_UP):
        player_y -= speed
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += speed
```

#### ポイント

- `btn()` は「押している間ずっと」反応するため、押下中は連続して速さが反映されます。
- 速度の値はゲームの難易度や世界観に合わせて調整しましょう。
- 修飾キー（SHIFT など）は他のキーと同時押しされる想定で設計すると操作性が良くなります。

#### 💡 困ったときは AI に聞こう

「Python の and の使い方を教えて」や「Pyxel で同時押し判定をする方法」など、分からないことがあれば遠慮なく AI に質問してみましょう！

### 5-2. キー組み合わせ判定

```python
def update():
    global player_x, player_y, player_color, player_size

    # 基本移動
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2

    # 組み合わせ操作
    if pyxel.btn(pyxel.KEY_SPACE) and pyxel.btnp(pyxel.KEY_UP):
        # スペース+上キーで大ジャンプ
        player_y -= 20

    if pyxel.btn(pyxel.KEY_SHIFT) and pyxel.btnp(pyxel.KEY_C):
        # シフト+Cでランダムカラー
        player_color = pyxel.rndi(1, 15)
```

---

## 🎯 6. 実習課題：「キャラクター操作マスター」を作ろう！

### 課題内容

多彩なキー操作に対応したキャラクター制御システムを作成しましょう。

### 必須要素

1. **矢印キー**: 基本移動（速度 2）
2. **WASD キー**: 高速移動（速度 4）
3. **スペースキー**: ジャンプ（一時的な大きな移動）
4. **R キー**: 位置リセット（画面中央に戻る）
5. **数字キー 1-9**: キャラクターの色変更
6. **画面画面端制限**: キャラクターが画面外に出ない

### 実装のヒント

#### 完全なコード例

```python
import pyxel

# キャラクターの初期状態
player_x = 80
player_y = 60
player_color = 8
jump_timer = 0

def update():
    global player_x, player_y, player_color, jump_timer

    # 基本移動（矢印キー - 速度2）
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2
    if pyxel.btn(pyxel.KEY_UP):
        player_y -= 2
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += 2

    # WASD高速移動（速度4）
    if pyxel.btn(pyxel.KEY_A):
        player_x -= 4
    if pyxel.btn(pyxel.KEY_D):
        player_x += 4
    if pyxel.btn(pyxel.KEY_W):
        player_y -= 4
    if pyxel.btn(pyxel.KEY_S):
        player_y += 4

    # スペースキーでジャンプ
    if pyxel.btnp(pyxel.KEY_SPACE):
        jump_timer = 15

    # ジャンプ処理
    if jump_timer > 0:
        jump_timer -= 1

    # Rキーでリセット
    if pyxel.btnp(pyxel.KEY_R):
        player_x = 80
        player_y = 60
        player_color = 8
        jump_timer = 0

    # 数字キー1-9で色変更
    if pyxel.btnp(pyxel.KEY_1):
        player_color = 1
    if pyxel.btnp(pyxel.KEY_2):
        player_color = 2
    if pyxel.btnp(pyxel.KEY_3):
        player_color = 3
    if pyxel.btnp(pyxel.KEY_4):
        player_color = 4
    if pyxel.btnp(pyxel.KEY_5):
        player_color = 5
    if pyxel.btnp(pyxel.KEY_6):
        player_color = 6
    if pyxel.btnp(pyxel.KEY_7):
        player_color = 7
    if pyxel.btnp(pyxel.KEY_8):
        player_color = 8
    if pyxel.btnp(pyxel.KEY_9):
        player_color = 9

    # 画面端制限
    player_x = max(8, player_x)      # 左端制限
    player_x = min(player_x, 152)    # 右端制限
    player_y = max(8, player_y)      # 上端制限
    player_y = min(player_y, 112)    # 下端制限

def draw():
    pyxel.cls(1)  # 背景

    # ジャンプ中の表示調整
    y = player_y - jump_timer * 2
    pyxel.circfill(player_x, y, 8, player_color)

    # 操作説明
    pyxel.text(5, 5, "Arrow: Move(2)", 7)
    pyxel.text(5, 15, "WASD: Fast(4)", 7)
    pyxel.text(5, 25, "Space: Jump", 7)
    pyxel.text(5, 35, "R: Reset", 7)
    pyxel.text(5, 45, "1-9: Color", 7)

    # 現在の情報表示
    pyxel.text(5, 65, f"X:{player_x} Y:{player_y}", 7)
    pyxel.text(5, 75, f"Color:{player_color}", 7)
    if jump_timer > 0:
        pyxel.text(5, 85, "JUMPING!", 10)

# 初期化とゲーム開始
pyxel.init(160, 120, title="Character Control Master")
pyxel.run(update, draw)
```

## 🎯 今日のゴール

- キーボード入力を検出してプログラムに反映できる
- `pyxel.btn()`と`pyxel.btnp()`の違いを理解する
- 滑らかで気持ちいい操作感を実現する
- 画面画面端での制御をマスターする
- 最後に「キャラクター操作マスター」を作成する

---

```

```
