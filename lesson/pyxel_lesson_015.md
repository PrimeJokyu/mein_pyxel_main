# 第 15 回：【アウトプット】ミニゲーム制作プロジェクト

**～サウンド・敵の動き・データ管理を使った楽しいゲームを作ろう！～**

## 🎯 今日のゴール

- 第 11 ～ 13 回で学んだ技術を統合したオリジナルミニゲームを完成させる
- サウンド・敵の動き・データ管理を効果的に組み合わせる
- 50 分間で完成度の高い作品を制作する
- 他の人の作品をプレイして相互に学び合う

---

## ⏰ 制作スケジュール

**制作時間**: 40 分  
**発表時間**: 10 分（全員でプレイ・感想交流）

### 時間配分の目安

- **企画・設計**: 10 分
- **基本システム実装**: 20 分
- **機能追加・調整**: 5 分
- **最終調整・テスト**: 5 分

---

## 🎮 必須実装要素

### 基本要件（必ず含める）

1. **自作スプライト（3 種類以上）**

   - プレイヤー、敵、アイテムなど
   - Pyxel エディタで作成したオリジナルスプライト

2. **効果音・BGM（どちらか 1 つで OK）**

   - アクション時の効果音 OR 背景音楽
   - 最低 1 つは音響効果を含める

3. **動く敵キャラクター（1 体以上）**

   - 何らかの動作パターンを持つ敵
   - プレイヤーとの相互作用がある

4. **スコア表示**

   - ゲーム中の進行状況が分かる数値
   - 点数、時間、ライフなど

5. **簡単なゲーム画面遷移**
   - 最低限：タイトル画面 → ゲーム画面
   - できれば：ゲームオーバー画面も

---

## 🎨 ゲームテーマ例

### テーマ 1：「よけろゲーム」

**コンセプト**: 敵を避けながらアイテム収集

#### 基本システム

- プレイヤー：矢印キーで移動
- 敵：自動で移動（複数体）
- アイテム：ランダム出現
- ルール：敵に当たるとライフ減少、アイテムでスコア増加

#### 実装のヒント

```python
import pyxel
import random

player_x = 80
player_y = 100
enemies = []
items = []
score = 0
life = 3

# 敵を初期配置
for i in range(3):
    enemies.append({
        'x': random.randint(0, 160),
        'y': random.randint(0, 50),
        'dx': random.choice([-1, 1]),
        'dy': 1
    })

def update_enemies():
    for enemy in enemies:
        enemy['x'] += enemy['dx']
        enemy['y'] += enemy['dy']

        # 画面端で跳ね返り
        if enemy['x'] <= 0 or enemy['x'] >= 160:
            enemy['dx'] = -enemy['dx']

        # 下端で上に戻す
        if enemy['y'] > 120:
            enemy['y'] = 0
            enemy['x'] = random.randint(0, 160)
```

### テーマ 2：「音楽アクション」

**コンセプト**: 音に合わせてキャラクターを操作

#### 基本システム

- BGM 再生中
- 数字キー 1 ～ 4 で異なるアクション
- 音のタイミングに合わせて高得点
- ミスすると音が止まる

### テーマ 3：「追いかけっこ」

**コンセプト**: プレイヤーか敵、どちらかが追いかける

#### 基本システム

- 敵がプレイヤーを追跡
- プレイヤーは逃げながらアイテム収集
- 捕まると役割が逆転
- 時間制限あり

### テーマ 4：「コレクションゲーム」

**コンセプト**: 制限時間内にアイテム集め

#### 基本システム

- 様々な種類のアイテムが出現
- アイテムごとに点数が異なる
- 障害物（敵）が邪魔をする
- 時間切れでゲーム終了

---

## 🛠️ 実装サンプル：基本ゲーム構造

### ゲーム状態管理

