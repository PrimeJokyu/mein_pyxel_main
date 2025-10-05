# 第 9 回：確認検定 - ゲーム要素実装の理解度チェック

**～第 2 検定コース～**

## 🎯 検定の目標

- ピクセルアート制作からゲーム状態管理までの技術統合力を評価する
- 創造的なゲーム要素を技術で実現する能力を確認する
- 実用的なゲームシステムの設計・実装スキルを測る

---

## 📋 検定概要

### 検定時間

**60 分間**（スプライト制作 15 分 + プログラミング実技 45 分）

### 検定形式

- **スプライト制作検定**（15 分）
- **プログラミング実技検定**（45 分・3 課題）

### 評価方法

- **技術的正確性**: 各システムが正常に動作するか
- **統合実装能力**: 複数技術の組み合わせ
- **完成度**: バグはないか

### 合格基準

- **スプライト**: テーマに沿った実用的なデザイン完成
- **プログラミング**: 3 課題中 2 課題以上で主要機能が動作
- **統合評価**: 全体として一貫性のあるシステム構築

---

## 🎨 Part 1: スプライト制作検定（15 分）

### 課題内容

指定されたテーマに基づいて、ゲームで使用可能なスプライトセットを制作してください。

### テーマ例

- **「冒険者と魔物」**: プレイヤーキャラ、敵キャラ、アイテム
- **「宇宙探索」**: 宇宙船、宇宙人、惑星、アイテム
- **「海の世界」**: 魚、サンゴ、宝物、海藻

### 制作要件

1. **プレイヤーキャラクター**: 16×16 サイズ（1 フレームでも OK）
2. **敵キャラクター**: 1 種類
3. **アイテム**: 1 種類（用途が分かるデザイン）

### 評価基準

- **テーマ統一性**: 一貫したデザインテーマ
- **視認性**: ゲーム中に判別しやすい明確なデザイン
- **最低限の完成度**: 形や色がはっきりしている

#### AI Tip

- 「AI に『16×16 のプレイヤーを見やすく描くコツ』を聞いてみよう」

### 実制作のヒント

#### スプライト配置の効率化

```
0,0    16,0   32,0   48,0
┌─────┬─────┬─────┬─────┐
│Player│Player│Enemy1│Enemy1│
│Frame1│Frame2│     │     │
├─────┼─────┼─────┼─────┤
│Enemy2│Item1 │Item2 │Item3 │
│     │     │     │     │
├─────┼─────┼─────┼─────┤
│BG1  │BG2  │     │     │
│     │     │     │     │
└─────┴─────┴─────┴─────┘
```

#### アニメーション設計のコツ

- **歩行**: 足の位置を変える（直立 → 左足前 → 直立 → 右足前）
- **待機**: 微細な動き（まばたき、呼吸）
- **敵**: 特徴的な動き（浮遊、震え、回転）

---

## 💻 Part 2: プログラミング実技検定（45 分）

### 課題 A: ランダム生成システム（15 分）

#### 課題内容

ランダムな位置に図形が定期的に出現し、画面に一定数まで表示されるシステムを作成してください。

#### 必須要素

1. **定期生成**: 3 秒（180 フレーム）ごとに円を出す
2. **ランダム**: 位置と色はランダム
3. **上限**: 同時に最大 3 個まで

#### 実装のヒント

```python
import pyxel

circles = []
spawn_timer = 0
MAX_CIRCLES = 3

pyxel.init(160, 120)

def update():
    global spawn_timer

    spawn_timer += 1

    # 3秒ごとに新しい円を生成
    if spawn_timer >= 180:
        spawn_timer = 0
        spawn_circle()

    # 円の数が上限を超えたら古いものを削除
    while len(circles) > MAX_CIRCLES:
        circles.pop(0)  # 最初の要素（最古）を削除

def spawn_circle():
    circle = {
        "x": pyxel.rndi(10, 150),
        "y": pyxel.rndi(10, 110),
        "color": pyxel.rndi(8, 15),
        "size": pyxel.rndi(5, 15)
    }
    circles.append(circle)

def draw():
    pyxel.cls(1)

    # 全ての円を描画
    for circle in circles:
        pyxel.circ(circle["x"], circle["y"], circle["size"], circle["color"])

    # 情報表示
    pyxel.text(5, 5, f"Circles: {len(circles)}", 7)
    pyxel.text(5, 15, f"Timer: {spawn_timer}", 7)

pyxel.run(update, draw)
```

