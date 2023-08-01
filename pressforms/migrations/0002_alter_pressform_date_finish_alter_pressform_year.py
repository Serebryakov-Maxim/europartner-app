# Generated by Django 4.2.3 on 2023-07-24 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pressforms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pressform',
            name='date_finish',
            field=models.DateField(blank=True, default=datetime.date(2000, 1, 1), null=True, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='pressform',
            name='year',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Год выпуска'),
        ),
    ]
