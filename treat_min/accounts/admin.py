from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AbstractUser, Admin, HospitalAdmin, User, PendingUser, LostPassword


class AbstractUserAdmin(admin.ModelAdmin):
    fields = ['email', 'password', 'name', 'phone']
    list_display = ['email', 'name', 'groups', 'date_joined', 'last_login']
    search_fields = ['email', 'name', 'phone']

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


class AbstractAdmin(admin.ModelAdmin):
    fields = ['user', 'email', 'name', 'phone', 'group', 'date_joined', 'last_login']
    readonly_fields = ['email', 'name', 'phone', 'group', 'date_joined', 'last_login']
    autocomplete_fields = ['user']
    list_display = ['email', 'name', 'date_joined', 'last_login']
    search_fields = ['user__email', 'user__name', 'user__phone']

    def email(self, obj):
        return obj.user.email
    email.short_description = _('email address')

    def name(self, obj):
        return obj.user.name
    name.short_description = _('name')

    def phone(self, obj):
        return obj.user.phone
    phone.short_description = _('phone')

    def group(self, obj):
        return obj.user.groups
    group.short_description = _('groups')

    def date_joined(self, obj):
        return obj.user.date_joined
    date_joined.short_description = _('date_joined')

    def last_login(self, obj):
        return obj.user.last_login
    last_login.short_description = _('last_login')


class AdminAdmin(AbstractAdmin):
    pass


class HospitalAdminAdmin(AbstractAdmin):
    fields = ['hospital'] + AbstractAdmin.fields
    autocomplete_fields = ['hospital', 'user']
    list_display = ['hospital'] + AbstractAdmin.list_display
    search_fields = ['hospital__name'] + AbstractAdmin.search_fields


class UserAdmin(AbstractAdmin):
    fields = AbstractAdmin.fields + ['gender', 'date_of_birth']


admin.site.register(AbstractUser, AbstractUserAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(HospitalAdmin, HospitalAdminAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PendingUser)
admin.site.register(LostPassword)
