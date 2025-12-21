from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product, Collection
from store.serializer import ProductSerializer, CollectionSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({"error": "Product cannot be deleted because it's associated with an order item"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, id=pk)
    serializer = CollectionSerializer(collection, many=False)
    return Response(serializer.data)