# -*- coding: utf-8 -*-
# @Time    : 2022/10/5 22:39
# @Author  : Marshall
# @FileName: urls.py

from django.urls import re_path, include
from apps.fadmin.views import LoginView,LogoutView
from . import views
from rest_framework.routers import DefaultRouter
from apps.fadmin.viewsets import FileModelViewSet

router = DefaultRouter()
router.register(r'file', FileModelViewSet)

urlpatterns = [
    re_path(r'^api-token-auth/', LoginView.as_view(), name='api_token_auth'),
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    # re_path(r'^register/$', RegisterView.as_view()),
    re_path(r'^logout/$', LogoutView.as_view()),
    # re_path(r'^getInfo/$', GetUserProfileView.as_view()),
]

urlpatterns += router.urls

