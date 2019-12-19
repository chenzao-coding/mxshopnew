from django.db import models

from users.models import BaseModel

from DjangoUeditor.models import UEditorField
# Create your models here.


class GoodsCategory(BaseModel):
    """
    商品多级分类, 一张表完成多级别的分类
    """
    CATEGORY_TYPE = (
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目'),
    )

    name = models.CharField(max_length=30, default='', verbose_name='类别名', help_text='类别名')
    code = models.CharField(max_length=30, default='', verbose_name='类别code', help_text='类别code')
    desc = models.TextField(max_length=300, default='', verbose_name='类别描述', help_text='类别描述')
    # 设置目录树级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别', help_text='类目级别')
    # 使用 self 设置指向自己的外键
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name='父类目', help_text='父类目', related_name='sub_cat')
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(BaseModel):
    """
    某一大类下的宣传商标
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='商品类目', help_text='商品类目', related_name='brands')
    name = models.CharField(max_length=30, default='', verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(max_length=300, default='', verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(max_length=200, upload_to='brands/', verbose_name='品牌图片', help_text='品牌图片')

    class Meta:
        verbose_name = '宣传品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品类别', help_text='商品类别')
    goods_sn = models.CharField(max_length=50, default='', verbose_name='商品唯一货号', help_text='商品唯一货号')
    name = models.CharField(max_length=100, verbose_name='商品名', help_text='商品名')
    click_num = models.IntegerField(default=0, verbose_name='点击数', help_text='点击数')
    sold_num = models.IntegerField(default=0, verbose_name='商品销量')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    goods_num = models.IntegerField(default=0, verbose_name='库存数')
    market_price = models.FloatField(default=0, verbose_name='市场价格')
    shop_price = models.FloatField(default=0, verbose_name='本店价格')
    goods_brief = models.TextField(max_length=500, verbose_name='商品简短描述')
    goods_desc = UEditorField(default='', width=600, height=300, imagePath='goods/images/',
                              filePath='goods/files/', verbose_name='商品详情')
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    # 首页中展示的商品封面图
    goods_front_image = models.ImageField(max_length=300, upload_to='goods/images/', null=True, blank=True,
                                          verbose_name='封面图')
    # 是否首页新品展示
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热卖')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def show_image(self):
        # 在 model 中定义方法，将图片显示在后台
        from django.utils.safestring import mark_safe
        return mark_safe("<img width='120px' height='90px' src='{}'>".format(self.goods_front_image.url))
    show_image.short_description = '封面图'


class GoodsImage(BaseModel):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品', related_name='images')
    image = models.ImageField(max_length=300, upload_to='goods/images/', null=True, blank=True, verbose_name='图片')

    class Meta:
        verbose_name = '商品轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(BaseModel):
    """
    首页轮播的商品图，为适配首页大图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(max_length=300, upload_to='banner/', null=True, blank=True, verbose_name='图片')

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
