# Generated by Django 4.2.3 on 2024-04-02 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pressforms', '0015_pressform_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pressform',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]
