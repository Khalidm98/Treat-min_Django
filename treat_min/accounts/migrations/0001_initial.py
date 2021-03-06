# Generated by Django 3.2 on 2021-05-25 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import treat_min.accounts.managers
import treat_min.entities.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('phone', models.CharField(max_length=11, verbose_name='phone')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
            ],
            options={
                'verbose_name': 'abstract user',
                'verbose_name_plural': 'Abstract Users',
            },
            managers=[
                ('objects', treat_min.accounts.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'admin',
                'verbose_name_plural': 'Admins',
            },
        ),
        migrations.CreateModel(
            name='HospitalAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'hospital admin',
                'verbose_name_plural': 'Hospitals Admins',
            },
        ),
        migrations.CreateModel(
            name='LostPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('code', models.PositiveSmallIntegerField(verbose_name='code')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is verified')),
            ],
            options={
                'verbose_name': 'lost password',
                'verbose_name_plural': 'Lost Passwords',
            },
        ),
        migrations.CreateModel(
            name='PendingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('code', models.PositiveSmallIntegerField(verbose_name='code')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is verified')),
            ],
            options={
                'verbose_name': 'pending user',
                'verbose_name_plural': 'Pending Users',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth', models.DateField(verbose_name='date of birth')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='gender')),
                ('photo', models.ImageField(default='photos/default.png', upload_to=treat_min.entities.models.image_update, verbose_name='photo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
