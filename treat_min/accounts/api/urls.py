from django.urls import path
from knox import views as knox_views
from .views import SendEmailView, VerifyEmailView, RegisterAPI, LoginAPI, SendEmailLostPassword, \
    VerifyEmailLostPassword, ChangePasswordAPI, UserDataAPI

urlpatterns = [
    path('send-email/', SendEmailView.as_view(), name='send_email'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout_all'),
    path('password-reset/', SendEmailLostPassword.as_view(), name='admin_password_reset'),
    path('code-verification/', VerifyEmailLostPassword.as_view(), name='verify_code_lost_password'),
    path('change-password/', ChangePasswordAPI.as_view(), name='change_password'),
    path('user-data/', UserDataAPI.as_view(), name='user_data'),
]
