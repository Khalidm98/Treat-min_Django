# Generated by Django 3.1.5 on 2021-04-05 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210405_0741'),
        ('entities_details', '0002_auto_20210405_0741'),
        ('user_appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clinicappointment',
            options={'verbose_name': 'clinic appointment', 'verbose_name_plural': 'Clinics Appointments'},
        ),
        migrations.AlterModelOptions(
            name='roomappointment',
            options={'verbose_name': 'room appointment', 'verbose_name_plural': 'Rooms Appointments'},
        ),
        migrations.AlterModelOptions(
            name='serviceappointment',
            options={'verbose_name': 'service appointment', 'verbose_name_plural': 'Services Appointments'},
        ),
        migrations.AlterField(
            model_name='clinicappointment',
            name='appointment_date',
            field=models.DateField(verbose_name='appointment_date'),
        ),
        migrations.AlterField(
            model_name='clinicappointment',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='booking_date'),
        ),
        migrations.AlterField(
            model_name='clinicappointment',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='entities_details.clinicschedule', verbose_name='schedule'),
        ),
        migrations.AlterField(
            model_name='clinicappointment',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='W', max_length=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='clinicappointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinics_appointments', to='accounts.user', verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='roomappointment',
            name='appointment_date',
            field=models.DateField(verbose_name='appointment_date'),
        ),
        migrations.AlterField(
            model_name='roomappointment',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='booking_date'),
        ),
        migrations.AlterField(
            model_name='roomappointment',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='entities_details.roomschedule', verbose_name='schedule'),
        ),
        migrations.AlterField(
            model_name='roomappointment',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='W', max_length=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='roomappointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms_appointments', to='accounts.user', verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='appointment_date',
            field=models.DateField(verbose_name='appointment_date'),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='booking_date'),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='entities_details.serviceschedule', verbose_name='schedule'),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='W', max_length=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_appointments', to='accounts.user', verbose_name='user'),
        ),
    ]