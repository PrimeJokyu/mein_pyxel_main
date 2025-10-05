# 【第 11 回】サウンドシステムと演出効果

## 🎵 今日の目標

音響効果と視覚演出を駆使したリッチなゲーム体験を実現しよう！

- Pyxel で音を作って鳴らせるようになる
- 画面に楽しい演出効果を加える
- 音と映像を組み合わせた表現を学ぶ

---

## 📚 学習内容

### 1. Pyxel サウンドシステムの基本

#### 音を鳴らそう

```bash
# ターミナルまたはコマンドプロンプトで実行
pyxel edit my_sound.pyxres
```

**サウンドエディタでできること：**

- 🎼 **音階**：ドレミファソラシドの音を作る
- 🥁 **リズム**：太鼓やドラムのような打楽器音
- 🎺 **音色**：ピアノ、ギター、笛などの楽器の音
- 🎵 **メロディ**：複数の音をつなげて曲を作る

#### 音を鳴らす基本コード

```python
import pyxel

def init():
    pyxel.init(160, 120, title="Sound Test")
    pyxel.run(update, draw)

def update():
    # 数字キー1を押すと音が鳴る
    if pyxel.btnp(pyxel.KEY_1):
        pyxel.play(0, 0)  # チャンネル0で音0を再生

    # 数字キー2を押すと違う音
    if pyxel.btnp(pyxel.KEY_2):
        pyxel.play(1, 1)  # チャンネル1で音1を再生

def draw():
    pyxel.cls(0)
    pyxel.text(30, 50, "Press 1 or 2 for sound!", 7)
    pyxel.text(40, 70, "Make some noise!", 10)

init()
```

### 2. 基本的な視覚演出

#### 点滅効果（フラッシュ）

```python
import pyxel

state = {"blink_timer": 0, "show_text": True}

def init():
    pyxel.init(160, 120, title="Blink Effect")
    pyxel.run(update, draw)

def update():
    state["blink_timer"] += 1

    # 30フレーム（0.5秒）ごとに表示・非表示を切り替え
    if state["blink_timer"] >= 30:
        state["show_text"] = not state["show_text"]
        state["blink_timer"] = 0

    # スペースキーで効果音と点滅
    if pyxel.btnp(pyxel.KEY_SPACE):
        pyxel.play(0, 0)
        state["show_text"] = True
        state["blink_timer"] = 0

def draw():
    pyxel.cls(0)

    if state["show_text"]:
        pyxel.text(60, 60, "BLINK!", 7)

    pyxel.text(30, 100, "Press SPACE for effect", 13)

init()
```

#### 色変化エフェクト（レインボー）

```python
import pyxel

color_timer = 0

def init():
    pyxel.init(160, 120, title="Rainbow Effect")
    pyxel.run(update, draw)

def update():
    global color_timer
    color_timer += 1

def draw():
    pyxel.cls(0)

    # 時間によって色を変える（16色をループ）
    color = (color_timer // 10) % 16
    pyxel.circ(80, 60, 20, color)

    # 虹色の文字
    for i, char in enumerate("RAINBOW"):
        char_color = (color_timer // 5 + i) % 16
        pyxel.text(55 + i * 8, 90, char, char_color)

init()
```

### 3. タイマーとイベント管理

#### 遅延実行システム

```python
import pyxel

timer = 0
message = ""

def init():
    pyxel.init(160, 120, title="Timer System")
    pyxel.run(update, draw)

def update():
    global timer, message
    timer += 1

    # イベントスケジュール
    if timer == 60:  # 1秒後
        message = "1 second passed!"
        pyxel.play(0, 0)
    elif timer == 180:  # 3秒後
        message = "3 seconds passed!"
        pyxel.play(0, 1)
    elif timer == 300:  # 5秒後
        message = "5 seconds! Reset!"
        pyxel.play(0, 2)
        timer = 0  # リセット

    # Rキーでリセット
    if pyxel.btnp(pyxel.KEY_R):
        timer = 0
        message = "Timer Reset!"

def draw():
    pyxel.cls(0)

    # 現在の秒数表示
    seconds = timer // 60
    pyxel.text(10, 20, f"Timer: {seconds} seconds", 7)

    # メッセージ表示
    if message:
        pyxel.text(10, 50, message, 10)

    # 操作説明
    pyxel.text(10, 100, "Press R to reset", 13)

init()
```

---

## 🎯 実習課題：「簡単ピアノゲーム」を作ろう

### 作るもの

- 数字キー 1 ～ 8 で異なる音階を再生
- キーを押すと対応する鍵盤が色変化
- 鍵盤をマウスでクリックしても音が鳴る
- 現在押している音階名を画面に表示

### 完成コード例

```python
import pyxel

notes = ["ド", "レ", "ミ", "ファ", "ソ", "ラ", "シ", "ド"]
note_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
pressed_key = -1
key_positions = []  # 鍵盤の位置

def init():
    pyxel.init(200, 150, title="Simple Piano Game")

    for i in range(8):
        x = 20 + i * 20
        key_positions.append((x, 60, 18, 40))

    pyxel.run(update, draw)

def update():
    global pressed_key
    pressed_key = -1

    # キーボード入力
    for i in range(8):
        if pyxel.btn(pyxel.KEY_1 + i):
            pressed_key = i
            play_note(i)

    # マウス入力
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        for i, (x, y, w, h) in enumerate(key_positions):
            if x <= mx <= x + w and y <= my <= y + h:
                pressed_key = i
                play_note(i)

def play_note(note_index):
    pyxel.play(0, note_index % 4)

def draw():
    pyxel.cls(5)

    # タイトル
    pyxel.text(60, 20, "Simple Piano", 7)
    pyxel.text(50, 30, "Press 1-8 or Click!", 13)

    # 鍵盤
    for i in range(8):
        x, y, w, h = key_positions[i]
        color = 8 if pressed_key == i else 7
        pyxel.rect(x, y, w, h, color)
        pyxel.rectb(x, y, w, h, 0)
        pyxel.text(x + 6, y + 30, str(i + 1), 0)

    # 現在の音階名
    if pressed_key >= 0:
        pyxel.text(80, 120, f"♪ {notes[pressed_key]} ({note_names[pressed_key]})", 7)
        for j in range(3):
            note_x = 70 + j * 20 + (pyxel.frame_count // 5) % 10
            note_y = 110 - j * 5
            pyxel.text(note_x, note_y, "♪", 10)

init()
```

### チャレンジ課題

1. **和音機能**: 複数のキーを同時に押すと和音が鳴る
2. **録音・再生**: 演奏を記録して再生できる機能
3. **楽曲再生**: あらかじめ用意された曲が自動演奏される
4. **視覚効果**: 音に合わせて背景色やパーティクルが変化

---

## 💡 今日のポイント

### 覚えておこう

- `pyxel.play(チャンネル, 音番号)` で音を再生
- `pyxel.frame_count` で時間経過を管理
- タイマーを使って遅延実行やイベント管理
- 視覚効果で表現力アップ
