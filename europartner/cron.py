from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from tpa.models import Cycle

def checking_controllers():

    obj = Cycle.objects.last()
    if obj == None:
        return
    
    difference = datetime.now() - obj.date.replace(tzinfo=None)

    total_seconds = difference.total_seconds()

    subject = 'Нет данных с контроллеров ТПА!'
    message = 'Последние показания были ' + str(int(total_seconds)) + ' сек. назад'
    send_mail(subject, message, settings.EMAIL_USER_SENDER, settings.EMAIL_USER_ALERT)