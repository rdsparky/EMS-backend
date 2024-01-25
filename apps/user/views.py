from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from apps.user.filters import UserFilter
from common.renderers import ApiRenderer
from common.constants import ApplicationMessages
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import views, status, viewsets, permissions, filters
from apps.user import serializers
from apps.user import models as user_models
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

# Create your views here.


class SignupAPIView(CreateAPIView):
    serializer_class = serializers.UserListSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Encrypt the password using make_password before saving it
        request.data["password"] = make_password(request.data["password"])

        # Use the modified request data to create the user
        response = super().create(request, *args, **kwargs)

        # Generating JWT tokens
        user = self.serializer_class.Meta.model.objects.get(
            email=request.data["email"].lower(),
        )
        refresh = RefreshToken.for_user(user)
        refresh.set_exp(lifetime=timedelta(minutes=10))

        response.data.update(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
        )

        return response


class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Call the save method to get the response
            response = serializer.validated_data

            user_data = response

            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle the exception for invalid credentials
            error_data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": ApplicationMessages.INVALID_PASSWORD,
                "error": True,
                "data": {},
            }
            return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(views.APIView):
    """
    Logout  api view
    """

    permission_classes = [permissions.IsAuthenticated]
    user_model = user_models.User

    def delete(self, request, *args, **kwargs):
        """
        Delete session
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            user = self.user_model.objects.get(id=request.user.id)
            qs = OutstandingToken.objects.filter(user=user)
            if qs.exists():
                qs.delete()
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": ApplicationMessages.LOGOUT_SUCCESSFULLY,
                        "error": False,
                        "data": {},
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Handle the case where qs is empty
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": ApplicationMessages.LOGOUT_FAILED_NO_TOKEN,
                        "error": True,
                        "data": {},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except self.user_model.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": ApplicationMessages.LOGOUT_FAILED,
                    "error": True,
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserViewSet(viewsets.ModelViewSet):
    renderer_classes = [ApiRenderer]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    filterset_class = UserFilter
    filterset_fields = [
        "id",
        "email",
    ]  # Define the fields available for filtering

    # Define fields available for filtering and ordering
    ordering_fields = [
        "first_name",
        "last_name",
        "email",
    ]
    search_fields = [
        "id",
        "first_name",
        "last_name",
    ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(is_active=True)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, pk=None):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
