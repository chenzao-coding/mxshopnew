from datetime import datetime
from django.shortcuts import redirect
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.alipay import AliPay
from rest_framework.response import Response
from mxshopnew.settings import ALI_APP_ID, ALI_NOTIFY_URL, PRIVATE_KEY_PATH, ALI_PUB_KEY_PATH, ALI_Test_DEBUG, ALI_RETURN_URL

from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, OrderInfoDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 设置 goods_id 做为查询详情，删除、修改时匹配的id
    lookup_field = 'goods_id'

    def perform_create(self, serializer):
        # 新增一个商品到购物车，商品库存数就相应减少
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        # 删除购物车商品的时候，商品库存数相应增加
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        # 修改购物车数量的时候，商品库存数相应修改
        # 1. 获取修改前数据库中的值
        existed_record = ShoppingCart.objects.get(id=serializer.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        goods = saved_record.goods
        goods.goods_num -= (saved_record.nums - existed_nums)
        goods.save()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderInfoViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoDetailSerializer
        return OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        # 将购物车中的所有商品全部加入到订单
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.save()
            # 删除购物车数据
            shop_cart.delete()
        return order


class AliPayView(APIView):
    def get(self, request):
        """
        处理支付宝的 return_url 返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)
        alipay = AliPay(
            appid=ALI_APP_ID,
            app_notify_url=ALI_NOTIFY_URL,
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALI_PUB_KEY_PATH,
            debug=ALI_Test_DEBUG,
            return_url=ALI_RETURN_URL
        )
        # 校验返回的数据
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            # 成功返回跳转到 template 的 orderlist 页面
            # 用户通过支付宝支付链接页面扫码成功后，跳转到127.0.0.1:8000的orderlist页面
            # 因为是前后端分离项目，return_url填写的是 django 的接口，因此，vue页面使用 支付宝支付链接，成功支付后，无法跳转到 vue 的 orderlist 页面
            # 有3种方法解决：1. 生成订单后不返回支付宝的支付链接，而是通过支付宝的接口参数 qr_pay_mode，返回支付的二维码图片，vue加载图片，并调用 django 接口不停的监听订单状态，来进行跳转控制
            # 2. vue 使用 npm run build 将 dev 的单页面文件放到django中，使用template 方式来进行跳转到orderlist页面
            # 3. 扫码支付后不监听状态，也不跳转回orderlist，用户自己进入orderlist刷新状态
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=3)
            return response
        else:
            # 失败跳转到 template 首页
            response = redirect('index')
            return response

    def post(self, request):
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)
        alipay = AliPay(
            appid=ALI_APP_ID,
            app_notify_url=ALI_NOTIFY_URL,
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALI_PUB_KEY_PATH,
            debug=ALI_Test_DEBUG,
            return_url=ALI_RETURN_URL
        )
        # 校验返回的数据
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 更新商品的卖出数量
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()
                # 更新 order 状态
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            # 给支付宝返回成功，如果不返回支付宝会不停的给接口发送数据
            # 如果 校验返回的数据 和 sign 不匹配，则不处理。
            return Response('success')
