from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

# from treat_min_django.treat_min.models import Hospital
from .managers import UserManager


GENDER = (('M', 'Male'), ('F', 'Female'),)


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
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['email']

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
        return str(self.user.email) + ' - ' + str(self.user.name)

    def clean(self):
        if not self.user.is_staff:
            raise ValidationError('Admin must be marked as a staff member!')
        elif self.user.is_superuser:
            raise ValidationError('Admin cannot be marked as a superuser!')
        super(Admin, self).clean()


class HospitalAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__email']

    def __str__(self):
        return str(self.user.email) + ' - ' + str(self.user.name)

    def clean(self):
        if not self.user.is_staff:
            raise ValidationError('Hospital Admin must be marked as a staff member!')
        elif self.user.is_superuser:
            raise ValidationError('Hospital Admin cannot be marked as a superuser!')
        super(HospitalAdmin, self).clean()


class User(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    photo = models.ImageField(upload_to='photos/users/', blank=True, null=True)

    class Meta:
        ordering = ['user__email']

    def __str__(self):
        return str(self.user.email) + ' - ' + str(self.user.name)

    def clean(self):
        if self.user.is_staff or self.user.is_superuser:
            raise ValidationError('User cannot be marked as a staff member or a superuser!')
        super(User, self).clean()
