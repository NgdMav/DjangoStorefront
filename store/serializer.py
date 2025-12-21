from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count', 'featured_product']

    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product) -> Decimal:
        return product.unit_price * Decimal(1.1)

    def validate(self, data: dict) -> dict:
        return super().validate(data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data: dict) -> Review:
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)