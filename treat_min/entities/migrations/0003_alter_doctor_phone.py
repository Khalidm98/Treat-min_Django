# Generated by Django 3.2 on 2021-04-10 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_auto_20210407_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='phone'),
        ),
    ]
