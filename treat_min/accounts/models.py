from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from ..entities.models import GENDER, Hospital


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_('email address'))
    name = models.CharField(max_length=50, verbose_name=_('name'))
    phone = models.CharField(max_length=11, verbose_name=_('phone'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('date_joined'))

    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('staff status'))
    groups = models.ForeignKey(
        Group, on_delete=models.RESTRICT, related_name='users', blank=True, null=True, verbose_name=_('groups')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # fields that will be prompted for when creating a superuser

    class Meta:
        verbose_name = _('abstract user')
        verbose_name_plural = _('Abstract Users')

    def __str__(self):
        return self.email + ' - ' + self.name

    def get_full_name(self):
        name = str(self.name)
        return name.strip()

    def get_short_name(self):
        name = str(self.name)
        return name.strip()

    def email_user(self, subject, message, from_email='Treat-min <noreply@treat-min.com>', **kwargs):
        send_mail(subject, message, from_email, [self.email], fail_silently=False, **kwargs)

    def welcome_email(self):
        self.email_user(
            'Welcome to Treat-min',
            'We are happy to have you on board with us.\n'
            'Take a look at our website:\n'
            'https://www.treat-min.com/\n\n'
            'Our mobile app will be available very soon.\nStay tuned.'
        )


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))

    class Meta:
        verbose_name = _('admin')
        verbose_name_plural = _('Admins')

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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hospital_admin', verbose_name=_('user')
    )
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT, verbose_name=_('hospital'))

    class Meta:
        verbose_name = _('hospital admin')
        verbose_name_plural = _('Hospitals Admins')

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    date_of_birth = models.DateField(verbose_name=_('date_of_birth'))
    gender = models.CharField(max_length=1, choices=GENDER, verbose_name=_('gender'))
    photo = models.ImageField(upload_to='static/photos/users/', blank=True, null=True, verbose_name=_('photo'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.user.email + ' - ' + self.user.name


class PendingUser(models.Model):
    email = models.EmailField(unique=True, verbose_name=_('email address'))
    code = models.PositiveSmallIntegerField(verbose_name=_('code'))
    is_verified = models.BooleanField(default=False, verbose_name=_('is_verified'))

    class Meta:
        verbose_name = _('pending user')
        verbose_name_plural = _('Pending Users')

    def __str__(self):
        return self.email


class LostPassword(models.Model):
    email = models.EmailField(unique=True, verbose_name=_('email address'))
    code = models.PositiveSmallIntegerField(verbose_name=_('code'))
    is_verified = models.BooleanField(default=False, verbose_name=_('is_verified'))

    class Meta:
        verbose_name = _('lost password')
        verbose_name_plural = _('Lost Passwords')

    def __str__(self):
        return self.email
