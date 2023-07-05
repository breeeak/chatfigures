# Ultralytics YOLO 🚀, AGPL-3.0 license

import torch

from ultralytics.yolo.v8.detect.predict import DetectionPredictor
from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.utils import DEFAULT_CFG, ROOT, ops


class OcrPredictor(DetectionPredictor):

    def __init__(self, cfg=DEFAULT_CFG, overrides=None, _callbacks=None):
        super().__init__(cfg, overrides, _callbacks)
        self.args.task = 'ocr'
        self.label_converter = ops.LabelTexts(alphabet=self.args.alphabet, ignore_case=self.args.ignore_case,max_length=self.args.seq_length)

    def postprocess(self, preds, img, orig_imgs):
        """Postprocesses predictions and returns a list of Results objects."""

        all_classes = list(self.model.model.names.keys())
        text_classes = self.args.ocr_classes
        other_classes = [c for c in all_classes if c not in text_classes]
        preds_nms = ops.non_max_suppression(preds[0],
                                            self.args.conf,
                                            self.args.iou,
                                            agnostic=self.args.agnostic_nms,
                                            max_det=self.args.max_det,
                                            classes=other_classes,
                                            is_soft_nms=True)      # 只对非ocr类进行nms
        pred_transcripts = preds[2]
        if len(pred_transcripts) == 3:
            pred_ocrs, pred_lens, text_boxes = pred_transcripts
        else:
            pred_ocrs, pred_lens, text_boxes = [], [], []
        results = []
        for i, pred in enumerate(preds_nms):
            path = self.batch[0]
            img_path = path[i] if isinstance(path, list) else path
            orig_img = orig_imgs[i] if isinstance(orig_imgs, list) else orig_imgs
            if not isinstance(orig_imgs, torch.Tensor):
                pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape)
                if len(text_boxes) > 0:
                    text_boxes[i][:, :4] = ops.scale_boxes(img.shape[2:], text_boxes[i][:, :4], orig_img.shape)

            ocr_strs = []
            for j in range(len(pred)):      # 非ocr 全部预测为空
                ocr_strs.append("")
            if len(pred_ocrs) > 0 and len(pred_ocrs) == len(preds_nms):
                for j in range(len(pred_ocrs[i])):
                    ocr_str = self.label_converter.greedy_decode(pred_ocrs[i][j].softmax(1).cpu().numpy(), pred_lens[i][j].cpu().numpy())       # 解码算法更新beam search？
                    ocr_strs.append(ocr_str)
            if len(text_boxes) > 0:
                pred = torch.cat((pred, text_boxes[i]), 0)
            results.append(Results(orig_img=orig_img, path=img_path, names=self.model.names, boxes=pred, ocrs=ocr_strs))
        return results


def predict(cfg=DEFAULT_CFG, use_python=False):
    """Runs YOLO model inference on input image(s)."""
    model = cfg.model or 'yolov8n.pt'
    source = cfg.source if cfg.source is not None else ROOT / 'assets' if (ROOT / 'assets').exists() \
        else 'https://ultralytics.com/images/bus.jpg'

    args = dict(model=model, source=source)
    if use_python:
        from ultralytics import YOLO
        YOLO(model)(**args)
    else:
        predictor = OcrPredictor(overrides=args)
        predictor.predict_cli()


if __name__ == '__main__':
    predict()
