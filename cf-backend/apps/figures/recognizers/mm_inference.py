# -*- coding: utf-8 -*-
# @Time    : 30/03/2023 20:28
# @Author  : Marshall
# @FileName: mm_inference.py

from apiproject.settings import DETECT_SESSION, TEXTREC_SESSION
import mmcv
import os
import numpy as np
from mmdet.apis import inference_detector


# from mmyolo.utils import register_all_modules
# from mmdet.apis import init_detector
# from mmocr.apis import TextRecInferencer
# DETECT_CFG_PATH = r'D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\models\mmlab\yolov8_l_syncbn_cf.py'
# DETECT_PTH_PATH = r'D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\models\mmlab\yolov8_epoch_300.pth'
# DETECT_SESSION = init_detector(DETECT_CFG_PATH, DETECT_PTH_PATH, device='cpu')  # or device='cpu'
#
# TEXTREC_CFG_PATH = r'D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\models\mmlab\robustscanner_resnet31_5e_st-sub_mj-sub_sa_real.py'
# TEXTREC_PTH_PATH = r'D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\models\mmlab\robustscanner_epoch_5.pth'
# TEXTREC_SESSION = TextRecInferencer(model=TEXTREC_CFG_PATH, weights=TEXTREC_PTH_PATH, device='cpu')
# register_all_modules()


def text_recognition(img_path, bbox=None):
    """
    使用mmocr识别网络
    """
    img = mmcv.imread(img_path)
    # 获得bbox下的图像
    img_crop = mmcv.imcrop(img, np.array(bbox))
    result = TEXTREC_SESSION(img_crop)
    return result["predictions"]



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


def obj_detection(img_path):
    image = mmcv.imread(img_path, channel_order='rgb')
    result = inference_detector(DETECT_SESSION, image)
    return result


def backend_recognize(img_path, pred_score_thr=0.3):
    result = obj_detection(img_path)
    categories_dict = {0: "figures", 1: "figure_nos", 2: "bars", 3: "labels"}
    bbox_result = {"figures": [], "figure_nos": [], "bars": [], "labels": [], "ppi": 0, "width": result.ori_shape[1],
                   "height": result.ori_shape[0], "name": os.path.basename(img_path), "meta": {}}

    all_scores = result.pred_instances.scores.numpy()
    filter_index = all_scores > pred_score_thr
    bboxes = result.pred_instances.bboxes.numpy()[filter_index]
    labels = result.pred_instances.labels.numpy()[filter_index]
    scores = result.pred_instances.scores.numpy()[filter_index]

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
        label = labels[other_index[i]]
        if label == 1 or label == 3:
            text_recognition_result = text_recognition(img_path, bbox)
            if len(text_recognition_result) > 0:
                obj["text"] = text_recognition_result[0]["text"]
                obj["text_score"] = text_recognition_result[0]["scores"]
            else:
                # no text detected
                obj["text"] = ""
                obj["text_score"] = 0.
        bbox_result[categories_dict[label]].append(obj)
        # 计算other_bboxes与figure_bboxes的iou
        if len(figure_bboxes) > 0 and len(other_bboxes) > 0:
            if batch_iou[i][max_iou_index[i]] == 0:  # 如果最大的iou为0，则不进行赋值
                continue
            relations[max_iou_index[i]][label] = i + 1 + len(figure_bboxes) # 最大iou的figure的id label是对应的索引，赋值为其他的id
    bbox_result["relations"] = relations.tolist()
    return bbox_result

if __name__ == '__main__':
    # mmlab_based_recognize()
    pass
    image_path = r"D:\3_Research\1_Project\1_Python\obj_det_fig_3\article_image_recognition\test\demo.jpg"
    backend_recognize(image_path)

