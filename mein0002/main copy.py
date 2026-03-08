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
