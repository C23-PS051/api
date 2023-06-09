from django.urls import include, re_path
from django.urls import path, include
from .views import (
    FavoriteListAPIView
)

urlpatterns = [
    path('', FavoriteListAPIView.as_view()),
]