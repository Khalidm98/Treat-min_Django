from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserAppointmentsConfig(AppConfig):
    name = 'treat_min.user_appointments'
    verbose_name = _('Users Appointments')

    def ready(self):
        import treat_min.user_appointments.signals
