# FileName: serializers
# Author: Tunny
# @time: 2019-12-22 19:37
# Desc:
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav
from goods.serializers import GoodsSerializer


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
