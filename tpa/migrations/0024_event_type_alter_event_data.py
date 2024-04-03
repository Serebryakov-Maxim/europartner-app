# Generated by Django 4.2.3 on 2024-01-26 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tpa', '0023_cycle_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(default='', max_length=255, verbose_name='Тип события'),
        ),
        migrations.AlterField(
            model_name='event',
            name='data',
            field=models.CharField(max_length=255, verbose_name='Данные'),
        ),
    ]