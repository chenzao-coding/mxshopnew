# -*- coding: utf-8 -*-
# FileName: serializers
# Author: Tunny
# @time: 2019-12-25 16:38
# Desc:
from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods
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


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_sn = serializers.CharField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    index = serializers.IntegerField(read_only=True)

    def generate_order_sn(self):
        # 生成订单号 时间+userid+随机数
        import time
        import random
        order_sn = '{time_str}{user_id}{random_str}'.format(time_str=time.strftime('%Y%m%d%H%M%S'), user_id=self.context['request'].user.id, random_str=random.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    # 根据 OrderGoods 的属性 goods 查出商品详情
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    # 使用 OrderGoods 的外键 order 反向查出有所有商品
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'
