from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'treat_min.accounts'
    verbose_name = _('Accounts')

    def ready(self):
        import treat_min.entities.signals
