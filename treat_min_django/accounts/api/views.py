from random import randint

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSerializer, PendingUserSerializer, AbstractUserSerializer, RegisterSerializer
from ..models import AbstractUser, PendingUser


class SendEmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = AbstractUser.objects.filter(email__iexact=email)
        if user.exists():
            return Response(
                {
                    "details": "This email address is already registered"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        code = randint(999, 9999)
        send_mail(
            'User Email Verification',
            'Please type this code to verify your email:\n{0}'.format(code),
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        user = PendingUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            user.code = code
            user.save()
        else:
            PendingUser.objects.create(email=email, code=code)

        return Response(
            {
                "details": "Verification email was sent successfully"
            },
            status=status.HTTP_200_OK
        )


class VerifyEmailView(APIView):
    serializer_class = PendingUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        user = PendingUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if str(user.code) == code:
                user.is_verified = True
                user.save()
                return Response(
                    {
                        "details": "Email was verified successfully"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "details": "Wrong code"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    "details": "This email address was not registered before"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        user = PendingUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if user.is_verified:
                user.delete()
                user = serializer.save()
                return Response(
                    {
                        "user": AbstractUserSerializer(user, context=self.get_serializer_context()).data,
                        "token": AuthToken.objects.create(user)[1]
                    },
                    status=status.HTTP_201_CREATED
                )

            else:
                return Response(
                    {
                        "details": "This email address was not verified"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    "details": "This email address was not verified"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
