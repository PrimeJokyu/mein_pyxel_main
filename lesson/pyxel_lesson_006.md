# 第 6 回：オブジェクト管理とピクセルアート制作

**～本格的なゲームの世界へ！スプライトとオブジェクトをマスターしよう～**

## 🎯 今日のゴール

- Pyxel エディタを使ってピクセルアートを作成できる
- アニメーション付きのキャラクターを実装できる
- 最後に「キャラクター図鑑システム」を作成する

---

## 🎨 1. Pyxel エディタの完全活用

### 1-1. Pyxel エディタの起動方法

```bash
# コマンドプロンプト/ターミナルで実行
pyxel edit my_game.pyxres
```

このコマンドを実行した場所に「my_game.pyxres」が作成されるので、自分のフォルダに移動させる
### 2-2. アニメーション用スプライトの作成

#### 歩行アニメーション（3 フレーム）

```python
# フレーム1: 左足前
# フレーム2: 直立
# フレーム3: 右足前

# プログラムでの切り替え例
walk_frame = (pyxel.frame_count // 15) % 3  # 0.25秒ごとに切り替え
sprite_x = walk_frame * 16  # 横に並べたスプライトを選択
```

---

## 🎮 3. スプライト表示システムの実装

### 3-1. pyxel.blt()関数の詳細

```python
pyxel.blt(描画先x, 描画先y, 画像バンク,
          スプライトx, スプライトy, 幅, 高さ, 透明色)
```

#### パラメータの説明

- **描画先 x, y**: 画面上の描画位置
- **画像バンク**: 0-2 の画像データ（通常は 0 を使用）
- **スプライト x, y**: スプライトシート上の切り出し位置
- **幅, 高さ**: 切り出すサイズ
- **透明色**: 透明として扱う色（省略可能）

### 3-2. 基本的なスプライト表示

```python
import pyxel

pyxel.init(160, 120)
pyxel.load("my_game.pyxres")  # リソースファイルを読み込み

def update():
    pass

def draw():
    pyxel.cls(1)

    # スプライト表示の基本形
    pyxel.blt(50, 50,     # 描画位置
              0,          # 画像バンク0
              0, 0,       # スプライト位置(0,0)
              16, 16,     # サイズ16×16
              0)          # 黒(0)を透明色に

pyxel.run(update, draw)
```

### 3-3. 動的なスプライト表示

```python
import pyxel

player_x = 80
player_y = 60
facing_right = True

pyxel.init(160, 120)
pyxel.load("my_game.pyxres")

def update():
    global player_x, facing_right

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= 2
        facing_right = False
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += 2
        facing_right = True

def draw():
    pyxel.cls(12)

    # 向きに応じてスプライトを反転
    if facing_right:
        pyxel.blt(player_x, player_y, 0, 0, 0, 16, 16, 0)
    else:
        pyxel.blt(player_x, player_y, 0, 0, 0, -16, 16, 0)  # 幅を負数で反転

pyxel.run(update, draw)
```

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

## 🎨 6. 実習課題：「キャラクター図鑑システム」を作ろう！

### 課題内容

様々なキャラクターを表示・切り替えできるシステムを作成しましょう。

### 必須要素

1. **8 種類以上のキャラクタースプライト**: Pyxel エディタで作成
2. **キー操作での切り替え**: 矢印キーや数字キーで選択
3. **キャラクター情報表示**: 名前・HP・特技などの情報
4. **アニメーション**: 選択されたキャラクターが動く

### 実装のヒント

#### ステップ 1: キャラクターデータの準備

```python
import pyxel

# キャラクターデータベース
characters = [
    {
        "name": "Fire Knight",
        "hp": 120,
        "mp": 30,
        "skill": "Fire Slash",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": "Brave warrior with fire sword"
    },
    {
        "name": "Water Mage",
        "hp": 80,
        "mp": 100,
        "skill": "Healing Wave",
        "sprite_x": 16,
        "sprite_y": 0,
        "color": 12,
        "description": "Wise mage who controls water"
    },
    {
        "name": "Wind Archer",
        "hp": 90,
        "mp": 60,
        "skill": "Wind Arrow",
        "sprite_x": 32,
        "sprite_y": 0,
        "color": 11,
        "description": "Swift archer with wind power"
    },
    # ... 他のキャラクターも追加
]

current_character = 0
pyxel.init(160, 120)
# pyxel.load("characters.pyxres")  # リソースファイルを読み込み
```

