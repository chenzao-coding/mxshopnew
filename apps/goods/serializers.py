# FileName: serializers
# Author: Tunny
# @time: 2019-12-20 21:04
# Desc: 
from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage, Banner


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


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ['image']


class GoodsSerializer(serializers.ModelSerializer):
    # serializer 的嵌套
    category = CategorySerializer()
    images = GoodsImagesSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ['name', 'click_num', 'market_price', 'add_time']
        fields = '__all__'


class BannerGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
