
from django.urls import path
from app.views import register_user

urlpatterns = [
    path('register/', register_user, name='register_user'),
]
