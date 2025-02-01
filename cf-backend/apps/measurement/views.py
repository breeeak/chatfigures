import random
import string

from django.core.files.base import ContentFile
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from apps.fadmin.models import SaveFile
from apps.fadmin.serializers import SaveFileCreateUpdateSerializer
from apps.fadmin.utils.response_util import SuccessResponse, ErrorResponse
from apps.fadmin.utils.json_util import NumpyJsonEncoder
import os
from apiproject.settings import INFERENCE_TYPE, SAM
from django.conf import settings
import json
from PIL import Image
from pathlib import Path
from apps.fadmin.utils.zip_util import zip_dir
import base64
import jwt
import time

import cv2
import numpy as np


if INFERENCE_TYPE == "onnx":
    from apps.figures.recognizers.onnx_inference import backend_recognize
elif INFERENCE_TYPE == "mmlab":
    from apps.figures.recognizers.mm_inference import backend_recognize
elif INFERENCE_TYPE =="yolo_each":
    from apps.figures.recognizers.yolo_each_inference import backend_recognize_bar
elif INFERENCE_TYPE == "yolo_ocr":
    from apps.figures.recognizers.inference import backend_recognize_bar
if SAM:
    from apiproject.settings import SAM_PREDICTOR
else:
    SAM_PREDICTOR = None

@api_view(['POST'])
def detect_scale_bars(request):
    cf_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    cf_token_encoded = jwt.encode({"cf_token": cf_token}, settings.SECRET_KEY, algorithm="HS256")
    if request.META.get("HTTP_AUTHORIZATION", None):
        cf_token_encoded = request.META.get("HTTP_AUTHORIZATION")
        if cf_token_encoded.startswith("Bearer "):
            cf_token_encoded = cf_token_encoded.split(" ")[1]
            cf_token_decoded = jwt.decode(cf_token_encoded, settings.SECRET_KEY, algorithms=["HS256"])
            if cf_token_decoded.get("cf_token", None):
                cf_token = cf_token_decoded["cf_token"]


    file = request.FILES.get("image")
    if request.user.is_authenticated:
        source = "user"
    else:
        source = "guest"
    file_data = {
        "file": file,
        "name": file.name,
        "size": file.size,
        "type": file.content_type,
        "source": source,
        "address": "local",
        "session_token": cf_token,
    }
    file_serializer = SaveFileCreateUpdateSerializer(data=file_data)
    if file_serializer.is_valid():
        file_instance = file_serializer.create(file_serializer.validated_data)
        file_path = file_instance.file.path
        # 识别
        result = backend_recognize_bar(file_path)
        result["id"] = file_instance.id
        # 使用 SaveFileCreateUpdateSerializer 保存json
        #  file_ext
        file_ext = file_path.split(".")[-1]
        json_path = file_path.replace(file_ext, "json")
        json_name = os.path.basename(json_path)
        js = json.dumps(result, cls=NumpyJsonEncoder)
        json_content = ContentFile(js.encode('utf-8'), name=json_name)
            # 保存到数据库
        json_file_data = {
            "file": json_content,
            "name": json_name,
            "size": json_content.size,
            "type": "application/json",
            "source": source,
            "address": "local",
            "session_token": cf_token,
        }
        json_file_serializer = SaveFileCreateUpdateSerializer(data=json_file_data)
        if json_file_serializer.is_valid():
            json_instance = json_file_serializer.create(json_file_serializer.validated_data)
            return SuccessResponse({"id": json_instance.id, "token": cf_token_encoded})
    else:
        return ErrorResponse(file_serializer.errors)


@api_view(['GET'])
def get_results(request):
    # 判断是否有这个session的权限
    cf_token = None
    if request.META.get("HTTP_AUTHORIZATION", None):
        cf_token_encoded = request.META.get("HTTP_AUTHORIZATION")
        if cf_token_encoded.startswith("Bearer "):
            cf_token_encoded = cf_token_encoded.split(" ")[1]
            cf_token_decoded = jwt.decode(cf_token_encoded, settings.SECRET_KEY, algorithms=["HS256"])
            if cf_token_decoded.get("cf_token", None):
                cf_token = cf_token_decoded["cf_token"]
        else:
            return ErrorResponse("No permission!")
    else:
        return ErrorResponse("No permission!")

    result_id = request.query_params.get("resultId")
    result_file = get_object_or_404(SaveFile, id=result_id)     # 找不到会报404
    # 判断是否有这个session的权限
    if result_file.session_token is None or cf_token is None or result_file.session_token != cf_token:
        return ErrorResponse("No permission!")
    with result_file.file.open() as f:
        results = json.load(f)
    domain_url = request.build_absolute_uri('/')[:-1].strip("/")  # 得到Django的运行的域名端口
    # results["name"] = os.path.join("media", "images", "tests",results["name"])
    results["name"] = os.path.join(domain_url, "media", result_file.source, results["name"])
    # test no bars or no labels
    # results["labels"] = []
    # results["bars"] = []
    # results["ppi"] = 0
    return SuccessResponse(results)

