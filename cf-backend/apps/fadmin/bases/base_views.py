# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 9:32
# @Author  : Marshall
# @FileName: base_views.py
from rest_framework.request import Request
from rest_framework.views import APIView
from types import FunctionType, MethodType


class CustomAPIView(APIView):
    """
    继承、增强DRF的APIView
    比APIView增加了几个权限类，logger类
    TODO 增加的如何使用
    """
    extra_permission_classes = ()
    # 仅当GET方法时会触发该权限的校验
    GET_permission_classes = ()

    # 仅当POST方法时会触发该权限的校验
    POST_permission_classes = ()

    # 仅当DELETE方法时会触发该权限的校验
    DELETE_permission_classes = ()

    # 仅当PUT方法时会触发该权限的校验
    PUT_permission_classes = ()

    view_logger_classes = ()

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.check_extra_permissions(request)
        self.check_method_extra_permissions(request)

    def get_view_loggers(self, request: Request, *args, **kwargs):
        logger_classes = self.view_logger_classes or []
        if not logger_classes:
            return []
        view_loggers = [logger_class(view=self, request=request, *args, **kwargs) for logger_class in logger_classes]
        return view_loggers

    def handle_logging(self, request: Request, *args, **kwargs):
        view_loggers = self.get_view_loggers(request, *args, **kwargs)
        method = request.method.lower()
        for view_logger in view_loggers:
            view_logger.handle(request, *args, **kwargs)
            logger_fun = getattr(view_logger, f'handle_{method}', f'handle_other')
            if logger_fun and isinstance(logger_fun, (FunctionType, MethodType)):
                logger_fun(request, *args, **kwargs)

    def get_extra_permissions(self):
        return [permission() for permission in self.extra_permission_classes]

    def check_extra_permissions(self, request: Request):
        for permission in self.get_extra_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def get_method_extra_permissions(self):
        _name = self.request.method.upper()
        method_extra_permission_classes = getattr(self, f"{_name}_permission_classes", None)
        if not method_extra_permission_classes:
            return []
        return [permission() for permission in method_extra_permission_classes]

    def check_method_extra_permissions(self, request):
        for permission in self.get_method_extra_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )




