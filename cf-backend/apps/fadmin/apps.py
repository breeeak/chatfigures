from django.apps import AppConfig


class FadminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.fadmin"
    verbose_name = "管理模块"

