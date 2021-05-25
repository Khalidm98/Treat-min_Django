from django.contrib import admin
from .models import ClinicDetail, ServiceDetail, ClinicSchedule, ServiceSchedule


class ScheduleInline(admin.TabularInline):
    fields = ['day', 'start', 'end']
    # min_num = 1
    extra = 0


class ClinicScheduleInline(ScheduleInline):
    model = ClinicSchedule


class ServiceScheduleInline(ScheduleInline):
    model = ServiceSchedule


class DetailInline(admin.TabularInline):
    exclude = ['rating_total', 'rating_users']
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospital_admin'):
            return qs.filter(id=request.user.hospital_admin.hospital.id)
        return qs


class ClinicDetailInline(DetailInline):
    model = ClinicDetail
    autocomplete_fields = ['hospital', 'clinic', 'doctor']


class ServiceDetailInline(DetailInline):
    model = ServiceDetail
    autocomplete_fields = ['hospital', 'service']


class DetailAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospital_admin'):
            return qs.filter(hospital=request.user.hospital_admin.hospital)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if hasattr(request.user, 'hospital_admin'):
            if db_field.name == 'hospital':
                kwargs['initial'] = request.user.hospital_admin.hospital.id
                kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ClinicDetailAdmin(DetailAdmin):
    fields = ['hospital', 'clinic', 'doctor', 'price']
    autocomplete_fields = ['hospital', 'clinic', 'doctor']
    inlines = [ClinicScheduleInline]
    list_display = ['hospital', 'clinic', 'doctor', 'price']


class ServiceDetailAdmin(DetailAdmin):
    fields = ['hospital', 'service', 'price']
    autocomplete_fields = ['hospital', 'service']
    inlines = [ServiceScheduleInline]
    list_display = ['hospital', 'service', 'price']


admin.site.register(ClinicDetail, ClinicDetailAdmin)
admin.site.register(ServiceDetail, ServiceDetailAdmin)
