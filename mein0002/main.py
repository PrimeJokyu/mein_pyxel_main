import pyxel

# タイル設定
TILE_SIZE = 16
FIELD_WIDTH = 40
FIELD_HEIGHT = 22

class SimpleFighter:
    def __init__(self):
        pyxel.init(640, 360, title="格闘ゲーム基礎（キャラ大きめ）")
        
        # 地面タイルマップ 0=空, 1=地面
        self.field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        for x in range(FIELD_WIDTH):
            self.field[FIELD_HEIGHT-1][x] = 1  # 地面

        # プレイヤー
        self.width = 24
        self.height = 48
        self.x = 100
        self.y = 280
        self.vy = 0
        self.on_ground_flag = True
        self.hp = 20

        # 敵
        self.enemy_width = 24
        self.enemy_height = 48
        self.enemy_x = 500
        self.enemy_y = 280
        self.enemy_vy = 0
        self.enemy_hp = 20

        pyxel.run(self.update, self.draw)

    def update(self):
        speed = 4

        # 左右移動
        if pyxel.btn(pyxel.KEY_A):
            self.move_horizontal(-speed)
        if pyxel.btn(pyxel.KEY_D):
            self.move_horizontal(speed)

        # ジャンプ
        if pyxel.btnp(pyxel.KEY_W) and self.on_ground_flag:
            self.vy = -12
            self.on_ground_flag = False

        # しゃがみ
        self.squatting = pyxel.btn(pyxel.KEY_S)

        # 重力
        self.vy += 0.5
        if self.vy > 6:
            self.vy = 6
        self.move_vertical(self.vy)

        # 敵AI（簡単にプレイヤー方向へ移動）
        if self.enemy_x > self.x + 30:
            self.enemy_x -= 2
        elif self.enemy_x < self.x - 30:
            self.enemy_x += 2

    def move_horizontal(self, dx):
        new_x = self.x + dx
        if not self.collide(new_x, self.y):
            self.x = new_x

    def move_vertical(self, dy):
        new_y = self.y + dy
        if not self.collide(self.x, new_y):
            self.y = new_y
        else:
            self.vy = 0
            self.on_ground_flag = True

    def collide(self, x, y):
        tx = int(x)//TILE_SIZE
        ty = int(y + self.height)//TILE_SIZE
        if 0 <= tx < FIELD_WIDTH and 0 <= ty < FIELD_HEIGHT:
            return self.field[ty][tx] != 0
        return False

    def draw(self):
        pyxel.cls(0)

        # 地面描画
        for x in range(FIELD_WIDTH):
            pyxel.rect(x*TILE_SIZE, (FIELD_HEIGHT-1)*TILE_SIZE, TILE_SIZE, TILE_SIZE, 10)

        # プレイヤー
        pyxel.rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height, 8)
        # 敵
        pyxel.rect(self.enemy_x - self.enemy_width//2, self.enemy_y - self.enemy_height//2, self.enemy_width, self.enemy_height, 9)

        # HPバー（画面固定）
        # プレイヤー左上
        pyxel.rect(20, 20, self.hp*10, 10, 11)
        pyxel.rectb(20, 20, 200, 10, 7)
        # 敵右上
        pyxel.rect(420, 20, self.enemy_hp*10, 10, 10)
        pyxel.rectb(420, 20, 200, 10, 7)

SimpleFighter()
