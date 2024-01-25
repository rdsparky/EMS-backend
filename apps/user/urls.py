from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "user"

router = DefaultRouter()
router.register(r"", views.UserViewSet, basename="user")

urlpatterns = [
    path("login/", views.LoginApiView.as_view(), name="user-login"),
    path("signup/", views.SignupAPIView.as_view(), name="user-signup"),
    path("logout/", views.LogoutAPIView.as_view(), name="user-logout"),
    path("", include(router.urls)),  # Include the router-generated URLs
]
