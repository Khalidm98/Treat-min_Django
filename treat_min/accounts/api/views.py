from random import randint

from django.contrib.auth import login
from django.core.mail import send_mail
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSerializer, CodeSerializer, PasswordSerializer, \
    AbstractUserSerializer, RegisterSerializer
from ..models import AbstractUser, PendingUser, LostPassword


def get_user(request):
    key = request.headers['Authorization'][6:14]
    return AuthToken.objects.get(token_key=key).user.user


class SendEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')

        user = AbstractUser.objects.filter(email__iexact=email)
        if user.exists():
            return Response(
                {"details": "This email address is already registered"},
                status.HTTP_400_BAD_REQUEST
            )

        code = randint(999, 9999)
        send_mail(
            'Email Verification',
            'Please type this code to verify your email:\n{0}'.format(code),
            'Treat-min <noreply@treat-min.com>',
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
    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        code = request.data.get('code')

        user = PendingUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if user.code == code:
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


class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')

        user = PendingUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if user.is_verified:
                user.delete()
                user = serializer.save()
                user.email_user(
                    'Welcome to Treat-min',
                    'We are happy to have you on board with us.\n'
                    'Take a look at our website:\n'
                    'https://www.treat-min.com/\n\n'
                    'Our mobile app will be available very soon.\nStay tuned.'
                )
                return Response(
                    {
                        "user": AbstractUserSerializer(user, context=serializer.context).data,
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
                {"details": "This email doesn't belong to an existing account"},
                status.HTTP_400_BAD_REQUEST
            )


class LoginAPI(KnoxLoginView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        try:
            reset_pass_fail_trial = LostPassword.objects.get(email=user.email)
            reset_pass_fail_trial.delete()
        except LostPassword.DoesNotExist:
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
            'Password Reset Request',
            'Please type this code to reset your password:\n{0}\n\n'
            'If you didn\'t request to reset your password please don\'t share this code with anyone.'.format(code),
            'Treat-min <noreply@treat-min.com>',
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
            if user.code == code:
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
                {"details": "This email user didn't request to reset his password before!"},
                status.HTTP_404_NOT_FOUND
            )


class ChangePasswordAPI(APIView):
    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        password = request.data.get('password')

        user = AbstractUser.objects.get(email=email)
        if not LostPassword.objects.get(email=email).is_verified:
            return Response(
                {"details": "Please verify your account with the code sent to your email."},
                status.HTTP_400_BAD_REQUEST
            )

        if len(password) < 8:
            return Response(
                {"detail": "Passwords can't be less than 8 characters"},
                status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()
        user = LostPassword.objects.get(email=email)
        user.delete()
        return Response({"detail": "Password changed successfully!"}, status.HTTP_202_ACCEPTED)
