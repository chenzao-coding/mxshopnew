from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 设置 goods_id 做为查询详情，删除、修改时匹配的id
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
