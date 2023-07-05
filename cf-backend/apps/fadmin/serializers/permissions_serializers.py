# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 15:05
# @Author  : Marshall
# @FileName: permissions_serializers.py

import hashlib

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.fadmin.models import Menu, Dept, Post, Role
from apps.fadmin.bases.base_serializers import CustomModelSerializer

User = get_user_model()

# ================================================= #
# ************** 菜单管理 序列化器  ************** #
# ================================================= #


class MenuSerializer(CustomModelSerializer):
    """
    简单菜单序列化器
    """
    parent_id = serializers.IntegerField(source="parent_id.id", default=0)

    class Meta:
        model = Menu
        exclude = ('description', 'creator', 'modifier')


class MenuCreateUpdateSerializer(CustomModelSerializer):
    """
    菜单管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        # name = attrs['name']
        # role: Role = Role.objects.filter(name=name).first()
        # if role and attrs.get('instanceId', '') != role.instanceId:
        #     raise APIException(message=f'角色名称[{name}]不能重复')
        # if getattr(self.instance, 'is_public', False) or attrs.get('is_public', False):
        #     up = UserPermission(self.request.user)
        #     if not up.is_manager():
        #         raise APIException(message=f'仅Manger能创建/更新角色为公共角色')
        return super().validate(attrs)

    def save(self, **kwargs):
        Menu.delete_cache()
        return super().save(**kwargs)

    class Meta:
        model = Menu
        fields = '__all__'


class MenuTreeSerializer(serializers.ModelSerializer):
    """
    菜单树形架构序列化器:递归序列化所有深度的子菜单
    """
    label = serializers.CharField(source='name', default='')
    parent_id = serializers.IntegerField(source="parent_id.id", default=0)

    class Meta:
        model = Menu
        fields = ('id', 'label', 'order_num', 'parent_id')      # label  fields选项中的名称可以映射到模型类中不存在参数的属性或方法


# ================================================= #
# ************** 部门管理 序列化器  ************** #
# ================================================= #

class DeptSerializer(CustomModelSerializer):
    """
    部门管理 简单序列化器
    """
    parent_id = serializers.IntegerField(source="parent_id.id", default=0)

    class Meta:
        model = Dept
        exclude = ('description', 'creator', 'modifier')


class DeptCreateUpdateSerializer(CustomModelSerializer):
    """
    部门管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Dept
        fields = '__all__'


class DeptTreeSerializer(serializers.ModelSerializer):
    """
    部门树形架构序列化器:递归序列化所有深度的子部门
    """
    label = serializers.CharField(source='dept_name', default='')
    parent_id = serializers.IntegerField(source="parent_id.id", default=0)

    class Meta:
        model = Dept
        fields = ('id', 'label', 'parent_id', 'status')


# ================================================= #
# ************** 岗位管理 序列化器  ************** #
# ================================================= #

class PostSerializer(CustomModelSerializer):
    """
    岗位管理 简单序列化器
    """

    class Meta:
        model = Post
        exclude = ('description', 'creator', 'modifier')


class ExportPostSerializer(CustomModelSerializer):
    """
    导出 岗位管理 简单序列化器
    """

    class Meta:
        model = Post
        fields = ('id', 'post_name', 'post_code', 'post_sort', 'status', 'creator', 'modifier', 'remark')


class PostSimpleSerializer(CustomModelSerializer):
    """
    岗位管理 极简单序列化器
    """

    class Meta:
        model = Post
        fields = ('id', 'post_name', 'post_code', 'status')


class PostCreateUpdateSerializer(CustomModelSerializer):
    """
    岗位管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Post
        fields = '__all__'


# ================================================= #
# ************** 角色管理 序列化器  ************** #
# ================================================= #

class RoleSerializer(CustomModelSerializer):
    """
    角色管理 简单序列化器
    """

    class Meta:
        model = Role
        exclude = ('description', 'creator', 'modifier')


class ExportRoleSerializer(CustomModelSerializer):
    """
    导出 角色管理 简单序列化器
    """
    dataScope = serializers.SerializerMethodField()

    def get_dataScope(self, obj):
        dataScope = obj.get_dataScope_display()
        return dataScope

    class Meta:
        model = Role
        fields = ('id', 'role_name', 'role_key', 'role_sort', 'data_scope', 'status', 'creator', 'modifier', 'remark')


class RoleSimpleSerializer(CustomModelSerializer):
    """
    角色管理 极简单序列化器
    """

    class Meta:
        model = Role
        fields = ('id', 'role_name', 'role_key', 'status')


class RoleCreateUpdateSerializer(CustomModelSerializer):
    """
    角色管理 创建/更新时的列化器
    """
    menu = MenuSerializer(many=True, read_only=True)
    dept = DeptSerializer(many=True, read_only=True)

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept.set(self.initial_data.get('dept'))
        data.menu.set(self.initial_data.get('menu'))
        return data

    class Meta:
        model = Role
        fields = '__all__'
