from random import randint

# from django.conf import settings
# from django.core.mail import send_mail
from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSerializer, UnverifiedUserSerializer, AbstractUserSerializer, RegisterSerializer
from ..models import AbstractUser, UnverifiedUser, User


class SendEmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = AbstractUser.objects.filter(email__iexact=email)
        if user.exists():
            return Response({
                "status": False,
                "details": "This email address is already registered"
            })

        code = randint(999, 9999)
        # send_mail(
        #     'User Email Verification',
        #     'Please type this code to verify your email\n{0}'.format(code),
        #     settings.EMAIL_HOST_USER,
        #     [email],
        #     fail_silently=False
        # )
        user = UnverifiedUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            user.code = code
            user.save()
        else:
            UnverifiedUser.objects.create(email=email, code=code)

        return Response({
            "status": True,
            "message": "Verification email was sent successfully"
        })


class VerifyEmailView(APIView):
    serializer_class = UnverifiedUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        user = UnverifiedUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if str(user.code) == code:
                user.is_verified = True
                user.save()
                return Response({
                    "status": True,
                    "details": "Email was verified successfully"
                })
            else:
                return Response({
                    "status": False,
                    "details": "Wrong code"
                })

        else:
            return Response({
                "status": False,
                "details": "This email address was not registered before"
            })


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        user = UnverifiedUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if user.is_verified:
                user.delete()
                user = serializer.save()
                # User.objects.create(user=user, date_of_birth, gender)
                return Response({
                    "user": AbstractUserSerializer(user, context=self.get_serializer_context()).data,
                    "token": AuthToken.objects.create(user)[1]
                })

            else:
                return Response({
                    "status": False,
                    "details": "This email address was not verified"
                })
        else:
            return Response({
                "status": False,
                "details": "This email address was not verified"
            })

        # user = serializer.save()
        # return Response({
        #     "user": AbstractUserSerializer(user, context=self.get_serializer_context()).data,
        #     "token": AuthToken.objects.create(user)[1]
        # })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
