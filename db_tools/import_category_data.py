# FileName: import_category_data
# Author: Tunny
# @time: 2019-12-19 21:17
# Desc: 独立使用 Django model
import sys
import os


# 获取当前脚本所在的目录
pwd = os.path.dirname(os.path.realpath(__file__))
# 将项目的根目录加入到 python 的根搜索路径下，即设置根目录为项目目录
sys.path.append(pwd + '../')
# 设置django model的环境变量，可以直接从 manage.py 中复制过来
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mxshopnew.settings')

# 初始化 django 后，就可以直接来使用 model 了
import django
django.setup()

from goods.models import GoodsCategory
from db_tools.data.category_data import row_data


for lev1_cat in row_data:
    lev1_instance = GoodsCategory()
    lev1_instance.code = lev1_cat['code']
    lev1_instance.name = lev1_cat['name']
    lev1_instance.category_type = 1
    lev1_instance.save()

    for lev2_cat in lev1_cat['sub_categorys']:
        lev2_instance = GoodsCategory()
        lev2_instance.code = lev2_cat['code']
        lev2_instance.name = lev2_cat['name']
        lev2_instance.category_type = 2
        lev2_instance.parent_category = lev1_instance
        lev2_instance.save()

        for lev3_cat in lev1_cat['sub_categorys']:
            lev3_instance = GoodsCategory()
            lev3_instance.code = lev3_cat['code']
            lev3_instance.name = lev3_cat['name']
            lev3_instance.category_type = 3
            lev3_instance.parent_category = lev2_instance
            lev3_instance.save()



