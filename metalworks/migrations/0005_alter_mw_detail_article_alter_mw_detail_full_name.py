# Generated by Django 4.2.3 on 2025-02-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metalworks', '0004_mw_detail_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mw_detail',
            name='article',
            field=models.CharField(blank=True, max_length=50, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='mw_detail',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Полное наименование'),
        ),
    ]
