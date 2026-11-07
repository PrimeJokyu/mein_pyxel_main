import pyxel
import random
import math

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
BALL_COUNT = 3  # 球の数

state = {
    "balls": []
}

def create_ball(other_balls):
    r = random.randint(4, 8)
    col = random.randint(1, 15)
    m = r ** 2
    
    while True:
        x = random.randint(r, SCREEN_WIDTH - r)
        y = random.randint(r, SCREEN_HEIGHT - r)
        
        overlap = False
        for other in other_balls:
            dist = math.sqrt((x - other["x"])**2 + (y - other["y"])**2)
            if dist < r + other["r"]:
                overlap = True
                break
        if not overlap:
            break

    return {
        "x": float(x),
        "y": float(y),
        "vx": random.uniform(-2, 2),
        "vy": random.uniform(-2, 2),
        "r": r,
        "col": col,
        "m": m
    }

def update_ball(ball):
    ball["x"] += ball["vx"]
    ball["y"] += ball["vy"]

    # 壁との衝突
    if ball["x"] < ball["r"]:
        ball["x"] = ball["r"]
        ball["vx"] *= -1
    elif ball["x"] > SCREEN_WIDTH - ball["r"]:
        ball["x"] = SCREEN_WIDTH - ball["r"]
        ball["vx"] *= -1

    if ball["y"] < ball["r"]:
        ball["y"] = ball["r"]
        ball["vy"] *= -1
    elif ball["y"] > SCREEN_HEIGHT - ball["r"]:
        ball["y"] = SCREEN_HEIGHT - ball["r"]
        ball["vy"] *= -1

def resolve_collision(b1, b2):
    dx = b2["x"] - b1["x"]
    dy = b2["y"] - b1["y"]
    dist = math.sqrt(dx*dx + dy*dy)

    if dist < b1["r"] + b2["r"] and dist > 0:
        overlap = (b1["r"] + b2["r"] - dist) / 2
        nx = dx / dist
        ny = dy / dist
        
        b1["x"] -= overlap * nx
        b1["y"] -= overlap * ny
        b2["x"] += overlap * nx
        b2["y"] += overlap * ny

        dvx = b2["vx"] - b1["vx"]
        dvy = b2["vy"] - b1["vy"]
        
        dot_product = dvx * nx + dvy * ny

        if dot_product > 0:
            return

        collision_scale = (2 * dot_product) / (b1["m"] + b2["m"])

        b1["vx"] += collision_scale * b2["m"] * nx
        b1["vy"] += collision_scale * b2["m"] * ny
        b2["vx"] -= collision_scale * b1["m"] * nx
        b2["vy"] -= collision_scale * b1["m"] * ny

def reset_balls():
    state["balls"] = []
    for _ in range(BALL_COUNT):
        state["balls"].append(create_ball(state["balls"]))

def update():
    for ball in state["balls"]:
        update_ball(ball)

    for i in range(len(state["balls"])):
        for j in range(i + 1, len(state["balls"])):
            resolve_collision(state["balls"][i], state["balls"][j])

    if pyxel.btnp(pyxel.KEY_SPACE):
        reset_balls()

def draw():
    pyxel.cls(0)
    for ball in state["balls"]:
        pyxel.circ(ball["x"], ball["y"], ball["r"], ball["col"])
        pyxel.pset(ball["x"], ball["y"], 7)

if __name__ == "__main__":
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Colliding Balls")
    reset_balls()
    pyxel.run(update, draw)