# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 23:15
# @Author  : Marshall
# @FileName: system_serializers.py

from django.core.cache import cache
from rest_framework import serializers

from django.conf import settings
from apps.fadmin.bases.base_serializers import CustomModelSerializer

from apps.fadmin.models import DictData, DictDetails, ConfigSettings, SaveFile


# ================================================= #
# ************** 字典管理 序列化器  ************** #
# ================================================= #

class DictDataSerializer(CustomModelSerializer):
    """
    字典管理 简单序列化器
    """

    class Meta:
        model = DictData
        exclude = ('description', 'creator', 'modifier')


class ExportDictDataSerializer(CustomModelSerializer):
    """
    导出 字典管理 简单序列化器
    """

    class Meta:
        model = DictData
        fields = ('id', 'dict_name', 'dict_type', 'status', 'creator', 'modifier', 'remark',)


class DictDataCreateUpdateSerializer(CustomModelSerializer):
    """
    字典管理 创建/更新时的列化器
    """

    class Meta:
        model = DictData
        fields = '__all__'


# ================================================= #
# ************** 字典详情 序列化器  ************** #
# ================================================= #

class DictDetailsSerializer(CustomModelSerializer):
    """
    字典详情 简单序列化器
    """
    dict_type = serializers.CharField(source='dict_data.dict_type', default='', read_only=True)

    class Meta:
        model = DictDetails
        exclude = ('description', 'creator', 'modifier')


class ExportDictDetailsSerializer(CustomModelSerializer):
    """
    导出 字典详情 简单序列化器
    """

    class Meta:
        model = DictDetails
        fields = ('id', 'dict_label', 'dict_value', 'is_default', 'status', 'sort', 'creator', 'modifier', 'remark',)


class DictDetailsListSerializer(CustomModelSerializer):
    """
    字典详情List 简单序列化器
    """

    class Meta:
        model = DictDetails
        fields = ('dict_label', 'dict_value', 'is_default')


class DictDetailsCreateUpdateSerializer(CustomModelSerializer):
    """
    字典详情 创建/更新时的列化器
    """

    def save(self, **kwargs):
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_dict_details')
        return super().save(**kwargs)

    class Meta:
        model = DictDetails
        fields = '__all__'


# ================================================= #
# ************** 参数设置 序列化器  ************** #
# ================================================= #

class ConfigSettingsSerializer(CustomModelSerializer):
    """
    参数设置 简单序列化器
    """

    class Meta:
        model = ConfigSettings
        exclude = ('description', 'creator', 'modifier')


class ExportConfigSettingsSerializer(CustomModelSerializer):
    """
    导出 参数设置 简单序列化器
    """

    class Meta:
        model = ConfigSettings
        fields = (
            'id', 'config_name', 'config_key', 'config_value', 'config_type', 'status', 'creator', 'modifier', 'remark')


class ConfigSettingsCreateUpdateSerializer(CustomModelSerializer):
    """
    参数设置 创建/更新时的列化器
    """

    def save(self, **kwargs):
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_configKey')
        return super().save(**kwargs)

    class Meta:
        model = ConfigSettings
        fields = '__all__'


# ================================================= #
# ************** 文件管理 序列化器  ************** #
# ================================================= #

class SaveFileSerializer(CustomModelSerializer):
    """
    文件管理 简单序列化器
    """
    file_url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = SaveFile
        exclude = ('description',)


class SaveFileCreateUpdateSerializer(CustomModelSerializer):
    """
    文件管理 创建/更新时的列化器
    """
    file_url = serializers.SerializerMethodField(read_only=True)

    def get_file_url(self, obj: SaveFile):
        return getattr(obj.file, "url", obj.file) if hasattr(obj, "file") else ""

    def save(self, **kwargs):
        files = self.context.get('request').FILES.get('file')
        self.validated_data['name'] = files.name
        self.validated_data['size'] = files.size
        self.validated_data['type'] = files.content_type
        self.validated_data['address'] = '本地存储'
        self.validated_data['source'] = '用户上传'
        instance = super().save(**kwargs)
        return instance

    class Meta:
        model = SaveFile
        fields = '__all__'

