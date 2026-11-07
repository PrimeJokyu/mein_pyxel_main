import pyxel
import random

# ゲームの状態管理用辞書 (class / global 不使用)
state = {
    "snake": [(10, 10), (10, 11), (10, 12)],  # 蛇の体の座標リスト (x, y)。先頭が頭。
    "dir": (0, -1),                          # 現在の移動方向 (dx, dy)。初期値は上。
    "input_queue": [],                       # キー入力のキュー（先行入力管理）
    "food": (5, 5),                          # エサの座標 (x, y)
    "score": 0,                              # 現在のスコア
    "high_score": 0,                         # ハイスコア
    "game_over": False,                      # ゲームオーバーフラグ
    "speed": 8,                              # 更新間隔（フレーム数）
    "frame_count": 0                         # フレームカウンタ
}

# エサをランダムな位置に再配置する関数
def spawn_food():
    if len(state["snake"]) >= 400:
        return
    while True:
        rx = random.randint(0, 19)
        ry = random.randint(0, 19)
        if (rx, ry) not in state["snake"]:
            state["food"] = (rx, ry)
            break

# ゲームを初期状態にリセットする関数
def reset_game():
    state["snake"] = [(10, 10), (10, 11), (10, 12)]
    state["dir"] = (0, -1)
    state["input_queue"] = []
    state["score"] = 0
    state["game_over"] = False
    state["speed"] = 8
    state["frame_count"] = 0
    spawn_food()

# 毎フレームの更新処理
def update():
    if state["game_over"]:
        if pyxel.btnp(pyxel.KEY_SPACE):
            reset_game()
        return

    # 入力の受付（入力キュー方式）
    # ※ 1フレーム内・1移動ステップ内の連続入力で自爆せず、滑らかな先行入力を実現
    last_dir = state["input_queue"][-1] if len(state["input_queue"]) > 0 else state["dir"]
    new_dir = None

    if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W)) and last_dir != (0, 1):
        new_dir = (0, -1)
    elif (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S)) and last_dir != (0, -1):
        new_dir = (0, 1)
    elif (pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A)) and last_dir != (1, 0):
        new_dir = (-1, 0)
    elif (pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D)) and last_dir != (-1, 0):
        new_dir = (1, 0)

    # 先行入力キューに2つまで蓄積可能にする（同じ方向の連続入力は無視）
    if new_dir is not None and new_dir != last_dir and len(state["input_queue"]) < 2:
        state["input_queue"].append(new_dir)

    # 一定フレームごとに移動を実行
    state["frame_count"] += 1
    if state["frame_count"] % state["speed"] == 0:
        # キューから次の移動方向を取り出す
        if len(state["input_queue"]) > 0:
            state["dir"] = state["input_queue"].pop(0)

        dx, dy = state["dir"]
        head_x, head_y = state["snake"][0]
        new_head = (head_x + dx, head_y + dy)

        # 衝突判定：壁との衝突
        if new_head[0] < 0 or new_head[0] >= 20 or new_head[1] < 0 or new_head[1] >= 20:
            state["game_over"] = True
            if state["score"] > state["high_score"]:
                state["high_score"] = state["score"]
            return

        # 衝突判定：自分自身の体との衝突
        # ※ エサを食べないフレームでは尻尾が消えるため、移動前の最後の尾を除外して判定
        body_to_check = state["snake"] if new_head == state["food"] else state["snake"][:-1]
        if new_head in body_to_check:
            state["game_over"] = True
            if state["score"] > state["high_score"]:
                state["high_score"] = state["score"]
            return

        # 頭をリストの先頭に追加
        state["snake"].insert(0, new_head)

        # エサの捕食判定
        if new_head == state["food"]:
            state["score"] += 10
            if state["score"] > state["high_score"]:
                state["high_score"] = state["score"]
            # スピードアップ（上限あり）
            if state["score"] % 30 == 0 and state["speed"] > 3:
                state["speed"] -= 1
            spawn_food()
        else:
            # エサを食べていなければ、尻尾を消すことで前進する
            state["snake"].pop()

# 毎フレームの描画処理
def draw():
    pyxel.cls(0)

    # グリッド描画
    for i in range(1, 20):
        pos = i * 8
        pyxel.line(pos, 0, pos, 160, 5)
        pyxel.line(0, pos, 160, pos, 5)

    # エサの描画
    fx, fy = state["food"]
    pyxel.circ(fx * 8 + 4, fy * 8 + 4, 3, 8)

    # 蛇の体の描画
    for i, (sx, sy) in enumerate(state["snake"]):
        if i == 0:
            pyxel.rect(sx * 8 + 1, sy * 8 + 1, 6, 6, 10)
            dx, dy = state["dir"]
            if dx != 0:
                eye_x = sx * 8 + (5 if dx > 0 else 2)
                pyxel.pset(eye_x, sy * 8 + 2, 7)
                pyxel.pset(eye_x, sy * 8 + 5, 7)
            else:
                eye_y = sy * 8 + (5 if dy > 0 else 2)
                pyxel.pset(sx * 8 + 2, eye_y, 7)
                pyxel.pset(sx * 8 + 5, eye_y, 7)
        else:
            pyxel.rect(sx * 8 + 1, sy * 8 + 1, 6, 6, 11)

    # スコアの描画
    pyxel.text(5, 5, f"SCORE: {state['score']}", 7)
    pyxel.text(100, 5, f"HIGH: {state['high_score']}", 7)

    # ゲームオーバー時の描画
    if state["game_over"]:
        pyxel.rect(20, 50, 120, 60, 0)
        pyxel.rectb(20, 50, 120, 60, 8)
        pyxel.text(60, 60, "GAME OVER", 8)
        pyxel.text(35, 75, f"FINAL SCORE: {state['score']}", 7)
        pyxel.text(30, 95, "PRESS SPACE TO RESTART", 7)

# 初期化と実行
pyxel.init(160, 160, title="Snake Game")
spawn_food()
pyxel.run(update, draw)
