from django.db import models
from django.contrib.auth import get_user_model

from users.models import BaseModel
from goods.models import Goods


User = get_user_model()


class UserFav(BaseModel):
    """
    用户收藏操作
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        # 多个字段作为一个联合唯一索引
        unique_together = ('user', 'goods')

    def __str__(self):
        return self.user.name


class UserAddress(BaseModel):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    province = models.CharField(max_length=100, default='', verbose_name='省份')
    city = models.CharField(max_length=100, default='', verbose_name='城市')
    district = models.CharField(max_length=100, default='', verbose_name='区域')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=100, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, verbose_name='联系方式')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class UserLeavingMessage(BaseModel):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name='留言类型',
                                       help_text='留言类型：1(留言),2(投诉),3(询问),4(售后),5(求购)')
    subject = models.CharField(max_length=100, default='', verbose_name='主题', help_text='主题')
    message = models.TextField(max_length=300, default='', verbose_name='留言内容')
    file = models.FileField(max_length=200, upload_to='message/images/', verbose_name='上传的文件', help_text='上传的文件')

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject
