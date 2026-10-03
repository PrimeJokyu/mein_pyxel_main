# 第5回（2/3）：メインの動きを動かす

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- init、update、drawを書く
- 作品のメインの動きを1つ動かす
- 見た目より先に、動くものを作る

前回のファイル: `pyxel_lesson_005_1.md`

---

### ステップ 2: 基本構造を作る（10 分）

```python
import pyxel

# ここに変数を定義

pyxel.init(160, 120)

def update():
    # ここにゲームロジック
    pass

def draw():
    # ここに描画処理
    pyxel.cls(1)  # 背景色

pyxel.run(update, draw)
```

### ステップ 3: コア機能を実装（30 分）

- 作品の「メイン」となる部分を作る
- 最低限動くものを目指す
- 完璧でなくても良いのでとにかく動かす

## 🎨 技術的なアドバイス

### よく使うパターン集

#### ランダム要素を活用

```python
# ランダムな位置
x = pyxel.rndi(0, 160)
y = pyxel.rndi(0, 120)

# ランダムな色
color = pyxel.rndi(1, 15)

# 確率での出現
if pyxel.rndi(0, 100) < 10:  # 10%の確率
    # 何かを実行
```

#### 時間変化を活用

```python
time = pyxel.frame_count

# 点滅効果
if (time // 30) % 2 == 0:  # 0.5秒ごとに点滅
    pyxel.text(10, 10, "Hello", 7)

# 波のような動き
import math
y = 60 + math.sin(time * 0.1) * 20
```

#### 複数オブジェクトの管理

```python
# リストを使った管理
objects = []

def update():
    # 新しいオブジェクトを追加
    if pyxel.btnp(pyxel.KEY_SPACE):
        objects.append({"x": 80, "y": 60, "color": pyxel.rndi(1, 15)})

    # すべてのオブジェクトを更新
    for obj in objects:
        obj["y"] += 1  # 下に移動

def draw():
    for obj in objects:
        pyxel.circ(obj["x"], obj["y"], 5, obj["color"])
```

---

## この回の確認

- ウィンドウが開く
- メインの動きが1つ見える
- 絵が止まっただけの画面ではない

次回は「見た目を整えて完成させる」です。ファイルは `pyxel_lesson_005_3.md` です。

### AI に聞いてみよう

「今のアイデアで、まず動かす最小のupdateとdrawを書いて」と聞いてみよう。
