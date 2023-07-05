# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 0:14
# @Author  : Marshall
# @FileName: exception_util.py

import logging
import traceback

from django.db.models import ProtectedError
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from rest_framework import exceptions
from rest_framework.views import set_rollback
from rest_framework.exceptions import APIException as DRFAPIException, AuthenticationFailed
from rest_framework import status

from apps.fadmin.utils.response_util import ErrorResponse

logger = logging.getLogger(__name__)


class APIException(Exception):
    """
    通用异常:(1)用于接口请求是抛出移除, 此时code会被当做标准返回的code, message会被当做标准返回的msg
    """

    def __init__(self, code=status.HTTP_400_BAD_REQUEST, message='API异常', args=('API异常',)):
        self.args = args
        self.code = code
        self.message = message

    def __str__(self):
        return self.message


class GenException(APIException):
    pass


class FrameworkException(Exception):
    """
    框架异常、配置异常等
    """

    def __init__(self, message='框架异常', *args: object, **kwargs: object) -> None:
        super().__init__(*args, )
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class JWTAuthenticationFailedException(APIException):
    """
    JWT认证异常
    """

    def __init__(self, code=status.HTTP_403_FORBIDDEN, message=None, args=('异常',)):
        if not message:
            message = 'JWT authentication failed!'
        super().__init__(code, message, args)


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
        Same as Django's standard shortcut, but make sure to also raise 404
        if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError, Http404):
        raise APIException(message='该对象不存在或者无访问权限')


def op_exception_handler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    msg = 'exception'
    code = status.HTTP_400_BAD_REQUEST

    if isinstance(ex, AuthenticationFailed):
        code = 401
        msg = ex.detail
    elif isinstance(ex, DRFAPIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, exceptions.APIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, ProtectedError):
        set_rollback()
        msg = "删除失败:该条数据与其他数据有相关绑定"
    # elif isinstance(ex, DatabaseError):
    #     set_rollback()
    #     msg = "接口服务器异常,请联系管理员"
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        msg = str(ex)
    return ErrorResponse(msg=msg, status=code)
