from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from tpa.models import Cycle
from django.utils import timezone

def checking_controllers():

    obj = Cycle.objects.last()
    if obj == None:
        return
    
    tz = timezone.get_current_timezone()
    date_now = datetime.now().astimezone(tz)
    
    difference = date_now - obj.date

    total_seconds = difference.total_seconds()

    if total_seconds < 100:
        return

    subject = 'Нет данных с контроллеров ТПА!'
    message = 'Последние показания были ' + str(int(total_seconds)) + ' сек. назад'
    send_mail(subject, message, settings.EMAIL_USER_SENDER, settings.EMAIL_USER_ALERT)