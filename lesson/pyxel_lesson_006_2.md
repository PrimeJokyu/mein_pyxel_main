# 第6回（2/3）：辞書とアニメーション

**全3回の2回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- キャラクターの情報を辞書に入れる
- 歩く絵を切り替える
- キーでアニメの種類を変える

前回のファイル: `pyxel_lesson_006_1.md`

---

## 📦 4. オブジェクト指向的設計思考

### 4-1. 辞書を使ったオブジェクトデータ管理

```python
# キャラクター情報を辞書で管理
player = {
    "x": 80,
    "y": 60,
    "hp": 100,
    "mp": 50,
    "level": 1,
    "sprite_x": 0,
    "sprite_y": 0,
    "facing": "right",
    "state": "idle"  # idle, walking, attacking, etc.
}

def update_player():
    if pyxel.btn(pyxel.KEY_LEFT):
        player["x"] -= 2
        player["facing"] = "left"
        player["state"] = "walking"
    elif pyxel.btn(pyxel.KEY_RIGHT):
        player["x"] += 2
        player["facing"] = "right"
        player["state"] = "walking"
    else:
        player["state"] = "idle"

def draw_player():
    # 状態に応じてスプライトを変更
    if player["state"] == "walking":
        # 歩行アニメーション
        frame = (pyxel.frame_count // 10) % 2
        sprite_x = frame * 16
    else:
        # 待機アニメーション
        sprite_x = 0

    # 向きに応じて反転
    width = 16 if player["facing"] == "right" else -16

    pyxel.blt(player["x"], player["y"], 0, sprite_x, 0, width, 16, 0)
```

### 4-2. 複数のオブジェクト管理

```python
# 敵キャラクターのリスト
enemies = [
    {"x": 30, "y": 80, "hp": 30, "type": "slime", "color": 11},
    {"x": 130, "y": 40, "hp": 50, "type": "goblin", "color": 8},
    {"x": 60, "y": 20, "hp": 20, "type": "bat", "color": 13}
]

def update_enemies():
    for enemy in enemies:
        # 敵の種類に応じた行動
        if enemy["type"] == "slime":
            # スライムは左右に移動
            enemy["x"] += pyxel.rndi(-1, 1)
        elif enemy["type"] == "goblin":
            # ゴブリンはプレイヤーに近づく
            if enemy["x"] < player["x"]:
                enemy["x"] += 1
            elif enemy["x"] > player["x"]:
                enemy["x"] -= 1
        elif enemy["type"] == "bat":
            # コウモリは円運動
            import math
            angle = pyxel.frame_count * 0.1
            enemy["x"] = 80 + math.cos(angle) * 30
            enemy["y"] = 60 + math.sin(angle) * 20

def draw_enemies():
    for enemy in enemies:
        # 敵の種類に応じたスプライト表示
        if enemy["type"] == "slime":
            pyxel.blt(enemy["x"], enemy["y"], 0, 16, 0, 16, 16, 0)
        elif enemy["type"] == "goblin":
            pyxel.blt(enemy["x"], enemy["y"], 0, 32, 0, 16, 16, 0)
        elif enemy["type"] == "bat":
            pyxel.blt(enemy["x"], enemy["y"], 0, 48, 0, 16, 16, 0)

        # HPバーの表示
        bar_width = enemy["hp"] // 5
        pyxel.rect(enemy["x"], enemy["y"] - 5, bar_width, 2, 8)
```

---

## 🎬 5. アニメーションシステムの実装

### 5-1. フレームベースアニメーション

```python
# 状態を辞書で管理（クラス不使用）
character = {
    "x": 80,
    "y": 60,
    "animation_frame": 0,
    "animation_speed": 10,
    "current_animation": "idle",
    # アニメーション定義
    "animations": {
        "idle": [(0, 0), (16, 0)],              # 2フレーム
        "walk": [(32, 0), (48, 0), (64, 0)],    # 3フレーム
        "attack": [(80, 0), (96, 0)]            # 2フレーム
    }
}

def update_character():
    c = character
    # アニメーションフレーム更新
    c["animation_frame"] += 1

    # 移動処理
    if pyxel.btn(pyxel.KEY_LEFT):
        c["x"] -= 2
        c["current_animation"] = "walk"
    elif pyxel.btn(pyxel.KEY_RIGHT):
        c["x"] += 2
        c["current_animation"] = "walk"
    elif pyxel.btnp(pyxel.KEY_SPACE):
        c["current_animation"] = "attack"
    else:
        c["current_animation"] = "idle"

def draw_character():
    c = character
    # 現在のアニメーションフレームを取得
    frames = c["animations"][c["current_animation"]]
    frame_index = (c["animation_frame"] // c["animation_speed"]) % len(frames)
    sprite_x, sprite_y = frames[frame_index]
    pyxel.blt(c["x"], c["y"], 0, sprite_x, sprite_y, 16, 16, 0)

# 使用例
def update():
    update_character()

def draw():
    pyxel.cls(12)
    draw_character()
```

### 5-2. 状態管理付きアニメーション

```python
character_states = {
    "hp": 100,
    "state": "idle",
    "state_timer": 0,
    "animation_frame": 0
}

def update_character_state():
    character_states["state_timer"] += 1
    character_states["animation_frame"] += 1

    # 状態遷移の管理
    if character_states["state"] == "idle":
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT):
            character_states["state"] = "walking"
            character_states["state_timer"] = 0
        elif pyxel.btnp(pyxel.KEY_SPACE):
            character_states["state"] = "attacking"
            character_states["state_timer"] = 0

    elif character_states["state"] == "walking":
        if not (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT)):
            character_states["state"] = "idle"
            character_states["state_timer"] = 0

    elif character_states["state"] == "attacking":
        if character_states["state_timer"] > 20:  # 攻撃アニメーション終了
            character_states["state"] = "idle"
            character_states["state_timer"] = 0

def draw_character_with_state():
    state = character_states["state"]
    frame = character_states["animation_frame"]

    if state == "idle":
        sprite_x = (frame // 30) % 2 * 16  # ゆっくりとした呼吸アニメーション
    elif state == "walking":
        sprite_x = (frame // 10) % 3 * 16 + 32  # 歩行アニメーション
    elif state == "attacking":
        sprite_x = (frame // 5) % 4 * 16 + 80   # 高速攻撃アニメーション

    pyxel.blt(player["x"], player["y"], 0, sprite_x, 0, 16, 16, 0)
```

---

---

## この回の確認

- 辞書にxとyがある
- 絵が2枚以上切り替わる
- キーを離すと待機の絵に戻る

次回は「キャラクター図鑑」です。ファイルは `pyxel_lesson_006_3.md` です。

### AI に聞いてみよう

「辞書に入ったフレーム番号で、絵を切り替える短い例を教えて」と聞いてみよう。
