from rest_framework import serializers
from app.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'phone_number',
            'username',
            'first_name',
            'last_name',
            'password',  # Make sure password is included for the user creation
        ]
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': True},  # Make first_name required
            'last_name': {'required': True}}  # Ensure password is not returned in responses

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Get password and remove it from validated_data
        user = CustomUser.objects.create(**validated_data)  # Create user without password initially

        if password:
            user.set_password(password)  # Hash the password
            user.save()  # Save the user with hashed password
        
        return user
