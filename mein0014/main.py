import tkinter as tk
import random
import winsound  # Windowsの標準ビープ音用
import ctypes
import os

# BGMファイルのパス
BGM_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "The_Apple_Chase.mp3")

# ゲーム設定
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPEED = 100  # 更新速度（ミリ秒）
BODY_PARTS = 3
SPACE_SIZE = 20
SNAKE_COLOR = "#00FF00"
EYE_COLOR = "#000000"      # 目の色（黒）
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
NUM_FOODS = 3  # 同時に画面に出現する餌の数

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("ヘビゲーム (Snake Game)")
        self.root.resizable(False, False)

        # スコア表示
        self.label = tk.Label(root, text="Score: 0", font=('consolas', 20))
        self.label.pack()

        # ゲーム画面
        self.canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        # リスタートボタン（最初は非表示）
        self.restart_button = tk.Button(root, text="リスタート (Restart)", font=('consolas', 16), command=self.restart_game)

        # WASDキー操作の割り当て（大文字・小文字の両方に対応）
        self.root.bind('<a>', lambda event: self.change_direction('left'))
        self.root.bind('<A>', lambda event: self.change_direction('left'))
        self.root.bind('<d>', lambda event: self.change_direction('right'))
        self.root.bind('<D>', lambda event: self.change_direction('right'))
        self.root.bind('<w>', lambda event: self.change_direction('up'))
        self.root.bind('<W>', lambda event: self.change_direction('up'))
        self.root.bind('<s>', lambda event: self.change_direction('down'))
        self.root.bind('<S>', lambda event: self.change_direction('down'))

        # ウィンドウを閉じた時の終了処理
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # ゲームの初期化と開始
        self.init_game()

    def play_bgm(self):
        try:
            if os.path.exists(BGM_PATH):
                ctypes.windll.winmm.mciSendStringW('close bgm', None, 0, None)
                ctypes.windll.winmm.mciSendStringW(f'open "{BGM_PATH}" type mpegvideo alias bgm', None, 0, None)
                ctypes.windll.winmm.mciSendStringW('play bgm repeat', None, 0, None)
        except Exception:
            pass

    def stop_bgm(self):
        try:
            ctypes.windll.winmm.mciSendStringW('stop bgm', None, 0, None)
            ctypes.windll.winmm.mciSendStringW('close bgm', None, 0, None)
        except Exception:
            pass

    def init_game(self):
        # BGM再生
        self.play_bgm()
        self.score = 0
        self.direction = 'down'
        self.is_game_over = False
        self.label.config(text=f"Score: {self.score}")
        
        self.restart_button.pack_forget()
        self.canvas.delete(tk.ALL)

        self.snake_coords = [[0, 0] for _ in range(BODY_PARTS)]
        self.snake_squares = []
        self.eye_squares = []  
        self.food_coords = []  

        self.create_snake()
        
        for _ in range(NUM_FOODS):
            self.create_food()

        self.next_turn()

    def create_snake(self):
        hx, hy = self.snake_coords[0]
        head_square = self.canvas.create_rectangle(
            hx, hy, hx + SPACE_SIZE, hy + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
        )
        self.snake_squares.append(head_square)
        
        self.create_eyes(hx, hy)

        for x, y in self.snake_coords[1:]:
            square = self.canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.snake_squares.append(square)
            self.eye_squares.append([])

    def create_eyes(self, x, y):
        eye_size = 4
        if self.direction == 'up':
            e1 = self.canvas.create_oval(x + 3, y + 3, x + 3 + eye_size, y + 3 + eye_size, fill=EYE_COLOR)
            e2 = self.canvas.create_oval(x + 13, y + 3, x + 13 + eye_size, y + 3 + eye_size, fill=EYE_COLOR)
        elif self.direction == 'down':
            e1 = self.canvas.create_oval(x + 3, y + 13, x + 3 + eye_size, y + 13 + eye_size, fill=EYE_COLOR)
            e2 = self.canvas.create_oval(x + 13, y + 13, x + 13 + eye_size, y + 13 + eye_size, fill=EYE_COLOR)
        elif self.direction == 'left':
            e1 = self.canvas.create_oval(x + 3, y + 3, x + 3 + eye_size, y + 3 + eye_size, fill=EYE_COLOR)
            e2 = self.canvas.create_oval(x + 3, y + 13, x + 3 + eye_size, y + 3 + eye_size, fill=EYE_COLOR)
        else: # right
            e1 = self.canvas.create_oval(x + 13, y + 3, x + 13 + eye_size, y + 3 + eye_size, fill=EYE_COLOR)
            e2 = self.canvas.create_oval(x + 13, y + 13, x + 13 + eye_size, y + 13 + eye_size, fill=EYE_COLOR)
        
        self.eye_squares.insert(0, [e1, e2])

    def create_food(self):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            
            if [x, y] not in self.snake_coords and [x, y] not in self.food_coords:
                break

        self.food_coords.append([x, y])
        self.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag=f"food_{x}_{y}"
        )

    def change_direction(self, new_direction):
        if self.is_game_over:
            return
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def next_turn(self):
        if self.is_game_over:
            return

        x, y = self.snake_coords[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.snake_coords.insert(0, [x, y])

        eaten_food = None
        for food in self.food_coords:
            if x == food[0] and y == food[1]:
                eaten_food = food
                break

        if eaten_food:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            
            # 餌を食べたときの効果音（高いピピッという音・非同期）
            try:
                winsound.Beep(800, 50)  # 周波数800Hz、50ミリ秒
            except:
                pass

            self.canvas.delete(f"food_{eaten_food[0]}_{eaten_food[1]}")
            self.food_coords.remove(eaten_food)
            
            self.create_food()
        else:
            self.snake_coords.pop()

        self.canvas.delete("snake")
        for eyes in self.eye_squares:
            for e in eyes:
                self.canvas.delete(e)
        self.snake_squares.clear()
        self.eye_squares.clear()

        for i, (px, py) in enumerate(self.snake_coords):
            square = self.canvas.create_rectangle(
                px, py, px + SPACE_SIZE, py + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.snake_squares.append(square)
            
            if i == 0:
                eye_size = 4
                if self.direction == 'up':
                    e1 = self.canvas.create_oval(px + 3, py + 3, px + 3 + eye_size, py + 3 + eye_size, fill=EYE_COLOR)
                    e2 = self.canvas.create_oval(px + 13, py + 3, px + 13 + eye_size, py + 3 + eye_size, fill=EYE_COLOR)
                elif self.direction == 'down':
                    e1 = self.canvas.create_oval(px + 3, py + 13, px + 3 + eye_size, py + 13 + eye_size, fill=EYE_COLOR)
                    e2 = self.canvas.create_oval(px + 13, py + 13, px + 13 + eye_size, py + 13 + eye_size, fill=EYE_COLOR)
                elif self.direction == 'left':
                    e1 = self.canvas.create_oval(px + 3, py + 3, px + 3 + eye_size, py + 3 + eye_size, fill=EYE_COLOR)
                    e2 = self.canvas.create_oval(px + 3, py + 13, px + 3 + eye_size, py + 3 + eye_size, fill=EYE_COLOR)
                else: # right
                    e1 = self.canvas.create_oval(px + 13, py + 3, px + 13 + eye_size, py + 3 + eye_size, fill=EYE_COLOR)
                    e2 = self.canvas.create_oval(px + 13, py + 13, px + 13 + eye_size, py + 13 + eye_size, fill=EYE_COLOR)
                self.eye_squares.append([e1, e2])
            else:
                self.eye_squares.append([])

        if self.check_collisions():
            self.game_over()
        else:
            self.root.after(SPEED, self.next_turn)

    def check_collisions(self, x=None, y=None):
        if x is None and y is None:
            x, y = self.snake_coords[0]

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        return False

    def game_over(self):
        self.is_game_over = True
        self.stop_bgm()
        self.label.config(text=f"Game Over! Final Score: {self.score}")
        
        # ゲームオーバー時の効果音（低いブーッという音）
        try:
            winsound.Beep(200, 250)  # 周波数200Hz、250ミリ秒
        except:
            pass

        self.restart_button.pack(pady=5)

    def restart_game(self):
        self.init_game()

    def on_close(self):
        self.stop_bgm()
        self.root.destroy()

# アプリケーションの実行
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()