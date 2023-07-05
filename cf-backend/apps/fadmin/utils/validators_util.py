# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 14:48
# @Author  : Marshall
# @FileName: validator_util.py


"""
重写校验器返回字段
"""
from rest_framework.validators import UniqueValidator, qs_exists

from .exception_util import APIException


class CustomUniqueValidator(UniqueValidator):
    """
    继承,重写必填字段的验证器结果,防止字段暴露
    主要重写了APIException
    """

    def __call__(self, value, serializer_field):
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        field_name = serializer_field.source_attrs[-1]
        # Determine the existing instance, if this is an update operation.
        instance = getattr(serializer_field.parent, 'instance', None)

        queryset = self.queryset
        queryset = self.filter_queryset(value, queryset, field_name)
        queryset = self.exclude_current_instance(queryset, instance)
        if qs_exists(queryset):
            raise APIException(message=self.message)

    def __repr__(self):
        return super().__repr__()
