from django.urls import path
from .views import (
    TestAuthenticatedAPIView
)

urlpatterns = [
    path('', TestAuthenticatedAPIView.as_view()),
]