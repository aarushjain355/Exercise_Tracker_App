from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView2

urlpatterns = [

    path("api/token/", TokenObtainPairView.as_view(), name="token-obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup_view", UserRegistrationView2.as_view(), name="my_api_view"),

]