from django.shortcuts import render
from store.models import Product, Collection


def say_hello(request):
    return render(request, 'hello.html', {"name": "Mav"})
