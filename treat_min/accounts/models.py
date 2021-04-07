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
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    name = models.CharField(verbose_name=_('name'), max_length=50)
    phone = models.CharField(verbose_name=_('phone'), max_length=11)
    date_joined = models.DateTimeField(verbose_name=_('date_joined'), auto_now_add=True)

    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active,\nUnselect this instead of deleting accounts.'
        )
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    groups = models.ForeignKey(
        Group,
        on_delete=models.RESTRICT,
        verbose_name=_('groups'),
        blank=True,
        null=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='users',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # fields that will be prompted for when creating a superuser

    class Meta:
        verbose_name_plural = _('Abstract Users')
        verbose_name = _('abstract user')

    def __str__(self):
        return self.email + ' - ' + self.name

    def get_full_name(self):
        name = str(self.name)
        return name.strip()

    def get_short_name(self):
        name = str(self.name)
        return name.strip()

    def email_user(self, subject, message, from_email=settings.EMAIL_HOST_USER, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))

    class Meta:
        verbose_name_plural = _('Admins')
        verbose_name = _('admin')

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hospital_admin',
                                verbose_name=_('user'))
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT, verbose_name=_('hospital'))

    class Meta:
        verbose_name_plural = _('Hospitals Admins')
        verbose_name = _('hospital admin')

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
    photo = models.ImageField(upload_to='photos/users/', blank=True, null=True, verbose_name=_('photo'))

    class Meta:
        verbose_name_plural = _('Users')
        verbose_name = _('user')

    def __str__(self):
        return self.user.email + ' - ' + self.user.name


class PendingUser(models.Model):
    email = models.EmailField(unique=True, verbose_name=_('email address'))
    code = models.PositiveSmallIntegerField(verbose_name=_('code'))
    is_verified = models.BooleanField(default=False, verbose_name=_('is_verified'))

    class Meta:
        verbose_name_plural = _('Pending Users')
        verbose_name = _('pending user')

    def __str__(self):
        return self.email


class LostPassword(models.Model):
    email = models.EmailField(unique=True, verbose_name=_('email address'))
    code = models.PositiveSmallIntegerField(verbose_name=_('code'))
    is_verified = models.BooleanField(default=False, verbose_name=_('is_verified'))

    class Meta:
        verbose_name_plural = _('Lost Passwords')
        verbose_name = _('lost password')

    def __str__(self):
        return self.email
