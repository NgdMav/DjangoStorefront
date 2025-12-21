from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product

@api_view()
def product_list(request):
    products = Product.objects.all()
    return Response('products')

@api_view()
def product_detail(request, id):
    return Response(id)
