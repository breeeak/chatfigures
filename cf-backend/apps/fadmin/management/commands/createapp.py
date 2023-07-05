import logging
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # 帮助文本, 一般备注命令的用途及如何使用 'manage.py help <subcommand>'。
    help = """
            创建App命令, 在APPs下:
            python manage.py createapp app名 --verbose # 模块的 verbose_name
            python manage.py createapp app01 app02 ...  --verbose
            python manage.py createapp 一级文件名/app01 ...  --verbose   # 支持多级目录建app
           """

    def add_arguments(self, parser):
        parser.add_argument('app_name', nargs='+', type=str, help='APP Name or Directory')
        # Named (optional) arguments
        parser.add_argument(
            '--verbose', '-vb', type=str,
            help='Verbose Name of APP'
        )

    def handle(self, *args, **options):
        app_name = options.get('app_name')
        for name in app_name:
            names = name.split('/')     # 支持目录
            app_path = os.path.join(settings.BASE_DIR, "apps", *names)
            # 判断app是否存在
            if os.path.exists(app_path):
                print(f"创建失败，App {name} 已存在！")
                break
            # 创建目标目录 同时拷贝template
            source_path = os.path.join(settings.BASE_DIR, "apps", "fadmin", "template")
            shutil.copytree(source_path, app_path)
            dnames = ".".join(names)  # 导包时使用
            config_name = names[-1] if len(names) > 0 else name
            verbose_name = options.get('verbose') if options.get('verbose') else config_name
            # 修改app中的apps 内容
            content = f"""from django.apps import AppConfig


class {config_name.capitalize()}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.{dnames}"
    verbose_name = "{verbose_name}"
"""
            with open(os.path.join(app_path, "apps.py"), 'w', encoding='UTF-8') as f:
                f.write(content)
                f.close()
            # 注册app到 settings.py 中
            self.injection(os.path.join(settings.BASE_DIR, "apiproject", "settings.py"), f"    'apps.{dnames}',\n", "INSTALLED_APPS",
                      "]")

            # 注册app到 urls.py 中
            self.injection(os.path.join(settings.BASE_DIR, "apiproject", "urls.py"),
                      f"    re_path(r'^{name}/', include('apps.{dnames}.urls')),\n", "urlpatterns = [",
                      "]")

            print(f"创建 {name} App成功")

    @staticmethod
    def injection(file_path, insert_content, startswith, endswith):
        with open(file_path, "r+", encoding="utf-8") as f:
            data = f.readlines()    # 先读出所有行来
            with open(file_path, 'w', encoding='UTF-8') as f1:
                is_INSTALLED_APPS = False
                is_insert = False
                for content in data:    #
                    # 判断文件是否 INSTALLED_APPS 开头
                    if not is_insert and content.startswith(startswith):
                        is_INSTALLED_APPS = True
                    if not is_insert and content.startswith(endswith) and is_INSTALLED_APPS:
                        # 给前一行插入数据
                        content = insert_content + content
                        is_insert = True
                    f1.writelines(content)
