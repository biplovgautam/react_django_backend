from rest_framework import serializers
from app.models import CustomUser, Category, Product, ProductImage, Order, OrderItem

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'phone_number',
            'username',
            'password',  # Make sure password is included for the user creation
        ]
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is not returned in responses

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Get password and remove it from validated_data
        user = CustomUser.objects.create(**validated_data)  # Create user without password initially

        if password:
            user.set_password(password)  # Hash the password
            user.save()  # Save the user with hashed password
        
        return user

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text"]

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "is_active",
            "category",
            "created_at",
            "updated_at",
            "image",
            "images",
        ]
