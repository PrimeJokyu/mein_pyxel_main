# 第11回（2/3）：点滅とタイマー

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 図形か文字を点滅させる
- 色が変わる演出を1つ出す
- 秒を数えて、時間が来たら文字を出す

前回のファイル: `pyxel_lesson_011_1.md`

---

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

---

## この回の確認

- 点滅か色の変化が見える
- 秒の数字が増える
- 指定の秒でメッセージが出る

次回は「簡単ピアノ」です。ファイルは `pyxel_lesson_011_3.md` です。
