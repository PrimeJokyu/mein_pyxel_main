# ==========================================
# 🥷 ハイパー忍者ダッシュ (Hyper Ninja Dash)
# （Pyxel / class・global 完全不使用）
# ==========================================
import math
import random
import pyxel

# 変数は一番上に書く！
name = "GUNYA KAZUKI"
age = 12
hobby = "game"

# ▶️ ゲーム開始
pyxel.init(160, 160)

# 🔄 更新処理（ゲームのルール・動きを管理）
def update():
    state = pyxel.user_state

    if state["game_state"] == "TITLE":
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            state["game_state"] = "PLAY"
            load_map_data(state)
        return

    if state["game_state"] == "PLAY":
        state["time_frames"] += 1
        update_player(state)
        update_enemies(state)
        update_particles(state)

    elif state["game_state"] in ("GAMEOVER", "CLEAR"):
        update_particles(state)
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            new_state = create_initial_state()
            pyxel.user_state = new_state
            load_map_data(pyxel.user_state)
            pyxel.user_state["game_state"] = "PLAY"

# ------------------------------------------
# 🎨 描画処理 (pyxel.draw)
# ------------------------------------------
def draw():
    pyxel.cls(1) 
    pyxel.text(5,15,"My Profile Card",7)
    pyxel.text(8,35,  f"name:  {name}",7)
    pyxel.text(8,45,  f"Age:   {age}",7)
    pyxel.text(8,55,  f"Hobby:  {hobby}",7)
 

pyxel.run(update, draw)