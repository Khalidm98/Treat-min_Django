from django.contrib import admin
from .models import AbstractUser, Admin, HospitalAdmin, User, PendingUser
from django.utils.translation import gettext_lazy as _

readonly = ['email', 'name', 'phone', 'date_joined', 'last_login']


class AbstractUserAdmin(admin.ModelAdmin):
    fields = ['email', 'name', 'phone', 'is_active', 'is_staff', 'date_joined', 'last_login', 'groups']
    readonly_fields = ['is_staff', 'date_joined', 'last_login', 'groups']
    list_display = ['email', 'name', 'groups', 'date_joined', 'last_login']


class AbstractAdmin(admin.ModelAdmin):
    def email(self, obj):
        return obj.user.email
    email.short_description = _('email address')

    def name(self, obj):
        return obj.user.name
    name.short_description = _('name')

    def phone(self, obj):
        return obj.user.phone
    phone.short_description = _('phone')

    def date_joined(self, obj):
        return obj.user.date_joined
    date_joined.short_description = _('date_joined')

    def last_login(self, obj):
        return obj.user.last_login
    last_login.short_description = _('last_login')


class AdminAdmin(AbstractAdmin):
    fields = ['user', 'email', 'name', 'phone', 'date_joined', 'last_login']
    readonly_fields = readonly
    list_display = ['email', 'name', 'date_joined', 'last_login']


class HospitalAdminAdmin(AbstractAdmin):
    fields = ['hospital', 'user', 'email', 'name', 'phone', 'date_joined', 'last_login']
    readonly_fields = readonly
    list_display = ['email', 'name', 'hospital', 'date_joined', 'last_login']


class UserAdmin(AbstractAdmin):
    fields = ['user', 'email', 'name', 'phone', 'date_of_birth', 'gender', 'photo', 'date_joined', 'last_login']
    readonly_fields = readonly
    list_display = ['email', 'name', 'date_joined']


admin.site.register(AbstractUser, AbstractUserAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(HospitalAdmin, HospitalAdminAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PendingUser)
