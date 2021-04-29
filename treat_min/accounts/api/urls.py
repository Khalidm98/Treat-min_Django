from django.urls import path
from knox import views as knox_views
from .views import RegisterEmailAPI, RegisterCodeAPI, RegisterAPI, ChangePhotoAPI, LoginAPI, \
    PasswordEmailAPI, PasswordCodeAPI, PasswordResetAPI, ChangePasswordAPI, UserDataAPI

urlpatterns = [
    path('register-email/', RegisterEmailAPI.as_view(), name='register_email'),
    path('register-code/', RegisterCodeAPI.as_view(), name='register_code'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('change-photo/', ChangePhotoAPI.as_view(), name='change_photo'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout_all'),
    path('password-email/', PasswordEmailAPI.as_view(), name='password_email'),
    path('password-code/', PasswordCodeAPI.as_view(), name='password_code'),
    path('password-reset/', PasswordResetAPI.as_view(), name='password_reset'),
    path('change-password/', ChangePasswordAPI.as_view(), name='change_password'),
    path('user-data/', UserDataAPI.as_view(), name='user_data'),
]
