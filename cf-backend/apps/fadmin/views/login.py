import datetime
import logging
from uuid import uuid4

from captcha.models import CaptchaStore
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler


from rest_framework_simplejwt.views import TokenObtainPairView

from apps.fadmin.serializers.user_serializers import LoginSerializer
from apps.fadmin.models import LoginInfo
from apps.fadmin.utils.request_util import save_login_log

from apps.fadmin.utils.jwt_util import jwt_get_session_id
from apps.fadmin.utils.request_util import get_request_ip, get_os, get_browser, get_login_location

from apps.fadmin.utils.exception_util import GenException
from apps.fadmin.utils.response_util import SuccessResponse, ErrorResponse

logger = logging.getLogger(__name__)

User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('access')
            session_id = jwt_get_session_id(token)
            save_login_log(request, '登录成功', session_id=session_id)
            return SuccessResponse(serializer.validated_data)
        # save_login_log(request, '登录失败，账户/密码不正确', False)  # 登录失败不记录先
        return ErrorResponse(data=serializer.errors, msg='账户/密码不正确', status=401)


# class RegisterView(ObtainJSONWebToken):
#     serializer_class = UserCreateUpdateSerializer
#
#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response = SuccessResponse(serializer.data)
#             return response
#         else:
#             print("error", serializer.errors)
#         return ErrorResponse(data=serializer.errors, msg='注册失败', code=422)
#
#     def handle_exception(self, exc):
#         print(exc)
#         return ErrorResponse(data=None, msg=exc.message)
class RegisterView():
    pass


class LogoutView(APIView):
    pass    # TODO 登出模块
#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated,)
#     prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX', 'JWT')
#
#     def post(self, request):
#         user = request.user
#         user.user_secret = uuid4()
#         user.save()
#         key = f"{self.prefix}_{user.username}"
#         if getattr(settings, "REDIS_ENABLE", False):
#             cache.delete(key)
#         return SuccessResponse()