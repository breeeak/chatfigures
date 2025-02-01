# -*- coding: utf-8 -*-
# @Time    : 19/05/2023 23:06
# @Author  : Marshall
# @FileName: train_ocr.py
from ultralytics import YOLO
import os
import cv2
import json
from pathlib import Path
import numpy as np
from ultralytics.yolo.utils.metrics import calc_batch_iou
from tqdm import tqdm
from .ocr_model.utils import CTCLabelConverter
from .ocr_model.model import Model, Options
import torch
from PIL import Image
import math
import torchvision.transforms as transforms
import torch.nn.functional as F
import re

class NormalizePAD(object):

    def __init__(self, max_size, PAD_type='right'):
        self.toTensor = transforms.ToTensor()
        self.max_size = max_size
        self.max_width_half = math.floor(max_size[2] / 2)
        self.PAD_type = PAD_type

    def __call__(self, img):
        img = self.toTensor(img)
        img.sub_(0.5).div_(0.5)
        c, h, w = img.size()
        Pad_img = torch.FloatTensor(*self.max_size).fill_(0)
        Pad_img[:, :, :w] = img  # right pad
        if self.max_size[2] != w:  # add border Pad
            Pad_img[:, :, w:] = img[:, :, w - 1].unsqueeze(2).expand(c, h, self.max_size[2] - w)

        return Pad_img


class ResizeNormalize(object):

    def __init__(self, size, interpolation=Image.BICUBIC):
        self.size = size
        self.interpolation = interpolation
        self.toTensor = transforms.ToTensor()

    def __call__(self, img):
        img = img.resize(self.size, self.interpolation)
        img = self.toTensor(img)
        img.sub_(0.5).div_(0.5)
        return img

def predict_texts(text_boxes, img_path, text_model):
    opt = text_model.module.opt
    if opt.rgb:
        img = Image.open(img_path).convert('RGB')  # for color image
    else:
        img = Image.open(img_path).convert('L')
    w, h = img.size
    if opt.PAD:
        resized_max_w = opt.imgW
        input_channel = 3 if opt.rgb else 1
        transform = NormalizePAD((input_channel, opt.imgH, resized_max_w))
    else:
        transform = ResizeNormalize((opt.imgW, opt.imgH))

    text_images = []
    for text_box in text_boxes:
        x1, y1, x2, y2 = text_box
        x1, y1, x2, y2 = int(max(0, math.floor(x1))), int(max(0, math.floor(y1))), int(min(w, math.ceil(x2))), int(min(h, math.ceil(y2)))
        text_img = img.crop((x1, y1, x2, y2))
        if opt.PAD:
            w_c, h_c = text_img.size
            ratio = w_c / float(h_c)
            if math.ceil(opt.imgH * ratio) > opt.imgW:
                resized_w = opt.imgW
            else:
                resized_w = math.ceil(opt.imgH * ratio)
            text_img = text_img.resize((resized_w, opt.imgH), Image.BICUBIC)
        text_images.append(transform(text_img))
    image_tensors = torch.cat([t.unsqueeze(0) for t in text_images], 0)
    batch_size = image_tensors.size(0)
    image = image_tensors.to(text_model.device)
    # For max length prediction
    length_for_pred = torch.IntTensor([opt.batch_max_length] * batch_size).to(text_model.device)
    text_for_pred = torch.LongTensor(batch_size, opt.batch_max_length + 1).fill_(0).to(text_model.device)
    if 'CTC' in opt.Prediction:
        preds = text_model(image, text_for_pred)
        # Select max probabilty (greedy decoding) then decode index to character
        preds_size = torch.IntTensor([preds.size(1)] * batch_size)
        _, preds_index = preds.max(2)
        # preds_index = preds_index.view(-1)
        preds_str = text_model.converter.decode(preds_index, preds_size)

    else:
        preds = text_model(image, text_for_pred, is_train=False)
        # select max probabilty (greedy decoding) then decode index to character
        _, preds_index = preds.max(2)
        preds_str = text_model.converter.decode(preds_index, length_for_pred)
    results = []
    preds_prob = F.softmax(preds, dim=2)
    preds_max_prob, _ = preds_prob.max(dim=2)
    for pred, pred_max_prob in zip(preds_str, preds_max_prob):
        if 'Attn' in opt.Prediction:
            pred_EOS = pred.find('[s]')
            pred = pred[:pred_EOS]  # prune after "end of sentence" token ([s])
            pred_max_prob = pred_max_prob[:pred_EOS]
        # calculate confidence score (= multiply of pred_max_prob)
        confidence_score = pred_max_prob.cumprod(dim=0)[-1]
        results.append({'text': pred, 'text_score': confidence_score.detach().cpu().numpy().item()})
    return results



