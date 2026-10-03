import pyxel
import random

# ==========================================
# 1. ゲームの設定と状態管理
# ==========================================
WINDOW_WIDTH = 200      # 画面の横幅
WINDOW_HEIGHT = 150     # 画面の縦幅
BLOCK_SIZE = 10         # 蛇と餌の1ブロックのサイズ
FPS = 10                # 1秒間の画面更新回数

COLOR_BLACK = 0         # 背景色
COLOR_WHITE = 7         # 文字の色
COLOR_GREEN = 11        # 蛇の色
COLOR_RED = 8           # 餌の色

# ゲームの状態管理辞書 (global不使用)
state = {
    "snake_head": [100, 70],
    "snake_body": [[100, 70], [90, 70], [80, 70]],
    "direction": "RIGHT",
    "change_to": "RIGHT",
    "food_pos": [0, 0],
    "is_game_over": False
}

# ==========================================
# 2. ゲームの処理をまとめた関数
# ==========================================

def generate_food():
    """新しい餌をランダムな位置に生成する関数"""
    while True:
        food_x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
        food_y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
        
        if [food_x, food_y] not in state["snake_body"]:
            state["food_pos"] = [food_x, food_y]
            break

def init_game():
    """ゲームの初期状態をセットする関数"""
    state["snake_head"] = [100, 70]
    state["snake_body"] = [[100, 70], [100 - BLOCK_SIZE, 70], [100 - BLOCK_SIZE * 2, 70]]
    state["direction"] = "RIGHT"
    state["change_to"] = "RIGHT"
    state["is_game_over"] = False
    generate_food()

def move_snake():
    """指定された方向に蛇の頭を移動させる関数"""
    x, y = state["snake_head"]
    
    # 進行方向の更新（真逆には進めない制限）
    if state["change_to"] == "UP" and state["direction"] != "DOWN":
        state["direction"] = "UP"
    elif state["change_to"] == "DOWN" and state["direction"] != "UP":
        state["direction"] = "DOWN"
    elif state["change_to"] == "LEFT" and state["direction"] != "RIGHT":
        state["direction"] = "LEFT"
    elif state["change_to"] == "RIGHT" and state["direction"] != "LEFT":
        state["direction"] = "RIGHT"
    
    # 方向に応じて座標を変化
    if state["direction"] == "UP":
        y -= BLOCK_SIZE
    elif state["direction"] == "DOWN":
        y += BLOCK_SIZE
    elif state["direction"] == "LEFT":
        x -= BLOCK_SIZE
    elif state["direction"] == "RIGHT":
        x += BLOCK_SIZE
        
    state["snake_head"] = [x, y]

def check_collision():
    """壁や自分自身との衝突を判定する関数"""
    x, y = state["snake_head"]
    
    # 壁との衝突判定
    if x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT:
        state["is_game_over"] = True
        
    # 自分自身との衝突判定
    if state["snake_head"] in state["snake_body"][1:]:
        state["is_game_over"] = True

def update():
    """毎フレームの更新処理"""
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
        
    if state["is_game_over"]:
        if pyxel.btnp(pyxel.KEY_R):
            init_game()
        return

    if pyxel.btnp(pyxel.KEY_R):
        init_game()
        
    # キーボードの入力処理
    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
        state["change_to"] = "UP"
    elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
        state["change_to"] = "DOWN"
    elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
        state["change_to"] = "LEFT"
    elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
        state["change_to"] = "RIGHT"
        
    move_snake()
    state["snake_body"].insert(0, list(state["snake_head"]))
    
    # 餌の捕食判定
    if state["snake_head"] == state["food_pos"]:
        generate_food()
    else:
        state["snake_body"].pop()
        
    check_collision()

def draw():
    """毎フレームの画面描画"""
    pyxel.cls(COLOR_BLACK)
    
    # 蛇の体の描画
    for block in state["snake_body"]:
        pyxel.rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE, COLOR_GREEN)
        
    # 餌の描画
    pyxel.rect(state["food_pos"][0], state["food_pos"][1], BLOCK_SIZE, BLOCK_SIZE, COLOR_RED)
    
    # ゲームオーバー画面
    if state["is_game_over"]:
        pyxel.text(80, 60, "GAME OVER", COLOR_WHITE)
        pyxel.text(50, 75, "PRESS R TO RESTART", COLOR_WHITE)

# ==========================================
# 3. メイン処理
# ==========================================
if __name__ == "__main__":
    pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="シンプルな蛇ゲーム（Pyxel版）", fps=FPS)
    init_game()
    pyxel.run(update, draw)
