from django.db.models import CharField

from apps.fadmin.bases.base_models import CoreModel


class ConfigSettings(CoreModel):
    config_name = CharField(max_length=64, verbose_name="参数名称")
    config_key = CharField(max_length=256, verbose_name="参数键名")
    config_value = CharField(max_length=256, verbose_name="参数键值")
    config_type = CharField(max_length=8, verbose_name="是否内置")
    status = CharField(max_length=8, verbose_name="参数状态")
    remark = CharField(max_length=256, verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = '参数设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.config_name}"
