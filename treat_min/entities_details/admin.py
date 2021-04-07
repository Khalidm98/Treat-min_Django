from django.contrib import admin
from .models import *


class ScheduleInline(admin.TabularInline):
    fields = ['day', 'start', 'end']
    min_num = 1
    extra = 0


class ClinicScheduleInline(ScheduleInline):
    model = ClinicSchedule


class RoomScheduleInline(ScheduleInline):
    model = RoomSchedule


class ServiceScheduleInline(ScheduleInline):
    model = ServiceSchedule


class ClinicDetailInline(admin.TabularInline):
    model = ClinicDetail
    fields = ['hospital', 'clinic', 'doctor', 'price']
    extra = 1


class RoomDetailInline(admin.TabularInline):
    model = RoomDetail
    fields = ['hospital', 'room', 'price']
    extra = 1


class ServiceDetailInline(admin.TabularInline):
    model = ServiceDetail
    fields = ['hospital', 'service', 'price']
    extra = 1


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
    inlines = [ClinicScheduleInline]
    list_display = ['hospital', 'clinic', 'doctor', 'price']


class RoomDetailAdmin(DetailAdmin):
    fields = ['hospital', 'room', 'price']
    inlines = [RoomScheduleInline]
    list_display = ['hospital', 'room', 'price']


class ServiceDetailAdmin(DetailAdmin):
    fields = ['hospital', 'service', 'price']
    inlines = [ServiceScheduleInline]
    list_display = ['hospital', 'service', 'price']


admin.site.register(ClinicDetail, ClinicDetailAdmin)
admin.site.register(RoomDetail, RoomDetailAdmin)
admin.site.register(ServiceDetail, ServiceDetailAdmin)
