# -*- coding: utf-8 -*-
# FileName: signals
# Author: Tunny
# @time: 2019-12-27 15:40
# Desc:
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserFav


@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        # 新增一个收藏商品记录，则给商品增加一个收藏量
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    # 删除一个收藏商品记录，则给商品减一个收藏量
    goods = instance.goods
    if goods.fav_num > 0:
        goods.fav_num -= 1
    else:
        goods.fav_num = 0
    goods.save()
