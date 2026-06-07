import os
import shutil

# 整理したいフォルダのパス（Windowsの場合は r"C:\Users\ユーザー名\Desktop\テスト仕分け" のように書き換えてください）
TARGET_DIR = r"C:\Users\owner\Desktop\仕分けpyテスト用"

# 拡張子と移動先フォルダの組み合わせルール
RULES = {
    "画像": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".heic"],
    "動画": [".mp4", ".mov", ".avi", ".wmv", ".mkv", ".flv"],
    "ドキュメント": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
    "圧縮ファイル": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
    "その他": [".exe", ".dmg", ".lnk", ".url", ".py", ".html", ".css", ".js", ".json", ".xml", ".cfg", ".ini", ".conf", ".log", ".csv"],
}

# フォルダの中身を1つずつチェック
for filename in os.listdir(TARGET_DIR):
    filepath = os.path.join(TARGET_DIR, filename)
    
    # フォルダではなく「ファイル」の場合だけ処理する
    if os.path.isfile(filepath):
        _, ext = os.path.splitext(filename)
        ext = ext.lower() # 大文字を小文字に統一
        
        moved = False
        # ルールに合うかチェック
        for folder_name, extensions in RULES.items():
            if ext in extensions:
                # 移動先のフォルダを作る
                new_dir = os.path.join(TARGET_DIR, folder_name)
                os.makedirs(new_dir, exist_ok=True)
                # ファイルを移動
                shutil.move(filepath, os.path.join(new_dir, filename))
                print(f"【{folder_name}】へ移動: {filename}")
                moved = True
                break
        
        # どのルールにも当てはまらない場合「その他」へ
        if not moved:
            new_dir = os.path.join(TARGET_DIR, "その他")
            os.makedirs(new_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(new_dir, filename))
            print(f"【その他】へ移動: {filename}")

print("ファイルの仕分けが完了しました！")
