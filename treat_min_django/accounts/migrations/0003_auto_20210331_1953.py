# Generated by Django 3.1.6 on 2021-03-31 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210331_1912'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='abstractuser',
            options={'verbose_name_plural': 'Abstract Users'},
        ),
        migrations.AlterModelOptions(
            name='pendinguser',
            options={'verbose_name_plural': 'Pending Users'},
        ),
    ]
