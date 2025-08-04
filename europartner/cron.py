from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from tpa.models import Cycle
from django.utils import timezone
import subprocess

def checking_controllers():

    # последние данные
    obj = Cycle.objects.last()
    if obj == None:
        return
    
    # расчет количества сек. с последних данных
    tz = timezone.get_current_timezone()
    date_now = datetime.now().astimezone(tz)
    difference = date_now - obj.date
    total_seconds = difference.total_seconds()

    # менее 100, ожидаем
    if total_seconds < 100:
        return
    
    # рассылка                         
    subject = 'Нет данных с контроллеров ТПА!'
    message = 'Последние показания были ' + str(int(total_seconds)) + ' сек. назад'
    send_mail(subject, message, settings.EMAIL_USER_SENDER, settings.EMAIL_USER_ALERT)
    
    # запуск скрипта на перезапуск службы
    subprocess.run(['. /home/user/code/restart_raspberry_service/restart_service.sh'], shell=True)