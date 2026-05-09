import pyxel
import random

# ==========================================
# 1. ゲームの設定（グローバル変数）
# ここを書き換えることでゲームの動きや見た目を変更できます
# ==========================================
WINDOW_WIDTH = 200      # 画面の横幅（Pyxelは最大256なので小さめに設定）
WINDOW_HEIGHT = 150     # 画面の縦幅
BLOCK_SIZE = 10         # 蛇と餌の1ブロックのサイズ（ピクセル）
FPS = 10                # 1秒間の画面更新回数（蛇の動く速さ）

# 色の設定（Pyxelは0〜15の番号で色を指定します）
COLOR_BLACK = 0         # 背景色（黒）
COLOR_WHITE = 7         # 文字などの色（白）
COLOR_GREEN = 11        # 蛇の色（緑）
COLOR_RED = 8           # 餌の色（赤）

# ゲーム内で変化する変数（初期値は仮の値で、後でリセットされます）
snake_head = [100, 70]
snake_body = [[100, 70], [90, 70], [80, 70]]
direction = "RIGHT"
change_to = "RIGHT"
food_pos = [0, 0]
is_game_over = False

# ==========================================
# 2. ゲームの処理をまとめた関数（def）
# ==========================================

def init_game():
    """ゲームの初期状態をセットする関数"""
    # globalを使うことで、関数の外にある変数を書き換えられるようにします
    global snake_head, snake_body, direction, change_to, is_game_over
    
    # 蛇の初期座標（画面の中央あたり）
    snake_head = [100, 70]
    # 蛇の全体のリスト（最初は頭から続く3つのブロック）
    snake_body = [[100, 70], [100 - BLOCK_SIZE, 70], [100 - BLOCK_SIZE*2, 70]]
    
    # 最初の進行方向
    direction = "RIGHT"
    change_to = "RIGHT"
    is_game_over = False
    
    # 最初の餌を生成
    generate_food()

def generate_food():
    """新しい餌をランダムな位置に生成する関数"""
    global food_pos
    while True:
        # 画面の範囲内でランダムなX座標を計算する（BLOCK_SIZEの倍数になるように）
        food_x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
        # 画面の範囲内でランダムなY座標を計算する（BLOCK_SIZEの倍数になるように）
        food_y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
        
        # 餌が蛇の体と被っていなければ、その座標を設定して終了
        if [food_x, food_y] not in snake_body:
            food_pos = [food_x, food_y]
            break

def move_snake():
    """指定された方向に蛇の頭を移動させる関数"""
    global snake_head, direction, change_to
    
    # 現在の頭のX座標とY座標を取得
    x = snake_head[0]
    y = snake_head[1]
    
    # 進行方向の更新（真逆には進めないようにする制限）
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"
    
    # 方向に応じて座標を変化させる
    if direction == "UP":
        y -= BLOCK_SIZE # 上へ移動
    elif direction == "DOWN":
        y += BLOCK_SIZE # 下へ移動
    elif direction == "LEFT":
        x -= BLOCK_SIZE # 左へ移動
    elif direction == "RIGHT":
        x += BLOCK_SIZE # 右へ移動
        
    # 新しい頭の座標を更新
    snake_head = [x, y]

def check_collision():
    """壁や自分自身との衝突を判定する関数"""
    global is_game_over
    
    # 壁との衝突判定（画面の外に出たかどうか）
    if snake_head[0] < 0 or snake_head[0] >= WINDOW_WIDTH:
        is_game_over = True # 横の壁にぶつかったらゲームオーバー
    if snake_head[1] < 0 or snake_head[1] >= WINDOW_HEIGHT:
        is_game_over = True # 縦の壁にぶつかったらゲームオーバー
        
    # 自分自身との衝突判定（頭が体の一部に重なったかどうか）
    if snake_head in snake_body[1:]:
        is_game_over = True # 体にぶつかったらゲームオーバー

def update():
    """毎フレーム（一定時間ごと）に実行される計算処理の関数"""
    global change_to, is_game_over
    
    # Qキーを押したらPyxelのウィンドウを閉じる処理
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
        
    # Rキーを押したら「いつでも」やり直し（リセット）
    
        
    # ゲームオーバー時はエンターキーで再スタート
    if is_game_over:
        if pyxel.btnp(pyxel.KEY_R):
            init_game() # ゲームを初期状態に戻す
        return# ゲームオーバー中はこれ以下の処理（移動など）をしない
    if pyxel.btnp(pyxel.KEY_R):
        init_game() 
        
    # キーボードの入力処理（矢印キーで進行方向の予約をする）
    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
        change_to = "UP"
    elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
        change_to = "DOWN"
    elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
        change_to = "LEFT"
    elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
        change_to = "RIGHT"
        
    # 蛇の移動処理を呼び出す
    move_snake()
    
    # 移動した新しい頭を体のリストの先頭に追加する
    snake_body.insert(0, list(snake_head))
    
    # 餌を食べたかどうかの判定
    if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
        # 餌を食べた場合は、新しい餌を生成する（体はそのまま長くなる）
        generate_food()
    else:
        # 餌を食べていない場合は、一番後ろの尻尾を削除して長さを保つ
        snake_body.pop()
        
    # 衝突判定（壁や自分にぶつかったか）を呼び出す
    check_collision()

def draw():
    """毎フレーム実行される画面描画の関数"""
    # 画面全体を黒色で塗りつぶす（前のフレームの絵を消す）
    pyxel.cls(COLOR_BLACK)
    
    # 蛇の体を1ブロックずつ描画する
    for block in snake_body:
        # rect(x, y, 幅, 高さ, 色番号) で四角形を描画
        pyxel.rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE, COLOR_GREEN)
        
    # 餌の四角形を描画
    pyxel.rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE, COLOR_RED)
    
    # ゲームオーバー時のテキスト表示
    if is_game_over:
        # 文字を表示：text(x, y, 文字列, 色番号)
        pyxel.text(80, 60, "GAME OVER", COLOR_WHITE)
        pyxel.text(50, 75, "PRESS ENTER TO RESTART", COLOR_WHITE)

# ==========================================
# 3. メインの処理
# ==========================================
if __name__ == "__main__":
    # Pyxelの初期化（画面サイズ、タイトル、FPSを指定）
    pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="シンプルな蛇ゲーム（Pyxel版）", fps=FPS)
    
    # ゲームの初期状態をセット
    init_game()
    
    # ゲームループの開始（update関数とdraw関数が自動で繰り返し呼ばれる）
    pyxel.run(update, draw)
