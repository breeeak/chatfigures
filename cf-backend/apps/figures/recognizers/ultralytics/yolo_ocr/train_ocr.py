# -*- coding: utf-8 -*-
# @Time    : 19/05/2023 23:06
# @Author  : Marshall
# @FileName: train_ocr.py
from ultralytics import YOLO

def batch_predict_yolo_ocr():
    model = YOLO('yolov8l-ocr.yaml', task="ocr")
    model.train(cfg="default-ocr.yaml")

def train_yolo_ocr():
    model = YOLO('yolov8l-ocr.yaml', task="ocr")
    model.train(cfg="default-ocr.yaml")

def train_yolo():
    model = YOLO('yolov8l.yaml', task="detect")
    model.train(cfg="default.yaml")

if __name__ == '__main__':
    train_yolo()
    pass
