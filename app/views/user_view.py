from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.serializer import CustomUserSerializer
from app.models import CustomUser


@api_view(['POST'])
def register_user(request):
    """
    API view to register a new user.
    """
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        # Instead of using commit=False, directly create the user instance
        user = serializer.create(serializer.validated_data)  # Create user without saving
        user.set_password(request.data['password'])  # Hash the password
        user.save()  # Now save the user

        return Response(
            {
                "message": "User registered successfully.",
                "user": CustomUserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