#### チェックポイント

- [ ] 180 フレームごとに円が出る
- [ ] 位置と色がランダム
- [ ] 同時に 3 個まで

#### AI Tip

- 「AI に『ランダムな位置に図形を出す方法（Pyxel）』を聞いてみよう」

---

### 課題 B: 当たり判定ミニゲーム（15 分）

#### 課題内容

プレイヤーキャラクターがアイテムを収集するシンプルなゲームシステムを作成してください。

#### 必須要素

1. **プレイヤー**: 矢印キーで動く四角形
2. **アイテム**: 定期的に生成されて上から落ちる円
3. **当たり判定**: 取ったらスコア+1（表示は任意）

#### 実装のヒント

```python
import pyxel

# プレイヤー
player = {"x": 80, "y": 100, "w": 12, "h": 12}

# ゲーム状態
items = []
score = 0
spawn_timer = 0

pyxel.init(160, 120)

def update():
    global spawn_timer, score

    # プレイヤー移動
    if pyxel.btn(pyxel.KEY_LEFT) and player["x"] > 0:
        player["x"] -= 2
    if pyxel.btn(pyxel.KEY_RIGHT) and player["x"] < 148:
        player["x"] += 2
    if pyxel.btn(pyxel.KEY_UP) and player["y"] > 0:
        player["y"] -= 2
    if pyxel.btn(pyxel.KEY_DOWN) and player["y"] < 108:
        player["y"] += 2

    # アイテム生成
    spawn_timer += 1
    if spawn_timer >= 60:  # 1秒ごと
        spawn_timer = 0
        spawn_item()

    # アイテム更新
    for item in items[:]:
        item["y"] += item["speed"]
        if item["y"] > 120:
            items.remove(item)

    # 当たり判定
    check_collisions()

def spawn_item():
    item = {
        "x": pyxel.rndi(5, 155),
        "y": -5,
        "radius": 6,
        "speed": pyxel.rndf(1, 3),
        "color": pyxel.rndi(9, 15)
    }
    items.append(item)

def check_collisions():
    global score

    player_center_x = player["x"] + player["w"] // 2
    player_center_y = player["y"] + player["h"] // 2

    for item in items[:]:
        # 距離計算（円と矩形の簡易当たり判定）
        dx = abs(item["x"] - player_center_x)
        dy = abs(item["y"] - player_center_y)

        if dx < player["w"]//2 + item["radius"] and dy < player["h"]//2 + item["radius"]:
            score += 1
            items.remove(item)

def draw():
    pyxel.cls(0)

    # プレイヤー描画
    pyxel.rect(player["x"], player["y"], player["w"], player["h"], 11)

    # アイテム描画
    for item in items:
        pyxel.circ(item["x"], item["y"], item["radius"], item["color"])

    # スコア表示
    pyxel.text(5, 5, f"Score: {score}", 7)

pyxel.run(update, draw)
```

#### チェックポイント

- [ ] 矢印キーでプレイヤーが動く
- [ ] アイテムが落ちてくる
- [ ] 取るとスコアが増える

#### AI Tip

- 「AI に『四角形と円の当たり判定を簡単にする方法』を聞いてみよう」

---

### 課題 C: 画面遷移システム（15 分）

#### 課題内容

タイトル画面とゲーム画面を切り替えるシステムを作成してください。

#### 必須要素

1. **タイトル画面**: メッセージを表示
2. **開始**: スペースキーでゲーム画面に切り替え
3. **ゲーム画面**: 矢印キーで四角形を動かせる

#### 実装のヒント

