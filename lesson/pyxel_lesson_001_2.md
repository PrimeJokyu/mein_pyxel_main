# 第1回（2/3）：図形と文字を描く

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 四角、円、線を1つずつ描く
- 文字を画面に出す
- 色や位置を変数に入れる

前回のファイル: `pyxel_lesson_001_1.md`

---

## 🔺 5. 図形描画をマスターしよう

### 5-1. 画面のクリア

```python
pyxel.cls(色番号)  # 画面を指定した色で塗りつぶす
```

### 5-2. 基本図形

#### ⬛ 四角形（矩形）

```python
pyxel.rect(x, y, 幅, 高さ, 色)        # 塗りつぶし
pyxel.rectb(x, y, 幅, 高さ, 色)       # 枠だけ（bはborder）
```

#### ⭕ 円

```python
pyxel.circ(中心x, 中心y, 半径, 色)      # 塗りつぶし
pyxel.circb(中心x, 中心y, 半径, 色)     # 枠だけ（bはborder）
```

#### 🔺 三角形

```python
pyxel.tri(x1, y1, x2, y2, x3, y3, 色)      # 塗りつぶし
pyxel.trib(x1, y1, x2, y2, x3, y3, 色)     # 枠だけ（bはborder）
```

#### 📏 線・点

```python
pyxel.line(開始x, 開始y, 終了x, 終了y, 色)  # 直線
pyxel.pix(x, y, 色)                       # 1ピクセルの点
```

### 💡 実践例：簡単なキャラクター

```python
import pyxel

pyxel.init(160, 120)

def update():
    pass

def draw():
    pyxel.cls(12)  # 青い背景

    # 顔（円）
    pyxel.circ(80, 60, 20, 15)  # ピーチ色の顔
    pyxel.circb(80, 60, 20, 0)      # 黒い輪郭

    # 目
    pyxel.circ(75, 55, 3, 0)    # 左目
    pyxel.circ(85, 55, 3, 0)    # 右目

    # 口
    pyxel.line(75, 65, 85, 65, 8)   # 赤い口

pyxel.run(update, draw)
```

---

## ✏️ 6. 文字表示をマスターしよう

### 基本的な文字表示

```python
pyxel.text(x, y, 文字列, 色)
```

### 応用テクニック

#### 変数を使った動的表示

```python
name = "太郎"
age = 15
score = 1250

pyxel.text(10, 10, f"名前: {name}", 7)
pyxel.text(10, 20, f"年齢: {age}歳", 7)
pyxel.text(10, 30, f"スコア: {score}点", 10)
```

---

## 💾 7. 変数を活用しよう

### 色や位置を変数で管理

```python
import pyxel

# 変数の定義
bg_color = 1        # 背景色
face_x = 80         # 顔のX座標
face_y = 60         # 顔のY座標
face_color = 15     # 顔の色

pyxel.init(160, 120)

def update():
    pass

def draw():
    pyxel.cls(bg_color)  # 変数を使って背景色を設定

    # 変数を使って顔を描画
    pyxel.circfill(face_x, face_y, 20, face_color)
    pyxel.circb(face_x, face_y, 20, 0)

pyxel.run(update, draw)
```

### 計算を使った配置

```python
# 画面中央を計算で求める
center_x = 160 // 2  # 80
center_y = 120 // 2  # 60

# 等間隔の配置
for i in range(5):
    x = 20 + i * 30  # 20, 50, 80, 110, 140
    pyxel.circfill(x, 60, 8, i + 8)
```

---

---

## この回の確認

- 顔のような絵が1つ出る
- 文字が1つ以上出る
- 色か位置が変数になっている

次回は「マイプロフィールカード」です。ファイルは `pyxel_lesson_001_3.md` です。

### AI に聞いてみよう

「Pyxelで円と四角を使って顔を描く短いコードを教えて」と聞いてみよう。
