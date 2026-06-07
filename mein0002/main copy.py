import pyxel

pyxel.init(160, 120, fps=3)

falling_objects = []


def weighted_choice(weights):
    total = sum(weights.values())
    r = pyxel.rndi(1, total)

    current = 0
    for key, weight in weights.items():
        current += weight
        if r <= current:
            return key


def spawn_object():
    new_object = {
        "x": pyxel.rndi(0, 159),
        "y": -10,
        "speed": pyxel.rndf(1.0, 4.0),
        "color": pyxel.rndi(8, 15),
        "size": pyxel.rndi(3, 8),
        "type": weighted_choice({
            "star": 60,
            "heart": 30,
            "diamond": 10
        })
    }
    falling_objects.append(new_object)


def update_objects():
    for obj in falling_objects:
        obj["y"] += obj["speed"]

    falling_objects[:] = [
        obj for obj in falling_objects
        if obj["y"] < 130
    ]


def draw_star(x, y, size, color):
    pyxel.circ(x, y, size, color)
    pyxel.line(x - size, y, x + size, y, 7)
    pyxel.line(x, y - size, x, y + size, 7)


def draw_heart(x, y, size, color):
    pyxel.circ(x - size // 2, y - size // 2, size // 2, color)
    pyxel.circ(x + size // 2, y - size // 2, size // 2, color)
    pyxel.tri(x - size, y, x, y + size, x + size, y, color)


def draw_diamond(x, y, size, color):
    pyxel.tri(x, y - size, x - size, y, x + size, y, color)
    pyxel.tri(x - size, y, x, y + size, x + size, y, color)


def draw_objects():
    for obj in falling_objects:
        if obj["type"] == "star":
            draw_star(obj["x"], obj["y"], obj["size"], obj["color"])
        elif obj["type"] == "heart":
            draw_heart(obj["x"], obj["y"], obj["size"], obj["color"])
        elif obj["type"] == "diamond":
            draw_diamond(obj["x"], obj["y"], obj["size"], obj["color"])


def update():
    if pyxel.frame_count % 5 == 0:  # 出現頻度を調整
        spawn_object()

    update_objects()


def draw():
    pyxel.cls(0)
    draw_objects()


pyxel.run(update, draw)