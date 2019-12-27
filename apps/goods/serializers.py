# FileName: serializers
# Author: Tunny
# @time: 2019-12-20 21:04
# Desc:
from django.db.models import Q
from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd


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


class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'

class IndexCategorySerializer(serializers.ModelSerializer):
    brands = GoodsCategoryBrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_instance = ad_goods[0].goods
            # 在Serializer中调用 Serializer时，被调用的Serializer中的图片是不会默认加上域名前缀的，需要手动配置上下文加上request
            # django 中的 image 在 serializer 会被默认加上域名前缀原因：image 字段在做序列化的时候，会判断上下文中是否含有request，如果有，则将request的域名拼接到image前
            goods_json = GoodsSerializer(goods_instance, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True)
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'
