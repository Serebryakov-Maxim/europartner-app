from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from tpa.models import Cycle
from django.utils import timezone
from django.conf import settings
from europartner.bot_MAX import bot_ERP
import subprocess

def checking_controllers():

    if settings.CRON_IS_ENABLE != None and settings.CRON_IS_ENABLE == False:
        print("Проверку пропускаем")
        return
    
    # последние данные
    obj = Cycle.objects.last()
    if obj == None:
        return
        
    # расчет количества сек. с последних данных
    tz = timezone.get_current_timezone()
    date_now = datetime.now().astimezone(tz)
    difference = date_now - obj.date
    total_seconds = difference.total_seconds()

    print("Количество секунд = " + str(total_seconds))

    # менее 100, ожидаем
    if total_seconds < 100:
        return
    
    # рассылка
    #print("Рассылка в MAX")
    subject = 'Нет данных с контроллеров ТПА!'
    message = 'Последние показания были ' + str(int(total_seconds)) + ' сек. назад'
    text = '<b>' + subject + '</b>' + '\n' + '<p>' + message + '</p>'

    bot = bot_ERP()
    bot.send_message(settings.MAX_USER_ID_SEREBRYAKOV, text)
    bot.send_message(settings.MAX_USER_ID_LOGACHEV, text)

    #print("Рассылка на почту")
    #send_mail(subject, message, settings.EMAIL_USER_SENDER, settings.EMAIL_USER_ALERT)
    
    # запуск скрипта на перезапуск службы
    print("Перезапуск скрипта")
    subprocess.run(['. /home/user/code/restart_raspberry_service/restart_service.sh'], shell=True)