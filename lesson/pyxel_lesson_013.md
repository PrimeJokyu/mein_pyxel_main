# 【第 13 回】スコア・背景・スピードアップ

## 🎯 今日の目標

- 距離でスコアを増やす
- パララックス背景（遠景と近景）を流す
- 時間で少しずつスピードを上げる

---

## 📚 学習内容（かんたん解説）

### 1. 距離スコア

- 毎フレーム進んだ距離を足していけばスコアになる（プレイヤーは画面中央に固定でも OK）
- スコアは整数で表示（小数は丸める）
- 速度が上がると同じ時間でスコアも上がりやすい

#### AI Tip

- 「AI に『ランナーで距離スコアを増やす計算の仕方』を聞いてみよう」

### 2. パララックス背景

- 遠景はゆっくり、近景は速く流す
- 画面の左に出たら右から続きが出るように、位置をループさせる
- まずは色付きの長方形で十分（画像は後で OK）

#### AI Tip

- 「AI に『Pyxel で背景をループさせる最小コード』を聞いてみよう」

### 3. スピードアップ

- 一定フレームごとに速度を少し上げる（例：5 秒ごとに+0.1）
- 上限を決めて上がり過ぎを防ぐ
- 上げ幅は小さくして遊びやすく調整

#### AI Tip

- 「AI に『時間で速度が上がる変数の設計』を聞いてみよう」

---

## 🛠 進め方（ステップ）

1. スケルトンを作る：初期化・`update()`・`draw()`とスコア表示
2. 背景を 2 層で流す：遠景（遅い）と近景（速い）
3. 速度上昇を入れる：一定時間ごとに`speed`を少しだけ増やす

---

## ✅ 完成イメージ（最小コード）

```python
import pyxel

# 画面
WIDTH, HEIGHT = 160, 120

# ゲーム状態
speed = 1.5           # ベース速度
speed_max = 3.0       # 上限
speed_step = 0.1      # 上がる量
speed_timer = 0       # 上昇までのカウント
speed_interval = 300  # 5秒ごと（60fps想定）

scroll_far = 0.0      # 遠景スクロール
scroll_near = 0.0     # 近景スクロール

distance = 0.0        # 距離スコア（小数）

pyxel.init(WIDTH, HEIGHT, title="Lesson 13: Score & Parallax & Speed")

def update():
    global speed, speed_timer, scroll_far, scroll_near, distance

    # スピードアップ
    speed_timer += 1
    if speed_timer >= speed_interval:
        speed_timer = 0
        speed = min(speed + speed_step, speed_max)

    # 背景スクロール（遠景は遅く、近景は速く）
    scroll_far += speed * 0.3
    scroll_near += speed * 0.8

    # ループ
    if scroll_far >= WIDTH:
        scroll_far -= WIDTH
    if scroll_near >= WIDTH:
        scroll_near -= WIDTH

    # 距離スコア（速度に応じて上がる）
    distance += speed * 0.1

def draw():
    pyxel.cls(0)

    # 背景（空）
    pyxel.rect(0, 0, WIDTH, HEIGHT, 1)

    # 遠景（山っぽい帯）
    draw_looping_band(y=60, h=20, color=3, offset=scroll_far)

    # 近景（草原）
    draw_looping_band(y=90, h=30, color=11, offset=scroll_near)

    # 地面ライン
    pyxel.line(0, 90, WIDTH, 90, 5)

    # プレイヤー（中央固定の四角形）
    pyxel.rect(WIDTH//3, 80, 12, 12, 7)

    # UI
    pyxel.text(5, 5, f"Speed: {speed:.1f}", 7)
    pyxel.text(5, 15, f"Score: {int(distance)}", 7)

def draw_looping_band(y: int, h: int, color: int, offset: float):
    # 幅WIDTHの帯を2枚描くと、左に流れても切れ目が出ない
    x0 = int(-offset)
    pyxel.rect(x0, y, WIDTH, h, color)
    pyxel.rect(x0 + WIDTH, y, WIDTH, h, color)

pyxel.run(update, draw)
```

---

## 🔍 チェックポイント

- スコアがじわじわ増える
- 背景が 2 層で流れる
- 時間で速度が少し上がる

---

## 🔧 チューニングの目安

- 速度の上限と上がる量を小さめにして遊びやすく
- 遠景と近景の倍率（0.3 / 0.8 など）を調整
- 帯の高さ・色を変えて見やすさを優先

---

## 🧪 チャレンジ（余裕があれば）

- 雲（遠景）や木（近景）を追加して見た目を良くする
- スコアで色を変えるなど、達成感の演出を入れる
- 速度の上がり方に段階（レベル）を付けてみる

---

## 💡 今日のポイント

- スコアは「距離＝積み上げ」で作れる
- パララックスは「速さの差」を付けるだけで成立
- 速度は「少しずつ・上限あり」で遊びやすく
