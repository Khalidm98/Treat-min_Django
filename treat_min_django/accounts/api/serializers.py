from rest_framework import serializers
from ..models import PendingUser, AbstractUser, User
from ...entities.models import GENDER


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingUser
        fields = ['email']


class PendingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingUser
        fields = ['email', 'code']


class AbstractUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = ['id', 'email', 'name', 'phone']


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=11)
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER)
    photo = serializers.ImageField(default=None)

    def create(self, validated_data):
        user = AbstractUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            phone=validated_data['phone'],
        )
        User.objects.create(
            user=user,
            date_of_birth=validated_data['date_of_birth'],
            gender=validated_data['gender'],
            photo=validated_data['photo'],
        )
        return user

    def update(self, instance, validated_data):
        super(RegisterSerializer, self).update(instance, validated_data)
