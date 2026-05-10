import pyxel

# 初期設定
pyxel.init(160, 120)
pyxel.load("my_game.pyxres")

current_character = 0
characters = (

    {
        "name": "Slime",
        "hp": 30,
        "mp": 0,
        "skill": "no",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": "Most famous slime in the world."
    },
    {
        "name": "Dracky",
        "hp": 20,
        "mp": 20,
        "skill": "no",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": ""
    },
    {
        "name": "Chimera",
        "hp": 60,
        "mp": 30,
        "skill": "",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": ""
    },
    {
        "name": "Giant Scorpion",
        "hp": 80,
        "mp": 10,
        "skill": "no",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": ""
    },
    {
        "name": "Golem",
        "hp": 100,
        "mp": 0,
        "skill": "no",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": ""
    },
    {
        "name": "Dragon",
        "hp": 200,
        "mp": 0,
        "skill": "",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": ""
    },
    {
        "name": "Dragon King",
        "hp": 200,
        "mp": 100,
        "skill": "",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": ""
    },
    {
        "name": "Metal Slime",
        "hp": 4,
        "mp": 30,
        "skill": "no",
        "sprite_x": 0,
        "sprite_y": 0,
        "color": 8,
        "description": ""
    },
)
def update():
    global current_character

    # 左右でキャラクター切り替え
    if pyxel.btnp(pyxel.KEY_LEFT):
        current_character = (current_character - 1) % len(characters)
    if pyxel.btnp(pyxel.KEY_RIGHT):
        current_character = (current_character + 1) % len(characters)

    # 数字キーで直接選択
    for i in range(min(8, len(characters))):
        if pyxel.btnp(ord(str(i + 1))):
            current_character = i

def draw():
    pyxel.cls(1)

    # 選択中のキャラクター情報を取得
    char = characters[current_character]

    # キャラクタースプライト表示（アニメーション付き）
    animation_frame = (pyxel.frame_count // 15) % 2
    sprite_x = char["sprite_x"] + animation_frame * 16

    # 中央に大きく表示
    pyxel.blt(72, 40, 0, sprite_x, char["sprite_y"], 16, 16, 0)

    # キャラクター情報表示
    pyxel.text(10, 10, f"Character: {current_character + 1}/{len(characters)}", 7)
    pyxel.text(10, 25, char["name"], char["color"])
    pyxel.text(10, 40, f"HP: {char['hp']}", 8)
    pyxel.text(10, 50, f"MP: {char['mp']}", 12)
    pyxel.text(10, 60, f"Skill: {char['skill']}", 10)
    pyxel.text(10, 80, char["description"], 6)

    # 操作説明
    pyxel.text(10, 100, "← → : Select", 7)
    pyxel.text(10, 110, "1-8 : Direct", 7)

    # キャラクター一覧（小さく表示）
    for i, c in enumerate(characters[:8]):
        x = 120 + (i % 4) * 10
        y = 80 + (i // 4) * 10
        color = 14 if i == current_character else 6
        pyxel.rect(x, y, 8, 8, color)


pyxel.run(update, draw)