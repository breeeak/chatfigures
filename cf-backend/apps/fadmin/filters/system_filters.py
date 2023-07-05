# -*- coding: utf-8 -*-
# @Time    : 24/03/2023 17:01
# @Author  : Marshall
# @FileName: system_filters.py

import django_filters

from apps.fadmin.models import DictDetails, DictData, ConfigSettings, MessagePush, SaveFile
from apps.fadmin.models import LoginInfo, OperationLog


class DictDataFilter(django_filters.rest_framework.FilterSet):
    """
    字典管理 简单过滤器
    """
    dictName = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = DictData
        fields = '__all__'


class DictDetailsFilter(django_filters.rest_framework.FilterSet):
    """
    字典详情 简单过滤器
    """
    dictLabel = django_filters.CharFilter(lookup_expr='icontains')
    dictType = django_filters.CharFilter(field_name='dict_data__dictType')

    class Meta:
        model = DictDetails
        fields = '__all__'


class ConfigSettingsFilter(django_filters.rest_framework.FilterSet):
    """
    参数设置 简单过滤器
    """
    configName = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ConfigSettings
        fields = '__all__'


class SaveFileFilter(django_filters.rest_framework.FilterSet):
    """
    文件管理 简单过滤器
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = SaveFile
        exclude = ('file',)


class MessagePushFilter(django_filters.rest_framework.FilterSet):
    """
    消息通知 简单过滤器
    """

    # is_read = django_filters.CharFilter(field_name='messagepushuser_message_push__is_read')
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = MessagePush
        fields = '__all__'


class LoginInfoFilter(django_filters.rest_framework.FilterSet):
    """
    登录日志 简单过滤器
    """
    loginLocation = django_filters.CharFilter(lookup_expr='icontains')
    userName = django_filters.CharFilter(field_name='creator__username', lookup_expr='icontains')

    class Meta:
        model = LoginInfo
        fields = '__all__'


class OperationLogFilter(django_filters.rest_framework.FilterSet):
    """
    操作日志 简单过滤器
    """
    request_modular = django_filters.CharFilter(lookup_expr='icontains')
    creator_username = django_filters.CharFilter(field_name='creator__username', lookup_expr='icontains')

    class Meta:
        model = OperationLog
        fields = '__all__'



