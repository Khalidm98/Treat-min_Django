# Generated by Django 3.2 on 2021-04-19 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicappointment',
            name='appointment_date',
            field=models.DateField(verbose_name='appointment date'),
        ),
        migrations.AlterField(
            model_name='clinicappointment',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='booking date'),
        ),
        migrations.AlterField(
            model_name='roomappointment',
            name='appointment_date',
            field=models.DateField(verbose_name='appointment date'),
        ),
        migrations.AlterField(
            model_name='roomappointment',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='booking date'),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='appointment_date',
            field=models.DateField(verbose_name='appointment date'),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='booking date'),
        ),
    ]