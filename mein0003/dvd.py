import pyxel

# ボールの情報と状態管理 (global不使用)
state = {
    "x": 80,
    "y": 60,
    "dx": 2,
    "dy": 1,
    "radius": 8
}

def update():
    state["x"] += state["dx"]
    state["y"] += state["dy"]

    r = state["radius"]
    # 画面の端で跳ね返る処理（ボールの半径を考慮）
    if state["x"] - r < 0 or state["x"] + r > 160:
        state["dx"] = -state["dx"]
    if state["y"] - r < 0 or state["y"] + r > 120:
        state["dy"] = -state["dy"]

def draw():
    pyxel.cls(1)
    pyxel.circ(state["x"], state["y"], state["radius"], 10)

if __name__ == "__main__":
    pyxel.init(160, 120, title="DVD Bounce")
    pyxel.run(update, draw)
