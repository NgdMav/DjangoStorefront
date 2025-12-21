from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='products'),
    path('products/<int:id>/', views.product_detail, name='products detail'),
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
]