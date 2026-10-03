# 第11回（3/3）：簡単ピアノ

**全3回の3回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- キーで違う音を鳴らす
- 画面に操作の案内を出す
- 押していないキーでは音が鳴らない

前回のファイル: `pyxel_lesson_011_2.md`

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

---

## この回の確認

- 3つのキーで違う音が鳴る
- 画面に操作が見える
- 音が鳴りっぱなしにならない

次回は「敵の基本の動き」です。ファイルは `pyxel_lesson_012_1.md` です。

### AI に聞いてみよう

「数字キーごとに違う音を鳴らすifを、3つまで書いて」と聞いてみよう。