@api_view(['GET'])
def initMeasureImage(request):

    if SAM_PREDICTOR is None:
        return ErrorResponse("SAM_PREDICTOR is None")
    result_id = request.query_params.get("resultId")
    result_file = get_object_or_404(SaveFile, id=result_id)  # 找不到会报404
    json_path = result_file.file.path
    with open(json_path, "r") as f:
        results = json.load(f)
    img_id = results["id"]
    img_file = get_object_or_404(SaveFile, id=img_id)  # 找不到会报404
    img_path = img_file.file.path
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    SAM_PREDICTOR.set_image(img)    # TODO 不同用户是否会冲突

    return SuccessResponse("initMeasureImagesuccess")


@api_view(['POST'])
def measureAnythingPoint(request):
    if SAM_PREDICTOR is None:
        return ErrorResponse("SAM_PREDICTOR is None")
    point = request.data.get("points")[0]
    input_point = np.array([
        [point["x"], point["y"]]
    ])
    input_label = np.array([1])
    masks, scores, logits = SAM_PREDICTOR.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    if len(masks) == 0:
        return SuccessResponse("No mask!")
    max_score_index = np.argmax(scores)
    max_mask = masks[max_score_index]
    max_score = scores[max_score_index]
    # 转为polygon
    max_mask = max_mask.astype(np.uint8)
    max_mask_poly = cv2.threshold(max_mask, 0.5, 255, cv2.THRESH_BINARY)[1]
    contours, hierarchy = cv2.findContours(max_mask_poly, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    poly_gon = contours[0].reshape(-1, 2).tolist()
    return SuccessResponse({"mask": poly_gon, "score": max_score.tolist()})




@api_view(['POST'])
def interactive_measurement_upload(request):
    cf_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    cf_token_encoded = jwt.encode({"cf_token": cf_token}, settings.SECRET_KEY, algorithm="HS256")
    if request.META.get("HTTP_AUTHORIZATION", None):
        cf_token_encoded = request.META.get("HTTP_AUTHORIZATION")
        if cf_token_encoded.startswith("Bearer "):
            cf_token_encoded = cf_token_encoded.split(" ")[1]
            cf_token_decoded = jwt.decode(cf_token_encoded, settings.SECRET_KEY, algorithms=["HS256"])
            if cf_token_decoded.get("cf_token", None):
                cf_token = cf_token_decoded["cf_token"]

    if request.user.is_authenticated:
        source = "user"
    else:
        source = "guest"
    image_data = request.data['base64data']
    image_name = request.data['filename']
    img_format, imgstr = image_data.split(';base64,')
    ext = img_format.split('/')[-1]
    if image_name is None:
        image_name = "unnamed." + ext
    image_content = ContentFile(base64.b64decode(imgstr), name=image_name)
    # 保存到数据库
    image_file_data = {
        "file": image_content,
        "name": image_name,
        "size": image_content.size,
        "type": img_format,
        "source": source,
        "address": "local",
        "session_token": cf_token,
    }
    image_file_serializer = SaveFileCreateUpdateSerializer(data=image_file_data)
    if image_file_serializer.is_valid():
        image_instance = image_file_serializer.create(image_file_serializer.validated_data)
        file_path = image_instance.file.path
        # 识别
        result = backend_recognize_bar(file_path)
        result["id"] = image_instance.id
        # 使用 SaveFileCreateUpdateSerializer 保存json

        #  file_ext
        file_ext = file_path.split(".")[-1]
        json_path = file_path.replace(file_ext, "json")
        json_name = os.path.basename(json_path)
        js = json.dumps(result, cls=NumpyJsonEncoder)
        json_content = ContentFile(js.encode('utf-8'), name=json_name)
        # 保存到数据库
        json_file_data = {
            "file": json_content,
            "name": json_name,
            "size": json_content.size,
            "type": "application/json",
            "source": source,
            "address": "local",
            "session_token": cf_token,
        }
        json_file_serializer = SaveFileCreateUpdateSerializer(data=json_file_data)
        if json_file_serializer.is_valid():
            json_instance = json_file_serializer.create(json_file_serializer.validated_data)
            domain_url = request.build_absolute_uri('/')[:-1].strip("/")  # 得到Django的运行的域名端口
            result["name"] = os.path.join(domain_url, "media", json_instance.source, result["name"])
            redirect_url = "measurement-results/" + str(json_instance.id)
            return SuccessResponse({"taskId": json_instance.id, "jsonDict": result, "redirectUrl": redirect_url,"token": cf_token_encoded})
    return ErrorResponse("error")
