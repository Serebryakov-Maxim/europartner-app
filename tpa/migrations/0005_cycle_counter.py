# Generated by Django 4.2.3 on 2023-12-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tpa', '0004_alter_cycle_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='counter',
            field=models.IntegerField(default=0, verbose_name='Счетчик'),
        ),
    ]
