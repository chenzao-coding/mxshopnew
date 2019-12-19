# -*- coding: utf-8 -*-
# FileName: adminx
# Author: Tunny
# @time: 2019-10-15 11:02
# Desc:
from goods.models import Goods, GoodsCategory, GoodsCategoryBrand, Banner, HotSearchWords, IndexAd, GoodsImage

import xadmin
from import_export import resources


class GoodsAdmin(object):
    class GoodsResource(resources.ModelResource):
        class Meta:
            model = Goods
    import_export_args = {'import_resource_class': GoodsResource, 'export_resource_class': GoodsResource}

    list_display = ["name", 'show_image', "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                    "shop_price", "goods_brief", "is_new", "is_hot", "add_time"]
    search_fields = ['name', ]
    list_editable = ["is_hot", ]
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time", "category__name"]
    style_fields = {"goods_desc": "ueditor"}

    class GoodsImageInline(object):
        model = GoodsImage
        exclude = ['add_time']
        extra = 1
        style = 'tab'

    inlines = [GoodsImageInline]


class GoodsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class GoodsBrandAdmin(object):
    list_display = ["category", "image", "name", "desc"]


class BannerGoodsAdmin(object):
    list_display = ["goods", "image", "index"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)
xadmin.site.register(Banner, BannerGoodsAdmin)
xadmin.site.register(HotSearchWords, HotSearchAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)
