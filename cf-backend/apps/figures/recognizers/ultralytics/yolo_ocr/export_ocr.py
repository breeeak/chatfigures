# -*- coding: utf-8 -*-
# @Time    : 23/05/2023 21:44
# @Author  : Marshall
# @FileName: export_ocr.py
from ultralytics import YOLO


def export_ocr():
    model_path = r"D:\3_Research\1_Project\1_Python\yolov8_edit\ultralytics\runs\ocr\train211\weights\best.pt"
    model = YOLO(model_path)  # load a custom trained
    model.export(format='onnx')


if __name__ == '__main__':
    export_ocr()

