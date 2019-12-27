from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import filters
# from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, CategorySerializer, BannerGoodsSerializer, IndexCategorySerializer
from .filters import GoodsFilter


# 使用最基础的 APIView 实现商品列表数据返回
class GoodsListView3(APIView):
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)

    def post(self, request):
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            # save 会调用 serializer 中的 create 方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodsResultsSetPagination(PageNumberPagination):
    """
    自定义分页参数
    """
    page_size = 12
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 20


class GoodsListView22(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsResultsSetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoodsListView2(generics.ListAPIView):
    # 分页时必须要设置 order_by 否则会出现该警告 Pagination may yield inconsistent results with an unordered object_list
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsResultsSetPagination


"""
GenericViewSet 包含了 generics.GenericAPIView 和 ViewSetMixin
ViewSetMixin：重写了 as_view 方法，让注册 url 变得更加简单；定义了 initialize_request 方法，让动态的设置 serializer 更加的好用
所以 缺少 list create等方法与get post 请求的绑定 因此 GenericViewSet 需要配合 mixins 来使用，并且 viewsets 需要配置 router 来使用
在url中配置，将 get post 请求 与 list create 方法相互绑定
goods_list = GoodsListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

使用 router 更加方便
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)

path('', include(router.urls)),


"""
class GoodsListViewSet22(mixins.ListModelMixin, viewsets.GenericViewSet):
    # queryset = Goods.objects.all().order_by('add_time')
    serializer_class = GoodsSerializer
    pagination_class = GoodsResultsSetPagination

    # 一般的过滤方法
    def get_queryset(self):
        # 此处的 .all() 并不会直接取出所有的数据，而是先拼凑出 sql 语句，在执行for循环的时候才真正的操作数据库
        queryset = Goods.objects.all()
        price_min = self.request.query_params.get('price_min', 0)
        if price_min:
            queryset = queryset.filter(shop_price__gt=int(price_min)).order_by('add_time')
        return queryset


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all().order_by('add_time')
    serializer_class = GoodsSerializer
    pagination_class = GoodsResultsSetPagination
    # DjangoFilterBackend 过滤，使用的是 django-filter
    # filters.SearchFilter 搜索，使用的是 DjangoRestFramework
    # filters.OrderingFilter 排序，使用的是 DjangoRestFramework
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GoodsFilter
    # 支持：^ 表示必须以xx开始；= 表示完全相等；@ 表示全文搜索；$ 表示正则表达式搜索
    search_fields = ['name', 'goods_brief', 'goods_desc']
    ordering_fields = ['sold_num', 'shop_price']


class GoodsCategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取商品列表
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
    pagination_class = None
    # authentication_classes = (TokenAuthentication, )


class BannerGoodsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerGoodsSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    pagination_class = None
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer
