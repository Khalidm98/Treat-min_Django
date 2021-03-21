# Generated by Django 3.1.6 on 2021-03-21 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('treat_min', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('rating', models.PositiveSmallIntegerField()),
                ('review', models.TextField(max_length=250)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treat_min.servicedetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceAppointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='W', max_length=1)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('appointment_date', models.DateField()),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treat_min.serviceschedule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'ordering': ['booking_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('rating', models.PositiveSmallIntegerField()),
                ('review', models.TextField(max_length=250)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treat_min.roomdetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomAppointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='W', max_length=1)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('appointment_date', models.DateField()),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treat_min.roomschedule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'ordering': ['booking_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClinicReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('rating', models.PositiveSmallIntegerField()),
                ('review', models.TextField(max_length=250)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treat_min.clinicdetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClinicAppointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Accepted'), ('C', 'Canceled'), ('R', 'Rejected'), ('W', 'Waiting')], default='W', max_length=1)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('appointment_date', models.DateField()),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treat_min.clinicschedule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'ordering': ['booking_date'],
                'abstract': False,
            },
        ),
    ]
