import requests
import json
from django.conf import settings

class bot_ERP():
    bot_id = settings.MAX_BOT_ID

    def __init__(self):
        pass

    def send_message(self, user_id, html_text):
        data = {'text':html_text, 'format':'html'}
        data_json = json.dumps(data)
        url = 'https://platform-api.max.ru' + '/messages?user_id=' + user_id
        answ = requests.post(url=url, data=data_json, headers={'Authorization': self.bot_id, 'Content-Type':'application/json'})

        print(answ.status_code)