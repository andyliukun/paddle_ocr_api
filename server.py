from paddleocr import PaddleOCR
from sanic import Sanic
from sanic.response import json
import re

app = Sanic("ocr_api")


def get_ocr_json(img):
    # use_gpu 如果paddle是GPU版本请设置为 True
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, det=False, ocr_version="PP-OCRv4")

    result_str = ocr.ocr(img, cls=False).__str__()
    result = re.findall(r'\((.*?)\)', result_str)
    return result


def get_text_json(text):
    text_dict = {}
    for line in text:
        line_rep = line.replace('\'', '')
        index = line_rep.index(', ')
        var_dict_before = line_rep[:index]
        var_dict_after = line_rep[index + 2:]
        text_dict[var_dict_before] = var_dict_after
    return text_dict


@app.post("/ocr")
async def ocr_api(request):
    # 通过文件流转bytes，获取到OCR内容
    result = get_ocr_json(request.files.get("img").body)
    # 处理ocr内容为字典类型，以便json传出
    json_str = get_text_json(result)
    return json(json_str)
