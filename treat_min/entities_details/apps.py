from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EntitiesDetailsConfig(AppConfig):
    name = 'treat_min.entities_details'
    verbose_name = _('Entities Details')
