# -*- coding: utf-8 -*-
from .predict import OcrPredictor, predict
from .train import OcrTrainer, train
from .val import OcrValidator, val

__all__ = 'OcrPredictor', 'predict', 'OcrTrainer', 'train', 'OcrValidator', 'val'
