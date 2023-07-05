# -*- coding: utf-8 -*-
# @Time    : 2022/10/15 23:41
# @Author  : Marshall
# @FileName: __init__.py.py

from apps.fadmin.models.permissions.departments import Dept
from apps.fadmin.models.permissions.menus import Menu
from apps.fadmin.models.permissions.posts import Post
from apps.fadmin.models.permissions.roles import Role
from apps.fadmin.models.permissions.users import User

from apps.fadmin.models.system.config_settings import ConfigSettings
from apps.fadmin.models.system.dict_data import DictData
from apps.fadmin.models.system.dict_details import DictDetails
from apps.fadmin.models.system.save_file import SaveFile
from apps.fadmin.models.system.push_messages import MessagePush, MessagePushUser
from apps.fadmin.models.system.login_info import LoginInfo
from apps.fadmin.models.system.operation_log import OperationLog