#### ステップ 2: キャラクター選択システム

```python
def update():
    global current_character

    # 左右でキャラクター切り替え
    if pyxel.btnp(pyxel.KEY_LEFT):
        current_character = (current_character - 1) % len(characters)
    if pyxel.btnp(pyxel.KEY_RIGHT):
        current_character = (current_character + 1) % len(characters)

    # 数字キーで直接選択
    for i in range(min(8, len(characters))):
        if pyxel.btnp(ord(str(i + 1))):
            current_character = i
```

#### ステップ 3: 表示システム

```python
def draw():
    pyxel.cls(1)

    # 選択中のキャラクター情報を取得
    char = characters[current_character]

    # キャラクタースプライト表示（アニメーション付き）
    animation_frame = (pyxel.frame_count // 15) % 2
    sprite_x = char["sprite_x"] + animation_frame * 16

    # 中央に大きく表示
    pyxel.blt(72, 40, 0, sprite_x, char["sprite_y"], 16, 16, 0)

    # キャラクター情報表示
    pyxel.text(10, 10, f"Character: {current_character + 1}/{len(characters)}", 7)
    pyxel.text(10, 25, char["name"], char["color"])
    pyxel.text(10, 40, f"HP: {char['hp']}", 8)
    pyxel.text(10, 50, f"MP: {char['mp']}", 12)
    pyxel.text(10, 60, f"Skill: {char['skill']}", 10)
    pyxel.text(10, 80, char["description"], 6)

    # 操作説明
    pyxel.text(10, 100, "← → : Select", 7)
    pyxel.text(10, 110, "1-8 : Direct", 7)

    # キャラクター一覧（小さく表示）
    for i, c in enumerate(characters[:8]):
        x = 120 + (i % 4) * 10
        y = 80 + (i // 4) * 10
        color = 14 if i == current_character else 6
        pyxel.rect(x, y, 8, 8, color)
```

### 応用チャレンジ

#### 詳細表示モード

```python
detail_mode = False

def update():
    global detail_mode

    # Enterキーで詳細表示切り替え
    if pyxel.btnp(pyxel.KEY_ENTER):
        detail_mode = not detail_mode

def draw():
    if detail_mode:
        # 詳細情報の表示
        char = characters[current_character]

        pyxel.cls(0)
        pyxel.text(10, 10, f"=== {char['name']} ===", 14)

        # ステータス詳細
        pyxel.text(10, 30, "STATUS:", 7)
        pyxel.text(10, 45, f"Health Points: {char['hp']}", 8)
        pyxel.text(10, 55, f"Magic Points : {char['mp']}", 12)
        pyxel.text(10, 65, f"Special Skill: {char['skill']}", 10)

        # 大きなスプライト表示
        pyxel.blt(100, 30, 0, char["sprite_x"], char["sprite_y"], 32, 32, 0)

        pyxel.text(10, 100, "ENTER: Back to list", 6)
    else:
        # 通常の一覧表示
        # ... 前述のコード
```

#### お気に入り機能

```python
favorites = []

def update():
    global favorites

    # Fキーでお気に入りに追加/削除
    if pyxel.btnp(pyxel.KEY_F):
        if current_character in favorites:
            favorites.remove(current_character)
        else:
            favorites.append(current_character)

def draw():
    # ... 通常の描画 ...

    # お気に入りマーク
    if current_character in favorites:
        pyxel.text(100, 25, "★ FAVORITE", 10)

    # お気に入り一覧
    pyxel.text(10, 70, f"Favorites: {len(favorites)}", 14)
    for i, fav_id in enumerate(favorites[:5]):
        pyxel.text(80 + i * 15, 70, str(fav_id + 1), 14)
```

---

## 🎮 7. ゲームオブジェクトの設計パターン

### 7-1. アイテムシステム

