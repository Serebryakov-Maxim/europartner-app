from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import mw_Detail

@receiver(post_save, sender=mw_Detail)
def post_save_pf_production(**kwargs):
    pass
    #print('Нужно обновить формы')