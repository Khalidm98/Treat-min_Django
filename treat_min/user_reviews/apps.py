from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserReviewsConfig(AppConfig):
    name = 'treat_min.user_reviews'
    verbose_name = _('Users Reviews')
