# 第6回（1/3）：絵を描いて画面に出す

**全3回の1回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- Pyxelエディタを開く
- 小さな絵を1枚描く
- bltで画面に出す

---

## 🎨 1. Pyxel エディタの完全活用

### 1-1. Pyxel エディタの起動方法

```bash
# コマンドプロンプト/ターミナルで実行
pyxel edit my_game.pyxres
```

このコマンドを実行した場所に「my_game.pyxres」が作成されるので、自分のフォルダに移動させる
### 2-2. アニメーション用スプライトの作成

#### 歩行アニメーション（3 フレーム）

```python
# フレーム1: 左足前
# フレーム2: 直立
# フレーム3: 右足前

# プログラムでの切り替え例
walk_frame = (pyxel.frame_count // 15) % 3  # 0.25秒ごとに切り替え
sprite_x = walk_frame * 16  # 横に並べたスプライトを選択
```

---

## 🎮 3. スプライト表示システムの実装

### 3-1. pyxel.blt()関数の詳細

```python
pyxel.blt(描画先x, 描画先y, 画像バンク,
          スプライトx, スプライトy, 幅, 高さ, 透明色)
```

#### パラメータの説明

- **描画先 x, y**: 画面上の描画位置
- **画像バンク**: 0-2 の画像データ（通常は 0 を使用）
- **スプライト x, y**: スプライトシート上の切り出し位置
- **幅, 高さ**: 切り出すサイズ
- **透明色**: 透明として扱う色（省略可能）

### 3-2. 基本的なスプライト表示

```python
import pyxel

pyxel.init(160, 120)
pyxel.load("my_game.pyxres")  # リソースファイルを読み込み

def update():
    pass

def draw():
    pyxel.cls(1)

    # スプライト表示の基本形
    pyxel.blt(50, 50,     # 描画位置
              0,          # 画像バンク0
              0, 0,       # スプライト位置(0,0)
              16, 16,     # サイズ16×16
              0)          # 黒(0)を透明色に

pyxel.run(update, draw)
```

### 3-3. 動的なスプライト表示

```python
import pyxel

player_x = 80
player_y = 60
facing_right = True

pyxel.init(160, 120)
pyxel.load("my_game.pyxres")

def update():
    global player_x, facing_right

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
        facing_right = False
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2
        facing_right = True

def draw():
    pyxel.cls(12)

    # 向きに応じてスプライトを反転
    if facing_right:
        pyxel.blt(player_x, player_y, 0, 0, 0, 16, 16, 0)
    else:
        pyxel.blt(player_x, player_y, 0, 0, 0, -16, 16, 0)  # 幅を負数で反転

pyxel.run(update, draw)
```

---

---

## この回の確認

- エディタで絵が残っている
- 画面にその絵が出る
- 左右のどちらを向くか、または絵が1枚出ている

次回は「辞書とアニメーション」です。ファイルは `pyxel_lesson_006_2.md` です。

### AI に聞いてみよう

「Pyxelエディタの開き方と、bltの引数を短い言葉で教えて」と聞いてみよう。
