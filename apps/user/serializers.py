from rest_framework import serializers, status
from apps.user import models as user_models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "city",
            "state",
            "is_verified",
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user or self.context["request"].user
        user_serializer = UserListSerializer(user)
        response = {
            "user": user_serializer.data,
        }
        response["user"]["token"] = data
        return response
