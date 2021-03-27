from rest_framework import serializers
from ..models import AbstractUser, UnverifiedUser


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnverifiedUser
        fields = ['email']


class UnverifiedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnverifiedUser
        fields = ['email', 'code']


class AbstractUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = ('id', 'email', 'name', 'phone')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = ('id', 'email', 'password', 'name', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = AbstractUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            phone=validated_data['phone'],
        )
        return user
