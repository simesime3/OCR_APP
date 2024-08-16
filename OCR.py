!pip install pyocr

import streamlit as st # フロントエンドを扱うstreamlitの機能をインポート
from PIL import Image # 画像扱うための機能をインポート
import pyocr # 外部OCRを扱うための機能をインポート
import platform # OSの判別するために、プラットフォームを読み込む機能をインポート

# それぞれのOSにインストールされるtesseractの場所を指定
# ※講義のためにmacでもwindowsでも動くように指定しています。
if platform.system() == "Windows":
    pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
elif platform.system() == "Darwin":
    pyocr.tesseract.TESSERACT_CMD = r"/opt/homebrew/bin/tesseract"
else:
    pyocr.tesseract.TESSERACT_CMD = r"/usr/local/bin/tesseract"



# 画像読み込みのための言語と言語のコードを変換するリストを設定
set_language_list = {
    "日本語" :"jpn",
    "英語" :"eng",
}


print("文字認識アプリ") # タイトル表示

set_language = st.selectbox("音声認識する言語を選んでください。",set_language_list.keys()) # 言語選択のためのリスト



# OCRエンジンを取得
engines = pyocr.get_available_tools() # pyocrが認識できるOCR外部ツールを検知
engine = engines[0] # ツールを複数選択して、エラーにならないように１つだけ選択

# tesseractが認識できるpngとjpgだけを許可するアップローダーの設置
file_upload = st.file_uploader("ここに音声認識したファイルをアップロードしてください。",type=["png","jpg"])
print(file_upload)  # 画像分析する画像を表示
if (file_upload !=None):
    # 画像の文字を読み込む
    # engine.image_to_string(開いた画像,画像認識する言語)で画像分析開始し、分析結果をtxtに代入
    txt = engine.image_to_string(Image.open(file_upload), lang=set_language_list[set_language])
    print(txt) # 分析結果を表示

    print("感情分析の結果") # 案内表示
    from asari.api import Sonar # 文字から感情分析する機能をインポート
    sonar = Sonar() # Sonar()をsonarに代入
    res = sonar.ping(text=txt) # sonar.ping(text=分析したい文字)で感情分析リクエストし、結果をresに代入
    print(res["classes"]) # res["classes"]に結果が変えて来るので、これを表示
