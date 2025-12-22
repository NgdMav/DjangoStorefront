from django.db.models import Count, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter

from store.filters import ProductFilter
from store.models import Product, Collection, OrderItem, Review, Cart, CartItem
from store.pagination import DefaultPagination
from store.serializer import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, \
    CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'unit_price', 'inventory']

    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs) -> Response:
        if OrderItem.objects.filter(product_id=kwargs.get('pk')).count() > 0:
            return Response({"error": "Product cannot be deleted because it's associated with an order item"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def delete(self, *args, **kwargs):
#         product = get_object_or_404(Product, id=kwargs.get('pk'))
#         if product.order_items.count() > 0:
#             return Response({"error": "Product cannot be deleted because it's associated with an order item"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['id', 'title', 'products_count']

    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs) -> Response:
        if Product.objects.filter(collection_id=kwargs.get('pk')).count() > 0:
            return Response({"error": "Collection cannot be deleted because it's associated with an product"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#
#     def delete(self, *args, **kwargs):
#         collection = get_object_or_404(Collection, id=kwargs.get('pk'))
#         if collection.products.count() > 0:
#             return Response({"error": "Collection cannot be deleted because it's associated with a product"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name', 'date']

    pagination_class = DefaultPagination

    def get_queryset(self) -> QuerySet:
        return Review.objects.filter(product_id=self.kwargs['product_pk']).all()

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}

class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    # This is if you want user to not delete a cart with items
    # def destroy(self, request, *args, **kwargs) -> Response:
    #     if CartItem.objects.filter(cart_id=kwargs.get('pk')).count() > 0:
    #         return Response({"error": "Cart cannot be deleted because it's associated with a cart item"},
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     return super().destroy(request, *args, **kwargs)

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self) -> QuerySet:
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk']).all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk')}
