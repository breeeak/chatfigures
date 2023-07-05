# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 9:55
# @Author  : Marshall
# @FileName: init_db.py
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    sql_path = os.path.join(settings.BASE_DIR, "apps", "fadmin", "system", "sqls")

    # 帮助文本, 一般备注命令的用途及如何使用 'manage.py help <subcommand>'。
    help = """
            初始化数据库, 在APPs下:
            python manage.py init_db [数据表名(不带.sql)] ：默认所有基础数据都初始化，或者指定sql执行，参考
            python manage.py init_db fadmin_post fadmin_user
           """

    def add_arguments(self, parser):
        parser.add_argument('init_name', nargs='*', type=str, help='sql script names')

    def handle(self, *args, **options):
        init_dict = os.listdir(self.sql_path)
        init_names = options.get('init_name')
        if init_names:
            for init_name in init_names:
                sql_filename = init_name + ".sql"
                if sql_filename in init_dict:
                    self.init(sql_filename)
                else:
                    logger.info(f'[{sql_filename}]未知表名！无法初始化，请检查sqls')
        else:
            for sql_filename in init_dict:
                self.init(sql_filename)

    def init(self, sql_filename):
        """
        初始化
        :param sql_filename: sql存放位置
        :param model_name: 模块名
        :param table_name: 表名
        :return:
        """
        table_name = sql_filename.replace(".sql", "")
        logger.info(f'正在初始化[{table_name}]中...')
        if self.custom_sql(self.get_sql(sql_filename), table_name):
            logger.info(f'[{table_name}]初始化完成！')
        else:
            logger.info(f'已取消[{table_name}]初始化')

    @staticmethod
    def custom_sql(sql_list, table_name):
        """
        批量执行sql, 执行成功返回True
        """
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from {}".format(table_name))
            result = cursor.fetchone()

            if result[0] > 0:
                while True:
                    inp = input(f'[{table_name}]模型已初始化完成，继续将清空[{table_name}]表中所有数据，是否继续初始化？【 Y/N 】')
                    if inp.upper() == 'N':
                        return False
                    elif inp.upper() == 'Y':
                        logger.info(f'正在清空[{table_name}]中数据...')
                        cursor.execute("SET foreign_key_checks = 0")
                        for ele in table_name.split(','):
                            cursor.execute("truncate table {};".format(ele))
                        cursor.execute("SET foreign_key_checks = 1")
                        connection.commit()
                        logger.info(f'清空[{table_name}]中数据{result[0]}条')
                        break

            for sql in sql_list:
                try:
                    cursor.execute(sql)
                except Exception as e:
                    print(e)
            connection.commit()
            return True

    def get_sql(self, filename):
        """
        获取文件内所有sql语句
        :param filename: 相对于scripts下的sql路径名字，如果多级目录：则传入：os.path.join('permission','permission_dept.sql')
        :return: 返回每一条sql语句列表
        """

        pwd = os.path.join(self.sql_path, filename)
        with open(pwd, 'rb') as fp:
            content = fp.read().decode('utf8')
        return [ele for ele in content.split('\n') if not ele.startswith('--') and ele.strip(' ')]