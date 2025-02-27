from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile_image', 'password']

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)

        if password is not None:
            user.set_password(password)

        user.save()
        return user



# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'role', 'profile_image']
#
#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username'],
#             role=validated_data['role'],
#             profile_image=validated_data.get('profile_image')
#         )
#         user.set_password(validated_data['password'])  # Hash the password
#         user.save()
#         return user
