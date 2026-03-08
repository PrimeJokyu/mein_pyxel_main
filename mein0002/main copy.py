import pyxel

FPS = 60
INTERVAL_SEC = 0.2
INTERVAL_FRAMES = int(FPS * INTERVAL_SEC)  # 12

class App:
    def __init__(self):
        pyxel.init(160, 120, fps=FPS)
        pyxel.load("my_game.pyxres")  # 必要なら
        self.anim = 0  # 0/1/2... のコマ番号
        self.num_frames = 4  # アニメーション枚数（例）
        pyxel.run(self.update, self.draw)

    def update(self):
        # 12フレームごとに anim を進める
        self.anim = (pyxel.frame_count // INTERVAL_FRAMES) % self.num_frames

    def draw(self):
        pyxel.cls(0)

        # 例：同じ行に 16x16 のスプライトが横並びで入っている想定
        u = self.anim * 16
        v = 0
        pyxel.blt(72, 52, 0, u, v, 16, 16, 0)

App()
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
pyxel.init(160, 120)
pyxel.load("my_game.pyxres")
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
    pyxel.blt(c["x"], c["y"], 0, sprite_x, sprite_y, 16, 16, 1)

# 使用例
def update():
    update_character()

def draw():
    pyxel.cls(12)
    draw_character()
    
pyxel.run(update, draw)