```python
items = [
    {
        "name": "Health Potion",
        "effect": "hp",
        "value": 50,
        "sprite_x": 0,
        "sprite_y": 16,
        "rarity": "common",
        "price": 100
    },
    {
        "name": "Magic Crystal",
        "effect": "mp",
        "value": 30,
        "sprite_x": 16,
        "sprite_y": 16,
        "rarity": "rare",
        "price": 300
    }
]

player_inventory = []

def use_item(item_index):
    if item_index < len(player_inventory):
        item = player_inventory[item_index]

        if item["effect"] == "hp":
            player["hp"] = min(player["hp"] + item["value"], 100)
        elif item["effect"] == "mp":
            player["mp"] = min(player["mp"] + item["value"], 100)

        # アイテム消費
        player_inventory.pop(item_index)

def draw_inventory():
    pyxel.text(5, 5, "INVENTORY", 7)

    for i, item in enumerate(player_inventory[:10]):
        y = 20 + i * 10

        # アイテムスプライト
        pyxel.blt(5, y, 0, item["sprite_x"], item["sprite_y"], 8, 8, 0)

        # アイテム名
        pyxel.text(15, y, item["name"], 7)

        # レアリティ色分け
        rarity_colors = {"common": 7, "rare": 10, "epic": 14}
        pyxel.text(15, y + 5, item["rarity"], rarity_colors[item["rarity"]])
```

### 7-2. 敵の行動パターン管理

```python
enemy_patterns = {
    "patrol": {
        "move_range": 50,
        "speed": 1,
        "behavior": "back_and_forth"
    },
    "chase": {
        "detection_range": 80,
        "speed": 1.5,
        "behavior": "follow_player"
    },
    "guard": {
        "position": "fixed",
        "attack_range": 30,
        "behavior": "ranged_attack"
    }
}

def update_enemy_by_pattern(enemy):
    pattern = enemy_patterns[enemy["pattern"]]

    if pattern["behavior"] == "back_and_forth":
        if not hasattr(enemy, "direction"):
            enemy["direction"] = 1

        enemy["x"] += pattern["speed"] * enemy["direction"]

        if enemy["x"] <= enemy["start_x"] - pattern["move_range"] or \
           enemy["x"] >= enemy["start_x"] + pattern["move_range"]:
            enemy["direction"] *= -1

    elif pattern["behavior"] == "follow_player":
        distance = abs(enemy["x"] - player["x"]) + abs(enemy["y"] - player["y"])

        if distance <= pattern["detection_range"]:
            if enemy["x"] < player["x"]:
                enemy["x"] += pattern["speed"]
            elif enemy["x"] > player["x"]:
                enemy["x"] -= pattern["speed"]
```

---

## 🏆 8. チェックポイント

### ✅ 基本機能チェック

- [ ] Pyxel エディタでスプライトを作成できる
- [ ] pyxel.blt()でスプライトを表示できる
- [ ] キー操作でキャラクターを切り替えられる
- [ ] キャラクター情報が正しく表示される

### ✅ 技術要素チェック

- [ ] 辞書を使ってオブジェクトデータを管理している
- [ ] リストを使って複数のオブジェクトを扱っている
- [ ] アニメーション機能が実装されている
- [ ] スプライトの切り替えが滑らかに動作する

---

## 📝 9. まとめ

### 今日学んだこと

- **Pyxel エディタの活用**: 本格的なピクセルアート制作
- **スプライトシステム**: `pyxel.blt()`を使った画像表示
- **オブジェクト管理**: 辞書とリストによる効率的なデータ管理
- **アニメーション**: フレームベースの動的表現
- **設計思想**: 拡張性を考慮したプログラム構造

### 重要なポイント

- **データ構造の重要性**: 適切なデータ管理がプログラムの品質を決める
- **再利用性**: 同じコードで多くのオブジェクトを扱う効率性
- **視覚的表現力**: スプライトによるリッチな表現の可能性
- **ユーザー体験**: 見た目の美しさが操作の楽しさにつながる

今日の学習で、ゲーム開発の本格的な入口に立ちました。スプライトとオブジェクト管理は、これから作るすべての作品の基礎になる重要な技術です。しっかりと復習して、次回の挑戦に備えましょう！ 🎨✨
