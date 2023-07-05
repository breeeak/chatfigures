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
def get_bbox_result(result):
    """
    获取json格式的bbox结果 包括了figures, relations
    """
    categories_dict = result.names
    bbox_result = {}
    for value in categories_dict.values():
        bbox_result[value] = []
    bboxes = result.boxes.data[:, :4].cpu().numpy()
    scores = result.boxes.conf.cpu().numpy()
    labels = result.boxes.cls.cpu().numpy()
    texts = result.ocrs
    # 获取labels中label=0的索引
    figure_index = np.where(labels == 0)[0]
    other_index = np.where(labels != 0)[0]
    figure_bboxes = bboxes[figure_index]
    other_bboxes = bboxes[other_index]

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
        if label == 1 or label == 3:
            obj["text"] = texts[other_index[i]]
            obj["text_score"] = 1.
        bbox_result[categories_dict[label]].append(obj)
        # 计算other_bboxes与figure_bboxes的iou
        if len(figure_bboxes) > 0 and len(other_bboxes) > 0:
            if batch_iou[i][max_iou_index[i]] == 0:  # 如果最大的iou为0，则不进行赋值
                continue
            relations[max_iou_index[i]][label] = i + 1 + len(figure_bboxes) # 最大iou的figure的id label是对应的索引，赋值为其他的id
    bbox_result["relations"] = relations.tolist()
    return bbox_result


def result2std_json(results, out_dir, origin_label_dir=None):
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
            result_dict = get_bbox_result(result)
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


def batch_predict_yolo_ocr(draw_result=False):
    dir_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\yolo_formal\images\val"
    origin_label_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\jsons"

    out_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\tests\exp1\predict_jsons"
    os.makedirs(out_dir, exist_ok=True)
    # model_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\stage1\epoch200.pt"
    # model_path = r"D:\3_Research\1_Project\1_Python\yolov8_edit\ultralytics\runs\ocr\train161\weights\best.pt"
    model_path = r"D:\3_Research\1_Project\1_Python\yolo_v8_v2\ultralytics\yolo_ocr\run_ocr\class22\weights\best.pt"

    model = YOLO(model_path)
    results = model(dir_path, stream=True)

    result2std_json(results, out_dir, origin_label_dir=origin_label_dir)


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


def predict_each():
    model_base_dir = r"D:\3_Research\1_Project\1_Python\yolo_v8_v2\ultralytics\yolo_ocr\run_each"
    category_dict = {0: "figures", 1: "figure_nos", 2: "bars", 3: "labels"}
    dir_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\scraper\stage1"
    #imgs_path = os.path.join(dir_path, "images")
    imgs_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\scraper\stage1\figures"
    predict_path = os.path.join(dir_path, "predict_each")
    os.makedirs(predict_path, exist_ok=True)
    for value in category_dict.values():
        model_path = os.path.join(model_base_dir, value, "weights", "best.pt")
        model = YOLO(model_path)
        if value == "figures":
            results = model(imgs_path, stream=True, is_predict_soft_nms=True)
        else:
            results = model(imgs_path, stream=True)
        out_dir = os.path.join(predict_path, value)
        os.makedirs(out_dir, exist_ok=True)
        for result in tqdm(results):
            result_dict = {}
            out_label_path = os.path.join(out_dir, Path(result.path).stem + ".json")
            result_dict["results"] = json.loads(result.tojson())
            result_dict["name"] = Path(result.path).name
            with open(out_label_path, "w") as f:
                json.dump(result_dict, f, indent=2, cls=NumpyJsonEncoder)


def get_bbox_result_from_json(result_json, categories_dict):
    bbox_result = {}
    i = 0
    figure_bboxes = []
    other_bboxes = []
    other_indexes = []
    other_cls = []
    relations = np.zeros((len(result_json["figures"]["results"]), 4))   # 按照figure的数目来 4是因为有4种类型
    for value in categories_dict.values():
        bbox_result[value] = []
    for label, value in enumerate(categories_dict.values()):
        for predict in result_json[value]["results"]:
            box = predict["box"]
            i += 1
            obj = {"points": [[box["x1"], box["y1"]], [box["x2"], box["y2"]]], "score": predict["confidence"], "id": i}
            if label == 1 or label == 3:
                if "text" in predict.keys() and "text_score" in predict.keys():
                    obj["text"] = predict["text"]
                    obj["text_score"] = 1.
            if value == "figures":
                relations[len(figure_bboxes)][0] = i
                figure_bboxes.append([box["x1"], box["y1"], box["x2"], box["y2"]])
            else:
                other_indexes.append(i)
                other_cls.append(label)
                other_bboxes.append([box["x1"], box["y1"], box["x2"], box["y2"]])
            bbox_result[value].append(obj)
    other_bboxes_len = len(result_json["figure_nos"]["results"]) + len(result_json["bars"]["results"]) + len(result_json["labels"]["results"])
    if len(figure_bboxes) > 0 and other_bboxes_len > 0:
        batch_iou = calc_batch_iou(np.array(other_bboxes), np.array(figure_bboxes))
        max_iou_index = np.argmax(batch_iou, axis=1)
        for i in range(len(other_bboxes)):
            if batch_iou[i][max_iou_index[i]] > 0:  # 如果最大的iou为0，则不进行赋值
                relations[max_iou_index[i]][other_cls[i]] = other_indexes[i]  # 最大iou的figure的id label是对应的索引，赋值为其他的id

    bbox_result["relations"] = relations.tolist()
    return bbox_result


def each_result2std_json():
    blank_labels_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\scraper\stage1\blank_jsons"
    predict_all_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\scraper\stage1\predict_each"
    predict_std_all_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\scraper\stage1\jsons"
    os.makedirs(predict_std_all_path, exist_ok=True)

    category_dict = {0: "figures", 1: "figure_nos", 2: "bars", 3: "labels"}
    for blank_label_name in tqdm(os.listdir(blank_labels_dir)):
        blank_label_path = os.path.join(blank_labels_dir, blank_label_name)
        with open(blank_label_path, "r") as f:
            blank_label = json.load(f)
        predict_results = {}
        for category in category_dict.values():
            predict_dir = os.path.join(predict_all_path, category)
            predict_path = os.path.join(predict_dir, blank_label_name)
            if os.path.exists(predict_path):
                with open(predict_path, "r") as f:
                    predict_results[category] = json.load(f)
            else:
                predict_results[category] = []
        # try:
        out_std_path = os.path.join(predict_std_all_path, blank_label_name)
        result_dict = get_bbox_result_from_json(predict_results, category_dict)

        result_dict["name"] = blank_label["name"]
        result_dict["width"] = blank_label["width"]
        result_dict["height"] = blank_label["height"]
        result_dict["ppi"] = blank_label["ppi"]
        result_dict["meta"] = blank_label["meta"]
        with open(out_std_path, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2, cls=NumpyJsonEncoder)

        # except Exception as e:
        #     print(e)
        #     print(blank_label_name)


def each_predict():
    # 1. predict each
    # predict_each()
    # 2. predict text

    # 3. each result to std json
    # each_result2std_json()
    pass

if __name__ == '__main__':
    batch_predict_yolo_ocr()
    pass
