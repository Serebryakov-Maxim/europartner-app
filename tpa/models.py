from django.db import models
import uuid

class Machine(models.Model):
    """Станки - справочник станков"""
    name = models.CharField('Наименование', max_length=255)
    id = models.IntegerField('Номер', primary_key=True)
    full_job_description = models.BooleanField('Полное описание задания', default=True)

    class Meta:
            db_table = 'tpa_machines'
            verbose_name = 'Станок'
            verbose_name_plural = 'Станки'
            ordering = ["id"]

    def __str__(self):
        return '№' + str(self.id) + ' ' + self.name
    
class Job(models.Model):
    """Задания - справочник заданий"""
    uuid_1C = models.CharField('Идентификатор задания в 1С', max_length=36, blank=True)
    date = models.DateTimeField('Дата', blank=True, )
    number = models.CharField('Номер', max_length=50, blank=True)
    name = models.CharField('Наименование', max_length=255, blank=True)
    status = models.CharField('Статус', max_length=50, blank=True)
    count_plan = models.IntegerField('Количество', blank=True)
    time_plan_ms = models.DecimalField('Плановое время цикла', blank=True, max_digits=5, decimal_places=2)
    socket_plan = models.IntegerField('Количество гнезд (план)', blank=True)
    socket_fact = models.IntegerField('Количество гнезд (факт)', blank=True)
    data_json = models.TextField('Данные JSON', blank=True)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, default=0)
    
    class Meta:
            db_table = 'tpa_jobs'
            verbose_name = 'Задание'
            verbose_name_plural = 'Задания'
            ordering = ["date"]

    def __str__(self):
        return 'Задание ' + str(self.name) + ' от ' + str(self.date)
    
class Event(models.Model):
    """Событие - события на станках"""
    date = models.DateTimeField('Дата')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    type = models.CharField('Тип события', max_length=255, default='')
    data = models.CharField('Данные', max_length=255)

    class Meta:
            db_table = 'tpa_events'
            verbose_name = 'Событие'
            verbose_name_plural = 'События'
            ordering = ["date"]

    def __str__(self):
        return str(self.machine) + ', ' + str(self.date) + ', ' + str(self.data)
    
class Cycle(models.Model):
    """Цикл - выполненные циклы"""
    date = models.DateTimeField('Дата', db_index=True)
    time_ms = models.IntegerField('Время цикла')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, default=0)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=uuid.uuid4)
    count = models.IntegerField('Количество', default=0)
    counter = models.IntegerField('Счетчик', default=0)

    class Meta:
            db_table = 'tpa_cycles'
            verbose_name = 'Цикл'
            verbose_name_plural = 'Циклы'

    def __str__(self):
        return str(self.machine) + ', ' + str(self.date) + ', ' + str(self.time_ms) + ' мс'