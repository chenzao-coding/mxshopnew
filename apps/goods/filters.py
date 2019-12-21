# FileName: filters
# Author: Tunny
# @time: 2019-12-21 09:20
# Desc:
from django_filters import rest_framework as filters
from .models import Goods


class GoodsFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    # icontains 包含且忽略大小写
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name']
