import pyxel
import math

# --- 設定 ---
SCREEN_W = 160
SCREEN_H = 120
GRID = 8
COLS = 100
ROWS = 100

pyxel.init(SCREEN_W, SCREEN_H, fps=30)

# --- マップ ---
map_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# --- プレイヤー ---
player_x = COLS * GRID // 2
player_y = ROWS * GRID // 2
player_speed = 2
player_size = 6  # 小さい四角

# --- 弾 ---
class Ink:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

inks = []

# --- 更新 ---
def update():
    global player_x, player_y

    mx, my = pyxel.mouse_x, pyxel.mouse_y
    world_mx = mx + player_x - SCREEN_W // 2
    world_my = my + player_y - SCREEN_H // 2

    angle = math.atan2(world_my - player_y, world_mx - player_x)

    if pyxel.btn(pyxel.KEY_W):
        player_x += math.cos(angle) * player_speed
        player_y += math.sin(angle) * player_speed

    # 画面端で止める
    player_x = max(0, min(COLS*GRID-1, player_x))
    player_y = max(0, min(ROWS*GRID-1, player_y))

    # 弾発射
    if pyxel.btnp(pyxel.KEY_SPACE):
        speed = 4
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        inks.append(Ink(player_x, player_y, dx, dy))

    # 弾更新
    for ink in inks[:]:
        ink.x += ink.dx
        ink.y += ink.dy
        gx = int(ink.x // GRID)
        gy = int(ink.y // GRID)
        if 0 <= gx < COLS and 0 <= gy < ROWS:
            map_grid[gy][gx] = 1
        else:
            inks.remove(ink)

# --- 描画 ---
def draw():
    pyxel.cls(7)  # 背景白

    camera_x = player_x - SCREEN_W // 2
    camera_y = player_y - SCREEN_H // 2

    start_col = int(camera_x // GRID)
    end_col = int((camera_x + SCREEN_W) // GRID) + 1
    start_row = int(camera_y // GRID)
    end_row = int((camera_y + SCREEN_H) // GRID) + 1

    # マップ描画
    for y in range(start_row, min(end_row, ROWS)):
        for x in range(start_col, min(end_col, COLS)):
            color = 7
            if map_grid[y][x] == 1:
                color = 9
            draw_x = x*GRID - camera_x
            draw_y = y*GRID - camera_y
            pyxel.rect(draw_x, draw_y, GRID, GRID, color)

    # --- キャラ描画（回転□） ---
    mx, my = pyxel.mouse_x, pyxel.mouse_y
    world_mx = mx + camera_x
    world_my = my + camera_y
    angle = math.atan2(world_my - player_y, world_mx - player_x)

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    # 外枠（灰色）
    size = player_size
    verts = [(-size,-size),(size,-size),(size,size),(-size,size)]
    verts_rot = []
    for x, y in verts:
        xr = player_x + x * cos_a - y * sin_a
        yr = player_y + x * sin_a + y * cos_a
        verts_rot.append((xr, yr))
    for i in range(4):
        x1, y1 = verts_rot[i]
        x2, y2 = verts_rot[(i+1)%4]
        pyxel.line(x1 - camera_x, y1 - camera_y, x2 - camera_x, y2 - camera_y, 7)  # 薄い外枠

    # 内側オレンジ
    inner = size - 2
    verts_in = [(-inner,-inner),(inner,-inner),(inner,inner),(-inner,inner)]
    verts_in_rot = []
    for x, y in verts_in:
        xr = player_x + x * cos_a - y * sin_a
        yr = player_y + x * sin_a + y * cos_a
        verts_in_rot.append((xr, yr))
    for i in range(4):
        x1, y1 = verts_in_rot[i]
        x2, y2 = verts_in_rot[(i+1)%4]
        pyxel.line(x1 - camera_x, y1 - camera_y, x2 - camera_x, y2 - camera_y, 9)  # オレンジ

    # 弾描画
    for ink in inks:
        pyxel.rect(ink.x - 1 - camera_x, ink.y - 1 - camera_y, 2, 2, 9)

    # マウスカーソル赤
    pyxel.circ(mx, my, 4, 8)

    # スコア
    score = sum(row.count(1) for row in map_grid)
    pyxel.text(5, 5, f"Score: {score}", 0)

pyxel.run(update, draw)
