"""treat_min URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from .accounts.api.views import SendEmailLostPassword

urlpatterns = [
    path('api/accounts/', include('treat_min.accounts.api.urls')),
    path('api/', include('treat_min.entities.api.urls')),
    path('api/', include('treat_min.entities_details.api.urls')),
    path('api/', include('treat_min.user_appointments.api.urls')),
    path('api/', include('treat_min.user_reviews.api.urls')),
]+i18n_patterns(
    path('admin/', admin.site.urls),
    path('admin/password-reset/', SendEmailLostPassword.as_view(), name='admin_password_reset'),
    prefix_default_language=True
)
