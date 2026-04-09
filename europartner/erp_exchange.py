import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def send_request(srv_tmpl, data_json):

    srv = srv_tmpl.substitute(srv=settings.ERP_SERVER, datebase=settings.ERP_DATEBASE)
    r = requests.post(srv, auth=HTTPBasicAuth(settings.ERP_USER, settings.ERP_PASSWORD), data=data_json, headers={'Content-Type': 'application/json'})

    return r