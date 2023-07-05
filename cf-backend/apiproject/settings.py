"""
Django settings for apiproject project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from configs.env import *
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-^#%%)5iuad%=hs-0+xvs_wv%7t+py403_@-t-j*!5(ala)fva3"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG

ALLOWED_HOSTS = ALLOWED_HOSTS
# 允许跨域源
CORS_ORIGIN_ALLOW_ALL = CORS_ORIGIN_ALLOW_ALL
# 允许ajax请求携带cookie
CORS_ALLOW_CREDENTIALS = CORS_ALLOW_CREDENTIALS
# XFrameOptionsMiddleware 可以在指定来源的 frame 中展示
X_FRAME_OPTIONS = "ALLOW-FROM"
# 这是设置根路由
ROOT_URLCONF = "apiproject.urls"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'corsheaders',      # 跨域请求
    'django_filters',   # 过滤器
    'captcha',  # 验证码
    'drf_yasg',  # swagger 接口

    # 自定义APP
    "apps.fadmin",
    'apps.figures',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',    # 跨域请求

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",  # 关闭全局CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'apps.fadmin.bases.base_middlewares.ApiLoggingMiddleware',  # 用于记录API访问日志
    'apps.fadmin.bases.base_middlewares.PermissionModeMiddleware',  # 权限中间件
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "apiproject.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DATABASE_TYPE == "MYSQL":
    # Mysql数据库
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": DATABASE_HOST,
            "PORT": DATABASE_PORT,
            "USER": DATABASE_USER,
            "PASSWORD": DATABASE_PASSWORD,
            "NAME": DATABASE_NAME,
        }
    }
else:
    # sqlite3 数据库
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# 是否启用redis
if REDIS_ENABLE:
    REDIS_URL = f'redis://:{REDIS_PASSWORD if REDIS_PASSWORD else ""}@{os.getenv("REDIS_HOST") or REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }
# ================================================= #
# ************** 登录方式配置  ************** #
# ================================================= #
AUTHENTICATION_BACKENDS = (
    'apps.fadmin.system.auth_backends.CustomBackend',
    'apps.fadmin.system.auth_backends.SessionAuthentication',
)
AUTH_USER_MODEL = 'fadmin.User'
# username_field
USERNAME_FIELD = 'username'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
# 配置语言
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True     # 语言环境决定的格式具有更高的优先级，并将被应用
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# 访问静态文件的url地址前缀 根路径下 不加前面斜杠是建立的app下
STATIC_URL = '/static/'
# 生产过程中收集静态文件，必须将 MEDIA_ROOT,STATICFILES_DIRS先注释，否则会覆盖掉 前后分离不需要
# python manage.py collectstatic
# # 设置django的静态文件目录
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'static'
    STATICFILES_DIRS = []
else:
    STATIC_ROOT = ""
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]

# 访问上传文件的url地址前缀
MEDIA_URL = "/media/"
# 项目中存储上传文件的根目录
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT.mkdir(exist_ok=True)


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# TODO 日志配置
# 可以改进 比如说发邮件 参考 https://docs.djangoproject.com/en/4.1/topics/logging/#configuring-logging

# log 配置部分BEGIN #
SERVER_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'server.log')
ERROR_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'error.log')
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))
# 格式:[2020-04-22 23:33:01][micoservice.apps.ready():16] [INFO] 这是一条日志:
# 格式:[日期][模块.函数名称():行号] [级别] 信息
STANDARD_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'
CONSOLE_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {     # 定义几种格式
        'standard': {
            'format': STANDARD_LOG_FORMAT
        },
        'console': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SERVER_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,  # 最多备份5个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 3,  # 最多备份3个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # default日志
        '': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        # 数据库相关日志
        'django.db.backends': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
        },
    }
}
# ================================================= #
# ***** 登录验证码配置 django-simple-captcha   ***** #
# ================================================= #
# 验证码状态 是否开启验证码
CAPTCHA_STATE = CAPTCHA_STATE
# 字母验证码
CAPTCHA_IMAGE_SIZE = (160, 60)  # 设置 captcha 图片大小
CAPTCHA_LENGTH = 4  # 字符个数
CAPTCHA_TIMEOUT = 1  # 超时(minutes)
# 加减乘除验证码
CAPTCHA_OUTPUT_FORMAT = '%(image)s %(text_field)s %(hidden_field)s '
CAPTCHA_FONT_SIZE = 40  # 字体大小
CAPTCHA_FOREGROUND_COLOR = '#0033FF'  # 前景色
CAPTCHA_BACKGROUND_COLOR = '#F5F7F4'  # 背景色
CAPTCHA_NOISE_FUNCTIONS = (
    # 'captcha.helpers.noise_arcs', # 线
    # 'captcha.helpers.noise_dots', # 点
)
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'



# ================================================= #
# ************** REST_FRAMEWORK 配置  ************** #
# ================================================= #
REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",  # 日期时间格式配置
    "DATE_FORMAT": "%Y-%m-%d",
    'DEFAULT_PERMISSION_CLASSES': (
        # "rest_framework.permissions.IsAuthenticated",  # 只有经过身份认证确定用户身份才能访问
        # 'rest_framework.permissions.IsAdminUser', # is_staff=True才能访问 —— 管理员(员工)权限
        'rest_framework.permissions.AllowAny', # 允许所有
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly', # 有身份 或者 只读访问(self.list,self.retrieve)
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'apps.fadmin.utils.jwt_util.RedisOpAuthJwtAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'apps.fadmin.utils.pagination_util.Pagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'EXCEPTION_HANDLER': 'apps.fadmin.utils.exception_util.op_exception_handler',
    # 限流设置
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',

    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/s',
        'user': '10/s'
    }
}

# ================================================= #
# ******************** JWT配置  ******************** #
# ================================================= #
# JWT_AUTH = {
#     'JWT_ALLOW_REFRESH': True,
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60 * 60 * 24),  # JWT有效时间24小时
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',  # JWT的Header认证头以'JWT '开始
#     'JWT_AUTH_COOKIE': 'AUTH_JWT',
#     'JWT_VERIFY_EXPIRATION': True,
#     'JWT_PAYLOAD_HANDLER': 'apps.fadmin.utils.jwt_util.jwt_payload_handler',
#     'JWT_GET_USER_SECRET_KEY': 'apps.fadmin.utils.jwt_util.jwt_get_user_secret_key',
#     'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.fadmin.utils.jwt_util.jwt_response_payload_handler',  # 配置自定义登录成功后的返回信息
# }

SIMPLE_JWT = {
    # token有效时长
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=120),
    # token刷新后的有效时间
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    # 设置前缀
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
}

# ================================================= #
# ******************** 模型加载  ******************** #
# ================================================= #
if INFERENCE_TYPE == "onnx":
    import onnxruntime
    TEXTREC_PATH = MEDIA_ROOT / 'models' / 'RobustScanner' / 'RobustScanner.onnx'
    TEXTREC_SESSION = onnxruntime.InferenceSession(str(TEXTREC_PATH))
    DICT_PATH = MEDIA_ROOT / 'models' / 'RobustScanner' / 'dict_file.txt'
    with open(DICT_PATH, 'r', encoding='utf-8') as f:
        CHAR_LIST = f.read().splitlines()
    DETECT_PATH = MEDIA_ROOT / 'models' / 'yolov8' / 'yolov8.onnx'
    DETECT_SESSION = onnxruntime.InferenceSession(str(DETECT_PATH))
elif INFERENCE_TYPE == "mmlab":
    import warnings
    warnings.filterwarnings('ignore')
    from mmyolo.utils import register_all_modules
    from mmdet.apis import init_detector
    from mmocr.apis import TextRecInferencer
    DETECT_CFG_PATH = MEDIA_ROOT / 'models' / 'mmlab' / 'yolov8_l_syncbn_cf.py'
    DETECT_PTH_PATH = MEDIA_ROOT / 'models' / 'mmlab' / 'yolov8_epoch_300.pth'
    DETECT_SESSION = init_detector(str(DETECT_CFG_PATH), str(DETECT_PTH_PATH), device='cpu')  # or device='cpu'
    TEXTREC_CFG_PATH = MEDIA_ROOT / 'models' / 'mmlab' / 'robustscanner_resnet31_5e_st-sub_mj-sub_sa_real.py'
    TEXTREC_PTH_PATH = MEDIA_ROOT / 'models' / 'mmlab' / 'robustscanner_epoch_5.pth'
    TEXTREC_SESSION = TextRecInferencer(model=str(TEXTREC_CFG_PATH), weights=str(TEXTREC_PTH_PATH), device='cpu')
    register_all_modules()
elif INFERENCE_TYPE == "yolo_ocr":
    from ultralytics import YOLO
    DETECT_PTH_PATH = MEDIA_ROOT / 'models' / 'yolo_ocr' / 'yolov8l_ocr.pt'
    DETECT_SESSION = YOLO(str(DETECT_PTH_PATH), task='ocr')
elif INFERENCE_TYPE == "yolo_each":
    from ultralytics import YOLO
    from apps.figures.recognizers.ultralytics.yolo_ocr.predict_ocr_each import load_text_model
    DETECT_PTH_PATH = MEDIA_ROOT / 'models' / 'yolo_ocr' / 'yolov8l.pt'
    DETECT_SESSION = YOLO(str(DETECT_PTH_PATH), task='detect')
    TEXTREC_PTH_PATH = MEDIA_ROOT / 'models' / 'yolo_ocr' / 'crnn.pth'
    TEXTREC_SESSION = load_text_model(str(TEXTREC_PTH_PATH))