```python
import pyxel

# ゲーム状態
STATE_TITLE = 0
STATE_GAME = 1

current_state = STATE_TITLE
player_x = 80
player_y = 60

pyxel.init(160, 120)

def update():
    global current_state

    if current_state == STATE_TITLE:
        update_title()
    elif current_state == STATE_GAME:
        update_game()

def draw():
    if current_state == STATE_TITLE:
        draw_title()
    elif current_state == STATE_GAME:
        draw_game()

def update_title():
    global current_state, player_x, player_y

    if pyxel.btnp(pyxel.KEY_SPACE):
        current_state = STATE_GAME
        # ゲーム開始時にプレイヤー位置をリセット
        player_x = 80
        player_y = 60

def update_game():
    global current_state, player_x, player_y

    # プレイヤー移動
    if pyxel.btn(pyxel.KEY_LEFT) and player_x > 0:
        player_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT) and player_x < 144:
        player_x += 2
    if pyxel.btn(pyxel.KEY_UP) and player_y > 0:
        player_y -= 2
    if pyxel.btn(pyxel.KEY_DOWN) and player_y < 104:
        player_y += 2

    # タイトル画面に戻る
    if pyxel.btnp(pyxel.KEY_R):
        current_state = STATE_TITLE

def draw_title():
    pyxel.cls(1)

    # タイトル
    pyxel.text(60, 40, "MINI GAME", 14)

    # 開始指示
    pyxel.text(35, 80, "Press SPACE to Start", 7)

def draw_game():
    pyxel.cls(0)

    # プレイヤー
    pyxel.rect(player_x, player_y, 16, 16, 10)

    # 操作説明
    pyxel.text(5, 5, "Arrow keys: Move", 7)
    pyxel.text(5, 15, "R: Return to Title", 7)

pyxel.run(update, draw)
```

#### チェックポイント

- [ ] タイトル画面が表示される
- [ ] スペースキーでゲームが始まる
- [ ] 四角形が動かせる

#### AI Tip

- 「AI に『タイトルとゲームの切り替えを作る最小のコード』を聞いてみよう」

---

## 🏆 評価基準詳細

### スプライト制作評価（40 点）

#### 技術的品質（20 点）

- **解像度・サイズ**: 指定サイズでの正確な制作（5 点）
- **色使い**: 16 色パレットの効果的活用（5 点）
- **アニメーション**: 滑らかで自然な動きのフレーム（5 点）
- **一貫性**: 統一されたアートスタイル（5 点）

#### 創造性・表現力（20 点）

- **テーマ表現**: 指定テーマの的確な表現（5 点）
- **独創性**: オリジナリティのあるデザイン（5 点）
- **ゲーム適性**: ゲームで使いやすいデザイン（5 点）
- **視覚的魅力**: 見た目の美しさ・魅力（5 点）

### プログラミング実技評価（60 点）

#### 課題 A: ランダム生成（20 点）

- **基本機能**: 定期的な円生成（5 点）
- **ランダム要素**: 位置・色のランダム性（5 点）
- **数量制限**: 適切な上限管理（5 点）
- **表示機能**: 情報表示の実装（5 点）

#### 課題 B: 当たり判定ゲーム（20 点）

- **操作制御**: 矢印キーでの移動（5 点）
- **オブジェクト生成**: アイテムの自動生成（5 点）
- **当たり判定**: 正確な衝突検出（5 点）
- **スコアシステム**: スコア計算・表示（5 点）

#### 課題 C: 画面遷移（20 点）

- **状態管理**: 適切な画面状態制御（8 点）
- **画面切り替え**: スムーズな遷移処理（6 点）
- **操作性**: 直感的な操作設計（6 点）

### 統合評価ボーナス（最大 10 点）

- **システム連携**: 複数技術の効果的な組み合わせ
- **コード品質**: 読みやすく保守性の高い実装
- **独創的工夫**: 課題要件を超えた創造的な実装
- **完成度**: ユーザー体験を考慮した完成度

---

## 🚨 よくあるミスと対策

### スプライト制作でのミス

#### ミス 1: サイズ・位置の不正確

```
❌ 間違い: 15×17のサイズで制作
✅ 正解: 正確に16×16で制作
```

