from django.db import models
import uuid

class Machine(models.Model):
    """Станки - справочник станков"""
    name = models.CharField('Наименование', max_length=255)
    id = models.IntegerField('Номер', primary_key=True)

    class Meta:
            db_table = 'tpa_machines'
            verbose_name = 'Станок'
            verbose_name_plural = 'Станки'
            ordering = ["id"]

    def __str__(self):
        return '№' + str(self.id) + ' ' + self.name
    
class Job(models.Model):
    """Задания - справочник заданий"""
    id = models.UUIDField('id', primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField('Дата')
    number = models.CharField('Номер', max_length=50)
    name = models.CharField('Наименование', max_length=255)
    status = models.CharField('Статус', max_length=50)
    count_plan = models.IntegerField('Количество')
    time_plan_ms = models.IntegerField('Плановое время цикла')
    socket_plan = models.IntegerField('Количество гнезд (план)')
    socket_fact = models.IntegerField('Количество гнезд (факт)')
    data_json = models.TextField('Данные JSON')
    
    class Meta:
            db_table = 'tpa_jobs'
            verbose_name = 'Задание'
            verbose_name_plural = 'Задания'
            ordering = ["date"]

    def __str__(self):
        return 'Задание' + str(self.name) + ' от ' + str(self.date)
    
class Event(models.Model):
    """Событие - события на станках"""
    date = models.DateTimeField('Дата')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    data = models.CharField('События', max_length=255)

    class Meta:
            db_table = 'tpa_events'
            verbose_name = 'Событие'
            verbose_name_plural = 'События'
            ordering = ["date"]

    def __str__(self):
        return str(self.machine) + ', ' + str(self.date) + ', ' + str(self.data)
    
class Cycle(models.Model):
    """Цикл - выполненные циклы"""
    date = models.DateTimeField('Дата')
    time_ms = models.IntegerField('Время цикла')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, default=0)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=uuid.uuid4)
    count = models.IntegerField('Количество', default=0)

    class Meta:
            db_table = 'tpa_cycles'
            verbose_name = 'Цикл'
            verbose_name_plural = 'Циклы'

    def __str__(self):
        return '№' + str(self.machine) + ', ' + str(self.date) + ', ' + str(self.time_ms) + ' мс'