```python
import pyxel
import random
import math

state = "title"  # "title", "game", "gameover"
player_x, player_y, player_life = 80, 60, 3
score, timer = 0, 1800
enemies, items = [], []

pyxel.init(160, 120, title="My Mini Game")
pyxel.sound(0).set("c3e3g3c4", "t", "7", "n", 10)
pyxel.sound(1).set("f2d2a2f2", "s", "6", "n", 20)

def spawn_enemy():
    enemies.append({
        'x': random.randint(0, 160),
        'y': random.randint(0, 60),
        'dx': random.choice([-1, 1]),
        'dy': random.randint(1, 2),
        'type': random.choice(['chaser', 'patrol'])
    })

def reset_game():
    global player_x, player_y, player_life, score, timer, enemies, items
    player_x, player_y, player_life = 80, 60, 3
    score, timer = 0, 1800
    enemies, items = [], []
    for _ in range(3):
        spawn_enemy()

def update():
    global state, player_x, player_y, player_life, score, timer
    if state == "title":
        if pyxel.btnp(pyxel.KEY_SPACE):
            state = "game"
            reset_game()
        return

    if state == "game":
        # player move
        if pyxel.btn(pyxel.KEY_LEFT):
            player_x = max(8, player_x - 2)
        if pyxel.btn(pyxel.KEY_RIGHT):
            player_x = min(152, player_x + 2)
        if pyxel.btn(pyxel.KEY_UP):
            player_y = max(8, player_y - 2)
        if pyxel.btn(pyxel.KEY_DOWN):
            player_y = min(112, player_y + 2)

        update_enemies()
        update_items()
        check_collisions()

        timer -= 1
        if timer <= 0 or player_life <= 0:
            state = "gameover"
        return

    if state == "gameover":
        if pyxel.btnp(pyxel.KEY_SPACE):
            state = "title"

def draw():
    pyxel.cls(1)
    if state == "title":
        pyxel.text(60, 40, "MY MINI GAME", 7)
        pyxel.text(55, 60, "Press SPACE to Start", 6)
        pyxel.text(45, 80, "Arrow Keys: Move", 5)
        pyxel.text(45, 90, "Avoid enemies, Get items!", 5)
        return

    if state == "game":
        pyxel.circfill(player_x, player_y, 6, 12)
        pyxel.circ(player_x, player_y, 6, 1)
        for enemy in enemies:
            color = 8 if enemy['type'] == 'chaser' else 4
            pyxel.circfill(int(enemy['x']), int(enemy['y']), 5, color)
        for item in items:
            if item['type'] == 'coin':
                pyxel.circfill(int(item['x']), int(item['y']), 3, 10)
            elif item['type'] == 'gem':
                pyxel.rectfill(int(item['x'])-2, int(item['y'])-2, 4, 4, 14)
            elif item['type'] == 'star':
                pyxel.pset(int(item['x']), int(item['y'])-3, 7)
                pyxel.pset(int(item['x'])-2, int(item['y'])+1, 7)
                pyxel.pset(int(item['x'])+2, int(item['y'])+1, 7)
        pyxel.text(5, 5, f"Score: {score}", 7)
        pyxel.text(5, 15, f"Life: {player_life}", 7)
        pyxel.text(100, 5, f"Time: {timer//60}", 7)
        return

    if state == "gameover":
        pyxel.text(65, 40, "GAME OVER", 8)
        pyxel.text(55, 60, f"Final Score: {score}", 7)
        pyxel.text(50, 80, "Press SPACE to Return", 6)

pyxel.run(update, draw)
```

---

## 🎵 サウンド実装のコツ

### 効果音パターン

```python
# アイテム取得音（明るい音）
pyxel.sound(0).set("c4e4g4c5", "t", "7", "n", 10)

# ダメージ音（低い音）
pyxel.sound(1).set("f2d2a1f2", "s", "6", "n", 20)

# ゲームオーバー音（悲しい音）
pyxel.sound(2).set("c4a3f3d3", "t", "5", "n", 30)

# レベルクリア音（華やかな音）
pyxel.sound(3).set("c4d4e4f4g4a4b4c5", "t", "7", "n", 5)
```

### BGM 実装例

```python
# シンプルなループBGM
pyxel.sound(0).set("c3c3g3g3a3a3g3f3f3e3e3d3d3c3", "t", "6", "n", 8)

def update():
    # BGMのループ再生
    if not pyxel.play_pos(0):  # チャンネル0で何も再生していない場合
        pyxel.play(0, 0, loop=True)
```

---

## 👾 敵の動きパターン集

### 基本パターン

