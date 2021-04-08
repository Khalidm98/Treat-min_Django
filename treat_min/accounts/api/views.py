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


from .serializers import EmailSerializer, AbstractUserSerializer, RegisterSerializer, CodeSerializer
from ..models import AbstractUser, PendingUser, LostPassword


def get_user(request):
    key = request.headers['Authorization'][6:14]
    return AuthToken.objects.get(token_key=key).user.user


class SendEmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = AbstractUser.objects.filter(email__iexact=email)
        if user.exists():
            return Response(
                {"details": "This email address is already registered"},
                status.HTTP_400_BAD_REQUEST
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

        return Response({"details": "Verification email was sent successfully"})


class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        code = request.data.get('code')
        user = PendingUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if str(user.code) == code:
                user.is_verified = True
                user.save()
                return Response({"details": "Email was verified successfully"})
            else:
                return Response(
                    {"details": "Wrong code"},
                    status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {"details": "This email address was not registered before"},
                status.HTTP_404_NOT_FOUND
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
                    status.HTTP_201_CREATED
                )

            else:
                return Response(
                    {"details": "This email address was not verified"},
                    status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"details": "This email doesnt belong to an existing account"},
                status.HTTP_400_BAD_REQUEST
            )


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)
        reset_pass_fail_trial = LostPassword.objects.get(email= user.email)
        if (reset_pass_fail_trial):
            reset_pass_fail_trial.delete()
        return super().post(request, format=None)


class SendEmailLostPassword(APIView):
    def post(self, request):

        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        user = AbstractUser.objects.filter(email__iexact=email)
        if not user.exists():
            return Response(
                {"details": "This email doesn't belong to any current user!"},
                status.HTTP_404_NOT_FOUND
            )

        code = randint(999, 9999)
        send_mail(
            'Password reset email',
            'Please type this code to change your password:\n{0}'.format(code),
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        user = LostPassword.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            user.code = code
            user.save()
        else:
            LostPassword.objects.create(email=email, code=code)

        return Response({"details": "Password reset email was sent successfully"})


class VerifyEmailLostPassword(APIView):
    def post(self, request):

        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        code = request.data.get('code')
        user = LostPassword.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if str(user.code) == code:
                user.is_verified = True
                user.save()
                return Response({"details": "Email was verified successfully"})
            else:
                return Response(
                    {"details": "Wrong code"},
                    status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {"details": "This email user didn't request to reset its password before!"},
                status.HTTP_404_NOT_FOUND
            )


class ChangePasswordAPI(APIView):
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')
        user = AbstractUser.objects.get(email=email)
        if LostPassword.objects.get(email=email).is_verified == False :
            return Response({
                "detail": "Please verify your account with the code sent to your email."
            }, status.HTTP_400_BAD_REQUEST)
        if len(password) <= 8:
            return Response({
                "detail": "Passwords can't be less than 8 characters"
            }, status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        deleted_user = LostPassword.objects.get(email=email)
        deleted_user.delete()
        return Response({
            "detail": "Password changed successfully!",
        }, status.HTTP_202_ACCEPTED)