# 第5回（1/3）：作るものを決める

**全3回の1回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 作りたいものを1つ決める
- 最初に動かす機能を1つ決める
- 紙に、何をどこへ置くか書く

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

---

## この回の確認

- 作品の名前がある
- キーか自動で、何が起きるかを言える
- 今日は、コードを完成させなくてよい

次回は「メインの動きを動かす」です。ファイルは `pyxel_lesson_005_2.md` です。

### AI に聞いてみよう

「図形、変数、キー入力だけで作れる小さな作品を1つ、最初に動かす機能つきで教えて」と聞いてみよう。
