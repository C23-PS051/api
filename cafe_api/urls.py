from django.urls import include, re_path
from django.urls import path, include
from .views import (
    CafeListAPIView
)

urlpatterns = [
    path('', CafeListAPIView.as_view()),
    path('<str:cafe_id>', CafeListAPIView.as_view()),
]