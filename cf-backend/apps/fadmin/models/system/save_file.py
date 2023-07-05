import os
import uuid
from django.db.models import CharField, FileField, BooleanField

from apps.fadmin.bases.base_models import CoreModel


def files_path(instance, filename):
    """
    存储路径格式参考： export/95c6f101-e2f6-4957-9f66-6eb296ece287.png
    :param instance:
    :param filename:
    :return:
    """
    return '/'.join([instance.source, str(uuid.uuid4()) + os.path.splitext(filename)[-1]])


class SaveFile(CoreModel):
    FILE_SOURCES = (
        ('export', "导出的Excel"),
        ('upload', "用户导入"),
        ('temp', "临时文件"),
        ('other', "其他文件"),
        ('guest', "游客文件"),
        ('user', "用户文件")
    )

    name = CharField(max_length=128, verbose_name="文件名称", null=True, blank=True)
    type = CharField(max_length=200, verbose_name="文件类型", null=True, blank=True)
    size = CharField(max_length=64, verbose_name="文件大小", null=True, blank=True)
    session_token = CharField(max_length=64, verbose_name="会话token", null=True, blank=True)
    address = CharField(max_length=16, verbose_name="存储位置", null=True, blank=True)  # 本地、阿里云、腾讯云..
    source = CharField(max_length=16, choices=FILE_SOURCES, verbose_name="文件来源", null=True, blank=True)  # 导出、用户上传.
    oss_url = CharField(max_length=200, verbose_name="OSS地址", null=True, blank=True)
    status = BooleanField(default=True, verbose_name="文件是否存在")
    file = FileField(verbose_name="文件URL", upload_to=files_path)

    class Meta:
        verbose_name = '文件管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
