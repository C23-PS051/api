from django.urls import include, re_path
from django.urls import path, include
from .views import (
    UserListAPIView
)

urlpatterns = [
    path('<str:user_id>', UserListAPIView().as_view()),
]