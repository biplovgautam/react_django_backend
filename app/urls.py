from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, register_user

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('', include(router.urls)),
]