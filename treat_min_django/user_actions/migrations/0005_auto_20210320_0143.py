# Generated by Django 3.1.6 on 2021-03-19 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_actions', '0004_auto_20210320_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicreview',
            name='review',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='roomreview',
            name='review',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='servicereview',
            name='review',
            field=models.CharField(max_length=250),
        ),
    ]
