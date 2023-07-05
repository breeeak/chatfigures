# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 21:02
# @Author  : Marshall
# @FileName: base_responses.py

"""
常用的Response以及Django的Response、DRF的Response
"""
from django.http.response import DjangoJSONEncoder, JsonResponse
from rest_framework.response import Response


class ChineseJSONEncoder(DjangoJSONEncoder):
    """
    重写DjangoJSONEncoder
    (1)默认返回支持中文格式的json字符串 ensure_ascii=False
    """

    def __init__(self, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=False, check_circular=check_circular,
                         allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators,
                         default=default)


class SuccessResponse(Response):
    """
    标准响应成功的返回, SuccessResponse(data)或者SuccessResponse(data=data, msg=msg)
    默认返回200, 也可指定其他返回码，status是success，可以指定msg
    """

    def __init__(self, data=None, msg='success', status=200, template_name=None, headers=None, exception=False,
                 content_type=None):
        self.std_data = {
            "code": status,
            "data": data,
            "msg": msg,
            "status": 'success'
        }
        super().__init__(self.std_data, status, template_name, headers, exception, content_type)

    def __str__(self):
        return str(self.std_data)


class ErrorResponse(Response):
    """
    标准响应错误的返回,ErrorResponse(msg='xxx')
    (1)默认错误码返回400, 也可以指定其他返回码:ErrorResponse(status=xxx)
    """

    def __init__(self, data=None, msg='error', status=400, template_name=None, headers=None,
                 exception=False, content_type=None):
        self.std_data = {
            "code": status,
            "data": data,
            "msg": msg,
            "status": 'error'
        }
        super().__init__(self.std_data, status, template_name, headers, exception, content_type)

    def __str__(self):
        return str(self.std_data)


class SuccessJsonResponse(JsonResponse):
    """
    标准JsonResponse
    """

    def __init__(self, data, msg='success', status=200,  encoder=ChineseJSONEncoder, safe=True, json_dumps_params=None, **kwargs):
        std_data = {
            "code": status,
            "data": data,
            "msg": msg,
            "status": 'success'
        }
        super().__init__(std_data, encoder, safe, json_dumps_params, **kwargs)


class ErrorJsonResponse(JsonResponse):
    """
    标准JsonResponse
    """

    def __init__(self, data, msg='error', status=400, encoder=ChineseJSONEncoder, safe=True, json_dumps_params=None,
                 **kwargs):
        std_data = {
            "code": status,
            "data": data,
            "msg": msg,
            "status": 'error'
        }
        super().__init__(std_data, encoder, safe, json_dumps_params, **kwargs)


