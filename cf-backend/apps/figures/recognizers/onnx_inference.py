# -*- coding: utf-8 -*-
# @Time    : 25/03/2023 16:27
# @Author  : Marshall
# @FileName: inference.py
import onnxruntime
import numpy as np
import cv2
import os
import math
from apiproject.settings import DETECT_SESSION, TEXTREC_SESSION, CHAR_LIST


# textrec_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\models\sar\sar.onnx"
# textrec_session = onnxruntime.InferenceSession(textrec_path)
# textdet_model_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\models\yolov8\yolov8.onnx"
# onet_session = onnxruntime.InferenceSession(textdet_model_path)

# dict_path = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\models\RobustScanner\dict_file.txt"
# with open(dict_path, 'r', encoding='utf-8') as f:
#     char_list = f.read().splitlines()


def resize_to_height(img, height=48, max_width=160, min_width=32, width_step=4):
    # resizeToHeight
    h, w = img.shape[:2]
    scale_h = height / h
    new_w = int(w * scale_h)
    if new_w > max_width:
        new_w = max_width
    if new_w < min_width:
        new_w = min_width
    if new_w % width_step != 0:
        new_w = new_w // width_step * width_step
    img = cv2.resize(img, (new_w, height), interpolation=cv2.INTER_LINEAR if scale_h > 1 else cv2.INTER_AREA)
    return img


def pad_to_width(img, width=160, pad_value=114):
    # padToWidth
    h, w = img.shape[:2]
    if w < width:
        img, padding_list = pad_image(img, width - w, 0, pad_value, pad_center=False)
    return img


def attention_ocr_decoder(preds):
    # Attention OCR 解码器
    end_index = len(CHAR_LIST)
    ignore_indexes = [end_index + 1]
    max_idx = np.argmax(preds, axis=-1)[0].tolist()
    max_value = np.max(preds, axis=-1)[0].tolist()
    index, score = [], []
    for char_index, char_score in zip(max_idx, max_value):
        if char_index in ignore_indexes:
            continue
        if char_index == end_index:
            break
        index.append(char_index)
        score.append(char_score)
    pred_text = ''.join([CHAR_LIST[i] for i in index])
    pred_score = np.mean(score)
    return pred_text, pred_score


def text_recognition(img_path, bbox=None):
    # 读取图片
    out_size = (160, 48)
    img = cv2.imread(img_path)
    if bbox is None:
        bbox = [0, 0, img.shape[1], img.shape[0]]
    img_box = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    if img_box.shape[0] == 0 or img_box.shape[1] == 0:
        return {"text": "", "score": 0.0}
    # resizeToHeight  ncomms9850_fig2_628.jpg ncomms9850_fig2_632.jpg
    img_box = resize_to_height(img_box, height=out_size[1], max_width=out_size[0], min_width=out_size[1], width_step=4)

    # padToWidth
    img_box = pad_to_width(img_box, out_size[0], pad_value=0)
    img_box = np.transpose(img_box, (2, 0, 1))
    # normalizeImg   # ss = data["inputs"][0].cpu().numpy()
    img_box_normal = normalize_img(img_box, img_mean=127., img_std=127.)
    img_batch = np.expand_dims(img_box_normal, axis=0)
    img_batch = img_batch.astype(np.float32)

    inputs = {TEXTREC_SESSION.get_inputs()[0].name: img_batch}
    outs = TEXTREC_SESSION.run(None, inputs)
    result_dict = {"text": "", "score": 0.0}
    if len(outs) > 0:
        out = outs[0]
        # Attention 解码出字符串
        pred_text, pred_score = attention_ocr_decoder(out)
        result_dict["text"] = pred_text
        result_dict["score"] = pred_score
    return result_dict


