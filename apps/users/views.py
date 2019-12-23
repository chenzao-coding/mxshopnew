# 自定义登录拦截，使手机号也可以登录
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import VerifyCode
from .serializers import SmsSerializer, UserMobileRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from utils.random_str import generate_random
from mxshopnew.settings import YUNPIAN_APIKEY


User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        # 发送短信
        yun_pian = YunPian(YUNPIAN_APIKEY)
        code = generate_random(4, 0)
        sms_stauts = yun_pian.send_sms(code=code, mobile=mobile)
        if sms_stauts['code'] != 0:
            # 保存到数据库
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": sms_stauts['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 保存到数据库
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserMobileRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTTokenUserAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    # 重载 get_serializer_class 动态配置各个action的序列化类
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserMobileRegSerializer
        return UserDetailSerializer

    # 重载 get_permissions 动态配置各个状态的权限
    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]

    # 注册完成，默认登录，重载 create 函数
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # 生成 token
        re_dict = self.get_tokens_for_user(user)
        re_dict['username'] = user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重载 perform_create 函数，因为原函数没有返回值，因此重载使其返回 user
    # serializer.save() 返回 user
    def perform_create(self, serializer):
        return serializer.save()

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

