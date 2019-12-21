# FileName: serializers
# Author: Tunny
# @time: 2019-12-21 17:18
# Desc: 
import re
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from mxshopnew.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        自定义校验 mobile 参数
        """
        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码不正确')
        # 验证手机号是否已存在
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('该手机号已注册')
        # 验证发送时间间隔
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError('距离上次发送不到60s')

        return mobile


class UserMobileRegSerializer(serializers.ModelSerializer):
    """
    用户注册Serializer
    """
    # write_only=True 返回到前端序列化的时候就不会序列化这个 code 字段
    code = serializers.CharField(required=True, max_length=4, min_length=4, write_only=True, label='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '验证码不能为空',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误'
                                 })
    # username 校验是否已存在
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')],
                                     label='用户名')
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='密码')

    # def create(self, validated_data):
    #     """
    #     重载 serializer 的 create 方法，将明文的密码加密存入数据库
    #     如果不想在此处重载create方法，也可以通过监听 django 信号量 post_save 的方式修改密码
    #     """
    #     user = super(UserMobileRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        record_code = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if record_code:
            last_record = record_code[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 验证码过期
            if five_minute_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            # 验证码错误
            if code != last_record.code:
                raise serializers.ValidationError('验证码错误')
        else:
            # 验证码错误
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        """
        serializer 最后会调用的校验方法
        """
        # 将用户名赋值给手机号
        attrs['mobile'] = attrs['username']
        # 删除不在 model 中的字段
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ['username', 'code', 'mobile', 'password']