def calc_batch_iou(boxes0: np.ndarray, boxes1: np.ndarray):
    """ 计算多个边界框和多个边界框的交并比

    Parameters
    ----------
    boxes0: `~np.ndarray` of shape `(A, 4)`
        边界框

    boxes1: `~np.ndarray` of shape `(B, 4)`
        边界框

    Returns
    -------
    iou: `~np.ndarray` of shape `(A, B)`
        交并比
    """
    A = boxes0.shape[0]
    B = boxes1.shape[0]
    xy_max = np.minimum(boxes0[:, np.newaxis, 2:].repeat(B, axis=1),
                        np.broadcast_to(boxes1[:, 2:], (A, B, 2)))
    xy_min = np.maximum(boxes0[:, np.newaxis, :2].repeat(B, axis=1),
                        np.broadcast_to(boxes1[:, :2], (A, B, 2)))
    # 计算交集面积
    inter = np.clip(xy_max - xy_min, a_min=0, a_max=np.inf)
    inter = inter[:, :, 0] * inter[:, :, 1]
    # 计算每个矩阵的面积
    area_0 = ((boxes0[:, 2] - boxes0[:, 0]) * (
            boxes0[:, 3] - boxes0[:, 1]))[:, np.newaxis].repeat(B, axis=1)
    area_1 = ((boxes1[:, 2] - boxes1[:, 0]) * (
            boxes1[:, 3] - boxes1[:, 1]))[np.newaxis, :].repeat(A, axis=0)
    return inter / (area_0 + area_1 - inter)


def pad_image(img, pad_x, pad_y, pad_value=114, pad_center=True):
    if isinstance(pad_value, int):
        pad_value = (pad_value, pad_value, pad_value)
    if pad_center:
        top_padding, left_padding = int(round(pad_y // 2 - 0.1)), int(
            round(pad_x // 2 - 0.1))
        bottom_padding = pad_y - top_padding
        right_padding = pad_x - left_padding
    else:
        top_padding, bottom_padding = 0, pad_y
        left_padding, right_padding = 0, pad_x
    padding_list = [
        top_padding, bottom_padding, left_padding, right_padding
    ]
    if top_padding != 0 or bottom_padding != 0 or \
            left_padding != 0 or right_padding != 0:
        img = cv2.copyMakeBorder(img, *padding_list, cv2.BORDER_CONSTANT,
                                 value=pad_value)
    return img, padding_list


def normalize_img(img, img_mean=0., img_std=255.):
    if img_mean is None:
        img_mean = np.array([[[0.]], [[0.]], [[0.]]])
    if img_std is None:
        img_std = np.array([[[255.]], [[255.]], [[255.]]])
    if isinstance(img_mean, float):
        img_mean = np.array([[[img_mean]], [[img_mean]], [[img_mean]]])
    if isinstance(img_std, float):
        img_std = np.array([[[img_std]], [[img_std]], [[img_std]]])
    img = (img - img_mean) / img_std
    return img


def load_image(img_path):
    out_size = (640, 640)
    # 读取图片
    img = cv2.imread(img_path)
    width = img.shape[1]
    height = img.shape[0]
    # 如果是灰度图，转换为BGR
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # 保留原始比例，640x640,其余部分用padval填充 1280  2560   320 160
    scale = max(img.shape[0] / out_size[0], img.shape[1] / out_size[1])
    new_size = (int(img.shape[1] / scale), int(img.shape[0] / scale))
    img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA if scale > 1 else cv2.INTER_LINEAR)
    pad_x = max(out_size[0] - new_size[0], 0)
    pad_y = max(out_size[1] - new_size[1], 0)
    img, padding_list = pad_image(img, pad_x, pad_y)
    img = np.transpose(img, (2, 0, 1))
    # normalize img_padded
    img = normalize_img(img)
    img_batch = np.expand_dims(img, axis=0)
    img_batch = img_batch.astype(np.float32)
    resize_meta = {
        "scale": scale,
        "width": width,
        "height": height,
        "padding_list": padding_list,
    }
    return img_batch, resize_meta


def get_oringinal_bbox(bboxes, resize_meta):
    scale = resize_meta["scale"]
    padding_list = resize_meta["padding_list"]
    bboxes[:, 0] = (bboxes[:, 0] - padding_list[2]) * scale
    bboxes[:, 1] = (bboxes[:, 1] - padding_list[0]) * scale
    bboxes[:, 2] = (bboxes[:, 2] - padding_list[2]) * scale
    bboxes[:, 3] = (bboxes[:, 3] - padding_list[0]) * scale
    return bboxes

def obj_detection(img_path):
    img_batch, resize_meta = load_image(img_path)
    inputs = {DETECT_SESSION.get_inputs()[0].name: img_batch}
    outs = DETECT_SESSION.run(None, inputs)
    return outs, resize_meta


def backend_recognize(img_path, pred_score_thresh=0.3):
    outs, resize_meta = obj_detection(img_path)
    categories_dict = {0: "figures", 1: "figure_nos", 2: "bars", 3: "labels"}
    bbox_result = {"figures": [], "figure_nos": [], "bars": [], "labels": [], "ppi": 0, "width": resize_meta["width"],
                   "height": resize_meta["height"], "name": os.path.basename(img_path), "meta": {}}
    if len(outs) == 4:
        scores = outs[2]
        filter_index = scores > pred_score_thresh
        bboxes = np.array(outs[1][filter_index])
        scores = np.array(outs[2][filter_index])
        labels = np.array(outs[3][filter_index])
        origin_boxes = get_oringinal_bbox(bboxes, resize_meta)
        # 获取labels中label=0的索引
        figure_index = np.where(labels == 0)[0]
        other_index = np.where(labels != 0)[0]
        figure_bboxes = origin_boxes[figure_index]
        other_bboxes = origin_boxes[other_index]
        # 重新计算relations 二维数组，第一列为figure的id，后面的列为其他的id，如果没有则为0。
        relations = np.zeros((len(figure_bboxes), 4))  # 按照figure的数目来 4是因为有4种类型
        for i, bbox in enumerate(figure_bboxes):
            left = math.floor(min(bbox[0], bbox[2]))
            top = math.floor(min(bbox[1], bbox[3]))
            right = math.ceil(max(bbox[0], bbox[2]))
            bottom = math.ceil(max(bbox[1], bbox[3]))
            # cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            obj = {"points": [[left, top], [right, bottom]], "score": scores[figure_index[i]], "id": i + 1}
            bbox_result["figures"].append(obj)
            relations[i][0] = i + 1  # 初始化第一列为figure的id

        if len(figure_bboxes) > 0 and len(other_bboxes) > 0:
            batch_iou = calc_batch_iou(other_bboxes, figure_bboxes)
            max_iou_index = np.argmax(batch_iou, axis=1)
        for i, bbox in enumerate(other_bboxes):
            left = math.floor(min(bbox[0], bbox[2]))
            top = math.floor(min(bbox[1], bbox[3]))
            right = math.ceil(max(bbox[0], bbox[2]))
            bottom = math.ceil(max(bbox[1], bbox[3]))
            obj = {"points": [[left, top], [right, bottom]], "score": scores[other_index[i]],
                   "id": i + 1 + len(figure_bboxes)}
            label = labels[other_index[i]]
            if label == 1 or label == 3:
                text_recognition_result = text_recognition(img_path, [left, top, right, bottom])
                obj["text"] = text_recognition_result["text"]
                obj["text_score"] = text_recognition_result["score"]
            bbox_result[categories_dict[label]].append(obj)
            # 计算other_bboxes与figure_bboxes的iou
            if len(figure_bboxes) > 0 and len(other_bboxes) > 0:
                if batch_iou[i][max_iou_index[i]] == 0:  # 如果最大的iou为0，则不进行赋值
                    continue
                relations[max_iou_index[i]][label] = i + 1 + len(figure_bboxes)  # 最大iou的figure的id label是对应的索引，赋值为其他的id
        bbox_result["relations"] = relations.tolist()
    return bbox_result


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