#### ミス 2: 色数の過多使用

```
❌ 間違い: 1つのスプライトに10色以上使用
✅ 正解: 3-5色程度に抑えて明確なデザイン
```

#### ミス 3: アニメーションの不自然

```
❌ 間違い: フレーム間の変化が大きすぎる
✅ 正解: 微細で連続性のある変化
```

### プログラミングでのミス

#### ミス 1: リスト操作でのエラー

```python
# ❌ 間違い: 反復中にリスト変更
for item in items:
    if condition:
        items.remove(item)  # エラーの原因

# ✅ 正解: コピーまたは逆順操作
for item in items[:]:  # コピーで安全
    if condition:
        items.remove(item)
```

#### ミス 2: 当たり判定の不正確さ

```python
# ❌ 間違い: 単純な位置比較
if player_x == item_x and player_y == item_y:

# ✅ 正解: 範囲を考慮した判定
if (abs(player_x - item_x) < threshold and
    abs(player_y - item_y) < threshold):
```

#### ミス 3: 状態管理の混乱

```python
# ❌ 間違い: グローバル状態の直接変更
current_state = STATE_GAME

# ✅ 正解: 適切な状態遷移関数
def change_state(new_state):
    global current_state
    current_state = new_state
    initialize_state(new_state)
```

---

## 📊 デバッグ・検定戦略

### 効率的な検定進行

#### 1. 段階的実装（各課題共通）

```python
# Step 1: 最小限の動作確認
def minimal_test():
    pyxel.cls(0)
    pyxel.text(10, 10, "Working!", 7)

# Step 2: 主要機能の追加
def add_main_feature():
    # コア機能を1つずつ追加
    pass

# Step 3: エラーハンドリング
def add_error_handling():
    # 境界条件やエラー処理を追加
    pass
```

#### 2. デバッグ用表示の活用

```python
def draw_debug_info():
    pyxel.text(5, 100, f"State: {current_state}", 6)
    pyxel.text(5, 110, f"Objects: {len(objects)}", 6)
    # リリース前に削除
```

#### 3. 時間管理のコツ

- **15 分＝課題 1 つ**: 完璧より動作を優先
- **5 分余裕**: 最後の検定・調整用
- **機能削減**: 時間不足時は要件の最小構成で

---

## 🎯 検定当日の心構え

### 準備すること

1. **基本関数の復習**: `pyxel.rndi()`, `pyxel.btn()`, `pyxel.blt()`等
2. **テンプレート暗記**: 基本的なゲームループ構造
3. **デバッグ手法**: エラー対処の基本パターン

### 時間配分戦略

- **スプライト制作（15 分）**: 丁寧に、しかし時間厳守
- **課題 A（15 分）**: 確実に動作するものを
- **課題 B（15 分）**: 当たり判定に重点
- **課題 C（15 分）**: 状態遷移の基本を確実に

### メンタル面での注意

- **焦らない**: 落ち着いて一つずつ実装
- **妥協する**: 完璧より動作を優先
- **楽しむ**: 学習の成果を発揮する機会として

---

## 📝 まとめ

### 検定の意義

この検定は、君たちの**ゲーム開発技術の総合力**を確認するものです。

- **技術的基礎**: 個別技術の確実な習得
- **統合力**: 複数技術を組み合わせる能力
- **創造性**: 技術を使って表現する力
- **問題解決力**: 限られた時間での実装能力

### 次のステップへ

検定合格後は、**第 3 サイクル：高度なゲームシステム**に進みます：

- **サウンドシステム**: 音響効果と演出
- **敵の動きパターン**: 高度な AI 実装
- **データ保存システム**: 永続化とプログレッション
- **総合ゲーム制作**: 本格的な作品開発

### 最後のメッセージ

君たちはここまでで、すでに**立派なゲーム開発者**です。今日の検定は、その証明の機会です。

これまでの学習を信じて、自信を持って取り組んでください。技術は身についています。あとは、それを形にするだけです。

頑張って！君たちの実力を存分に発揮してください！ 🌟✨

---

**Good luck! Show us what you've learned!** 🚀🎮
