from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from ..models import AbstractUser, User
from ...entities.models import GENDER


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CodeSerializer(EmailSerializer):
    code = serializers.IntegerField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)

    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class EmailPasswordSerializer(PasswordSerializer):
    email = serializers.EmailField()


class RegisterSerializerEmail(EmailPasswordSerializer):
    name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=11)
    birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER)

    def create(self, validated_data):
        user = AbstractUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            phone=validated_data['phone'],
        )
        User.objects.create(
            user=user,
            birth=validated_data['birth'],
            gender=validated_data['gender'],
        )
        return user


class LoginSerializer(EmailSerializer):
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # The authenticate call simply returns None for is_active=False users
            user = authenticate(
                request=self.context.get('request'), username=email, password=password
            )
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(PasswordSerializer):
    old = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if not self.instance:
            msg = 'Cannot find user.'
            raise serializers.ValidationError(msg, code='authorization')

        email = self.instance.email
        old = attrs.get('old')
        if old:
            # The authenticate call simply returns None for is_active=False users
            user = authenticate(
                request=self.context.get('request'), username=email, password=old
            )
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "old".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EditAccountSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=11)
    birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.phone = validated_data['phone']
        instance.save()
        user = instance.user
        user.birth = validated_data['birth']
        user.gender = validated_data['gender']
        user.save()
        return instance

    def validate(self, attrs):
        if not self.instance:
            msg = 'Cannot find user.'
            raise serializers.ValidationError(msg, code='authorization')

        email = self.instance.email
        password = attrs.get('password')
        if password:
            # The authenticate call simply returns None for is_active=False users
            user = authenticate(
                request=self.context.get('request'), username=email, password=password
            )
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['photo']


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    email = serializers.SerializerMethodField('get_email')
    phone = serializers.SerializerMethodField('get_phone')

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email

    def get_phone(self, obj):
        return obj.user.phone

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'gender', 'birth']
