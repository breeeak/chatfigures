# -*- coding: utf-8 -*-
# @Time    : 2022/10/6 20:51
# @Author  : Marshall
# @FileName: swaggerAPI.py
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from configs.env import DEVELOP_LICENSE, DEVELOP_EMAIL

# swaggerAPI
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=DEVELOP_EMAIL),
        license=openapi.License(name=DEVELOP_LICENSE),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
)

