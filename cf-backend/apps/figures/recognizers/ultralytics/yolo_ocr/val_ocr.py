# -*- coding: utf-8 -*-
# @Time    : 17/06/2023 22:25
# @Author  : Marshall
# @FileName: val_ocr.py

from ultralytics import YOLO

import os
import numpy as np
import json
from pathlib import Path
import torch
from tqdm import tqdm
import seaborn as sn
import matplotlib.pyplot as plt


def box_iou(box1, box2, eps=1e-7):
    """
    Calculate intersection-over-union (IoU) of boxes.
    Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
    Based on https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py

    Args:
        box1 (torch.Tensor): A tensor of shape (N, 4) representing N bounding boxes.
        box2 (torch.Tensor): A tensor of shape (M, 4) representing M bounding boxes.
        eps (float, optional): A small value to avoid division by zero. Defaults to 1e-7.

    Returns:
        (torch.Tensor): An NxM tensor containing the pairwise IoU values for every element in box1 and box2.
    """

    # inter(N,M) = (rb(N,M,2) - lt(N,M,2)).clamp(0).prod(2)
    (a1, a2), (b1, b2) = box1.unsqueeze(1).chunk(2, 2), box2.unsqueeze(0).chunk(2, 2)
    inter = (torch.min(a2, b2) - torch.max(a1, b1)).clamp(0).prod(2)

    # IoU = inter / (area1 + area2 - inter)
    return inter / ((a2 - a1).prod(2) + (b2 - b1).prod(2) - inter + eps)

def compute_ap(recall, precision):
    """
    Compute the average precision (AP) given the recall and precision curves.

    Arguments:
        recall (list): The recall curve.
        precision (list): The precision curve.

    Returns:
        (float): Average precision.
        (np.ndarray): Precision envelope curve.
        (np.ndarray): Modified recall curve with sentinel values added at the beginning and end.
    """

    # Append sentinel values to beginning and end
    mrec = np.concatenate(([0.0], recall, [1.0]))
    mpre = np.concatenate(([1.0], precision, [0.0]))

    # Compute the precision envelope
    mpre = np.flip(np.maximum.accumulate(np.flip(mpre)))

    # Integrate area under curve
    method = 'interp'  # methods: 'continuous', 'interp'
    if method == 'interp':
        x = np.linspace(0, 1, 101)  # 101-point interp (COCO)
        ap = np.trapz(np.interp(x, mrec, mpre), x)  # integrate
    else:  # 'continuous'
        i = np.where(mrec[1:] != mrec[:-1])[0]  # points where x-axis (recall) changes
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])  # area under curve

    return ap, mpre, mrec

