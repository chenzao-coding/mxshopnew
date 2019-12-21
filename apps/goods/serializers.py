# FileName: serializers
# Author: Tunny
# @time: 2019-12-20 21:04
# Desc: 
from rest_framework import serializers
from .models import Goods, GoodsCategory


class GoodsSerializer2(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    click_num = serializers.IntegerField(default=0)

    def create(self, validated_data):
        """
        可以根据前端传递过来的数据，先通过 serializer 进行校验，然后执行 create 方法存储数据库
        :param validated_data:
        :return:
        """
        return Goods.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    # serializer 的嵌套
    category = CategorySerializer()

    class Meta:
        model = Goods
        # fields = ['name', 'click_num', 'market_price', 'add_time']
        fields = '__all__'



