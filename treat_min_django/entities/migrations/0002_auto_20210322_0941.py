# Generated by Django 3.1.6 on 2021-03-22 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicdetail',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='entities.clinic'),
        ),
        migrations.AlterField(
            model_name='clinicdetail',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='entities.hospital'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='roomdetail',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='entities.hospital'),
        ),
        migrations.AlterField(
            model_name='roomdetail',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='entities.room'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='servicedetail',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='entities.hospital'),
        ),
        migrations.AlterField(
            model_name='servicedetail',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='entities.service'),
        ),
    ]
