from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 're_password')

    # def create(self, validated_data):
    #     first_name = validated_data.pop('first_name', '')
    #     last_name = validated_data.pop('last_name', '')
    #     user = super().create(validated_data)
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.save()
    #     return user

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'avatar')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'avatar')

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'email', 'first_name', 'last_name', 'avatar', 'is_active')

class RegisterSerializer(serializers.ModelSerializer):
    pass
    # password = serializers.CharField(write_only=True, min_length=8)
    #
    # class Meta:
    #     model = CustomUser
    #     fields = ['email', 'username', 'first_name', 'last_name', 'password']
    #
    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         first_name=validated_data.get('first_name', ''),
    #         last_name=validated_data.get('last_name', ''),
    #         password=validated_data['password'],
    #         is_active=False
    #     )
    #     return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()