from __future__ import unicode_literals
from datetime import datetime
from random import random, seed

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from treat_min_django.treat_min.models.entities import GENDER, Hospital
from .managers import UserManager


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=50)
    phone = models.CharField(_('phone'), max_length=11, default='')
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    groups = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        verbose_name=_('groups'),
        blank=True,
        null=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    # fields that will be prompted for when creating a user via the createsuperuser

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email + ' - ' + self.name

    def clean(self):
        if not self.password:
            seed(datetime.now())
            self.password = random()
        super(AbstractUser, self).clean()

    def get_full_name(self):
        name = str(self.name)
        return name.strip()

    def get_short_name(self):
        name = str(self.name)
        return name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__email']

    def __str__(self):
        return self.user.email + ' - ' + self.user.name

    def save(self, *args, **kwargs):
        abstract_user = AbstractUser.objects.get(id=self.user.id)
        abstract_user.groups = Group.objects.get(name='Admin')
        abstract_user.is_superuser = False
        abstract_user.is_staff = True
        abstract_user.save()
        super().save(*args, **kwargs)


class HospitalAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT)

    class Meta:
        ordering = ['user__email']
        verbose_name_plural = 'Hospitals Admins'

    def __str__(self):
        return self.user.email + ' - ' + self.user.name

    def save(self, *args, **kwargs):
        abstract_user = AbstractUser.objects.get(id=self.user.id)
        abstract_user.groups = Group.objects.get(name='Hospital')
        abstract_user.is_superuser = False
        abstract_user.is_staff = True
        abstract_user.save()
        super().save(*args, **kwargs)


class User(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    photo = models.ImageField(upload_to='photos/users/', blank=True, null=True)

    class Meta:
        ordering = ['user__email']

    def __str__(self):
        return self.user.email + ' - ' + self.user.name

    def clean(self):
        if self.user.is_staff or self.user.is_superuser:
            raise ValidationError('User cannot be marked as a staff member or a superuser!')
        super(User, self).clean()
