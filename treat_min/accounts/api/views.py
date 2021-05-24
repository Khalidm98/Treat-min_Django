from random import randint
from django.contrib.auth import login
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSerializer, CodeSerializer, EmailPasswordSerializer, ChangePasswordSerializer, \
    RegisterSerializerEmail, LoginSerializer, PhotoSerializer, EditAccountSerializer, UserSerializer
from ..models import AbstractUser, PendingUser, LostPassword


def get_user(request):
    key = request.headers['Authorization'][6:14]
    return AuthToken.objects.get(token_key=key).user.user


class RegisterEmailAPI(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')

        user = AbstractUser.objects.filter(email__iexact=email)
        if user.exists():
            return Response(
                {"details": "This email address is already registered!"},
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

        return Response({"details": "Verification email was sent successfully."})


class RegisterCodeAPI(APIView):
    def patch(self, request):
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
                return Response({"details": "Email was verified successfully."})
            else:
                return Response(
                    {"details": "Wrong code!"},
                    status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {"details": "This email address was not registered before!"},
                status.HTTP_404_NOT_FOUND
            )


class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializerEmail(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')

        user = PendingUser.objects.filter(email__iexact=email)
        if user.exists():
            user = user.first()
            if user.is_verified:
                user.delete()
                user = serializer.save()
                user.welcome_email()
                return Response(
                    {
                        "user": UserSerializer(user.user, context=serializer.context).data,
                        "token": AuthToken.objects.create(user)[1]
                    },
                    status.HTTP_201_CREATED
                )

            else:
                return Response(
                    {"details": "This email address was not verified!"},
                    status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"details": "This email doesn't belong to an existing account!"},
                status.HTTP_404_NOT_FOUND
            )


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)

        try:
            reset_pass_fail_trial = LostPassword.objects.get(email=user.email)
            reset_pass_fail_trial.delete()
        except LostPassword.DoesNotExist:
            pass

        return Response(
            {
                "user": UserSerializer(user.user, context=serializer.context).data,
                "token": AuthToken.objects.create(request.user)[1]
            },
        )


class PasswordEmailAPI(APIView):
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

        return Response({"details": "Password reset email was sent successfully."})


class PasswordCodeAPI(APIView):
    def patch(self, request):
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
                return Response({"details": "Email was verified successfully."})
            else:
                return Response(
                    {"details": "Wrong code!"},
                    status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {"details": "This user didn't request to reset his password!"},
                status.HTTP_404_NOT_FOUND
            )


class PasswordResetAPI(APIView):
    def patch(self, request):
        serializer = EmailPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        password = request.data.get('password')

        user = AbstractUser.objects.filter(email__iexact=email)
        if user.exists():
            lost = LostPassword.objects.filter(email__iexact=email)
            if lost.exists():
                lost = lost.first()
                if lost.is_verified:
                    user = user.first()
                    user.set_password(password)
                    user.save()
                    lost.delete()
                    return Response({"detail": "Password changed successfully!"}, status.HTTP_202_ACCEPTED)

                else:
                    return Response(
                        {"details": "Please verify your account with the code sent to your email!"},
                        status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    {"details": "This user didn't request to reset his password!"},
                    status.HTTP_404_NOT_FOUND
                )

        else:
            return Response(
                {"details": "There is no user with this email address!"},
                status.HTTP_404_NOT_FOUND
            )


class ChangePasswordAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = get_user(request).user
        serializer = ChangePasswordSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(request.data.get('password'))
        user.save()
        return Response({"details": "Password changed successfully."}, status.HTTP_202_ACCEPTED)


class ChangePhotoAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = PhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user(request)
        user.photo = request.data.get('photo')
        user.save()
        return Response({"details": "Photo changed successfully."}, status.HTTP_202_ACCEPTED)


class EditAccountAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = get_user(request)
        serializer = EditAccountSerializer(user.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": "Account was updated successfully."}, status.HTTP_202_ACCEPTED)


class UserDataAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user(request)
        return Response(UserSerializer(user).data)
