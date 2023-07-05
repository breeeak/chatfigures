# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 20:48
# @Author  : Marshall
# @FileName: base_viewsets.py
from types import FunctionType, MethodType

from rest_framework.viewsets import ViewSetMixin
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.settings import api_settings
from django_filters.rest_framework import DjangoFilterBackend

from apps.fadmin.bases.base_mixins import *
from apps.fadmin.bases.base_generics import GenericAPIView
from apps.fadmin.bases.base_serializers import CustomModelSerializer
from apps.fadmin.bases.base_loggers import CustomerModelViewLogger

from apps.fadmin.utils.filters_util import AdvancedSearchFilter
from apps.fadmin.utils.exception_util import get_object_or_404


class GenericViewSet(ViewSetMixin, GenericAPIView):
    """
    主要是改进了drf的功能 增加了filter,logger,自定义serializer
    原代码参考#
    """
    # TODO 了解这个ViewSet代码
    extra_filter_backends = []
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter, AdvancedSearchFilter]
    view_logger_classes = (CustomerModelViewLogger,)

    def handle_logging(self, request: Request, *args, **kwargs):
        view_loggers = self.get_view_loggers(request, *args, **kwargs)
        for view_logger in view_loggers:
            handle_action = getattr(view_logger, f'handle_{self.action}', None)
            if handle_action and isinstance(handle_action, (FunctionType, MethodType)):
                handle_action(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        serializer = serializer_class(*args, **kwargs)
        if isinstance(serializer, CustomModelSerializer):
            serializer.request = self.request
        return serializer

    def filter_queryset(self, queryset):
        for backend in set(set(self.filter_backends) | set(self.extra_filter_backends or [])):
            queryset = backend().filter_queryset(self.request, queryset, self)
        queryset = self.action_extra_filter_queryset(queryset)
        return queryset

    def action_extra_filter_queryset(self, queryset):
        action__extra_filter_backends = getattr(self, f"{self.action}_extra_filter_backends", None)
        if not action__extra_filter_backends:
            return queryset
        for backend in action__extra_filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_serializer_class(self):
        action_serializer_name = f"{self.action}_serializer_class"
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    def reverse_action(self, url_name, *args, **kwargs):
        return super().reverse_action(url_name, *args, **kwargs)

    def get_action_extra_permissions(self):
        """
        获取已配置的action权限校验,并且实例化其对象
        :return:
        """
        action_extra_permission_classes = getattr(self, f"{self.action}_extra_permission_classes", None)
        if not action_extra_permission_classes:
            return []
        return [permission() for permission in action_extra_permission_classes]

    def check_action_extra_permissions(self, request):
        """
        逐个校验action权限校验
        :param request:
        :return:
        """
        for permission in self.get_action_extra_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def check_action_extra_object_permissions(self, request, obj):
        """
        action方法的专属对象权限校验
        :param request:
        :param obj:
        :return:
        """
        for permission in self.get_action_extra_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def initial(self, request, *args, **kwargs):
        """
        重写initial方法
        (1)新增action的权限校验
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        super().initial(request, *args, **kwargs)
        self.check_action_extra_permissions(request)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def check_object_permissions(self, request, obj):
        """
        重新check_object_permissions
        (1)新增action方法的专属对象权限检查入口
        (2)先校验共同的object_permissions, 再校验action的object_permissions
        :param request:
        :param obj:
        :return:
        """
        super().check_object_permissions(request, obj)
        self.check_action_extra_object_permissions(request, obj)


class ModelViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    pass


class CustomModelViewSet(ModelViewSet, TableSerializerMixin,
                         ImportSerializerMixin,
                         ExportSerializerMixin):
    """
    自定义的ModelViewSet:
    (1)默认分页器就为统一分页器op_drf.pagination.Pagination
    (1)默认使用统一标准返回格式
    (1)默认支持高级搜索
    (1)默认支持生成前端动态table的option
    (1)ORM性能优化, 尽可能使用values_queryset形式
    """
    values_queryset = None
    ordering_fields = '__all__'

    def get_queryset(self):
        if getattr(self, 'values_queryset', None):
            return self.values_queryset
        return super().get_queryset()

