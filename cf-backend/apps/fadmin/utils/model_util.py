# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 11:07
# @Author  : Marshall
# @FileName: model_util.py

from django.apps import apps
from django.apps.config import AppConfig
from django.db.models.fields import Field

from apps.fadmin.models import Dept


def get_primary_field(model, many=False):
    """
    获取模型的主键列对应的Field
    :param model:
    :param many:
    :return:
    """
    primary_field: Field = list(filter(lambda field: field.primary_key, model._meta.local_fields))
    if many:
        return primary_field
    return primary_field[0]


def get_primary_key_name(model, many=False):
    primary_field = get_primary_field(model=model, many=many)
    if many:
        return [field.name for field in primary_field]
    return primary_field.name


def get_business_key_name(model):
    """
    获取业务列名称
    :param model:
    :return:
    """
    return getattr(model, 'business_field_name', get_primary_key_name(model, False))


def get_business_field(model):
    """
    获取模型的业务列对应的Field
    :param model:
    :return:
    """
    business_key_name = get_business_key_name(model)
    business_field = list(filter(lambda field: field.name == business_key_name, model._meta.local_fields))
    return business_field[0]


def get_model(app_label: str = None, model_name: str = None, model_label: str = None):
    """
    根据App、Model名称获取model_class
    使用:get_model(app_label='op_cmdb', model_name='Business')
    或者:get_model(model_label='op_cmdb.Business')
    :param app_label: settings中注册的app的名称, 例如:op_cmdb, admin
    :param model_name: 某个app中模型的类名, 如:Business, host, dept(忽略大小写)
    :param model_label: 例如: op_cmdb.Business
    :return:
    """
    if model_label:
        app_label, model_name = model_label.split(".")
    app_conf: AppConfig = apps.get_app_config(app_label)
    return app_conf.get_model(model_name)

def get_dept(dept_id: int, dept_all_list=None, dept_list=None):
    """
    递归获取部门的所有下级部门
    :param dept_id: 需要获取的部门id
    :param dept_all_list: 所有部门列表
    :param dept_list: 递归部门list
    :return:
    """
    if not dept_all_list:
        dept_all_list = Dept.objects.all().values('id', 'parentId')
    if dept_list is None:
        dept_list = [dept_id]
    for ele in dept_all_list:
        if ele.get('parentId') == int(dept_id):
            dept_list.append(ele.get('id'))
            get_dept(ele.get('id'), dept_all_list, dept_list)
    return list(set(dept_list))

