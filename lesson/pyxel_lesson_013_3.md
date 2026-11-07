# 第13回（3/3）：時間でスピードを上げる

**全3回の3回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 一定時間ごとに速度を少し上げる
- 速度に上限を付ける
- 遠景と近景の速さの差は残す

前回のファイル: `pyxel_lesson_013_2.md`

---

## スピードアップ

- 一定フレームごとに速度を少し上げる（例: 5秒ごとに +0.1）
- 上限を決めて、上がり過ぎを防ぐ
- 上げ幅は小さくして、遊びやすく調整する

前回までのスコアと背景に、速度上昇を足します。このファイルだけで動きます。

```python
import pyxel

WIDTH = 160
HEIGHT = 120

state = {
    "speed": 1.5,
    "speed_max": 3.0,
    "speed_step": 0.1,
    "speed_timer": 0,
    "speed_interval": 300,
    "distance": 0.0,
    "scroll_far": 0.0,
    "scroll_near": 0.0,
}

pyxel.init(WIDTH, HEIGHT, title="Lesson 13-3 Speed")

def update():
    state["speed_timer"] = state["speed_timer"] + 1
    if state["speed_timer"] >= state["speed_interval"]:
        state["speed_timer"] = 0
        if state["speed"] + state["speed_step"] < state["speed_max"]:
            state["speed"] = state["speed"] + state["speed_step"]
        else:
            state["speed"] = state["speed_max"]

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
    pyxel.text(5, 5, f"Speed: {state['speed']:.1f}", 7)
    pyxel.text(5, 15, f"Score: {int(state['distance'])}", 7)

pyxel.run(update, draw)
```

## チューニングの目安

- 速度の上限と上がる量を小さめにして、遊びやすくする
- 遠景と近景の倍率（0.3 / 0.8 など）を調整する
- 帯の高さや色を変えて、見やすさを優先する

## チャレンジ（余裕があれば）

- 雲（遠景）や木（近景）を追加して、見た目を良くする
- スコアで色を変えるなど、達成感の演出を入れる
- 速度の上がり方に段階（レベル）を付けてみる

## 今日のポイント

- スコアは「距離の積み上げ」で作れる
- パララックスは「速さの差」を付けるだけで成立する
- 速度は「少しずつ、上限あり」で遊びやすくなる

### AI Tip

- 「AI に『時間で速度が上がる変数の設計』を聞いてみよう」

---

## この回の確認

- 時間で速度が少し上がる
- 上限を超えない
- 背景とスコアも動いている

次回は「音を鳴らす」です。ファイルは `pyxel_lesson_014_1.md` です。
