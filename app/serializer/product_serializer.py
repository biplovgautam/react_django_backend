from rest_framework import serializers
from app.models import Product, Category
from .category_serializer import CategorySerializer
from .image_serializer import ProductImageSerializer
from .feature_serializer import ProductFeatureSerializer


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    features = ProductFeatureSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'is_active', 'categories', 'features', 'images', 'created_at', 'updated_at']