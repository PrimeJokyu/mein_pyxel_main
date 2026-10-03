# 第8回（2/3）：タイトルとプレイ

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- 状態をタイトルとプレイに分ける
- キーでプレイを始める
- プレイ中だけキャラが動く

前回のファイル: `pyxel_lesson_008_1.md`

---

## 🎮 2. ゲーム状態管理システム

### 2-1. 基本的な状態管理

```python
import pyxel

# ゲーム状態の定義
GAME_STATE_TITLE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_PAUSED = 2
GAME_STATE_GAME_OVER = 3
GAME_STATE_RESULT = 4

# 現在の状態
current_state = GAME_STATE_TITLE
state_timer = 0  # 状態に入ってからの経過時間

def update():
    global current_state, state_timer
    state_timer += 1

    if current_state == GAME_STATE_TITLE:
        update_title()
    elif current_state == GAME_STATE_PLAYING:
        update_playing()
    elif current_state == GAME_STATE_PAUSED:
        update_paused()
    elif current_state == GAME_STATE_GAME_OVER:
        update_game_over()
    elif current_state == GAME_STATE_RESULT:
        update_result()

def draw():
    if current_state == GAME_STATE_TITLE:
        draw_title()
    elif current_state == GAME_STATE_PLAYING:
        draw_playing()
    elif current_state == GAME_STATE_PAUSED:
        draw_paused()
    elif current_state == GAME_STATE_GAME_OVER:
        draw_game_over()
    elif current_state == GAME_STATE_RESULT:
        draw_result()

def change_state(new_state):
    """状態を変更する"""
    global current_state, state_timer
    current_state = new_state
    state_timer = 0  # タイマーリセット
```

### 2-2. 各状態の実装

#### タイトル画面

```python
def update_title():
    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        change_state(GAME_STATE_PLAYING)
        initialize_game()  # ゲーム初期化

def draw_title():
    pyxel.cls(1)

    # タイトルロゴ
    title_text = "COLLECTOR CHALLENGE"
    text_width = len(title_text) * 4
    x = (160 - text_width) // 2
    pyxel.text(x, 40, title_text, 14)

    # 点滅する開始指示
    if (state_timer // 30) % 2:  # 0.5秒ごとに点滅
        pyxel.text(45, 80, "PRESS SPACE TO START", 7)

    # 簡単な背景演出
    for i in range(10):
        x = (state_timer + i * 16) % 180 - 10
        y = 20 + i * 8
        pyxel.pix(x, y, 12)
```

#### ゲームプレイ画面

```python
# ゲーム変数
player = {"x": 80, "y": 100, "score": 0, "lives": 3}
items = []
enemies = []

def initialize_game():
    """ゲーム開始時の初期化"""
    global player, items, enemies
    player = {"x": 80, "y": 100, "score": 0, "lives": 3}
    items = []
    enemies = []

def update_playing():
    # プレイヤー操作
    if pyxel.btn(pyxel.KEY_LEFT) and player["x"] > 0:
        player["x"] -= 2
    if pyxel.btn(pyxel.KEY_RIGHT) and player["x"] < 144:
        player["x"] += 2
    if pyxel.btn(pyxel.KEY_UP) and player["y"] > 0:
        player["y"] -= 2
    if pyxel.btn(pyxel.KEY_DOWN) and player["y"] < 104:
        player["y"] += 2

    # ポーズ機能
    if pyxel.btnp(pyxel.KEY_P):
        change_state(GAME_STATE_PAUSED)

    # アイテム生成
    if state_timer % 60 == 0:  # 1秒ごと
        spawn_item()

    # 敵生成
    if state_timer % 90 == 0:  # 1.5秒ごと
        spawn_enemy()

    # オブジェクト更新
    update_items()
    update_enemies()

    # 当たり判定
    check_collisions()

    # ゲームオーバー判定
    if player["lives"] <= 0:
        change_state(GAME_STATE_GAME_OVER)

def draw_playing():
    pyxel.cls(0)

    # プレイヤー描画
    pyxel.rect(player["x"], player["y"], 16, 16, 11)

    # アイテム描画
    for item in items:
        pyxel.circ(item["x"], item["y"], 4, item["color"])

    # 敵描画
    for enemy in enemies:
        pyxel.rect(enemy["x"], enemy["y"], 12, 12, 8)

    # UI描画
    pyxel.text(5, 5, f"Score: {player['score']}", 7)
    pyxel.text(5, 15, f"Lives: {player['lives']}", 7)
    pyxel.text(130, 5, "P: Pause", 6)
```

---

## この回の確認

- 起動時はタイトル
- キーでプレイに入る
- タイトル中はゲームが動かない

次回は「ポーズとゲームオーバー」です。ファイルは `pyxel_lesson_008_3.md` です。

### AI に聞いてみよう

「状態を文字列で持って、タイトルとプレイでdrawを分ける例を教えて」と聞いてみよう。
