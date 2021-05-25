from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=_('name'))

    class Meta:
        ordering = ['name']
        verbose_name = _('city')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=_('name'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name='areas', verbose_name=_('city'), null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return self.name
