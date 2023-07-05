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
from apiproject.settings import INFERENCE_TYPE
from django.conf import settings
import json
from PIL import Image
from pathlib import Path
from apps.fadmin.utils.zip_util import zip_dir
import base64
import jwt

if INFERENCE_TYPE == "onnx":
    from apps.figures.recognizers.onnx_inference import backend_recognize
elif INFERENCE_TYPE == "mmlab":
    from apps.figures.recognizers.mm_inference import backend_recognize
elif INFERENCE_TYPE =="yolo_each":
    from apps.figures.recognizers.yolo_each_inference import backend_recognize
elif INFERENCE_TYPE == "yolo_ocr":
    from apps.figures.recognizers.inference import backend_recognize

@api_view(['POST'])
def getNewLabel(request):
    # data_name = "tests"
    data_name = "stage1"
    # data_name = "generated"
    # data_name = "clefmed/test"
    # data_name = "clefmed/train"

    label_dir = os.path.join(settings.MEDIA_ROOT, data_name, "data_pred_labels_yolov8_4class2")
    # label_dir = os.path.join(settings.MEDIA_ROOT, data_name, "jsons")
    # img_dir = os.path.join(settings.MEDIA_ROOT, data_name, "figures")
    img_dir = os.path.join(settings.MEDIA_ROOT, data_name, "coco/test")

    # 保存当前的结果       不用保存当前， “next”保存并跳到下一个，“last” 上一个，“current" 切换到这一个
    if request.data["save"]:  # 以下是修改了结果后的保存
        # name 修改
        file_all_name = request.data["results"]["name"]
        file_name = str(file_all_name).split("\\")[-1]
        request.data["results"]["name"] = file_name
        # label的text unit的修改
        for label in request.data["results"]["labels"]:
            if label["text"] is not None and len(label["text"].split(" ")) == 2:
                label["number"] = label["text"].split(" ")[0]
                label["unit"] = label["text"].split(" ")[1]

        label_save_name = ".".join(file_name.split(".")[:-1]) + ".json"
        label_save_path = os.path.join(label_dir, label_save_name)
        js = json.dumps(request.data["results"], indent=2)
        with open(label_save_path, "w", encoding="utf-8") as f:
            f.write(js)

    # 跳转到上一个或下一个
    index = 0
    all_imgs = os.listdir(img_dir)
    if request.data["index"] is not None:  # 如果有穿过来第几个了，就继续
        index = int(request.data["index"])
    if request.data["type"] == "next":
        if (index + 1) < len(all_imgs):
            index = index + 1
        else:
            index = 0
    if request.data["type"] == "last":
        if (index - 1) < 0:
            index = len(all_imgs) - 1
        else:
            index = index - 1
    # if request.data["type"] == "current":
    #         index = index
    img_name = all_imgs[index]
    label_name = ".".join(img_name.split(".")[:-1]) + ".json"
    img_path = os.path.join(img_dir, img_name)
    label_path = os.path.join(label_dir, label_name)
    blank_label_path = os.path.join(settings.MEDIA_ROOT, "blank.json")
    if os.path.exists(label_path):
        with open(label_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    else:
        with open(blank_label_path, "r", encoding="utf-8") as f:
            results = json.load(f)
        img = Image.open(img_path)
        results["width"] = img.width
        results["height"] = img.height
    domain_url = request.build_absolute_uri('/')[:-1].strip("/")  # 得到Django的运行的域名端口
    # results["name"] = os.path.join("media", "images", "tests",results["name"])
    results["name"] = os.path.join(domain_url, "media", data_name, "figures", img_name)
    request.data["index"] = index
    request.data["results"] = results
    return SuccessResponse(request.data)


@api_view(['POST'])
def getLabelList(request):
    # data_name = "tests"
    data_name = "stage1"
    # data_name = "generated"
    # data_name = "clefmed/test"
    # data_name = "clefmed/train"

    label_dir = os.path.join(settings.MEDIA_ROOT, data_name, "data_pred_labels_yolov8_4class2")
    # label_dir = os.path.join(settings.MEDIA_ROOT, data_name, "jsons")
    # img_dir = os.path.join(settings.MEDIA_ROOT, data_name, "figures")
    img_dir = os.path.join(settings.MEDIA_ROOT, data_name, "coco/test")

    index = 0
    page_size = 10
    all_imgs = os.listdir(img_dir)
    if request.data["index"] is not None:  # 如果有穿过来第几个了，就继续
        index = int(request.data["index"])
        if index >= len(all_imgs):
            return ErrorResponse("index out of range")
    # 取索引前后10个
    start_index = index - page_size//2
    end_index = index + page_size//2
    image_list = []
    if start_index < 0:
        start_index = 0
    if end_index >= len(all_imgs):
        end_index = -1
    image_list.extend(all_imgs[start_index:end_index])
    results = []
    domain_url = request.build_absolute_uri('/')[:-1].strip("/")  # 得到Django的运行的域名端口
    for image_name in image_list:
        image_obj = {"name": os.path.join(domain_url, "media", data_name, "figures", image_name),
                     "index": all_imgs.index(image_name)}
        # 是否已经标注了
        label_name = ".".join(image_name.split(".")[:-1]) + ".json"
        label_path = os.path.join(label_dir, label_name)
        if os.path.exists(label_path):
            image_obj["label"] = True
        else:
            image_obj["label"] = False
        results.append(image_obj)
    return SuccessResponse(results)


# 压缩label 同时返回下载文件响应
@api_view(['POST'])
def export_all_separtions(request):
    result_id = request.data.get("resultId")
    result_file = get_object_or_404(SaveFile, id=result_id)     # 找不到会报404
    with open(result_file.file.path, "r", encoding="utf-8") as f:
        json_dict = json.load(f)
    figure_path = settings.MEDIA_ROOT / result_file.source / json_dict["name"]
    separate_dir = settings.MEDIA_ROOT / result_file.source / figure_path.stem
    zip_out_name = settings.MEDIA_ROOT / "tmp" / (figure_path.stem+".zip")
    if separate_dir.exists():
        # 压缩
        zip_dir(separate_dir, zip_out_name)
    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    try:
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法（.pdf,.mp3,.mp4等等什么样格式的文件都可以下载）
        response = StreamingHttpResponse(file_iterator(zip_out_name))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment;filename={file_name}{format}'.format(
            file_name=str(figure_path.stem), format=".zip")
    except:
        return ErrorResponse("Sorry but Not Found the File")
        # 在这里千万记得return,否则不会出现下载
    return response


