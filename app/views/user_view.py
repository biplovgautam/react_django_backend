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
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create the user using the validated data
            user = serializer.save()
            
            # Optionally, you can set the password here before saving
            # user.set_password(request.data['password'])  # if password handling needed separately
            user.save()  # Save the user after setting password

            # Return success response with user data (but without the password)
            return Response(
                {
                    "message": "User registered successfully.",
                    "user": CustomUserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