def smooth(y, f=0.05):
    """Box filter of fraction f."""
    nf = round(len(y) * f * 2) // 2 + 1  # number of filter elements (must be odd)
    p = np.ones(nf // 2)  # ones padding
    yp = np.concatenate((p * y[0], y, p * y[-1]), 0)  # y padded
    return np.convolve(yp, np.ones(nf) / nf, mode='valid')  # y-smoothed

def plot_pr_curve(px, py, ap, save_dir=Path('pr_curve.png'), names=()):
    """Plots a precision-recall curve."""
    fig, ax = plt.subplots(1, 1, figsize=(9, 6), tight_layout=True)
    py = np.stack(py, axis=1)

    if 0 < len(names) < 21:  # display per-class legend if < 21 classes
        for i, y in enumerate(py.T):
            ax.plot(px, y, linewidth=1, label=f'{names[i]} {ap[i, 0]:.3f}')  # plot(recall, precision)
    else:
        ax.plot(px, py, linewidth=1, color='grey')  # plot(recall, precision)

    ax.plot(px, py.mean(1), linewidth=3, color='blue', label='all classes %.3f mAP@0.5' % ap[:, 0].mean())
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    ax.set_title('Precision-Recall Curve')
    fig.savefig(save_dir, dpi=250)
    plt.close(fig)

def plot_mc_curve(px, py, save_dir=Path('mc_curve.png'), names=(), xlabel='Confidence', ylabel='Metric'):
    """Plots a metric-confidence curve."""
    fig, ax = plt.subplots(1, 1, figsize=(9, 6), tight_layout=True)

    if 0 < len(names) < 21:  # display per-class legend if < 21 classes
        for i, y in enumerate(py):
            ax.plot(px, y, linewidth=1, label=f'{names[i]}')  # plot(confidence, metric)
    else:
        ax.plot(px, py.T, linewidth=1, color='grey')  # plot(confidence, metric)

    y = smooth(py.mean(0), 0.05)
    ax.plot(px, y, linewidth=3, color='blue', label=f'all classes {y.max():.2f} at {px[y.argmax()]:.3f}')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    ax.set_title(f'{ylabel}-Confidence Curve')
    fig.savefig(save_dir, dpi=250)
    plt.close(fig)

def ap_per_class(tp, conf, pred_cls, target_cls, plot=False, save_dir=Path(), names=(), eps=1e-16, prefix=''):
    """
    Computes the average precision per class for object detection evaluation.

    Args:
        tp (np.ndarray): Binary array indicating whether the detection is correct (True) or not (False).
        conf (np.ndarray): Array of confidence scores of the detections.
        pred_cls (np.ndarray): Array of predicted classes of the detections.
        target_cls (np.ndarray): Array of true classes of the detections.
        plot (bool, optional): Whether to plot PR curves or not. Defaults to False.
        save_dir (Path, optional): Directory to save the PR curves. Defaults to an empty path.
        names (tuple, optional): Tuple of class names to plot PR curves. Defaults to an empty tuple.
        eps (float, optional): A small value to avoid division by zero. Defaults to 1e-16.
        prefix (str, optional): A prefix string for saving the plot files. Defaults to an empty string.

    Returns:
        (tuple): A tuple of six arrays and one array of unique classes, where:
            tp (np.ndarray): True positive counts for each class.
            fp (np.ndarray): False positive counts for each class.
            p (np.ndarray): Precision values at each confidence threshold.
            r (np.ndarray): Recall values at each confidence threshold.
            f1 (np.ndarray): F1-score values at each confidence threshold.
            ap (np.ndarray): Average precision for each class at different IoU thresholds.
            unique_classes (np.ndarray): An array of unique classes that have data.

    """

    # Sort by objectness
    i = np.argsort(-conf)
    tp, conf, pred_cls = tp[i], conf[i], pred_cls[i]

    # Find unique classes
    unique_classes, nt = np.unique(target_cls, return_counts=True)
    nc = unique_classes.shape[0]  # number of classes, number of detections

    # Create Precision-Recall curve and compute AP for each class
    px, py = np.linspace(0, 1, 1000), []  # for plotting
    ap, p, r = np.zeros((nc, tp.shape[1])), np.zeros((nc, 1000)), np.zeros((nc, 1000))
    for ci, c in enumerate(unique_classes):
        i = pred_cls == c
        n_l = nt[ci]  # number of labels
        n_p = i.sum()  # number of predictions
        if n_p == 0 or n_l == 0:
            continue

        # Accumulate FPs and TPs
        fpc = (1 - tp[i]).cumsum(0)
        tpc = tp[i].cumsum(0)

        # Recall
        recall = tpc / (n_l + eps)  # recall curve
        r[ci] = np.interp(-px, -conf[i], recall[:, 0], left=0)  # negative x, xp because xp decreases

        # Precision
        precision = tpc / (tpc + fpc)  # precision curve
        p[ci] = np.interp(-px, -conf[i], precision[:, 0], left=1)  # p at pr_score

        # AP from recall-precision curve
        for j in range(tp.shape[1]):
            ap[ci, j], mpre, mrec = compute_ap(recall[:, j], precision[:, j])
            if plot and j == 0:
                py.append(np.interp(px, mrec, mpre))  # precision at mAP@0.5

    # Compute F1 (harmonic mean of precision and recall)
    f1 = 2 * p * r / (p + r + eps)
    names = [v for k, v in names.items() if k in unique_classes]  # list: only classes that have data
    names = dict(enumerate(names))  # to dict
    if plot:
        plot_pr_curve(px, py, ap, save_dir / f'{prefix}PR_curve.png', names)
        plot_mc_curve(px, f1, save_dir / f'{prefix}F1_curve.png', names, ylabel='F1')
        plot_mc_curve(px, p, save_dir / f'{prefix}P_curve.png', names, ylabel='Precision')
        plot_mc_curve(px, r, save_dir / f'{prefix}R_curve.png', names, ylabel='Recall')

    i = smooth(f1.mean(0), 0.1).argmax()  # max F1 index
    p, r, f1 = p[:, i], r[:, i], f1[:, i]
    tp = (r * nt).round()  # true positives
    fp = (tp / (p + eps) - tp).round()  # false positives
    return tp, fp, p, r, f1, ap, unique_classes.astype(int)

class FigureEvaluator:
    def __init__(self, categories_dict, save_dir=Path('./plots'), plot=False):
        self.iouv = torch.linspace(0.5, 0.95, 10)  # iou vector for mAP@0.5:0.95
        self.niou = self.iouv.numel()
        self.iou_clef = 0.66
        self.iouv = torch.cat((self.iouv, torch.Tensor([self.iou_clef])))   # add 0.66
        self.correct_clef = 0
        self.all_clef = 0

        self.names = categories_dict
        self.nc = len(categories_dict)
        self.stats = []

        self.p = []  # (nc, )
        self.r = []  # (nc, )
        self.f1 = []  # (nc, )
        self.all_ap = []  # (nc, 10)
        self.ap_class_index = []  # (nc, )

        self.save_dir = save_dir
        self.plot = plot
        if self.plot:
            self.save_dir.mkdir(parents=True, exist_ok=True)
        self.nc = len(categories_dict)
        self.matrix = np.zeros((self.nc + 1, self.nc + 1))
        self.iou_thres = 0.5
        self.conf = 0.3




    @property
    def mp(self):
        """
        Returns the Mean Precision of all classes.

        Returns:
            (float): The mean precision of all classes.
        """
        return self.p.mean() if len(self.p) else 0.0

    @property
    def mf1(self):
        """
        Returns the Mean f1 of all classes.

        Returns:
            (float): The mean precision of all classes.
        """
        return self.f1.mean() if len(self.f1) else 0.0

    @property
    def mr(self):
        """
        Returns the Mean Recall of all classes.

        Returns:
            (float): The mean recall of all classes.
        """
        return self.r.mean() if len(self.r) else 0.0

    @property
    def map50(self):
        """
        Returns the mean Average Precision (mAP) at an IoU threshold of 0.5.

        Returns:
            (float): The mAP50 at an IoU threshold of 0.5.
        """
        return self.all_ap[:, 0].mean() if len(self.all_ap) else 0.0

    @property
    def map66(self):
        """
        Returns the clef iou 0.66

        Returns:
            (float): The mAP50 at an IoU threshold of 0.5.
        """
        if self.all_clef == 0:
            return 0.0
        else:
            return self.correct_clef/self.all_clef

    @property
    def map(self):
        """
        Returns the mean Average Precision (mAP) over IoU thresholds of 0.5 - 0.95 in steps of 0.05.

        Returns:
            (float): The mAP over IoU thresholds of 0.5 - 0.95 in steps of 0.05.
        """
        return self.all_ap.mean() if len(self.all_ap) else 0.0

    def get_correct(self, detections, labels, gt_texts, pred_texts):
        """
        Return correct prediction matrix
        Arguments:
            detections (array[N, 6]), x1, y1, x2, y2, class, conf
            labels (array[M, 5]),  x1, y1, x2, y2, class
        Returns:
            correct (array[N, 10]), for 10 IoU levels
        """
        iou = box_iou(labels[:, :-1], detections[:, :4])
        correct = np.zeros((detections.shape[0], self.iouv.shape[0])).astype(bool)
        correct_class = labels[:, 4:5] == detections[:, 4]
        for i in range(len(self.iouv)):
            x = torch.where((iou >= self.iouv[i]) & correct_class)  # IoU > threshold and classes match
            if x[0].shape[0]:
                matches = torch.cat((torch.stack(x, 1), iou[x[0], x[1]][:, None]), 1).numpy()  # [label, detect, iou]
                if x[0].shape[0] > 1:
                    matches = matches[matches[:, 2].argsort()[::-1]]  # sort by IoU
                    matches = matches[np.unique(matches[:, 1], return_index=True)[1]]  # unique detections
                    # matches = matches[matches[:, 2].argsort()[::-1]]
                    matches = matches[np.unique(matches[:, 0], return_index=True)[1]]  # unique labels
                    # clac ocr accuracy
                correct[matches[:, 1].astype(int), i] = True
        correct = torch.tensor(correct, dtype=torch.bool)
        self.all_clef = self.all_clef + max(detections.shape[0], labels.shape[0])
        self.correct_clef = self.correct_clef + correct[:, self.niou].sum().numpy().item()
        correct = correct[:, :self.niou]
        return correct

    def get_confusion_matrix(self, detections, labels):

        """
        Update confusion matrix for object detection task.

        Args:
            detections (Array[N, 6]): Detected bounding boxes and their associated information.
                                      Each row should contain (x1, y1, x2, y2, conf, class).  x1, y1, x2, y2, class, conf
            labels (Array[M, 5]): Ground truth bounding boxes and their associated class labels.
                                  Each row should contain (class, x1, y1, x2, y2). x1, y1, x2, y2, class
        """
        if detections is None:
            gt_classes = labels.int()
            for gc in gt_classes:
                self.matrix[self.nc, gc] += 1  # background FN
            return

        detections = detections[detections[:, 5] > self.conf]
        gt_classes = labels[:, 4].int()
        detection_classes = detections[:, 4].int()
        iou = box_iou(labels[:, :-1], detections[:, :4])

        x = torch.where(iou > self.iou_thres)
        if x[0].shape[0]:
            matches = torch.cat((torch.stack(x, 1), iou[x[0], x[1]][:, None]), 1).cpu().numpy()
            if x[0].shape[0] > 1:
                matches = matches[matches[:, 2].argsort()[::-1]]
                matches = matches[np.unique(matches[:, 1], return_index=True)[1]]
                matches = matches[matches[:, 2].argsort()[::-1]]
                matches = matches[np.unique(matches[:, 0], return_index=True)[1]]
        else:
            matches = np.zeros((0, 3))

        n = matches.shape[0] > 0
        m0, m1, _ = matches.transpose().astype(int)
        for i, gc in enumerate(gt_classes):
            j = m0 == i
            if n and sum(j) == 1:
                self.matrix[detection_classes[m1[j]], gc] += 1  # correct
            else:
                self.matrix[self.nc, gc] += 1  # true background

        if n:
            for i, dc in enumerate(detection_classes):
                if not any(m1 == i):
                    self.matrix[dc, self.nc] += 1  # predicted background

    def confusion_matrix_plot(self, save_dir='.', names=(), normalize=False):
        """
                Plot the confusion matrix using seaborn and save it to a file.

                Args:
                    normalize (bool): Whether to normalize the confusion matrix.
                    save_dir (str): Directory where the plot will be saved.
                    names (tuple): Names of classes, used as labels on the plot.
                """
        array = self.matrix / ((self.matrix.sum(0).reshape(1, -1) + 1E-9) if normalize else 1)  # normalize columns
        array[array < 0.005] = np.nan  # don't annotate (would appear as 0.00)

        fig, ax = plt.subplots(1, 1, figsize=(12, 9), tight_layout=True)
        nc, nn = self.nc, len(names)  # number of classes, names
        sn.set(font_scale=2.0 if nc < 50 else 0.8)  # for label size
        labels = (0 < nn < 99) and (nn == nc)  # apply names to ticklabels
        ticklabels = (list(names) + ['Background']) if labels else 'auto'
        sn.heatmap(array,
                   ax=ax,
                   annot=nc < 30,
                   annot_kws={
                       'size': 15},
                   cmap='Blues',
                   fmt='.2f' if normalize else '.0f',
                   square=True,
                   vmin=0.0,
                   xticklabels=ticklabels,
                   yticklabels=ticklabels).set_facecolor((1, 1, 1))
        title = 'Confusion Matrix' + ' Normalized' * normalize
        ax.set_xlabel('Ground Truth')
        ax.set_ylabel('Predicted')
        ax.set_title(title)
        fig.savefig(Path(save_dir) / f'{title.lower().replace(" ", "_")}.png', dpi=300)
        plt.close(fig)



    def calc_metrics(self):
        stats = [torch.cat(x, 0).cpu().numpy() for x in zip(*self.stats)]  # to numpy
        if len(stats) and stats[0].any():
            tp, conf, pred_cls, target_cls = stats
            results = ap_per_class(tp, conf, pred_cls, target_cls, plot=self.plot, save_dir=self.save_dir,
                                   names=self.names)[2:]
            self.p, self.r, self.f1, self.all_ap, self.ap_class_index = results
        self.plot_results()
        return [self.mp, self.mr, self.mf1,  self.map66, self.map50, self.map]

    def plot_results(self):
        if self.plot:
            for normalize in True, False:
                self.confusion_matrix_plot(save_dir=self.save_dir, names=self.names.values(), normalize=normalize)

    def update_stats(self, gt_labels, pred_labels):
        detections = torch.Tensor(pred_labels)
        labels = torch.Tensor(gt_labels)

        nl, npr = labels.shape[0], detections.shape[0]  # number of labels, predictions
        if nl:
            cls = labels[:, 4]
        else:
            cls = torch.Tensor()
        correct_bboxes = torch.zeros(npr, self.niou, dtype=torch.bool)  # init
        if npr == 0:
            if nl:
                self.stats.append((correct_bboxes, *torch.zeros((2, 0)), cls))
                if self.plot:
                    self.get_confusion_matrix(detections=None, labels=cls)
            return
        if nl:
            correct_bboxes = self.get_correct(detections, labels, None, None)
            if self.plot:
                self.get_confusion_matrix(detections=detections, labels=labels)
        pcls = detections[:, 4]
        conf = detections[:, 5]
        self.stats.append((correct_bboxes, conf, pcls, cls))

class LabelEvaluater(FigureEvaluator):
    def __init__(self, categories_dict, save_dir=None, plot=False):
        super().__init__(categories_dict, save_dir, plot)
        self.iouv = torch.linspace(0.5, 0.95, 10)  # iou vector for mAP@0.5:0.95

    def get_correct(self, detections, labels, gt_texts, pred_texts):
        iou = box_iou(labels[:, :-1], detections[:, :4])
        correct = np.zeros((detections.shape[0], self.iouv.shape[0])).astype(bool)
        correct_class = torch.zeros((labels.shape[0], detections.shape[0]), dtype=torch.bool)
        for i, gt_text in enumerate(gt_texts):
            for j, pred_text in enumerate(pred_texts):
                if str(gt_text).lower == str(pred_text).lower and labels[i, 4] == detections[j, 4]:
                    correct_class[i, j] = True
        for i in range(len(self.iouv)):
            x = torch.where((iou >= self.iouv[i]) & correct_class)  # IoU > threshold and classes match
            if x[0].shape[0]:
                matches = torch.cat((torch.stack(x, 1), iou[x[0], x[1]][:, None]), 1).numpy()  # [label, detect, iou]
                if x[0].shape[0] > 1:
                    matches = matches[matches[:, 2].argsort()[::-1]]  # sort by IoU
                    matches = matches[np.unique(matches[:, 1], return_index=True)[1]]  # unique detections
                    # matches = matches[matches[:, 2].argsort()[::-1]]
                    matches = matches[np.unique(matches[:, 0], return_index=True)[1]]  # unique labels
                    # clac ocr accuracy
                correct[matches[:, 1].astype(int), i] = True
        return torch.tensor(correct, dtype=torch.bool)

    def update_stats(self, gt_labels, pred_labels):
        nl, npr = len(gt_labels), len(pred_labels)  # number of labels, detections
        correct_ocrs = torch.zeros(npr, self.niou, dtype=torch.bool)  # init
        if nl:
            labels = np.array(gt_labels)[:, :5].astype(np.float64)  # x1, y1, x2, y2, cls
            cls = torch.from_numpy(labels[:, 4])  # cls
            gt_texts = np.array(gt_labels)[:, 5]  # text
            labels = torch.from_numpy(labels)
            if npr == 0:
                self.stats.append((correct_ocrs, *torch.zeros((2, 0)), cls))
            else:
                detections = np.array(pred_labels)[:, :6].astype(np.float64)  # x1, y1, x2, y2, cls, score
                pcls = torch.from_numpy(detections[:, 4])  # pred cls
                conf = torch.from_numpy(detections[:, 5])  # score
                pred_texts = np.array(pred_labels)[:, 6]  # text
                detections = torch.from_numpy(detections)
                correct_ocrs = self.get_correct(detections, labels, gt_texts, pred_texts)
                self.stats.append((correct_ocrs, conf, pcls, cls))  # (correct, conf, pcls, tcls)
        else:
            if npr:
                detections = np.array(pred_labels)[:, :6].astype(np.float64)  # x1, y1, x2, y2, cls, score
                pcls = torch.from_numpy(detections[:, 4])  # pred cls
                conf = torch.from_numpy(detections[:, 5])  # score
                self.stats.append((correct_ocrs, conf, pcls, torch.Tensor()))  # (correct, conf, pcls, tcls)
def val_dataset():
    predict_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\yolo_formal\eval\yolov8_crnn_predict"
    gt_dir = r"D:\3_Research\1_Project\1_Python\web_develop\backend\apiproject\media\formal\jsons"
    categories_dict = {0: "figures", 1: "figure_nos"}
    texts_dict = {1: "figure_nos"}
    figure_evaluator = FigureEvaluator(categories_dict, plot=True)
    label_evaluator = LabelEvaluater(texts_dict)
    for lbl_name in tqdm(os.listdir(predict_dir)):
        gt_path = os.path.join(gt_dir, lbl_name)
        prdict_path = os.path.join(predict_dir, lbl_name)
        with open(gt_path, 'r') as f:
            gt_json = json.load(f)
        with open(prdict_path, 'r') as f:
            predict_json = json.load(f)
        gt_labels = []
        pred_labels = []
        gt_ocrs = []
        pred_ocrs = []
        h, w = int(gt_json["height"]), int(gt_json["width"])
        for cls in categories_dict.keys():
            for obj in gt_json[categories_dict[cls]]:
                x1 = min(obj["points"][0][0], obj["points"][1][0])
                x2 = max(obj["points"][0][0], obj["points"][1][0])
                y1 = min(obj["points"][0][1], obj["points"][1][1])
                y2 = max(obj["points"][0][1], obj["points"][1][1])
                x1 = max(0, x1)
                x2 = min(w, x2)
                y1 = max(0, y1)
                y2 = min(h, y2)
                if cls in texts_dict.keys():
                    gt_ocrs.append([x1, y1, x2, y2, cls, obj["text"]])
                gt_labels.append([x1, y1, x2, y2, cls])
            for obj in predict_json[categories_dict[cls]]:
                x1 = min(obj["points"][0][0], obj["points"][1][0])
                x2 = max(obj["points"][0][0], obj["points"][1][0])
                y1 = min(obj["points"][0][1], obj["points"][1][1])
                y2 = max(obj["points"][0][1], obj["points"][1][1])
                x1 = max(0, x1)
                x2 = min(w, x2)
                y1 = max(0, y1)
                y2 = min(h, y2)
                score = obj["score"]
                if cls in texts_dict.keys():
                    pred_ocrs.append([x1, y1, x2, y2, cls, score, obj["text"], obj["text_score"]])
                pred_labels.append([x1, y1, x2, y2, cls, score])
        figure_evaluator.update_stats(gt_labels, pred_labels)
        label_evaluator.update_stats(gt_ocrs, pred_ocrs)
    figure_metrics = figure_evaluator.calc_metrics()
    label_metrics = label_evaluator.calc_metrics()
    print("[mp, mr, mf1,  map66, map50, map]")
    print(figure_metrics)
    print(label_metrics)



def val_yolo_ocr():
    model_path = r"D:\3_Research\1_Project\1_Python\yolo_v8_v2\ultralytics\yolo_ocr\clefmed\yolov8l\weights\best.pt"
    data = "compound-figures.yaml"
    model = YOLO(model_path, task="detect")
    metrics = model.val(data=data)
    print(metrics)






if __name__ == '__main__':
    val_dataset()
    #  val_yolo_ocr()


