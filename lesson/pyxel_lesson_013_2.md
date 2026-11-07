# 第13回（2/3）：遠景と近景を流す

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 遠い景色は遅く、近い景色は速く流す
- 画面の外に出たら、反対側から続ける
- スコア表示は残す

前回のファイル: `pyxel_lesson_013_1.md`

---

## パララックス背景

- 遠景はゆっくり、近景は速く流す
- 画面の左に出たら右から続きが出るように、位置をループさせる
- まずは色付きの長方形で十分（画像は後でよい）

前回のスコアに、流れる背景を足します。このファイルだけで動きます。

```python
import pyxel

WIDTH = 160
HEIGHT = 120

state = {
    "speed": 1.5,
    "distance": 0.0,
    "scroll_far": 0.0,
    "scroll_near": 0.0,
}

pyxel.init(WIDTH, HEIGHT, title="Lesson 13-2 Parallax")

def update():
    state["scroll_far"] = state["scroll_far"] + state["speed"] * 0.3
    state["scroll_near"] = state["scroll_near"] + state["speed"] * 0.8
    if state["scroll_far"] >= WIDTH:
        state["scroll_far"] = state["scroll_far"] - WIDTH
    if state["scroll_near"] >= WIDTH:
        state["scroll_near"] = state["scroll_near"] - WIDTH
    state["distance"] = state["distance"] + state["speed"] * 0.1

def draw_looping_band(y, h, color, offset):
    x0 = int(-offset)
    pyxel.rect(x0, y, WIDTH, h, color)
    pyxel.rect(x0 + WIDTH, y, WIDTH, h, color)

def draw():
    pyxel.cls(0)
    pyxel.rect(0, 0, WIDTH, HEIGHT, 1)
    draw_looping_band(60, 20, 3, state["scroll_far"])
    draw_looping_band(90, 30, 11, state["scroll_near"])
    pyxel.line(0, 90, WIDTH, 90, 5)
    pyxel.rect(WIDTH // 3, 80, 12, 12, 7)
    pyxel.text(5, 5, f"Score: {int(state['distance'])}", 7)

pyxel.run(update, draw)
```

### AI Tip

- 「AI に『Pyxel で背景をループさせる最小コード』を聞いてみよう」

---

## この回の確認

- 背景が2層で流れる
- 切れ目が目立たない
- スコアは増え続ける

次回は「時間でスピードを上げる」です。ファイルは `pyxel_lesson_013_3.md` です。
