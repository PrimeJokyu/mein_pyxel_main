import pyxel
import random

# ゲームの状態管理用辞書
state = {
    "snake": [(10, 10), (10, 11), (10, 12)],  # 蛇の体の座標リスト (x, y)。先頭が頭。
    "dir": (0, -1),                          # 移動方向 (dx, dy)。初期値は上。
    "next_dir": (0, -1),                     # 次のフレームで適用する方向（先行入力用）
    "food": (5, 5),                          # エサの座標 (x, y)
    "score": 0,                              # 現在のスコア
    "high_score": 0,                         # ハイスコア
    "game_over": False,                      # ゲームオーバーフラグ
    "speed": 8,                              # 更新間隔（フレーム数、小さいほど速い）
    "frame_count": 0                         # フレームカウンタ
}

# エサをランダムな位置に再配置する関数
def spawn_food():
    while True:
        rx = random.randint(0, 19)
        ry = random.randint(0, 19)
        # 蛇の体と重ならない位置に配置
        if (rx, ry) not in state["snake"]:
            state["food"] = (rx, ry)
            break

# ゲームを初期状態にリセットする関数
def reset_game():
    state["snake"] = [(10, 10), (10, 11), (10, 12)]
    state["dir"] = (0, -1)
    state["next_dir"] = (0, -1)
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

    # 入力の受付（現在の進行方向と逆方向には進めないようにする）
    # ※ globalを使わず、stateの辞書を直接更新する
    current_dir = state["dir"]
    if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W)) and current_dir != (0, 1):
        state["next_dir"] = (0, -1)
    elif (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S)) and current_dir != (0, -1):
        state["next_dir"] = (0, 1)
    elif (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A)) and current_dir != (1, 0):
        state["next_dir"] = (-1, 0)
    elif (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)) and current_dir != (-1, 0):
        state["next_dir"] = (1, 0)

    # 一定フレームごとに移動を実行
    state["frame_count"] += 1
    if state["frame_count"] % state["speed"] == 0:
        # 進行方向を確定する
        state["dir"] = state["next_dir"]
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
        if new_head in state["snake"]:
            state["game_over"] = True
            if state["score"] > state["high_score"]:
                state["high_score"] = state["score"]
            return

        # 頭をリストの先頭に追加
        state["snake"].insert(0, new_head)

        # エサの捕食判定
        if new_head == state["food"]:
            state["score"] += 10
            # スピードアップ（上限あり）
            if state["score"] % 30 == 0 and state["speed"] > 3:
                state["speed"] -= 1
            spawn_food()
        else:
            # エサを食べていなければ、尻尾を消すことで前進する
            state["snake"].pop()

# 毎フレームの描画処理
def draw():
    # 画面クリア（黒）
    pyxel.cls(0)

    # グリッドの枠線を描画（うっすらとしたグレーで境界線を分かりやすく）
    # ※1マスは8ピクセル。20x20マスなので、8の倍数で線を引く
    for i in range(1, 20):
        pos = i * 8
        # 点線または薄い色でグリッド線を描く (カラー5: 暗いグレー)
        pyxel.line(pos, 0, pos, 160, 5)
        pyxel.line(0, pos, 160, pos, 5)

    # エサの描画（赤色、丸）
    fx, fy = state["food"]
    pyxel.circ(fx * 8 + 4, fy * 8 + 4, 3, 8)

    # 蛇の体の描画
    # 体は緑（カラー11）
    for i, (sx, sy) in enumerate(state["snake"]):
        if i == 0:
            # 頭は少し違う色（カラー10: 黄緑）で描画し、目を描く
            pyxel.rect(sx * 8 + 1, sy * 8 + 1, 6, 6, 10)
            # 進行方向に応じて目を描く
            dx, dy = state["dir"]
            if dx != 0: # 左右移動
                pyxel.pset(sx * 8 + 4, sy * 8 + 2, 7)
                pyxel.pset(sx * 8 + 4, sy * 8 + 5, 7)
            else: # 上下移動
                pyxel.pset(sx * 8 + 2, sy * 8 + 4, 7)
                pyxel.pset(sx * 8 + 5, sy * 8 + 4, 7)
        else:
            pyxel.rect(sx * 8 + 1, sy * 8 + 1, 6, 6, 11)

    # スコアの描画
    pyxel.text(5, 5, f"SCORE: {state['score']}", 7)
    pyxel.text(100, 5, f"HIGH: {state['high_score']}", 7)

    # ゲームオーバー時の描画
    if state["game_over"]:
        # 半透明っぽく見せるための暗幕（実際には黒い矩形などを重ねる）
        pyxel.rect(20, 50, 120, 60, 0)
        pyxel.rectb(20, 50, 120, 60, 8) # 赤い枠線
        pyxel.text(60, 60, "GAME OVER", 8)
        pyxel.text(35, 75, f"FINAL SCORE: {state['score']}", 7)
        pyxel.text(30, 95, "PRESS SPACE TO RESTART", 7)

# 初期化と実行
pyxel.init(160, 160, title="Snake Game")
# 初期のエサを配置
spawn_food()
pyxel.run(update, draw)
