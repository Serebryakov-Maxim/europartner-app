# Generated by Django 4.2.3 on 2024-06-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tpa', '0025_alter_cycle_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='full_job_description',
            field=models.BooleanField(default=True, verbose_name='Полное описание задания'),
        ),
    ]