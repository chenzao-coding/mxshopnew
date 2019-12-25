# -*- coding: utf-8 -*-
# FileName: serializers
# Author: Tunny
# @time: 2019-12-25 16:38
# Desc:
from rest_framework import serializers

from .models import ShoppingCart
from goods.models import Goods
from goods.serializers import GoodsSerializer


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, label='数量', error_messages={
        'require': '请选择购买数量',
        'min_value': '商品数量不能少于一',
    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all(), label='商品')

    def create(self, validated_data):
        user = self.context['request'].user
        goods = validated_data['goods']
        nums = validated_data['nums']
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # BaseSerializer 中有个 update 方法，直接返回错误
        # 由于 Serializer 继承自 BaseSerializer，并且没有重写 update 方法，因此直接使用更新操作同样会报错，因此需要自己重写 update 方法
        # ModelSerializer 中已经重写了 update 方法，因此就不用自己重写 update 方法了
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = ShoppingCart
        fields = '__all__'
