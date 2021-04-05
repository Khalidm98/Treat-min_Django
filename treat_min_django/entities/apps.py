from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class EntitiesConfig(AppConfig):
    name = 'treat_min_django.entities'
    verbose_name = _('Entities')