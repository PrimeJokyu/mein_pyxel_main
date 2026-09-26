# 第8回（3/3）：ポーズとゲームオーバー

**全3回の3回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- ポーズで動きを止める
- ゲームオーバーの文字を出す
- やり直すキーを1つ付ける

前回のファイル: `pyxel_lesson_008_2.md`

---

#### ポーズ画面

```python
def update_paused():
    if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_SPACE):
        change_state(GAME_STATE_PLAYING)

    if pyxel.btnp(pyxel.KEY_Q):  # Quit
        change_state(GAME_STATE_TITLE)

def draw_paused():
    # ゲーム画面を暗くして表示
    draw_playing()

    # オーバーレイ
    pyxel.rect(40, 45, 80, 30, 0)
    pyxel.rectb(40, 45, 80, 30, 7)

    pyxel.text(60, 55, "PAUSED", 14)
    pyxel.text(45, 65, "P: Resume  Q: Quit", 7)
```

#### ゲームオーバー画面

```python
def update_game_over():
    if state_timer > 120:  # 2秒後から操作可能
        if pyxel.btnp(pyxel.KEY_R):
            change_state(GAME_STATE_PLAYING)
            initialize_game()
        if pyxel.btnp(pyxel.KEY_Q):
            change_state(GAME_STATE_TITLE)

def draw_game_over():
    pyxel.cls(8)  # 赤い背景

    # ゲームオーバー文字
    pyxel.text(55, 40, "GAME OVER", 7)
    pyxel.text(45, 55, f"Final Score: {player['score']}", 7)

    if state_timer > 120:
        pyxel
```

ゲームオーバー画面の最後は、元の原稿が `pyxel` のところで終わっています。GAME OVER とスコアが表示できれば、この回は完了です。

---

## この回の確認

- ポーズ中は動きが止まる
- GAME OVER とスコアが見える
- ポーズからプレイに戻れる

次回は「スプライトを作る」です。ファイルは `pyxel_lesson_009_1.md` です。

### AI に聞いてみよう

「ポーズ中は、キャラクターの移動だけ止める書き方を教えて」と聞いてみよう。
