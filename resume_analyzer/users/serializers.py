from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UidAndTokenSerializer, PasswordSerializer
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'role', 'email_verified')
        ref_name = 'CustomUserSerializer'


class RegisterSerializer(BaseUserCreateSerializer):
    password = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'role')

    def create(self, validated_data):
        return super().create(validated_data)


class PasswordResetConfirmSerializer(UidAndTokenSerializer, PasswordSerializer):
    class Meta:
        fields = ['uid', 'token', 'new_password']

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['username', 'password']

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            logger.warning(f"Failed login attempt for username: {data['username']}")
            raise serializers.ValidationError('Invalid credentials')
        return user
