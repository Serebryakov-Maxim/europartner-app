# Generated by Django 4.2.3 on 2025-02-11 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0003_alter_sensor_work_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='work_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sensors.workarea'),
        ),
    ]
