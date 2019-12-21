from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ('male', '男'),
    ('female', '女')
)


class BaseModel(models.Model):
    """
    抽象基类
    """
    # 此处如果使用 datetime.now() 时间统一会为编译时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    index = models.IntegerField(default=0, verbose_name='排序', help_text='排序')

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    """
    用户
    """
    # 因为用户注册的时候，没有机会填写 name 所以此处可以为 null
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月日')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female', verbose_name='性别')
    email = models.EmailField(max_length=50, null=True, blank=True, verbose_name='邮箱')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            return self.name
        return self.username


class VerifyCode(BaseModel):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
