# Generated by Django 4.2.3 on 2024-05-22 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tpa', '0024_event_type_alter_event_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycle',
            name='date',
            field=models.DateTimeField(db_index=True, verbose_name='Дата'),
        ),
    ]