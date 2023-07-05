
# ================================================= #
# ************** mysql数据库 配置  ************** #
# ================================================= #
# 数据库类型 MYSQL/SQLITE3
DATABASE_TYPE = "MYSQL"
# 数据库地址
DATABASE_HOST = "177.8.0.13"
# 数据库端口
DATABASE_PORT = 3306
# 数据库用户名
DATABASE_USER = "root"
# 数据库密码
DATABASE_PASSWORD = "chatfigures2234"
# 数据库名
DATABASE_NAME = "apiproject_db"

# ================================================= #
# ************** redis 数据库配置  ************** #
# ================================================= #
# 是否启用Redis缓存
# 注：不使用redis则无法使用celery
REDIS_ENABLE = True
REDIS_DB = 1
REDIS_HOST = '177.8.0.14'
REDIS_PORT = 6379
REDIS_PASSWORD = None
# celery 定时任务redis 库号
CELERY_DB = 2

# 开发人员邮箱    swagger使用
DEVELOP_EMAIL = "shuomeng2-c@my.cityu.edu"
DEVELOP_LICENSE = "BSD License"

# ================================================= #
# ************** 默认配置  ************** #
# ================================================= #
# 验证码状态
CAPTCHA_STATE = False

DEBUG = False
# 允许访问的ip地址列表
ALLOWED_HOSTS = ['*']
# 允许跨域源
CORS_ORIGIN_ALLOW_ALL = True
# 允许ajax请求携带cookie
CORS_ALLOW_CREDENTIALS = False
# 接口权限
INTERFACE_PERMISSION = True

# ================================================= #
# ************** 模型配置  ************** #
# ================================================= #
INFERENCE_TYPE = "yolo_each"     # onnx or mmlab or yolo_each or yolo_ocr

