# Generated by Django 3.1.6 on 2021-04-07 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'clinic',
                'verbose_name_plural': 'Clinics',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='gender')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='phone')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/doctors/', verbose_name='photo')),
            ],
            options={
                'verbose_name': 'doctor',
                'verbose_name_plural': 'Doctors',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('phone', models.CharField(max_length=11, verbose_name='phone')),
                ('address', models.CharField(max_length=100, verbose_name='address')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='longitude')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/hospitals/', verbose_name='photo')),
            ],
            options={
                'verbose_name': 'Hospital',
                'verbose_name_plural': 'Hospitals',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'room',
                'verbose_name_plural': 'Rooms',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'Services',
                'ordering': ['name'],
            },
        ),
    ]