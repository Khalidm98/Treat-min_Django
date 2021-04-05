# Generated by Django 3.1.6 on 2021-04-04 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicreview',
            name='rating',
            field=models.CharField(choices=[('A', 1), ('B', 2), ('C', 3), ('D', 4), ('E', 5)], max_length=1),
        ),
        migrations.AlterField(
            model_name='clinicreview',
            name='review',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='roomreview',
            name='rating',
            field=models.CharField(choices=[('A', 1), ('B', 2), ('C', 3), ('D', 4), ('E', 5)], max_length=1),
        ),
        migrations.AlterField(
            model_name='roomreview',
            name='review',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='servicereview',
            name='rating',
            field=models.CharField(choices=[('A', 1), ('B', 2), ('C', 3), ('D', 4), ('E', 5)], max_length=1),
        ),
        migrations.AlterField(
            model_name='servicereview',
            name='review',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]