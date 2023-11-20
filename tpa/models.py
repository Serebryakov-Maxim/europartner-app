from django.db import models

# Create your models here.

class Machine(models.Model):
    """Станки - справочник станков"""
    name = models.CharField('Наименование', max_length=255)
    id = models.IntegerField('Номер', primary_key=True)

    class Meta:
            db_table = 'pf_machine'
            verbose_name = 'Станок'
            verbose_name_plural = 'Станки'
            ordering = ["id"]

    def __str__(self):
        return '№' + str(self.id) + ' ' + self.name

class Cycle(models.Model):
    """Цикл - выполненные циклы"""
    date = models.DateTimeField('Дата')
    time_ms = models.IntegerField('Время цикла')
    id_machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    class Meta:
            db_table = 'pf_cycle'
            verbose_name = 'Цикл'
            verbose_name_plural = 'Циклы'

    def __str__(self):
        return '№' + str(self.id_machine) + ', ' + str(self.date) + ', ' + str(self.time_ms) + ' мс'