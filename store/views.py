from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product, Collection
from store.serializer import ProductSerializer, CollectionSerializer


@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(
        queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    # try:
    #     product = Product.objects.get(id=id)
    #     serializer = ProductSerializer(product, many=False)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, id=pk)
    serializer = CollectionSerializer(collection, many=False)
    return Response(serializer.data)