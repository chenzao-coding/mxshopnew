# FileName: serializers
# Author: Tunny
# @time: 2019-12-22 19:37
# Desc:
import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer

from mxshopnew.settings import REGEX_MOBILE


class UserFavSerializer(serializers.ModelSerializer):
    # user 只能是当前登录用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        # user goods 两个字段联合唯一
        validators = [
            UniqueTogetherValidator(queryset=UserFav.objects.all(), fields=['user', 'goods'], message='已经收藏过了')
        ]
        fields = ['user', 'goods', 'id']


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ['goods', 'id']


class UserLeavingMsgSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # read_only 表示只返回，不提交
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLeavingMessage
        fields = ['id', 'user', 'message_type', 'subject', 'message', 'file', 'add_time']


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_signer_mobile(self, mobile):
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码不合法')
        return mobile

    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile']
