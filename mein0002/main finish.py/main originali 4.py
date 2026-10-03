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