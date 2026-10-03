# 第6回（3/3）：キャラクター図鑑

**全3回の3回目。このファイルが、授業1回（40分）です。**

## この回のゴール

- キャラを2人以上のデータにする
- 左右キーで選ぶ
- 名前と数値を表示する

前回のファイル: `pyxel_lesson_006_2.md`

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

---

## この回の確認

- キャラを切り替えられる
- 名前が見える
- 今選んでいるキャラが分かる

次回は「ランダムとリスト」です。ファイルは `pyxel_lesson_007_1.md` です。

### AI に聞いてみよう

「リストの中の辞書を、左右キーで切り替える書き方を教えて」と聞いてみよう。
