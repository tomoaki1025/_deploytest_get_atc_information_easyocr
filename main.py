import easyocr
import re
import cv2
import tempfile
import requests
import os


# url = "https://www.data.jma.go.jp/airinfo/data/pict/comment/ADJH01_RJFU.png"
# res = requests.get(url)
# img = None
# with tempfile.NamedTemporaryFile(dir='./') as fp:
#     fp.write(res.content)
#     fp.file.seek(0)
#     img = cv2.imread(fp.name)
#     print(fp.name)


def imread_web(url):
    res = requests.get(url)  # 画像をリクエストする
    img = None
    # Tempfileを作成して即読み込む
    fp = tempfile.NamedTemporaryFile(dir='./', delete=False)
    fp.write(res.content)
    fp.close()
    img = cv2.imread(fp.name)
    os.remove(fp.name)
    return img


def get_gai_comme():
    img = imread_web('https://www.data.jma.go.jp/airinfo/data/pict/comment/ADJH01_RJFU.png')
    cropped_image = img[117: 450, 45: 1056]
    date_image = img[25: 62, 1280: 1640]

    reader = easyocr.Reader(['ja', 'en'], gpu=False)  # this needs to run only once to load the model into memory
    result = reader.readtext(cropped_image, text_threshold=0.94)
    date_result = reader.readtext(date_image, text_threshold=0.94)
    date = date_result[0][1]

    text = ""
    for t in result:
        try:
            if re.compile("[亜-熙ぁ-んァ-ヶ]").search(t[1]):
                text = text + t[1]
        except:
            continue

    print(text)
    # 正規表現による必要文字列の切り出し
    p = r'(?<=湿).*(?=【長崎)'
    com_p = r'(?<=コメント】).*'
    gaikyo = re.findall(p, text)[0]
    comment = re.findall(com_p, text)[0]
    # OCR誤植の修正
    trans_gaikyo = gaikyo.translate(str.maketrans({'ガ': 'が', '順': '傾'}))
    trans_comment = comment.translate(str.maketrans({'ガ': 'が'}))
    gai_comme = {f'天気概況 {date}': trans_gaikyo, f'コメント {date}': trans_comment}

    return gai_comme
