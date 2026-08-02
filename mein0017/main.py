import pyxel
import random

# 定数
SCREEN_SIZE = 160
BOARD_COLS = 10
BOARD_ROWS = 20
BLOCK_SIZE = 6
BOARD_X = 12
BOARD_Y = 20

# テトリミノの形状定義
SHAPES = {
    'I': [[0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'S': [[0, 1, 1],
          [1, 1, 0],
          [0, 0, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]],
    'J': [[1, 0, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'L': [[0, 0, 1],
          [1, 1, 1],
          [0, 0, 0]]
}

# 各ミノのカラーID
COLORS = {
    'I': 12, # 水色
    'O': 10, # 黄色
    'T': 14, # ピンク
    'S': 11, # 緑
    'Z': 8,  # 赤
    'J': 13, # 青紫
    'L': 9   # オレンジ
}

def rotate_clockwise(matrix):
    return [list(x) for x in zip(*matrix[::-1])]

def rotate_counter_clockwise(matrix):
    return [list(x) for x in zip(*matrix)][::-1]

def check_collision(board, shape, offset_x, offset_y):
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                board_x = offset_x + c
                board_y = offset_y + r
                # 左右・下の境界チェック
                if board_x < 0 or board_x >= BOARD_COLS or board_y >= BOARD_ROWS:
                    return True
                # 上部境界（出現直後など）は左右のみチェック
                if board_y < 0:
                    continue
                # 既存ブロックとの衝突チェック
                if board[board_y][board_x] != 0:
                    return True
    return False

def check_lines(board):
    full_lines = []
    for r in range(BOARD_ROWS):
        if all(board[r][c] != 0 for c in range(BOARD_COLS)):
            full_lines.append(r)
    return full_lines


class Mino:
    def __init__(self, kind):
        self.kind = kind
        self.shape = [row[:] for row in SHAPES[kind]]
        self.color = COLORS[kind]
        # 中央付近に出現させる
        self.x = BOARD_COLS // 2 - len(self.shape[0]) // 2
        self.y = -2
        if kind == 'O':
            self.x = 4
            self.y = 0
        elif kind == 'I':
            self.y = -2


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-2.5, 0.5)
        self.color = color
        self.life = random.randint(12, 22)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15 # 重力
        self.life -= 1
        return self.life > 0

    def draw(self):
        pyxel.pset(self.x, self.y, self.color)


class TitleParticle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_SIZE)
        self.y = random.randint(-80, 0)
        self.speed = random.uniform(0.6, 1.8)
        self.color = random.choice([8, 9, 10, 11, 12, 13, 14])
        self.size = random.choice([1, 2])

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_SIZE:
            self.y = random.randint(-40, 0)
            self.x = random.randint(0, SCREEN_SIZE)

    def draw(self):
        if self.size == 1:
            pyxel.pset(self.x, self.y, self.color)
        else:
            pyxel.rect(self.x, self.y, 2, 2, self.color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, title="PYXELIS", fps=30)
        self.init_sounds()
        self.reset()
        
        # タイトル画面用の装飾パーティクル
        self.title_particles = [TitleParticle() for _ in range(30)]
        
        pyxel.run(self.update, self.draw)

    def init_sounds(self):
        # 0: 移動・ホールド
        pyxel.sounds[0].set("g3", "p", "2", "n", 2)
        # 1: 回転
        pyxel.sounds[1].set("c4", "p", "3", "n", 2)
        # 2: 通常の接地・通常消去
        pyxel.sounds[2].set("c3e3g3c4", "s", "4", "n", 5)
        # 3: テトリス (4ライン消去) ファンファーレ
        pyxel.sounds[3].set("c3e3g3c4e4g4c4", "p", "5", "n", 6)
        # 4: ゲームオーバー
        pyxel.sounds[4].set("c3g2c2r c2", "s", "5", "n", 15)

    def reset(self):
        self.board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
        self.state = "TITLE" # TITLE, PLAYING, FLUSHING, GAMEOVER
        self.score = 0
        self.lines = 0
        self.level = 1
        
        self.bag = []
        self.current_mino = None
        self.next_mino = None
        self.hold_mino = None
        self.can_hold = True
        
        self.fall_timer = 0
        self.lock_delay = 0
        
        self.particles = []
        self.flash_lines = []
        self.flash_timer = 0
        
        self.gameover_y = 0
        self.gameover_timer = 0

    def get_next_mino(self):
        if not self.bag:
            self.bag = list(SHAPES.keys())
            random.shuffle(self.bag)
        return Mino(self.bag.pop())

    def spawn_new_mino(self):
        if self.next_mino is None:
            self.current_mino = self.get_next_mino()
        else:
            self.current_mino = self.next_mino
        self.next_mino = self.get_next_mino()
        self.can_hold = True
        
        # 出現直後の衝突判定 -> 即ゲームオーバー
        if check_collision(self.board, self.current_mino.shape, self.current_mino.x, self.current_mino.y):
            self.state = "GAMEOVER"
            self.gameover_y = 0
            self.gameover_timer = 0
            pyxel.play(0, 4)

    def hold(self):
        if not self.can_hold:
            return
        pyxel.play(0, 0)
        
        if self.hold_mino is None:
            self.hold_mino = Mino(self.current_mino.kind)
            self.spawn_new_mino()
        else:
            temp = self.hold_mino.kind
            self.hold_mino = Mino(self.current_mino.kind)
            self.current_mino = Mino(temp)
            # ホールド先から出現したミノが即座に衝突するか確認
            if check_collision(self.board, self.current_mino.shape, self.current_mino.x, self.current_mino.y):
                self.state = "GAMEOVER"
                self.gameover_y = 0
                self.gameover_timer = 0
                pyxel.play(0, 4)
                
        self.can_hold = False

    def get_ghost_y(self):
        ghost_y = self.current_mino.y
        # 下に衝突するまでY座標を増やす
        while not check_collision(self.board, self.current_mino.shape, self.current_mino.x, ghost_y + 1):
            ghost_y += 1
        return ghost_y

    def spawn_land_particles(self):
        # 接地時のエフェクト
        for r, row in enumerate(self.current_mino.shape):
            for c, val in enumerate(row):
                if val:
                    is_bottom = (r == len(self.current_mino.shape) - 1) or (not self.current_mino.shape[r+1][c])
                    if is_bottom:
                        px_x = BOARD_X + (self.current_mino.x + c) * BLOCK_SIZE + BLOCK_SIZE // 2
                        px_y = BOARD_Y + (self.current_mino.y + r + 1) * BLOCK_SIZE
                        for _ in range(2):
                            self.particles.append(Particle(px_x, px_y, 7)) # 白い火花

    def lock_mino(self):
        for r, row in enumerate(self.current_mino.shape):
            for c, val in enumerate(row):
                if val:
                    bx = self.current_mino.x + c
                    by = self.current_mino.y + r
                    if 0 <= bx < BOARD_COLS and 0 <= by < BOARD_ROWS:
                        self.board[by][bx] = self.current_mino.color
                        
        pyxel.play(0, 2)
        
        # ライン消去のチェック
        full_lines = check_lines(self.board)
        if full_lines:
            self.state = "FLUSHING"
            self.flash_lines = full_lines
            self.flash_timer = 10 # 10フレームフラッシュ
            
            # 消去ラインからパーティクルを発生
            for r in full_lines:
                for c in range(BOARD_COLS):
                    color = self.board[r][c]
                    px_x = BOARD_X + c * BLOCK_SIZE + BLOCK_SIZE // 2
                    px_y = BOARD_Y + r * BLOCK_SIZE + BLOCK_SIZE // 2
                    for _ in range(4):
                        self.particles.append(Particle(px_x, px_y, color))
            
            if len(full_lines) == 4:
                pyxel.play(0, 3) # テトリス消去音
            else:
                pyxel.play(0, 2)
        else:
            self.spawn_new_mino()

    def rotate_mino(self, clockwise):
        old_shape = self.current_mino.shape
        if clockwise:
            new_shape = rotate_clockwise(old_shape)
        else:
            new_shape = rotate_counter_clockwise(old_shape)
            
        # 簡易SRS（壁蹴り）オフセット
        # 1. ズレなし、2. 左に1、3. 右に1、4. 上に1（床蹴り）、5. 左に2、6. 右に2
        kick_offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0)]
        
        for dx, dy in kick_offsets:
            if not check_collision(self.board, new_shape, self.current_mino.x + dx, self.current_mino.y + dy):
                self.current_mino.shape = new_shape
                self.current_mino.x += dx
                self.current_mino.y += dy
                pyxel.play(0, 1)
                # 接地時のディレイをリセット
                if check_collision(self.board, self.current_mino.shape, self.current_mino.x, self.current_mino.y + 1):
                    self.lock_delay = 0
                break

    def handle_input(self):
        # 左右移動
        if pyxel.btnp(pyxel.KEY_LEFT, 9, 3):
            if not check_collision(self.board, self.current_mino.shape, self.current_mino.x - 1, self.current_mino.y):
                self.current_mino.x -= 1
                pyxel.play(0, 0)
                if check_collision(self.board, self.current_mino.shape, self.current_mino.x, self.current_mino.y + 1):
                    self.lock_delay = 0
        if pyxel.btnp(pyxel.KEY_RIGHT, 9, 3):
            if not check_collision(self.board, self.current_mino.shape, self.current_mino.x + 1, self.current_mino.y):
                self.current_mino.x += 1
                pyxel.play(0, 0)
                if check_collision(self.board, self.current_mino.shape, self.current_mino.x, self.current_mino.y + 1):
                    self.lock_delay = 0

        # ソフトドロップ
        if pyxel.btn(pyxel.KEY_DOWN):
            if not check_collision(self.board, self.current_mino.shape, self.current_mino.x, self.current_mino.y + 1):
                self.current_mino.y += 1
                self.score += 1
                self.fall_timer = 0
                if pyxel.frame_count % 3 == 0:
                    pyxel.play(0, 0)

        # ハードドロップ
        if pyxel.btnp(pyxel.KEY_UP):
            ghost_y = self.get_ghost_y()
            drop_dist = ghost_y - self.current_mino.y
            self.score += drop_dist * 2
            self.current_mino.y = ghost_y
            
            # 接地エフェクトと固定
            self.spawn_land_particles()
            self.lock_mino()
            return

        # 回転
        if pyxel.btnp(pyxel.KEY_Z):
            self.rotate_mino(clockwise=False)
        if pyxel.btnp(pyxel.KEY_X):
            self.rotate_mino(clockwise=True)

        # ホールド
        if pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.KEY_SPACE):
            self.hold()

    def get_fall_interval(self):
        # レベル上昇に応じて落下速度をアップ（最小2フレーム）
        return max(2, 30 - (self.level - 1) * 3)

    def update_playing(self):
        self.handle_input()
        
        # 自動落下
        self.fall_timer += 1
        if self.fall_timer >= self.get_fall_interval():
            self.fall_timer = 0
            if not check_collision(self.board, self.current_mino.shape, self.current_mino.x, self.current_mino.y + 1):
                self.current_mino.y += 1
                self.lock_delay = 0
            else:
                self.lock_delay += 1
                
        # 接地状態での猶予時間 (約0.5秒)
        if check_collision(self.board, self.current_mino.shape, self.current_mino.x, self.current_mino.y + 1):
            self.lock_delay += 1
            if self.lock_delay >= 15:
                self.lock_mino()
        else:
            self.lock_delay = 0
            
        self.particles = [p for p in self.particles if p.update()]

    def update_flushing(self):
        self.flash_timer -= 1
        self.particles = [p for p in self.particles if p.update()]
        
        if self.flash_timer <= 0:
            # 揃ったラインの消去と詰め
            for r in sorted(self.flash_lines):
                del self.board[r]
                self.board.insert(0, [0] * BOARD_COLS)
                
            # 得点計算 (1ライン:100, 2ライン:300, 3ライン:600, 4ライン:1000)
            line_bonus = {1: 100, 2: 300, 3: 600, 4: 1000}
            self.score += line_bonus.get(len(self.flash_lines), 0) * self.level
            self.lines += len(self.flash_lines)
            self.level = self.lines // 10 + 1
            
            self.flash_lines = []
            self.state = "PLAYING"
            self.spawn_new_mino()

    def update_gameover(self):
        self.gameover_timer += 1
        # 積み上がったブロックを徐々に灰色にする
        if self.gameover_timer % 2 == 0 and self.gameover_y < BOARD_ROWS:
            for c in range(BOARD_COLS):
                if self.board[BOARD_ROWS - 1 - self.gameover_y][c] != 0:
                    self.board[BOARD_ROWS - 1 - self.gameover_y][c] = 5 # 暗いグレーにする
            self.gameover_y += 1
            
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.reset()
            self.state = "PLAYING"
            self.spawn_new_mino()

    def update(self):
        if self.state == "TITLE":
            for p in self.title_particles:
                p.update()
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = "PLAYING"
                self.spawn_new_mino()
        elif self.state == "PLAYING":
            self.update_playing()
        elif self.state == "FLUSHING":
            self.update_flushing()
        elif self.state == "GAMEOVER":
            self.update_gameover()

    def draw_block(self, x, y, color_id, is_ghost=False):
        if color_id == 0:
            return
            
        if is_ghost:
            # ゴーストは輪郭のみ
            pyxel.rectb(x, y, BLOCK_SIZE, BLOCK_SIZE, color_id)
            return
            
        # 立体感のあるブロックの描画
        pyxel.rect(x, y, BLOCK_SIZE, BLOCK_SIZE, color_id)
        # 上と左の明るいエッジ (白=7)
        pyxel.line(x, y, x + BLOCK_SIZE - 1, y, 7)
        pyxel.line(x, y, x, y + BLOCK_SIZE - 1, 7)
        # 下と右の暗いエッジ (黒=0)
        pyxel.line(x, y + BLOCK_SIZE - 1, x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1, 0)
        pyxel.line(x + BLOCK_SIZE - 1, y, x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1, 0)

    def draw_preview_mino(self, kind, box_x, box_y):
        if kind is None:
            return
        shape = SHAPES[kind]
        color = COLORS[kind]
        
        # プレビューボックス (36x30) 内のセンタリング用オフセット
        offsets = {
            'I': (6, 9),
            'O': (12, 9),
            'T': (9, 9),
            'S': (9, 9),
            'Z': (9, 9),
            'J': (9, 9),
            'L': (9, 9)
        }
        ox, oy = offsets[kind]
        
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    bx = box_x + ox + c * BLOCK_SIZE
                    by = box_y + oy + r * BLOCK_SIZE
                    self.draw_block(bx, by, color)

    def draw_board(self):
        # 枠線
        pyxel.rectb(BOARD_X - 1, BOARD_Y - 1, BOARD_COLS * BLOCK_SIZE + 2, BOARD_ROWS * BLOCK_SIZE + 2, 6)
        
        # グリッド背景
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                bx = BOARD_X + c * BLOCK_SIZE
                by = BOARD_Y + r * BLOCK_SIZE
                # 細かいグリッド点を描画
                if (r + c) % 2 == 0:
                    pyxel.pset(bx + BLOCK_SIZE // 2, by + BLOCK_SIZE // 2, 1) # 暗い青の点
                    
        # 固定されたブロック
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                color = self.board[r][c]
                if color != 0:
                    bx = BOARD_X + c * BLOCK_SIZE
                    by = BOARD_Y + r * BLOCK_SIZE
                    # ライン消去フラッシュ中
                    if self.state == "FLUSHING" and r in self.flash_lines:
                        # 白と元の色を交互に表示
                        if pyxel.frame_count % 2 == 0:
                            pyxel.rect(bx, by, BLOCK_SIZE, BLOCK_SIZE, 7)
                        else:
                            pyxel.rect(bx, by, BLOCK_SIZE, BLOCK_SIZE, color)
                    else:
                        self.draw_block(bx, by, color)

    def draw_playing(self):
        pyxel.cls(0)
        
        # ボード
        self.draw_board()
        
        # ゴーストミノ（落下予測）
        ghost_y = self.get_ghost_y()
        for r, row in enumerate(self.current_mino.shape):
            for c, val in enumerate(row):
                if val:
                    bx = BOARD_X + (self.current_mino.x + c) * BLOCK_SIZE
                    by = BOARD_Y + (ghost_y + r) * BLOCK_SIZE
                    if by >= BOARD_Y:
                        self.draw_block(bx, by, self.current_mino.color, is_ghost=True)

        # 落下中のミノ
        for r, row in enumerate(self.current_mino.shape):
            for c, val in enumerate(row):
                if val:
                    bx = BOARD_X + (self.current_mino.x + c) * BLOCK_SIZE
                    by = BOARD_Y + (self.current_mino.y + r) * BLOCK_SIZE
                    if by >= BOARD_Y:
                        self.draw_block(bx, by, self.current_mino.color)

        # パーティクル
        for p in self.particles:
            p.draw()

        # UI: NEXTボックス
        pyxel.text(92, 12, "NEXT", 10)
        pyxel.rectb(92, 20, 36, 30, 6)
        self.draw_preview_mino(self.next_mino.kind if self.next_mino else None, 92, 20)

        # UI: HOLDボックス
        pyxel.text(92, 53, "HOLD", 14)
        pyxel.rectb(92, 60, 36, 30, 6)
        if self.hold_mino:
            self.draw_preview_mino(self.hold_mino.kind, 92, 60)

        # UI: 統計情報
        pyxel.text(92, 98, f"SCORE", 7)
        pyxel.text(92, 105, f"{self.score:06d}", 12)
        
        pyxel.text(92, 116, f"LINES", 7)
        pyxel.text(92, 123, f"{self.lines:03d}", 11)
        
        pyxel.text(92, 134, f"LEVEL", 7)
        pyxel.text(92, 141, f"{self.level:02d}", 10)

        # 操作説明（下部）
        pyxel.text(12, 148, "Z/X:ROTATE  C:HOLD  UP:DROP", 5)

    def draw_title(self):
        pyxel.cls(1) # 深い青背景
        
        # パーティクル描画
        for p in self.title_particles:
            p.draw()
            
        # タイトルロゴ (3D風重ね文字)
        pyxel.text(48, 40, "P Y X E L I S", 2)
        pyxel.text(50, 42, "P Y X E L I S", 13)
        pyxel.text(49, 41, "P Y X E L I S", 7)
        
        # 枠線
        pyxel.rectb(20, 65, 120, 60, 6)
        
        # 説明文
        pyxel.text(25, 72, "CONTROLS:", 10)
        pyxel.text(25, 82, "- LEFT/RIGHT : MOVE", 7)
        pyxel.text(25, 92, "- DOWN/UP    : SOFT/HARD DROP", 7)
        pyxel.text(25, 102, "- Z/X        : ROTATE L/R", 7)
        pyxel.text(25, 112, "- SPACE/C    : HOLD MINO", 7)
        
        # スタート点滅テキスト
        if pyxel.frame_count % 30 < 15:
            pyxel.text(38, 138, "PRESS ENTER TO START", 7)
        else:
            pyxel.text(38, 138, "PRESS ENTER TO START", 5)

    def draw_gameover(self):
        # プレイ中の画面をベースに描く
        self.draw_playing()
        
        # 半透明風の網掛け
        for y in range(0, SCREEN_SIZE, 2):
            pyxel.line(0, y, SCREEN_SIZE, y, 0)
            
        # ダイアログ
        pyxel.rect(30, 55, 100, 50, 2)
        pyxel.rectb(30, 55, 100, 50, 8)
        
        pyxel.text(61, 65, "GAME OVER", 8)
        pyxel.text(42, 80, f"SCORE: {self.score:06d}", 7)
        pyxel.text(42, 90, "PRESS ENTER TO RETRY", pyxel.frame_count % 20 < 10 and 7 or 5)

    def draw(self):
        if self.state == "TITLE":
            self.draw_title()
        elif self.state == "PLAYING" or self.state == "FLUSHING":
            self.draw_playing()
        elif self.state == "GAMEOVER":
            self.draw_gameover()


if __name__ == "__main__":
    App()
