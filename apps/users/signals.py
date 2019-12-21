# FileName: signals
# Author: Tunny
# @time: 2019-12-21 21:35
# Desc: 使用信号量机制，监听 django 数据库操作 的信号量
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
