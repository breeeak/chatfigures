# -*- coding: utf-8 -*-
# @Time    : 24/03/2023 16:51
# @Author  : Marshall
# @FileName: files_viewset.py
from rest_framework.request import Request
from apps.fadmin.bases.base_viewsets import CustomModelViewSet
from apps.fadmin.utils.response_util import SuccessResponse
from apps.fadmin.models import SaveFile
from apps.fadmin.serializers import SaveFileSerializer, SaveFileCreateUpdateSerializer
from apps.fadmin.filters import SaveFileFilter
from apps.fadmin.utils.permissions_util import CommonPermission
from apps.fadmin.utils.filters_util import DataLevelPermissionsFilter


class FileModelViewSet(CustomModelViewSet):
    """
   文件管理 模型的CRUD视图
   """
    queryset = SaveFile.objects.all()
    serializer_class = SaveFileSerializer
    create_serializer_class = SaveFileCreateUpdateSerializer
    update_serializer_class = SaveFileCreateUpdateSerializer
    filter_class = SaveFileFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    # create_extra_permission_classes = (CommonPermission,)  # 匿名用户而言 上传文件是不需要权限的
    search_fields = ('configName',)
    ordering = '-create_datetime'  # 默认排序

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return SuccessResponse(serializer.data, status=201, headers=headers)

    def clearsavefile(self, request: Request, *args, **kwargs):
        """
        清理废弃文件
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pass