class NumpyJsonEncoder(json.JSONEncoder):
    """
    重写json的encoder，使其可以序列化numpy的数据
    """
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        else:
            return super(NumpyJsonEncoder, self).default(o)
def get_bbox_result(result, text_model=None, text_classes=None, other_classes=None, is_scale_bar=False):
    """
    获取json格式的bbox结果 包括了figures, relations
    """
    if text_classes is None:
        text_classes = [1, 3]
    if other_classes is None:
        other_classes = [1, 2, 3]
    categories_dict = result.names
    bbox_result = {}
    for value in categories_dict.values():
        bbox_result[value] = []
    bboxes = result.boxes.data[:, :4].cpu().numpy()
    scores = result.boxes.conf.cpu().numpy()
    labels = result.boxes.cls.cpu().numpy()

    if is_scale_bar:    # scale bar的类别加了2
        bbox_result['figures'] = []
        labels = labels + 2
        categories_dict = {}
        for key in result.names.keys():
            categories_dict[key + 2] = result.names[key]


    # 获取labels中label=0的索引
    figure_index = np.where(labels == 0)[0]
    text_index = []
    other_index = []
    if len(labels) > 0:
        for classs in other_classes:
            class_index = np.where(labels == classs)[0]
            if classs in text_classes:
                text_index.extend(class_index)
            other_index.extend(class_index)

    figure_bboxes = bboxes[figure_index]
    other_bboxes = bboxes[other_index]

    if len(text_index) > 0:
        text_bboxes = bboxes[text_index]
        texts = predict_texts(text_bboxes, result.path, text_model)
    else:
        texts = []

    # 重新计算relations 二维数组，第一列为figure的id，后面的列为其他的id，如果没有则为0。
    relations = np.zeros((len(figure_bboxes), 4))   # 按照figure的数目来 4是因为有4种类型
    for i, bbox in enumerate(figure_bboxes):
        obj = {"points": [[bbox[0], bbox[1]], [bbox[2], bbox[3]]], "score": scores[figure_index[i]], "id": i + 1}
        bbox_result["figures"].append(obj)
        relations[i][0] = i + 1     # 初始化第一列为figure的id

    if len(figure_bboxes) > 0 and len(other_bboxes) > 0:
        batch_iou = calc_batch_iou(other_bboxes, figure_bboxes)
        max_iou_index = np.argmax(batch_iou, axis=1)
    for i, bbox in enumerate(other_bboxes):
        obj = {"points": [[bbox[0], bbox[1]], [bbox[2], bbox[3]]], "score": scores[other_index[i]], "id": i + 1 + len(figure_bboxes)}
        label = int(labels[other_index[i]])
        if label in text_classes:
            text_i = np.argwhere(text_index == other_index[i])[0][0]
            obj["text"] = texts[text_i]["text"]
            obj["text_score"] = texts[text_i]["text_score"]
        bbox_result[categories_dict[label]].append(obj)
        # 计算other_bboxes与figure_bboxes的iou
        if len(figure_bboxes) > 0 and len(other_bboxes) > 0:
            if batch_iou[i][max_iou_index[i]] == 0:  # 如果最大的iou为0，则不进行赋值
                continue
            relations[max_iou_index[i]][label] = i + 1 + len(figure_bboxes) # 最大iou的figure的id label是对应的索引，赋值为其他的id
    bbox_result["relations"] = relations.tolist()
    return bbox_result

def get_ppi(result):
    """
    简单获取ppi 只取第一个bar和第一个label 并且直接使用bbox的坐标计算
    :param result: 预测结果
    :return: ppi    pixelsPerMeter
    """
    unit_list = ["nm", "um", "mm", "cm", "dm", "m", "km"]
    ppi = 0
    # 只取第一个bar和第一个label
    bar_len = result["bars"][0]["points"][1][0] - result["bars"][0]["points"][0][0]
    if bar_len <= 0:
        return ppi
    bar_text = result["labels"][0]["text"]
    # 正则提取单位和数字
    pattern = re.compile(r"(\d+\.?\d*)(\D+)")
    matchs = pattern.match(bar_text)
    if matchs:
        unit = matchs.group(2).lower()
        if unit in unit_list:
            num = float(matchs.group(1))
            act_length = 0
            if num > 0:
                if unit == "nm":
                    act_length = num / 1e9
                elif unit == "um":
                    act_length = num / 1e6
                elif unit == "mm":
                    act_length = num / 1e3
                elif unit == "cm":
                    act_length = num / 1e2
                elif unit == "dm":
                    act_length = num / 1e1
                elif unit == "m":
                    act_length = num / 1
                elif unit == "km":
                    act_length = num / 1e-3
            if act_length > 0:
                ppi = bar_len / act_length
    return ppi

def result2std_json(results, out_dir, origin_label_dir=None, text_model=None):
    """
    将预测结果转换为标准的json格式,
    :param results: 预测结果
    :param out_dir: 输出路径
    :param origin_label_dir: 原始标注的路径 包含ppi和meta信息  如果没有则为None
    """
    for result in results:
        try:
            img_name = Path(result.path).name
            out_label_path = os.path.join(out_dir, Path(result.path).stem + ".json")
            result_dict = get_bbox_result(result, text_model)
            result_dict["name"] = img_name
            result_dict["width"] = result.orig_shape[1]
            result_dict["height"] = result.orig_shape[0]
            if origin_label_dir:
                origin_label_path = os.path.join(origin_label_dir,  Path(result.path).stem + ".json")
                with open(origin_label_path, "r", encoding="utf-8") as f:
                    origin_label = json.load(f)
                result_dict["ppi"] = origin_label["ppi"]
                result_dict["meta"] = origin_label["meta"]
            else:
                result_dict["ppi"] = 0
                result_dict["meta"] = {}
            js = json.dumps(result_dict, indent=2, cls=NumpyJsonEncoder)
            with open(out_label_path, "w", encoding="utf-8") as f:
                f.write(js)
        except Exception as e:
            print(e)
            print(result["img_path"])
            continue

def load_text_model(text_model_path):
    """
    加载text model
    """
    opt = Options()
    opt.PAD = False
    opt.imgW = 50
    opt.rgb = True
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = Model(opt)
    converter = CTCLabelConverter(model.opt.character)
    model = torch.nn.DataParallel(model).to(device)
    model.load_state_dict(torch.load(text_model_path, map_location=device))
    model.eval()
    model.converter = converter
    model.device = device
    return model


def batch_predict_yolo_ocr(draw_result=False):
    dir_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\yolo_formal\images\val"
    origin_label_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\jsons"

    out_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\yolo_formal\eval\yolov8_crnn_predict"
    os.makedirs(out_dir, exist_ok=True)
    # model_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\stage1\epoch200.pt"
    # model_path = r"D:\3_Research\1_Project\1_Python\yolov8_edit\ultralytics\runs\ocr\train161\weights\best.pt"
    yolo_model_path = r"D:\3_Research\1_Project\1_Python\yolo_v8_v2\ultralytics\yolo_ocr\detect\960detect_formal4\weights\best.pt"
    text_model_path = r"D:\3_Research\1_Project\1_Python\yolov8_edit\deep-text-recognition-benchmark-master\saved_models\None-VGG-BiLSTM-CTC-PAD-Seed777-figure-no\best_accuracy.pth"

    text_model = load_text_model(text_model_path)

    model = YOLO(yolo_model_path, task="detect")
    results = model.predict(dir_path, stream=True, conf=0.3)

    result2std_json(results, out_dir, origin_label_dir=origin_label_dir, text_model=text_model)


    if draw_result:

        out_draw_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\tests\exp1\predict_draws"

        os.makedirs(out_draw_dir, exist_ok=True)
        for result in results:
            res_plotted = result.plot(probs=False)
            img_name = result.path.split("\\")[-1]
            out_path = os.path.join(out_draw_dir, img_name)
            cv2.imwrite(out_path, res_plotted)
            # js = json.loads(results[0].tojson())
            # out_json_path = os.path.join(out_draw_dir, img_name.replace(".jpg", ".json"))
            # with open(out_json_path, "w") as f:
            #     json.dump(js, f, indent=4)


class NumpyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        else:
            return super(NumpyJsonEncoder, self).default(o)


def predict_one():
    img_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\yolo_formal\images\val\srep32784_fig1.jpg"
    model_path = r"D:\3_Research\1_Project\1_Python\yolo_v8_v2\ultralytics\yolo_ocr\detect\960detect\weights\best.pt"
    model = YOLO(model_path)
    result = model.predict(img_path, conf=0.3)
    print(result)


def add_height():
    import cv2
    from tqdm import tqdm
    gt_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\jsons"
    img_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\figures"
    for lbl_name in tqdm(os.listdir(gt_dir)):
        gt_path = os.path.join(gt_dir, lbl_name)
        with open(gt_path, 'r', encoding="utf-8") as f:
            gt_json = json.load(f)
        if "height" in gt_json.keys():
            continue
        img_name = gt_json["name"]
        img_path = os.path.join(img_dir, img_name)
        height, width = cv2.imread(img_path).shape[:2]
        gt_json["height"] = height
        js = json.dumps(gt_json, indent=2, cls=NumpyJsonEncoder)
        with open(gt_path, "w", encoding="utf-8") as f:
            f.write(js)

if __name__ == '__main__':
    # batch_predict_yolo_ocr()
    add_height()
    pass