```python
# 1. 直線移動
enemy['x'] += enemy['dx']
enemy['y'] += enemy['dy']

# 2. 跳ね返り移動
enemy['x'] += enemy['dx']
if enemy['x'] <= 0 or enemy['x'] >= 160:
    enemy['dx'] = -enemy['dx']

# 3. プレイヤー追跡
if enemy['x'] < player_x:
    enemy['x'] += 1
elif enemy['x'] > player_x:
    enemy['x'] -= 1

# 4. ランダム移動
if random.randint(1, 30) == 1:  # 1/30の確率で方向変更
    enemy['dx'] = random.choice([-2, -1, 0, 1, 2])
    enemy['dy'] = random.choice([-2, -1, 0, 1, 2])

# 5. 円運動
enemy['angle'] += 0.1
enemy['x'] = center_x + math.cos(enemy['angle']) * radius
enemy['y'] = center_y + math.sin(enemy['angle']) * radius
```

---

## 📊 データ管理のテクニック

### スコアシステム

```python
score_state = {"score": 0, "multiplier": 1, "combo": 0}

def add_score(points, item_type="normal"):
    s = score_state
    base_points = points * s["multiplier"]
    if item_type == "combo":
        s["combo"] += 1
        base_points *= s["combo"]
    else:
        s["combo"] = 0
    s["score"] += base_points
    if s["score"] > 1000:
        s["multiplier"] = 2
```

### 統計情報

```python
stats = {"items_collected": 0, "enemies_avoided": 0, "time_survived": 0, "max_combo": 0}

def stats_update():
    stats["time_survived"] += 1

def show_results():
    pyxel.text(10, 40, f"Items: {stats['items_collected']}", 7)
    pyxel.text(10, 50, f"Time: {stats['time_survived']//60}s", 7)
    pyxel.text(10, 60, f"Max Combo: {stats['max_combo']}", 7)
```

---

## 🎨 発表形式

### 個人発表（各自 3 分）

#### 1. 作品タイトル・概要紹介（30 秒）

- ゲーム名
- 基本的な遊び方
- 特徴・面白さ

#### 2. ライブデモンストレーション（2 分）

- 実際にプレイして見せる
- 主要機能の実演
- おもしろポイントの紹介

#### 3. 工夫点の説明（30 秒）

- 「ここを頑張った！」ポイント
- 実装で苦労した部分
- 技術的な工夫

### 相互プレイタイム（10 分）

- 他の人の作品を実際にプレイ
- 感想やアドバイスの交換
- 「最も面白かった作品」投票

---

## 📝 評価ポイント

### 完成度（40 点）

- 基本機能がちゃんと動作する
- ゲームとして成立している
- エラーが少ない

### 楽しさ（25 点）

- プレイしていて面白い
- やりこみ要素がある
- 操作感が良い

### 技術活用（25 点）

- 学んだ技術を効果的に使用
- サウンド・敵・データ管理の統合
- コードが整理されている

### 独創性（10 点）

- オリジナルなアイデア
- 予想を超える表現
- 個性的な世界観

---

## 💡 制作のコツ

### 企画段階

1. **シンプルから始める**: 複雑すぎる企画は時間内に完成しない
2. **核となる面白さを決める**: 「何が楽しいのか」を明確に
3. **技術要件を確認**: 必須要素をリストアップ

### 実装段階

1. **動く最小版を先に作る**: 基本動作 → 機能追加の順番
2. **こまめにテスト**: 少し作ったら動作確認
3. **時間配分を意識**: 完璧を目指さず、完成を優先

### 調整段階

1. **バランス調整**: 難しすぎ・簡単すぎを修正
2. **演出の追加**: 音や視覚効果で楽しさアップ
3. **バグ修正**: 最後に動作チェック

---

## 🚀 発展課題（時間があれば）

### レベルアップ要素

- ハイスコア保存機能
- 複数のゲームモード
- プレイヤー名入力
- 実績・トロフィー機能

### 視覚効果

- パーティクル効果（爆発、キラキラ）
- 画面シェイク
- 色変化エフェクト

### ゲームプレイ

- パワーアップアイテム
- ボス敵の登場
- ステージ進行システム

---

## 🎉 まとめ

今日は第 3 サイクルの集大成として、これまで学んだ技術を自由に組み合わせてオリジナルゲームを作成しました。
