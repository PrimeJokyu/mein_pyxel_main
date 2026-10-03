# 第3回（1/3）：キー入力と btn / btnp

**全3回の1回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 押しているキーを読む
- btnとbtnpの違いを言う
- 左右移動と、押した瞬間だけの変化を出す

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

---

## この回の確認

- 左右キーで図形が動く
- スペースを押した瞬間だけ何かが変わる
- 押し続けても、瞬間の処理は連続して起きない

次回は「4方向移動と画面の端」です。ファイルは `pyxel_lesson_003_2.md` です。
