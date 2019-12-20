# -*- coding: utf-8 -*-
# FileName: views_base
# Author: Tunny
# @time: 2019-12-20 16:01
# Desc: 使用 Django 的方式来完成数据的返回，对比以后使用的 DjangoRestFramework
# django cbv 方式里最常用的 view
from django.views.generic.base import View
from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:10]
# 第一种方法
        # for good in goods:
        #     json_dict = {"name": good.name, "category": good.category.name, "market_price": good.market_price}
        #     json_dict.update({"name2": "123"})
        #     # 如果此处直接序列化 time 会报序列化异常错误，djangorestframework 会帮我们处理这些问题
        #     # json_dict.update({"add_time": good.add_time})
        #     json_list.append(json_dict)
# 第二种方法
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     # 但是使用这个方法还是会存在 datetime imagefield 序列化出错问题，django为我们提供了
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
# 第三种方法
        from django.core import serializers
        json_data = serializers.serialize('json', goods)

        from django.http import HttpResponse, JsonResponse
        import json
        # return HttpResponse(json.dumps(json_list), content_type='application/json')
        # return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(json.loads(json_data), safe=False)
