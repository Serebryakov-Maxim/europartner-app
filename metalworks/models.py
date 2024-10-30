from django.db import models
from partners.models import Partner

class mw_Detail(models.Model):
    """Деталь - информация о детали"""
    
    TYPE = [
        (0, "-"),
        (1, "Европартнер"),
        (2, "Клиент"),
        (3, "Импорт"),
    ]

    STATUS = [
        (0, "-"),
        (1, "В работе"),
        (2, "Выполнена"),
    ]

    name = models.CharField('Наименование', max_length=255)
    full_name = models.CharField('Полное наименование', max_length=255, blank=True)
    article = models.CharField('Артикул', max_length=50, blank=True)
    assembly = models.CharField('Сборка', max_length=255, default='', blank=True)
    shield = models.BooleanField('Шильда', default=False)
    type = models.IntegerField('Тип прессформы',
                                choices=TYPE,
                                default=0
                                )
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='Клиент')
    quantity = models.IntegerField('Количество, шт.', default=1)
    date_start = models.DateField('Дата начала')
    date_finish = models.DateField('Дата окончания', blank=True, null=True)
    priority = models.IntegerField('Очередность', default=0)
    status = models.IntegerField('Статус', choices=STATUS, default=0)
    year = models.IntegerField('Год выпуска', blank=True, null=True)
    date_modified = models.DateTimeField('Дата изменения', auto_now=True)
    uuid_1C = models.CharField('Идентификатор детали в 1С', max_length=36, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.date_finish is not None:
            self.year = self.date_finish.year
        else:
            self.year = 0        

        super(mw_Detail, self).save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mw_detail'
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def getYear(self):
        if self.year is None or self.year == 0:
            return "-"
        else:
            return self.year

class mw_Work(models.Model):
    """Работа - работа, которую необходимо выполнить"""
    name = models.CharField('Наименование', max_length=255)
    priority = models.IntegerField('Очередность', default=0)

    class Meta:
            db_table = 'mw_work'
            verbose_name = 'Работа'
            verbose_name_plural = 'Работы'

    def __str__(self):
        return str(self.priority) + '. ' + self.name
    
class mw_Progress(models.Model):
    """Выполнение - прогресс выполнения плана производства"""
    detail = models.ForeignKey(mw_Detail, on_delete=models.CASCADE)
    work = models.ForeignKey(mw_Work, on_delete=models.CASCADE)
    progress = models.IntegerField('Выполнение', default=0)
    week = models.IntegerField('Неделя', default=0)
    date_finish = models.DateField('Дата выполнения', blank=True, null=True)

    class Meta:
            db_table = 'mw_execute'
            verbose_name = 'Выполнение'
            verbose_name_plural = 'Выполнение'
            unique_together = ('detail', 'work')

    def __str__(self):
        return str(self.detail.name) + '. ' + str(self.work.name)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.progress != 3:
            self.week = 0
            self.date_finish = None

        super(mw_Progress, self).save()