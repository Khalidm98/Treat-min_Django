from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class UserAppointmentsConfig(AppConfig):
    name = 'treat_min_django.user_appointments'
    verbose_name = _('Users Appointments')
