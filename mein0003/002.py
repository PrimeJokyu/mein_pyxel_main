import pyxel
import math

W, H = 160, 120

# position
ball1_x, ball1_y = 30, 60
ball2_x, ball2_y = 80, 30
ball3_x, ball3_y = 130, 90

# velocity（元の動きを維持）
ball1_dx, ball1_dy = 2, 0
ball2_dx, ball2_dy = 0, 3
ball3_dx, ball3_dy = -1, -2

# radius
r1, r2, r3 = 8, 6, 4

pyxel.init(W, H)

def bounce_wall(x, y, dx, dy, r):
    # 半径を考慮して壁で反射
    if x - r <= 0 or x + r >= W:
        dx = -dx
    if y - r <= 0 or y + r >= H:
        dy = -dy
    return dx, dy

def collide_and_flip(x1, y1, dx1, dy1, r1, x2, y2, dx2, dy2, r2):
    # 円同士が重なったら、両方の速度を反転する（角度は無視）
    nx = x2 - x1
    ny = y2 - y1
    min_dist = r1 + r2

    if nx * nx + ny * ny <= min_dist * min_dist:
        # 連続反転（重なりっぱなしでブルブル）を防ぐために少し押し戻す
        dist = math.sqrt(nx * nx + ny * ny) if (nx != 0 or ny != 0) else 1.0
        ux, uy = nx / dist, ny / dist
        overlap = min_dist - dist

        x1 -= ux * overlap / 2
        y1 -= uy * overlap / 2
        x2 += ux * overlap / 2
        y2 += uy * overlap / 2

        # 方向だけ反転
        dx1, dy1 = -dx1, -dy1
        dx2, dy2 = -dx2, -dy2

    return x1, y1, dx1, dy1, x2, y2, dx2, dy2

def update():
    global ball1_x, ball1_y, ball1_dx, ball1_dy
    global ball2_x, ball2_y, ball2_dx, ball2_dy
    global ball3_x, ball3_y, ball3_dx, ball3_dy

    # move
    ball1_x += ball1_dx
    ball1_y += ball1_dy
    ball2_x += ball2_dx
    ball2_y += ball2_dy
    ball3_x += ball3_dx
    ball3_y += ball3_dy

    # wall bounce（半径考慮）
    ball1_dx, ball1_dy = bounce_wall(ball1_x, ball1_y, ball1_dx, ball1_dy, r1)
    ball2_dx, ball2_dy = bounce_wall(ball2_x, ball2_y, ball2_dx, ball2_dy, r2)
    ball3_dx, ball3_dy = bounce_wall(ball3_x, ball3_y, ball3_dx, ball3_dy, r3)

    # ball-ball collisions（組み合わせ：1-2, 1-3, 2-3）
    ball1_x, ball1_y, ball1_dx, ball1_dy, ball2_x, ball2_y, ball2_dx, ball2_dy = collide_and_flip(
        ball1_x, ball1_y, ball1_dx, ball1_dy, r1,
        ball2_x, ball2_y, ball2_dx, ball2_dy, r2
    )
    ball1_x, ball1_y, ball1_dx, ball1_dy, ball3_x, ball3_y, ball3_dx, ball3_dy = collide_and_flip(
        ball1_x, ball1_y, ball1_dx, ball1_dy, r1,
        ball3_x, ball3_y, ball3_dx, ball3_dy, r3
    )
    ball2_x, ball2_y, ball2_dx, ball2_dy, ball3_x, ball3_y, ball3_dx, ball3_dy = collide_and_flip(
        ball2_x, ball2_y, ball2_dx, ball2_dy, r2,
        ball3_x, ball3_y, ball3_dx, ball3_dy, r3
    )

def draw():
    pyxel.cls(0)
    pyxel.circ(ball1_x, ball1_y, r1, 8)
    pyxel.circ(ball2_x, ball2_y, r2, 10)
    pyxel.circ(ball3_x, ball3_y, r3, 12)

pyxel.run(update, draw)
