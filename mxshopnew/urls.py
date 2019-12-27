"""mxshopnew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from mxshopnew.settings import MEDIA_ROOT
import xadmin
from goods.views import GoodsListViewSet, GoodsCategoryViewSet, BannerGoodsViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, UserLeavingMsgViewSet, UserAddressViewSet
from trade.views import ShoppingCartViewSet, OrderInfoViewSet, AliPayView
# from goods.views_base import GoodsListView
# from goods.views import GoodsListView2

router = DefaultRouter()
# 注册商品 router
# AssertionError: basename argument not specified, and could not automatical
# 如果 views 中没有定义 queryset 字段时，在路由注册的时候必须加上 basename
router.register(r'goods', GoodsListViewSet, basename='goods')
router.register(r'categories', GoodsCategoryViewSet)
router.register(r'code', SmsCodeViewSet, basename='code')
router.register(r'users', UserViewSet, basename='user')
router.register(r'userfavs', UserFavViewSet, basename='userfav')
router.register(r'messages', UserLeavingMsgViewSet, basename='messages')
router.register(r'address', UserAddressViewSet, basename='address')
router.register(r'shopcarts', ShoppingCartViewSet, basename='shopcarts')
router.register(r'orders', OrderInfoViewSet, basename='orders')
router.register(r'banners', BannerGoodsViewSet, basename='banners')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # coreapi 文档功能
    url(r'docs/', include_docs_urls(title='学习文档')),
    # 调试 api 的登录 url
    url(r'^api-auth/', include('rest_framework.urls')),
    # 使用 router 来配置 各模块 url
    url(r'^', include(router.urls)),

    # JWT 认证
    # 由于这里的登录默认是使用 username 来登录的，如果需要手机号也能登录需要自定义
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),

    # Alipay 回调和return_url 接口
    url(r'^alipay/return/', AliPayView.as_view(), name='alipay'),

    url(r'^index/', TemplateView.as_view(template_name='index.html'))

    # DRF token 认证
    # url(r'^api-token-auth/', views.obtain_auth_token),
    # 商品列表页
    # url(r'goods/$', GoodsListView2.as_view(), name='goods-list'),
]
