# 第3回（3/3）：操作感とキャラクター操作

**全3回の3回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- シフトキーで速く動く
- 画面端で止めたまま操作する
- キャラクター操作の課題を動かす

前回のファイル: `pyxel_lesson_003_2.md`

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

---

## この回の確認

- 普通の速さと速い動きがある
- 端で止まる
- 色を変えるキーが1つある

次回は「図形と、変数で動く円」です。ファイルは `pyxel_lesson_004_1.md` です。
