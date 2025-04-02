import paho.mqtt.client as mqtt
import json
import requests
from requests.auth import HTTPBasicAuth
from string import Template
from django.conf import settings

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        mqtt_client.subscribe("/dev/TPA_projectors/+")
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    if '/dev/TPA_projectors/K' in msg.topic:
        value = int(msg.payload)
        data = {'topic':msg.topic, 'msg':value}

        data_json = json.dumps(data)
        srv_tmpl = Template('http://$srv/$datebase/hs/django/TPA_projectors/')
        srv = srv_tmpl.substitute(srv=settings.ERP_SERVER, datebase=settings.ERP_DATEBASE)
        r = requests.post(srv, auth=HTTPBasicAuth(settings.ERP_USER, settings.ERP_PASSWORD), data=data_json, headers={'Content-Type': 'application/json'})

        #print(f'Client: {mqtt_client} Received message on topic: {msg.topic} with payload: {msg.payload}')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)