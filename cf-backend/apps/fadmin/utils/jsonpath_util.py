# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 10:24
# @Author  : Marshall
# @FileName: jsonpath_util.py


import logging
from collections import Iterable

import jsonpath

logger = logging.getLogger(__name__)


def get_jsonpath(params: dict = None, exclude_params: list = None, type_params: dict = None):
    """
    生成jsonpath表达式 根据给出的条件
    :param params:
    :param exclude_params:
    :param type_params:
    :return:
    """
    if params is None:
        params = {}
    if exclude_params is None:
        exclude_params = []
    _filters = []
    for param_name, param_value in params.items():
        if param_name in exclude_params:
            continue
        if type_params is None or type_params.get(param_name, 'str') == 'str':
            _filter = f"@.{param_name}=='{param_value}'"
        else:
            _filter = f"@.{param_name}=={param_value}"
        _filters.append(_filter)
    _path = " || ".join(_filters)
    if not _path:
        return ""
    return f"[?({_path})]"


def filter_json(obj: list, expr: str, *args, **kwargs):
    """
    根据jsonpath表达式过滤一个json list
    :param obj:
    :param expr:
    :param args:
    :param kwargs:
    :return:
    """
    if not isinstance(obj, Iterable):
        return []
    if not expr.startswith('$'):
        expr = f"${expr}"
    logger.debug(f"expr={expr}, len={len(obj)}")
    return jsonpath.jsonpath(obj, expr, *args)


def search_json(obj: list, search: str, search_fields: list):
    """
    根据 搜索条件和搜索字段 过滤一个列表 不区分大小写相等
    :param obj:
    :param search:
    :param search_fields:
    :return:
    """
    queryset = []
    search = search.lower()
    for ele in obj:
        for field_name in search_fields:
            value = ele.get(field_name, None)
            if value and search in str(value).lower():
                queryset.append(ele)
                break
    return queryset
