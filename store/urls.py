from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
urlpatterns = router.urls + products_router.urls

# urlpatterns = [
#     path('', include(router.urls)),
#     path('products/', views.ProductList.as_view(), name='products'),
#     path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
#     path('collections/', views.CollectionList.as_view(), name='collections'),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]