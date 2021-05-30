# Generated by Django 3.2 on 2021-05-25 17:12

from django.db import migrations, models
import django.db.models.deletion
import treat_min.entities.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filtration', '0001_initial'),
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
                ('phone', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='phone')),
                ('photo', models.ImageField(default='photos/default.png', upload_to=treat_min.entities.models.image_update, verbose_name='photo')),
            ],
            options={
                'verbose_name': 'doctor',
                'verbose_name_plural': 'Doctors',
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
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('phone', models.CharField(max_length=11, verbose_name='phone')),
                ('address', models.CharField(max_length=100, verbose_name='address')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='longitude')),
                ('photo', models.ImageField(default='photos/default.png', upload_to=treat_min.entities.models.image_update, verbose_name='photo')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hospitals', to='filtration.area', verbose_name='area')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hospitals', to='filtration.city', verbose_name='city')),
            ],
            options={
                'verbose_name': 'hospital',
                'verbose_name_plural': 'Hospitals',
                'ordering': ['name'],
            },
        ),
    ]
