import pyxel
import random
import math

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
BALL_COUNT = 3  # 球の数を3個に設定

class Ball:
    def __init__(self, other_balls):
        self.r = random.randint(4, 8) # 少し大きめにして見やすく
        self.col = random.randint(1, 15)
        # 質量は面積（半径の2乗）に比例させると自然な挙動になります
        self.m = self.r ** 2 
        
        # 重ならない位置が見つかるまでループして初期位置を決める
        while True:
            self.x = random.randint(self.r, SCREEN_WIDTH - self.r)
            self.y = random.randint(self.r, SCREEN_HEIGHT - self.r)
            
            # 他のボールと重なっていないかチェック
            overlap = False
            for other in other_balls:
                dist = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
                if dist < self.r + other.r:
                    overlap = True
                    break
            if not overlap:
                break

        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # 壁との衝突
        if self.x < self.r:
            self.x = self.r
            self.vx *= -1
        elif self.x > SCREEN_WIDTH - self.r:
            self.x = SCREEN_WIDTH - self.r
            self.vx *= -1

        if self.y < self.r:
            self.y = self.r
            self.vy *= -1
        elif self.y > SCREEN_HEIGHT - self.r:
            self.y = SCREEN_HEIGHT - self.r
            self.vy *= -1

    def draw(self):
        pyxel.circ(self.x, self.y, self.r, self.col)
        # 中心を見やすくするために点を打つ
        pyxel.pset(self.x, self.y, 7)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Colliding Balls")
        
        self.balls = []
        for _ in range(BALL_COUNT):
            # 新しいボールを作るとき、既存のボールリストを渡して重なりを防ぐ
            new_ball = Ball(self.balls)
            self.balls.append(new_ball)

        pyxel.run(self.update, self.draw)

    def resolve_collision(self, b1, b2):
        dx = b2.x - b1.x
        dy = b2.y - b1.y
        dist = math.sqrt(dx*dx + dy*dy)

        # 衝突判定（中心距離 < 半径の和）
        if dist < b1.r + b2.r and dist > 0:
            # 1. 位置の補正（めり込み防止）
            # めり込んでいる分だけお互いを押し戻します
            overlap = (b1.r + b2.r - dist) / 2
            nx = dx / dist  # 衝突の法線ベクトルX
            ny = dy / dist  # 衝突の法線ベクトルY
            
            b1.x -= overlap * nx
            b1.y -= overlap * ny
            b2.x += overlap * nx
            b2.y += overlap * ny

            # 2. 速度の更新（弾性衝突の計算）
            # 相対速度
            dvx = b2.vx - b1.vx
            dvy = b2.vy - b1.vy
            
            # 法線方向の相対速度成分（内積）
            dot_product = dvx * nx + dvy * ny

            # すでに離れようとしている場合は何もしない
            if dot_product > 0:
                return

            # 運動量保存則に基づいた反発係数の計算（質量を考慮）
            # 簡略化のため完全弾性衝突（反発係数e=1）とします
            collision_scale = (2 * dot_product) / (b1.m + b2.m)

            b1.vx += collision_scale * b2.m * nx
            b1.vy += collision_scale * b2.m * ny
            b2.vx -= collision_scale * b1.m * nx
            b2.vy -= collision_scale * b1.m * ny

    def update(self):
        # 個々のボールの移動
        for ball in self.balls:
            ball.update()

        # ボール同士の衝突判定
        # 全てのペアに対してチェックを行います
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                self.resolve_collision(self.balls[i], self.balls[j])

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.balls = []
            for _ in range(BALL_COUNT):
                self.balls.append(Ball(self.balls))

    def draw(self):
        pyxel.cls(0)
        for ball in self.balls:
            ball.draw()

if __name__ == "__main__":
    App()


