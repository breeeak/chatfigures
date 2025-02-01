# -*- coding: utf-8 -*-
# @Time    : 25/03/2023 16:27
# @Author  : Marshall
# @FileName: inference.py
import onnxruntime
import numpy as np
import cv2
import os
import math
from apiproject.settings import DETECT_SESSION, TEXTREC_SESSION, DETECT_BAR_SESSION, TEXTREC_BAR_SESSION
from apps.figures.recognizers.ultralytics.yolo_ocr.predict_ocr_each import get_bbox_result, get_ppi


def backend_recognize(img_path, pred_score_thresh=0.3):
    result = DETECT_SESSION.predict(img_path, conf=pred_score_thresh)[0]
    result_dict = get_bbox_result(result, TEXTREC_SESSION)
    result_dict["ppi"] = 0
    result_dict["meta"] = {}
    result_dict["name"] = os.path.basename(img_path)
    result_dict["width"] = result.orig_shape[1]
    result_dict["height"] = result.orig_shape[0]
    return result_dict

def backend_recognize_bar(img_path, pred_score_thresh=0.3):
    result = DETECT_BAR_SESSION.predict(img_path, conf=pred_score_thresh)[0]
    result_dict = get_bbox_result(result, TEXTREC_BAR_SESSION, is_scale_bar=True)
    # 如果没有figure，但是有bar和label，则计算ppi
    if len(result_dict["figures"]) == 0 and len(result_dict["bars"]) > 0 and len(result_dict["labels"]) > 0:
        result_dict["ppi"] = get_ppi(result_dict)
    else:
        result_dict["ppi"] = 0
    result_dict["meta"] = {}
    result_dict["name"] = os.path.basename(img_path)
    result_dict["width"] = result.orig_shape[1]
    result_dict["height"] = result.orig_shape[0]
    return result_dict


if __name__ == '__main__':
    pass
    # img_path = r"E:\1_dataset\scalebar_stage1\stage1\coco\test\ncomms9850_fig2.jpg"
    # img_path = r"D:\3_Research\1_Project\1_Python\obj_det_fig_3\article_image_recognition\test\demo_text.jpg"
    # img_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\stage1\text_rec_ic11\test"
    # for img_name in os.listdir(img_dir):
    #     img_path = os.path.join(img_dir, img_name)
    #     text_recognition(img_path)
    # TODO onnx模型与pytorh模型在文本识别上有较大差异 怀疑是prim:constant 异常警告
    # img_path = r"D:\3_Research\1_Project\1_Python\obj_det_fig_3\article_image_recognition\test\demo3.jpg"
    # demo_test3(img_path)