@api_view(['POST'])
def detect_subfigures(request):
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
        result = backend_recognize(file_path)
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
def get_figure_separation_results(request):
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
    return SuccessResponse(results)

@api_view(['POST'])
def get_figure_separation_list(request):
    result_id = request.data.get("resultId")
    json_dict = request.data.get("jsonDict")
    result_file = get_object_or_404(SaveFile, id=result_id)     # 找不到会报404
    figure_ext = json_dict["name"].split(".")[-1]
    figure_path = settings.MEDIA_ROOT / result_file.source / result_file.name.replace("json", figure_ext)
    separate_dir = settings.MEDIA_ROOT / result_file.source / figure_path.stem
    if separate_dir.exists():   # 以前生成过需要删除
        # delete all files in the directory
        for file in separate_dir.iterdir():
            file.unlink()
    domain_url = request.build_absolute_uri('/')[:-1].strip("/")  # 得到Django的运行的域名端口
    base_url = domain_url + "/media/" + result_file.source + "/" + figure_path.stem + "/"
    # 每次都重新生成
    separate_list = separate_one(figure_path, json_dict, separate_dir, base_url=base_url)
    return SuccessResponse(separate_list)


def separate_one(figure_path, scale_dict, separate_dir,  base_url=""):
    figure_path = Path(figure_path)
    full_figure = Image.open(figure_path).convert("RGB")
    out_figure_root = Path(separate_dir)
    out_figure_root.mkdir(parents=True, exist_ok=True)
    img_width = scale_dict["width"]
    img_height = scale_dict["height"]
    img_objs = []
    for i, entity in enumerate(scale_dict["figures"]):
        points = entity["points"]  # [[x1,y1],[x2,y2]]
        left = max(min(points[0][0], points[1][0]), 0)
        top = max(min(points[0][1], points[1][1]), 0)
        right = min(max(points[0][0], points[1][0]), img_width)
        bottom = min(max(points[0][1], points[1][1]), img_height)
        region = full_figure.crop((left, top, right, bottom))
        figure_id = entity["id"]
        figure_no = ""
        for relation in scale_dict["relations"]:
            if relation[0] == figure_id:
                if relation[1] > 0:
                    figure_no_id = relation[1]  # 第二个是figure_no的id
                    for figure_no_obj in scale_dict["figure_nos"]:
                        if figure_no_obj["id"] == figure_no_id:
                            figure_no = figure_no_obj["text"]
                            break
                    break
        out_name = f"Fig-{figure_no}-{i+1}"
        out_name = (out_name + figure_path.suffix)
        out_path = out_figure_root / out_name    # 保存的路径
        region.save(out_path)
        img_obj = {"name": base_url + out_name, "figure_no": figure_no}
        img_objs.append(img_obj)
    return img_objs

@api_view(['POST'])
def figure_separation_upload(request):
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
        result = backend_recognize(file_path)
        # 使用 SaveFileCreateUpdateSerializer 保存json
        # 去掉 bar和labels
        result["bars"] = []
        result["labels"] = []
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
            redirect_url = "separation-results/" + str(json_instance.id)
            return SuccessResponse({"taskId": json_instance.id, "jsonDict": result, "redirectUrl": redirect_url,"token": cf_token_encoded})
    return ErrorResponse("error")

