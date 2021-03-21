from django.contrib import admin
from .models import *

SCHEDULE_FIELDS = ['day', 'start', 'end']


class ClinicScheduleInline(admin.TabularInline):
    model = ClinicSchedule
    fields = SCHEDULE_FIELDS
    extra = 1


class RoomScheduleInline(admin.TabularInline):
    model = RoomSchedule
    fields = SCHEDULE_FIELDS
    extra = 1


class ServiceScheduleInline(admin.TabularInline):
    model = ServiceSchedule
    fields = SCHEDULE_FIELDS
    extra = 1


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


class ClinicAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline]
    list_display = ['name']


class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomDetailInline]
    list_display = ['name']


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceDetailInline]
    list_display = ['name']


class DoctorAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline]
    list_display = ['name', 'speciality']


class HospitalAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline, RoomDetailInline, ServiceDetailInline]
    list_display = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospitaladmin'):
            return qs.filter(id=request.user.hospitaladmin.hospital.id)
        return qs


class ClinicDetailAdmin(admin.ModelAdmin):
    fields = ['hospital', 'clinic', 'doctor', 'price']
    inlines = [ClinicScheduleInline]
    list_display = ['hospital', 'clinic', 'doctor', 'price']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospitaladmin'):
            return qs.filter(hospital=request.user.hospitaladmin.hospital)
        return qs


class RoomDetailAdmin(admin.ModelAdmin):
    fields = ['hospital', 'room', 'price']
    inlines = [RoomScheduleInline]
    list_display = ['hospital', 'room', 'price']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospitaladmin'):
            return qs.filter(hospital=request.user.hospitaladmin.hospital)
        return qs


class ServiceDetailAdmin(admin.ModelAdmin):
    fields = ['hospital', 'service', 'price']
    inlines = [ServiceScheduleInline]
    list_display = ['hospital', 'service', 'price']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospitaladmin'):
            return qs.filter(hospital=request.user.hospitaladmin.hospital)
        return qs


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Service, ServiceAdmin)

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Hospital, HospitalAdmin)

admin.site.register(ClinicDetail, ClinicDetailAdmin)
admin.site.register(RoomDetail, RoomDetailAdmin)
admin.site.register(ServiceDetail, ServiceDetailAdmin)
