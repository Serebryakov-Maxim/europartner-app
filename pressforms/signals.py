from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Pressform

@receiver(post_save, sender=Pressform)
def post_save_pf_production(**kwargs):
    pass
    #print('Нужно обновить формы')