from rest_framework import serializers
from app.models import ProductImage
import base64

class ProductImageSerializer(serializers.ModelSerializer):
    image_file = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'alt_text', 'image_file']

    def get_image_file(self, obj):
        if obj.image:
            return base64.b64encode(obj.image).decode('utf-8')
        return None