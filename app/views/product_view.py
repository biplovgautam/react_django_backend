from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from app.models import Product, Category
from app.serializer import ProductSerializer, CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_slug>[^/.]+)')
    def by_category(self, request, category_slug=None):
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(categories=category)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='featured')
    def featured(self, request):
        products = Product.objects.filter(is_active=True)[:3]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='details')
    def details(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)