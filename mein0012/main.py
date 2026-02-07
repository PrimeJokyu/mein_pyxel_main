import pyxel
import random

W, H = 160, 120
pyxel.init(W, H, title="2分の1ゲート運ゲー")

# ゲーム状態
stage = 1
game_over = False

def new_stage():
    # 正解ゲートをランダムで決定（0=左,1=右）
    global correct_gate
    correct_gate = random.randint(0, 1)

def update():
    global stage, game_over
    if game_over:
        if pyxel.btnp(pyxel.KEY_R):  # Rでリセット
            stage = 1
            game_over = False
            new_stage()
        return

    if pyxel.btnp(pyxel.KEY_LEFT):
        check_gate(0)
    elif pyxel.btnp(pyxel.KEY_RIGHT):
        check_gate(1)

def check_gate(choice):
    global stage, game_over
    if choice == correct_gate:
        stage += 1
        new_stage()
    else:
        game_over = True

def draw():
    pyxel.cls(0)

    # ステージ表示
    pyxel.text(5, 5, f"STAGE: {stage}", 7)
    if game_over:
        pyxel.text(W//2-40, H//2-5, "GAME OVER! Press R", 8)

    # ゲート描画
    gate_w, gate_h = 40, 60
    pyxel.rect(W//4 - gate_w//2, H//2 - gate_h//2, gate_w, gate_h, 7)  # 左
    pyxel.rect(3*W//4 - gate_w//2, H//2 - gate_h//2, gate_w, gate_h, 7)  # 右

    # ゲートラベル
    pyxel.text(W//4 - 6, H//2 - gate_h//2 - 10, "←", 7)
    pyxel.text(3*W//4 - 6, H//2 - gate_h//2 - 10, "→", 7)

# 初期ステージ
new_stage()
pyxel.run(update, draw)
