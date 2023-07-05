# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 14:20
# @Author  : Marshall
# @FileName: permissions_serializers.py


import hashlib
import datetime
from captcha.views import CaptchaStore
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.fadmin.bases.base_serializers import CustomModelSerializer
from apps.fadmin.utils.validators_util import CustomUniqueValidator
from apps.fadmin.utils.exception_util import GenException

from apps.fadmin.models import MessagePush
from .permissions_serializers import RoleSerializer, PostSerializer

User = get_user_model()

# ================================================= #
# ************** 用户管理 序列化器  ************** #
# ================================================= #


class UserSerializer(CustomModelSerializer):
    """
    简单用户序列化器
    """
    admin = serializers.SerializerMethodField(read_only=True)
    dept_id = serializers.IntegerField(source='dept.id', read_only=True)
    # 未读通知数量
    unread_msg_count = serializers.SerializerMethodField(read_only=True)

    def get_admin(self, obj: User):
        role_list = obj.role.filter(status='1').values_list('admin', flat=True)
        if True in list(set(role_list)):
            return True
        return False

    def get_unread_msg_count(self, obj: User):
        return MessagePush.objects.filter(status='2').exclude(messagepushuser_message_push__is_read=True,
                                                              messagepushuser_message_push__user=obj).count()

    class Meta:
        model = User
        depth = 1
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined', 'creator')


class ExportUserSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    dept__deptName = serializers.CharField(source='dept.deptName', default='')
    dept__owner = serializers.CharField(source='dept.owner', default='')

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'mobile', 'gender', 'is_active', 'last_login', 'dept__deptName',
                  'dept__owner')


class UserCreateUpdateSerializer(CustomModelSerializer):
    """
    用户管理 创建/更新时的列化器
    """
    admin = serializers.SerializerMethodField(read_only=True)
    post = PostSerializer(many=True, read_only=True)
    role = RoleSerializer(many=True, read_only=True)
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[
                                         CustomUniqueValidator(queryset=User.objects.all(), message="用戶已存在")],
                                     error_messages={
                                         "blank": "请输入用户名称",
                                         "required": "用户名称不能为空",
                                         "max_length": "用户名称过长",
                                     })
    email = serializers.EmailField(required=True, max_length=150,
                                     validators=[
                                         CustomUniqueValidator(queryset=User.objects.all(), message="该邮箱已经注册")],
                                     error_messages={
                                         "blank": "请输入邮箱名称",
                                         "required": "邮箱不能为空",
                                         "max_length": "邮箱过长",
                                     })

    def get_admin(self, obj: User):
        role_list = obj.role.filter(status='1').values_list('admin', flat=True)
        if True in list(set(role_list)):
            return True
        return False

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        self.validated_data['dept_id'] = self.initial_data.get('dept_id', None)
        data = super().save(**kwargs)
        data.post.set(self.initial_data.get('post_ids'))
        data.role.set(self.initial_data.get('role_ids'))
        return data

    def create(self, validated_data):
        data = super().create(validated_data)
        data.set_password(self.initial_data.get('password', None))
        data.save()
        return data

    class Meta:
        model = User
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined')
        read_only_fields = ('dept',)


class UserImportSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        data = super().save(**kwargs)
        password = hashlib.new('md5', self.initial_data.get('password', '').encode(encoding='UTF-8')).hexdigest()
        data.set_password(password)
        data.save()
        return data

    def run_validation(self, data={}):
        # 把excel 数据进行格式转换
        if type(data) is dict:
            data['role'] = str(data['role']).split(',')
            data['post'] = str(data['post']).split(',')
            data['gender'] = {'男': '0', '女': '1', '未知': '2'}.get(data['gender'])
            data['is_active'] = {'启用': True, '禁用': False}.get(data['is_active'])
        return super().run_validation(data)

    class Meta:
        model = User
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined')


class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """
    captcha = serializers.CharField(
        max_length=6, required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["id"]
    default_error_messages = {"no_active_account": _("账号/密码错误")}

    def judge_captcha(self):
        """
        校验验证码
        :param request:
        :return:
        """
        if not settings.CAPTCHA_STATE:  # 未开启验证码则返回 True
            return True
        captcha = self.initial_data.get("captcha", None)
        if captcha is None:
            raise GenException(message='请输入验证码')
        # 验证码过期时间
        five_minute_ago = datetime.now() - datetime.timedelta(hours=0, minutes=5, seconds=0)
        get_captcha = CaptchaStore.objects.filter(
            id=self.initial_data["captchaKey"]
        ).first()
        if get_captcha:
            if five_minute_ago > get_captcha.expiration:
                get_captcha.delete()
                raise GenException("验证码过期")
            else:
                if str(get_captcha.response).lower() == captcha.lower():  # 如果验证码匹配
                    get_captcha.delete()
                    return True
                else:
                    get_captcha.delete()
                    raise GenException("图片验证码错误")
        else:
            raise GenException("验证码生成错误,请重试")

    def validate(self, attrs):
        self.judge_captcha()
        data = super().validate(attrs)
        return data

