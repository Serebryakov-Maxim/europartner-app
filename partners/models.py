from django.db import models

# Create your models here.
class Partner(models.Model):
    """Партнеры - информация о партнерах"""
    name = models.CharField('Наименование', max_length=255)
    full_name = models.CharField('Полное наименование', max_length=255)
    code_1C = models.CharField('Код 1С', max_length=11)
    uuid_1C = models.CharField('Идентификатор партнера в 1С', max_length=36, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pr_partner'
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'