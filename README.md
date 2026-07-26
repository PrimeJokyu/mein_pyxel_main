#プロジェクトについて

## 概要
pyxelというpythonライブラリを活用して、パラメーターを調整することでクリアタイムを早くするゲームを作成した。

## 参考

chatGPTとの会話は以下
https://chatgpt.com/share/68ae604c-e724-8012-a4d9-33f832d3ff6d

## ビルド方法

PyxelアプリをWeb（HTML）用や配布用パッケージとしてビルドするには、Pyxel標準のコマンドを使用します。作業ディレクトリ（例: `mein0012/`）に移動してから実行してください。

### 1. アプリケーションのパッケージ化（必須）
まず、プログラムとそのリソースを一つのファイル（`.pyxapp`）にまとめます。

```powershell
python -m pyxel package . main.py
```
コマンドを実行したフォルダ内にパッケージファイル（例: `mein0012.pyxapp`）が生成されます。

### 2. Web（HTML）版の生成
生成した `.pyxapp` ファイルを利用して、ブラウザ上で動作するHTMLファイルを生成します。

```powershell
python -m pyxel app2html mein0012.pyxapp
```
これで `mein0012.html` が出力されます。パソコン上のブラウザにドラッグ＆ドロップして開くだけで遊べます。

### 3. Windows実行ファイル（.exe）の生成
単独で動作するWindows用exeファイルとして配布したい場合は、事前に `pyinstaller` をインストールした上で以下を実行します。

```powershell
pip install pyinstaller
python -m pyxel app2exe mein0012.pyxapp
```
