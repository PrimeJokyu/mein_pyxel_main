# 第 5 回：オリジナル作品制作 - アウトプット

**～創造性を解放しよう！自分だけの作品を作る時間～**

## 🎯 今日のゴール

- これまで学んだ技術を自由に組み合わせて作品を作る

---

## 🌟 制作方針：「今まで学習したことを使って自由にコーディングしてみよう」

### 基本コンセプト

**技術習得よりも創造性と楽しさを最優先！**

- **テーマは完全自由**: 好きなものを何でも作ろう
- **完成度は問わない**: アイデアが形になっていれば OK

### 要件

以下を含む物を作ろう

- **図形描画**: 何らかの図形・文字を使った表現
- **動きの要素**: 自動で動く OR キー操作で動く
- **変化の要素**: 時間や操作で何かが変わる

---

## 💡 【参考】作品アイデア集

### 🎨 アート・表現系

#### デジタル絵画

```python
# 例：キーで色や図形を変えながら描画
colors = [8, 10, 12, 14, 15]
current_color = 0

def update():
    global current_color
    if pyxel.btnp(pyxel.KEY_SPACE):
        current_color = (current_color + 1) % len(colors)

    # マウス位置に図形を描く（簡単版）
    if pyxel.btn(pyxel.KEY_Z):
        # 描画処理...
```

#### 万華鏡シミュレーター

```python
import math
time = pyxel.frame_count

def draw():
    pyxel.cls(0)
    for i in range(8):
        angle = (time + i * 45) * 0.1
        x = 80 + math.cos(angle) * 40
        y = 60 + math.sin(angle) * 40
        pyxel.circ(x, y, 5, (i + time // 10) % 16)
```

#### 自動お絵描きマシン

- ランダムな位置に図形が描かれ続ける
- キーで描画モードを変更
- 時間とともに色が変化

### 🐾 生き物・ペット系

#### デジタルペット

```python
pet_mood = "happy"  # happy, sleepy, hungry
pet_x, pet_y = 80, 60

def update():
    global pet_mood, pet_x, pet_y

    # ランダムに移動
    if pyxel.rndi(0, 60) == 0:
        pet_x += pyxel.rndi(-10, 10)
        pet_y += pyxel.rndi(-10, 10)

    # キーで世話をする
    if pyxel.btnp(pyxel.KEY_F):  # Feed
        pet_mood = "happy"
```

#### 魚の群れシミュレーション

- 複数の魚が画面を泳ぎ回る
- キー操作で餌をあげる
- 時間で昼夜が変化

### 🎮 簡単ゲーム系

#### 色合わせゲーム

```python
target_color = pyxel.rndi(1, 15)
player_color = 8

def update():
    global player_color

    if pyxel.btnp(pyxel.KEY_SPACE):
        player_color = pyxel.rndi(1, 15)

    # 色が合ったら新しいターゲット
    if player_color == target_color:
        target_color = pyxel.rndi(1, 15)
```

#### 追いかけっこ

- プレイヤーが何かを追いかける
- または何かがプレイヤーを追いかける
- 触れたら何かが起こる

### 🌊 自然現象・シミュレーション系

#### 雨シミュレーター

```python
raindrops = []

def update():
    # 新しい雨粒を追加
    if pyxel.rndi(0, 5) == 0:
        raindrops.append([pyxel.rndi(0, 160), 0])

    # 雨粒を下に移動
    for drop in raindrops:
        drop[1] += 3

    # 画面外の雨粒を削除
    raindrops[:] = [d for d in raindrops if d[1] < 120]

def draw():
    pyxel.cls(13)  # 暗い空
    for drop in raindrops:
        pyxel.line(drop[0], drop[1], drop[0], drop[1]+3, 7)
```


### 📚 物語・インタラクティブ系

#### デジタル紙芝居

```python
scene = 0
scenes = [
    "昔々、ある所に...",
    "小さな村がありました",
    "そこに勇者が現れて...",
    "冒険が始まりました"
]

def update():
    global scene
    if pyxel.btnp(pyxel.KEY_SPACE):
        scene = (scene + 1) % len(scenes)

def draw():
    pyxel.cls(1)
    pyxel.text(10, 50, scenes[scene], 7)
    pyxel.text(10, 100, "Press SPACE", 6)
```

#### 選択式アドベンチャー

- キーで選択肢を選ぶ
- 選択によって物語が分岐
- 簡単なエンディング

---

## 🛠️ 制作のヒント

### ステップ 1: アイデアを決める（5 分）

1. **何を作りたいか考える**

   - 好きなもの、興味があるものから発想
   - 上のアイデア集を参考にしても良い
   - 完全オリジナルでも良い

2. **シンプルに始める**
   - 最初は小さな機能から
   - 後から機能を追加していく
   - 「動くもの」を早めに作る

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

### ステップ 4: 装飾・改良（15 分）

- 色を変える、図形を追加する
- 小さな動きや効果を追加する
- 見た目を良くする

---

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

### デバッグのコツ

```python
def draw():
    # 作品の描画
    # ...

    # デバッグ情報（最後に削除）
    pyxel.text(5, 5, f"Frame: {pyxel.frame_count}", 7)
    pyxel.text(5, 15, f"Objects: {len(objects)}", 7)
```

---

## 🚀 応用チャレンジ

基本的な作品ができたら、以下の要素も試してみよう！

### エフェクト・演出

- **パーティクル効果**: 小さな粒が飛び散る
- **画面シェイク**: 画面が揺れる効果
- **フェード効果**: 徐々に明るく/暗くなる

### インタラクション

- **マルチキー操作**: 複数のキーを組み合わせる
- **ホバー効果**: 特定の位置で何かが起こる
