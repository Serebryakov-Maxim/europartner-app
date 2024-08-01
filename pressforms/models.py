from datetime import date
from django.db import models

class Pressform(models.Model):
    """Прессформа - информация о прессформе"""

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
    assembly = models.CharField('Сборка', max_length=255, default='', blank=True)
    article = models.CharField('Артикул', max_length=50)
    date_start = models.DateField('Дата начала')
    date_finish = models.DateField('Дата окончания', blank=True, null=True)
    priority = models.IntegerField('Очередность', default=0)
    shield = models.BooleanField('Шильда', default=False)
    type = models.IntegerField('Тип прессформы',
                                choices=TYPE,
                                default=0
                                )
    status = models.IntegerField('Статус',
                                choices=STATUS,
                                default=0
                                )
    year = models.IntegerField('Год выпуска', blank=True, null=True)
    date_modified = models.DateTimeField('Дата изменения', auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.date_finish is not None:
            self.year = self.date_finish.year
        else:
            self.year = 0        

        super(Pressform, self).save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pf_pressform'
        verbose_name = 'Прессформа'
        verbose_name_plural = 'Прессформы'

    def getYear(self):
        if self.year is None or self.year == 0:
            return "-"
        else:
            return self.year

class TypeWork(models.Model):
    """Тип работы - группировка работ по видам"""
    name = models.CharField('Наименование', max_length=255)
    priority = models.IntegerField('Очередность')

    class Meta:
            db_table = 'pf_type_work'
            verbose_name = 'Тип работы'
            verbose_name_plural = 'Типы работ'
    
    def __str__(self):
        return str(self.priority) + '. ' + self.name

class Work(models.Model):
    """Работа - работа, которую необходимо выполнить"""
    name = models.CharField('Наименование', max_length=255)
    priority = models.IntegerField('Очередность', default=0)
    type = models.ForeignKey(TypeWork, on_delete=models.CASCADE)

    class Meta:
            db_table = 'pf_work'
            verbose_name = 'Работа'
            verbose_name_plural = 'Работы'

    def __str__(self):
        return str(self.priority) + '. ' + self.name + ' (' + self.type.name + ')'

class Progress(models.Model):
    """Выполнение - прогресс выполнения плана производства"""
    pressform = models.ForeignKey(Pressform, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    progress = models.IntegerField('Выполнение', default=0)
    week = models.IntegerField('Неделя', default=0)
    date_finish = models.DateField('Дата выполнения', blank=True, null=True)

    class Meta:
            db_table = 'pf_execute'
            verbose_name = 'Выполнение'
            verbose_name_plural = 'Выполнение'
            unique_together = ('pressform', 'work')

    def __str__(self):
        return str(self.pressform.name) + '. ' + str(self.work.name)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.progress != 3:
            self.week = 0
            self.date_finish = None

        super(Progress, self).save()

class MediaFile(models.Model):
    """Медиа файлы - видио и фото контент"""
    TYPE = [
        (0, "Видео"),
        (1, "Фото"),
    ]

    name = models.CharField('Наименование', max_length=255)
    file = models.FileField(upload_to='instrumentalka')
    type = models.IntegerField('Тип контента',
                                choices=TYPE,
                                default=0
                                )

    class Meta:
            db_table = 'pf_mediafiles'
            verbose_name = 'Файл'
            verbose_name_plural = 'Медиа файлы'
    
    def __str__(self):
        return str(self.type) + '. ' + self.name