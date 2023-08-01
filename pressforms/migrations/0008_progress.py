# Generated by Django 4.2.3 on 2023-07-28 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pressforms', '0007_remove_work_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField(default=0, verbose_name='Выполнение')),
                ('week', models.IntegerField(default=0, verbose_name='Неделя')),
                ('pressform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pressforms.pressform')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pressforms.work')),
            ],
            options={
                'verbose_name': 'Выполнение',
                'verbose_name_plural': 'Выполнение',
                'db_table': 'Выполнение',
            },
        ),
    ]
