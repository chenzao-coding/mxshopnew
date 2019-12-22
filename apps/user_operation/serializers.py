# FileName: serializers
# Author: Tunny
# @time: 2019-12-22 19:37
# Desc:
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav


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
