import pyxel

# =========================
# 初期設定
# =========================

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Monster Library")
pyxel.load("my_game.pyxres")

current_character = 0
detail_mode = False

characters = [
    {
        "name": "Slime",
        "hp": 30,
        "mp": 0,
        "skill": "Bounce",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 11,
        "description": "Most famous slime in the world."
    },
    {
        "name": "Dracky",
        "hp": 20,
        "mp": 20,
        "skill": "Sleep",
        "sprite_x": 16,
        "sprite_y": 0,
        "color": 13,
        "description": "A small vampire monster."
    },
    {
        "name": "Chimera",
        "hp": 60,
        "mp": 30,
        "skill": "Fire",
        "sprite_x": 32,
        "sprite_y": 0,
        "color": 10,
        "description": "A flying beast with fire breath."
    },
    {
        "name": "Giant Scorpion",
        "hp": 80,
        "mp": 10,
        "skill": "Poison",
        "sprite_x": 48,
        "sprite_y": 0,
        "color": 8,
        "description": "A deadly giant scorpion."
    },
    {
        "name": "Golem",
        "hp": 100,
        "mp": 0,
        "skill": "Punch",
        "sprite_x": 64,
        "sprite_y": 0,
        "color": 5,
        "description": "A giant stone monster."
    },
    {
        "name": "Dragon",
        "hp": 200,
        "mp": 0,
        "skill": "Flame",
        "sprite_x": 80,
        "sprite_y": 0,
        "color": 9,
        "description": "A legendary fire dragon."
    },
    {
        "name": "Dragon King",
        "hp": 200,
        "mp": 100,
        "skill": "Inferno",
        "sprite_x": 96,
        "sprite_y": 0,
        "color": 14,
        "description": "The king of dragons."
    },
    {
        "name": "Metal Slime",
        "hp": 4,
        "mp": 30,
        "skill": "Escape",
        "sprite_x": 112,
        "sprite_y": 0,
        "color": 7,
        "description": "Extremely hard to defeat."
    },
]

number_keys = [
    pyxel.KEY_1,
    pyxel.KEY_2,
    pyxel.KEY_3,
    pyxel.KEY_4,
    pyxel.KEY_5,
    pyxel.KEY_6,
    pyxel.KEY_7,
    pyxel.KEY_8,
]


# =========================
# 更新処理
# =========================

def update():
    global current_character, detail_mode

    # 詳細画面切り替え
    if pyxel.btnp(pyxel.KEY_RETURN):
        detail_mode = not detail_mode

    # 左右移動
    if pyxel.btnp(pyxel.KEY_LEFT):
        current_character = (current_character - 1) % len(characters)

    if pyxel.btnp(pyxel.KEY_RIGHT):
        current_character = (current_character + 1) % len(characters)

    # 数字キー選択
    for i in range(min(8, len(characters))):
        if pyxel.btnp(number_keys[i]):
            current_character = i


# =========================
# HPバー
# =========================

def draw_hp_bar(x, y, hp):
    max_width = 50

    # 最大HP200基準
    width = int((hp / 200) * max_width)

    pyxel.rect(x, y, max_width, 5, 5)
    pyxel.rect(x, y, width, 5, 8)
    pyxel.rectb(x, y, max_width, 5, 7)


# =========================
# 描画処理
# =========================

def draw():
    pyxel.cls(1)

    char = characters[current_character]

    # =====================
    # 詳細画面
    # =====================

    if detail_mode:

        pyxel.cls(0)

        pyxel.text(10, 10, f"=== {char['name']} ===", 14)

        # 大きなスプライト
        pyxel.blt(
            100,
            25,
            0,
            char["sprite_x"],
            char["sprite_y"],
            16,
            16,
            0
        )

        # ステータス
        pyxel.text(10, 35, f"HP : {char['hp']}", 8)
        pyxel.text(10, 45, f"MP : {char['mp']}", 12)
        pyxel.text(10, 55, f"Skill : {char['skill']}", 10)

        # HPバー
        draw_hp_bar(10, 70, char["hp"])

        # 説明文
        pyxel.text(10, 85, char["description"], 6)

        pyxel.text(10, 110, "RETURN : Back", 7)

    # =====================
    # 一覧画面
    # =====================

    else:

        # アニメーション
        animation_frame = (pyxel.frame_count // 20) % 2
        sprite_x = char["sprite_x"] + animation_frame * 16

        # メインスプライト
        pyxel.blt(
            68,
            35,
            0,
            sprite_x,
            char["sprite_y"],
            16,
            16,
            0
        )

        # 情報
        pyxel.text(
            10,
            10,
            f"Monster {current_character + 1}/{len(characters)}",
            7
        )

        pyxel.text(10, 25, char["name"], char["color"])

        pyxel.text(10, 40, f"HP : {char['hp']}", 8)
        pyxel.text(10, 50, f"MP : {char['mp']}", 12)
        pyxel.text(10, 60, f"Skill : {char['skill']}", 10)

        # HPバー
        draw_hp_bar(10, 72, char["hp"])

        # 説明文
        pyxel.text(10, 82, char["description"], 6)

        # 操作説明
        pyxel.text(10, 95, "LEFT/RIGHT : Select", 7)
        pyxel.text(10, 103, "1-8 : Direct Select", 7)
        pyxel.text(10, 111, "RETURN : Detail", 7)

        # 小キャラ一覧
        for i, c in enumerate(characters):

            x = 115 + (i % 4) * 10
            y = 70 + (i // 4) * 12

            # 選択枠
            if i == current_character:
                pyxel.rectb(x - 1, y - 1, 10, 10, 14)

            # 小スプライト
            pyxel.blt(
                x,
                y,
                0,
                c["sprite_x"],
                c["sprite_y"],
                8,
                8,
                0
            )


# =========================
# 実行
# =========================

pyxel.run(update, draw)