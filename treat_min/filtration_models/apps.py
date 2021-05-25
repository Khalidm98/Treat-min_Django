from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FiltrationModelsConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treat_min.filtration_models'
    verbose_name = _('Filtration Models')
