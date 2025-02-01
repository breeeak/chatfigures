"""apiproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from apps.fadmin.system.swaggerAPI import schema_view
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    # 这是Django默认的管理站点路径
    path("admin/", admin.site.urls),
    # 这里是swagger相关 API后台    # 共支持四种样式的 API 样式的显示  json yaml swagger redoc
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^fadmin/', include('apps.fadmin.urls')),
    # 自定义应用
    re_path(r'^figures/', include('apps.figures.urls')),
    re_path(r'^measurement/', include('apps.measurement.urls')),
]

# if settings.DEBUG:
# TODO 静态目录可以直接进行访问下载，是否有问题？
# 这里之所以使用if settings.DEBUG，是因为这种配置模式应该仅限用于开发模式，在生产环境应该通过web前端来处理这些媒体文件的访问
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]
