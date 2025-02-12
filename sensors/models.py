from django.db import models

class WorkArea(models.Model):
    """Рабочий учаcток - информация о рабочий участках"""
    name = models.CharField('Наименование', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sn_work_areas'
        verbose_name = 'Рабочий участок'
        verbose_name_plural = 'Рабочие участки'

class Sensor(models.Model):
    """Сенсоры - информация о сенсорах"""
    name = models.CharField('Наименование', max_length=255)
    work_area = models.ForeignKey(WorkArea, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sn_sensors'
        verbose_name = 'Сенсор'
        verbose_name_plural = 'Сенсоры'

class Parameter(models.Model):
    """Параметры - информация о параметрах"""
    name = models.CharField('Наименование', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sn_parameters'
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

class ValueParameter(models.Model):
    """Параметры - информация о параметрах"""
    date = models.DateTimeField('Дата', db_index=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.DecimalField('Значение', blank=True, max_digits=9, decimal_places=3)

    def __str__(self):
        return self.sensor.name + ' / ' + self.parameter.name + ' / ' + str(self.value)

    class Meta:
        db_table = 'sn_values_parameters'
        verbose_name = 'Значение параметра'
        verbose_name_plural = 'Значения параметров'