import pyxel

# ゲームの状態（辞書で管理）
state = {
    "score": 0,
    "combo": 0,
    "best_combo": 0,
    "notes": [],          # ノーツのリスト {"x", "lane", "hit", "missed"}
    "judgment": "",       # "PERFECT!" "GOOD!" "MISS!"
    "judgment_timer": 0,
    "frame": 0,
    "next_note_frame": 40,
    "flash_timer": [0, 0],  # レーンごとのフラッシュ
    "bg_beat": 0,
    "speed": 3,           # ノーツ速度
}

HIT_X = 35
LANE_Y = [55, 95]        # 2レーン（上・下）
PERFECT_R = 5            # PERFECT判定 ±5px
GOOD_R    = 9            # GOOD判定 ±9px

# 鬼ハードパターン：短い間隔・不規則
NOTE_PATTERN = [12, 8, 12, 8, 16, 10, 8, 12, 10, 8, 12, 8, 16, 8, 10, 12]
LANE_PATTERN = [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
pattern_index = [0]


def spawn_note():
    """ノーツを右端に生成する"""
    idx = pattern_index[0] % len(LANE_PATTERN)
    lane = LANE_PATTERN[idx]
    state["notes"].append({"x": 162.0, "lane": lane, "hit": False, "missed": False})


def get_combo_multiplier(combo):
    """コンボ倍率（コンボが高いほどスコア増）"""
    if combo >= 30:
        return 5
    elif combo >= 20:
        return 4
    elif combo >= 10:
        return 3
    elif combo >= 5:
        return 2
    return 1


def update():
    st = state
    st["frame"] += 1

    # リズムに合わせてノーツ生成
    if st["frame"] >= st["next_note_frame"]:
        spawn_note()
        interval = NOTE_PATTERN[pattern_index[0] % len(NOTE_PATTERN)]
        pattern_index[0] += 1
        st["next_note_frame"] = st["frame"] + interval
        st["bg_beat"] = 3

    # ノーツを左へ移動（高速！）
    for note in st["notes"]:
        if not note["hit"]:
            note["x"] -= st["speed"]

    # ミス判定（ヒットゾーンを通り過ぎた）
    for note in st["notes"]:
        if not note["hit"] and not note["missed"] and note["x"] < HIT_X - GOOD_R:
            note["missed"] = True
            st["combo"] = 0
            st["judgment"] = "MISS!"
            st["judgment_timer"] = 20

    # 画面外のノーツを消す
    st["notes"] = [n for n in st["notes"] if n["x"] > -20]

    # レーン0（上）：Z or SPACE
    # レーン1（下）：X or M
    lane_keys = [
        (pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE)),
        (pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_M)),
    ]

    for lane_id, pressed in enumerate(lane_keys):
        if pressed:
            best_note = None
            best_dist = 999
            for note in st["notes"]:
                if not note["hit"] and not note["missed"] and note["lane"] == lane_id:
                    d = abs(note["x"] - HIT_X)
                    if d < best_dist:
                        best_dist = d
                        best_note = note

            if best_note and best_dist <= GOOD_R:
                best_note["hit"] = True
                st["flash_timer"][lane_id] = 6
                mul = get_combo_multiplier(st["combo"])
                if best_dist <= PERFECT_R:
                    st["score"] += 100 * mul
                    st["combo"] += 1
                    st["judgment"] = "PERFECT!"
                    st["judgment_timer"] = 28
                else:
                    st["score"] += 50 * mul
                    st["combo"] += 1
                    st["judgment"] = "GOOD!"
                    st["judgment_timer"] = 22
                if st["combo"] > st["best_combo"]:
                    st["best_combo"] = st["combo"]
            else:
                st["combo"] = 0
                st["judgment"] = "MISS!"
                st["judgment_timer"] = 20

    # タイマーをカウントダウン
    if st["judgment_timer"] > 0:
        st["judgment_timer"] -= 1
    for i in range(2):
        if st["flash_timer"][i] > 0:
            st["flash_timer"][i] -= 1
    if st["bg_beat"] > 0:
        st["bg_beat"] -= 1

    # Q で終了
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    st = state

    # 背景
    bg = 2 if st["bg_beat"] > 0 else 1
    pyxel.cls(bg)

    # タイトル
    pyxel.text(30, 4, "!! RHYTHM GAME - DEVIL !!", 8)
    pyxel.line(0, 14, 160, 14, 5)

    # ２レーン描画
    lane_labels = ["Z/SPACE", "X/M"]
    for lane_id, ly in enumerate(LANE_Y):
        # ガイドライン
        pyxel.line(HIT_X, ly, 160, ly, 5)

        # ヒットゾーン（フラッシュ）
        hc = 10 if st["flash_timer"][lane_id] > 0 else 9
        pyxel.circb(HIT_X, ly, 9, hc)
        pyxel.circb(HIT_X, ly, 5, hc)
        pyxel.text(HIT_X - 14, ly + 12, lane_labels[lane_id], hc)

        # ノーツ描画
        for note in st["notes"]:
            if note["lane"] != lane_id:
                continue
            if not note["hit"] and not note["missed"]:
                dist = abs(note["x"] - HIT_X)
                if dist < PERFECT_R:
                    color = 10  # 超近い＝黄色
                elif dist < GOOD_R:
                    color = 9
                else:
                    color = 8
                pyxel.circ(int(note["x"]), ly, 5, color)
                pyxel.circb(int(note["x"]), ly, 5, 7)

    # 判定テキスト（PERFECT / GOOD / MISS）
    if st["judgment_timer"] > 0:
        j = st["judgment"]
        color = 10 if j == "PERFECT!" else (11 if j == "GOOD!" else 8)
        pyxel.text(58, 76, j, color)

    # コンボ倍率表示
    mul = get_combo_multiplier(st["combo"])
    mul_color = 10 if mul >= 3 else 7
    pyxel.text(5, 20, f"SCORE: {st['score']}", 7)
    pyxel.text(5, 29, f"COMBO: {st['combo']}  x{mul}", mul_color)
    pyxel.text(5, 38, f"BEST:  {st['best_combo']}", 6)

    # 操作説明
    pyxel.line(0, 130, 160, 130, 5)
    pyxel.text(5, 133, "UPPER: Z or SPACE", 7)
    pyxel.text(5, 141, "LOWER: X or M", 7)
    pyxel.text(5, 149, "Q: QUIT", 6)


pyxel.init(160, 160, title="RHYTHM GAME - DEVIL MODE")
pyxel.run(update, draw)
