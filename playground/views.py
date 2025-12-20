from django.shortcuts import render
from store.models import Product, Collection


def say_hello(request):
    collection = Collection()
    collection.title = "Video Games"
    collection.featured_product = Product(pk=1)
    collection.save()

    Collection.objects.create(title='a', featured_product_id=2)
    return render(request, 'hello.html', {"name": "Mav"})
