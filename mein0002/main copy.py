import pyxel

def create_physics_object(x, y):
    return {
        "x": x, "y": y,
        "velocity_x": pyxel.rndf(-3.0, 3.0),  # 横方向の初期速度
        "velocity_y": 0,                       # 縦方向の初期速度
        "gravity": 0.2,                       # 重力加速度
        "bounce": 0.7,                        # 跳ね返り係数
        "friction": 0.98                      # 空気抵抗
    }

def update_physics_object(obj):
    # 重力を適用
    obj["velocity_y"] += obj["gravity"]

    # 空気抵抗を適用
    obj["velocity_x"] *= obj["friction"]

    # 位置を更新
    obj["x"] += obj["velocity_x"]
    obj["y"] += obj["velocity_y"]

    # 地面との当たり判定
    if obj["y"] > 110:  # 地面の高さ
        obj["y"] = 110
        obj["velocity_y"] = -obj["velocity_y"] * obj["bounce"]  # 跳ね返り

    # 左右の壁との当たり判定
    if obj["x"] < 0 or obj["x"] > 160:
        obj["velocity_x"] = -obj["velocity_x"] * obj["bounce"]
        obj["x"] = max(0, min(obj["x"], 160))


def create_projectile(start_x, start_y, target_x, target_y, flight_time=60):
    """指定された時間で目標地点に到達する放物線軌道"""
    dx = target_x - start_x
    dy = target_y - start_y

    # 初期速度を計算
    velocity_x = dx / flight_time
    velocity_y = dy / flight_time - 0.5 * 0.2 * flight_time  # 重力を考慮

    return {
        "x": start_x, "y": start_y,
        "velocity_x": velocity_x,
        "velocity_y": velocity_y,
        "gravity": 0.2,
        "time": 0
    }

def update_projectile(proj):
    proj["time"] += 1

    proj["x"] += proj["velocity_x"]
    proj["y"] += proj["velocity_y"]
    proj["velocity_y"] += proj["gravity"]

    # スペースキーで発射
    if pyxel.btnp(pyxel.KEY_SPACE):
        return create_projectile(
            obj["x"],
            obj["y"],
            pyxel.mouse_x,
            pyxel.mouse_y
        )

    # 画面の下に行ったらランダム発射
    if proj["y"] > 120:
        return create_projectile(
            20,
            100,
            pyxel.rndi(20, 140),
            pyxel.rndi(20, 100)
        )

    return proj
def update():
    global projectile

    update_physics_object(obj)
    projectile = update_projectile(projectile)

def draw():
    pyxel.cls(0)
    pyxel.circ(int(obj["x"]), int(obj["y"]), 5, 8)
    pyxel.circ(int(projectile["x"]), int(projectile["y"]), 3, 10)
    pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 1, 7)

pyxel.init(160, 120, title="Physics Demo")

obj = create_physics_object(80, 60)
projectile = create_projectile(20, 100, 140, 40)
pyxel.run(update, draw)
