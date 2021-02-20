from django.contrib import admin
from .models import AbstractUser, Admin, HospitalAdmin, User


class AbstractUserAdmin(admin.ModelAdmin):
    fields = ['email', 'name', 'phone', 'is_active', 'is_staff', 'date_joined', 'last_login', 'groups']
    readonly_fields = ['is_staff', 'date_joined', 'last_login']


admin.site.register(AbstractUser, AbstractUserAdmin)
admin.site.register(Admin)
admin.site.register(HospitalAdmin)
admin.site.register(User)
