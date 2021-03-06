# Generated by Django 3.2 on 2021-05-30 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9, verbose_name='longitude'),
        ),
    ]
