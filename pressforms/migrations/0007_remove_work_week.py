# Generated by Django 4.2.3 on 2023-07-26 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pressforms', '0006_remove_work_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='week',
        ),
    ]
