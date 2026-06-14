import pyxel
import random

object_pool_active = []
object_pool_inactive = []
object_pool_max = 100


def pool_create_empty_object():
    return {
        "x": 0, "y": 0, "active": False,
        "speed": 0, "color": 0, "size": 0, "type": ""
    }


def pool_init(max_objects=100):
    global object_pool_max
    object_pool_max = max_objects
    object_pool_active.clear()
    object_pool_inactive.clear()
    for _ in range(max_objects):
        object_pool_inactive.append(pool_create_empty_object())


def pool_spawn(x, y, object_type):
    if object_pool_inactive:
        obj = object_pool_inactive.pop()
        obj.update({
            "x": x, "y": y, "active": True,
            "speed": pyxel.rndf(1.0, 4.0),
            "color": pyxel.rndi(8, 15),
            "size": pyxel.rndi(3, 8),
            "type": object_type
        })
        object_pool_active.append(obj)
        return obj
    return None


def pool_despawn(obj):
    if obj in object_pool_active:
        obj["active"] = False
        object_pool_active.remove(obj)
        object_pool_inactive.append(obj)


def pool_update():
    to_remove = []

    for obj in object_pool_active:
        obj["y"] += obj["speed"]

        if obj["y"] > 130:
            to_remove.append(obj)

    for obj in to_remove:
        pool_despawn(obj)


# ここ追加（あなたのコードに不足していた部分）
def weighted_choice(weight_dict):
    items = []
    for k, v in weight_dict.items():
        items += [k] * v
    return random.choice(items)


def spawn_random_object():
    x = pyxel.rndi(0, 160)
    object_type = weighted_choice({"star": 60, "heart": 30, "diamond": 10})
    pool_spawn(x, -10, object_type)


# =========================
# Pyxel本体
# =========================

class App:
    def __init__(self):
        pyxel.init(160, 120)
        pool_init(100)
        pyxel.run(self.update, self.draw)

    def update(self):
        # 定期的に生成
        if pyxel.frame_count % 10 == 0:
            spawn_random_object()

        pool_update()

    def draw(self):
        pyxel.cls(0)

        for obj in object_pool_active:
            if obj["type"] == "star":
                pyxel.circ(obj["x"], obj["y"], obj["size"], obj["color"])

            elif obj["type"] == "heart":
                pyxel.circ(obj["x"] - 2, obj["y"], obj["size"] // 2, obj["color"])
                pyxel.circ(obj["x"] + 2, obj["y"], obj["size"] // 2, obj["color"])
                pyxel.tri(
                    obj["x"] - obj["size"], obj["y"],
                    obj["x"], obj["y"] + obj["size"],
                    obj["x"] + obj["size"], obj["y"],
                    obj["color"]
                )

            elif obj["type"] == "diamond":
                pyxel.tri(
                    obj["x"], obj["y"] - obj["size"],
                    obj["x"] - obj["size"], obj["y"],
                    obj["x"] + obj["size"], obj["y"],
                    obj["color"]
                )
                pyxel.tri(
                    obj["x"] - obj["size"], obj["y"],
                    obj["x"], obj["y"] + obj["size"],
                    obj["x"] + obj["size"], obj["y"],
                    obj["color"]
                )


App()