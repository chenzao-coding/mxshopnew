from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, UserLeavingMsgSerializer, UserAddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取收藏列表
    retrieve:
        获取收藏的商品详情
    destroy:
        删除收藏
    create:
        收藏商品
    """
    # serializer_class = UserFavSerializer
    # jwt token 正确性验证，因此如果有权限验证，则需要一下两个都配置
    pagination_class = None
    authentication_classes = (JWTAuthentication, SessionAuthentication,)
    # IsAuthenticated 是否登录  IsOwnerOrReadOnly 请求的数据是否是自己的
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    # 设置查询、删除使用的 id 是 goods_id。/userfav/2
    # 这个配置是将获取到的 queryset 再通过 goods_id 进行查询
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return UserFavDetailSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class UserLeavingMsgViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
        list:
            获取留言列表
        retrieve:
            获取留言详情
        destroy:
            删除留言
        create:
            创建留言
        """
    pagination_class = None
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserLeavingMsgSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
        list:
            获取收货地址列表
        retrieve:
            获取收货地址详情
        destroy:
            删除收货地址
        create:
            添加收货地址
        update:
            修改收货地址
        """
    pagination_class = None
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
