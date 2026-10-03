# 第13回（1/3）：距離でスコアを増やす

**全3回の1回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 進んだ距離をスコアにする
- スコアを整数で表示する
- プレイヤーは画面の中央付近に固定してよい

---

## 距離スコア

- 毎フレーム進んだ距離を足せば、スコアになる（プレイヤーは画面の中央に固定でもよい）
- スコアは整数で表示する（小数は丸める）
- 速度が上がると、同じ時間でもスコアは増えやすい

状態は辞書に入れます。関数の中から、その辞書を書き換えます。

```python
import pyxel

WIDTH = 160
HEIGHT = 120

state = {
    "speed": 1.5,
    "distance": 0.0,
}

pyxel.init(WIDTH, HEIGHT, title="Lesson 13-1 Score")

def update():
    state["distance"] = state["distance"] + state["speed"] * 0.1

def draw():
    pyxel.cls(1)
    pyxel.rect(WIDTH // 3, 80, 12, 12, 7)
    pyxel.text(5, 5, f"Score: {int(state['distance'])}", 7)

pyxel.run(update, draw)
```

### AI Tip

- 「AI に『ランナーで距離スコアを増やす計算の仕方』を聞いてみよう」

---

## この回の確認

- スコアの数字が増える
- 小数ではなく整数で出ている
- キャラクターの絵か四角が見える

次回は「遠景と近景を流す」です。ファイルは `pyxel_lesson_013_2.md` です。
