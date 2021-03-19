# Generated by Django 3.1.6 on 2021-03-18 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treat_min', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicappointment',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='Waiting', max_length=1),
        ),
        migrations.AlterField(
            model_name='roomappointment',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='Waiting', max_length=1),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='Waiting', max_length=1),
        ),
    ]
