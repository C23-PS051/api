from django.urls import path
from .views import (
    RecommendationAPIView
)

urlpatterns = [
    path('recommend', RecommendationAPIView.as_view()),
]