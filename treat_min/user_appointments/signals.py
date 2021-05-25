from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClinicAppointment, ServiceAppointment


@receiver(post_save, sender=ClinicAppointment)
@receiver(post_save, sender=ServiceAppointment)
def email_notification(sender, instance, **kwargs):
    if instance.status == 'W' or instance.status == 'C':
        url = 'https://www.treat-min.com/admin/user_appointments/'
        if sender is ClinicAppointment:
            admins = instance.schedule.clinic.hospital.admins.all()
            url += 'clinicappointment/' + str(instance.id) + '/change/'
        else:
            admins = instance.schedule.service.hospital.admins.all()
            url += 'serviceappointment/' + str(instance.id) + '/change/'

        if instance.status == 'W':
            for admin in admins:
                admin.user.email_user(
                    'A New Appointment has been Reserved',
                    'Please, respond to this appointment:\n\n' + url
                )

        else:
            for admin in admins:
                admin.user.email_user(
                    'An Appointment has been Canceled',
                    'This appointment was canceled by user:\n\n' + url
                )

    else:
        if sender is ClinicAppointment:
            detail = instance.schedule.clinic
            msg = 'Appointment Details:\n' \
                  + detail.hospital.name + '\n' \
                  + detail.clinic.name + '\n' \
                  + detail.doctor.name + '\n'
        else:
            detail = instance.schedule.service
            msg = 'Appointment Details:\n' \
                  + detail.hospital.name + '\n' \
                  + detail.service.name + '\n'

        msg += str(instance.appointment_date) + '\n' \
            + str(instance.schedule.start) + ' - ' + str(instance.schedule.end) + '\n\n'
        user = instance.user

        if instance.status == 'A':
            user.user.email_user(
                'Your Appointment has been Accepted',
                msg + 'Please, be safe <3'
            )

        else:
            user.user.email_user(
                'Your Appointment has been Rejected',
                msg + 'May be try a different schedule.'
            )
