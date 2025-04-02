from django.shortcuts import render
from django.http import JsonResponse
from pyModbusTCP.client import ModbusClient
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from europartner.mqtt import client as mqtt_client

def index(request):
    return render(request, 'main/index.html')

@csrf_exempt
def ventilation(request):
    '''Данная вьюха управляет вентиляцией через протокол modbus'''

    def get_connection():
        '''Получает соединение с modbus'''
        connection = ModbusClient(host="192.168.1.167", port=502, unit_id=16, auto_open=True, timeout=5.0)
        connection.open()
        return connection

    def getDataVentilation()->dict:
        '''Возвращает данные из контроллера'''

        # Данные собираем только по этим адресам
        data = dict.fromkeys(['512', '513', '514', '515', '516', '517', '518', '519', 
                                '520', '521', '522', '523', '524', '525', '526', '527', '528', '529', 
                                '530', '531', '532', '533', '534', '535', '536', '537',
                                '538', '539', '540', '541', '542', '543', '544', '545',
                                '546', '547', '548',
                                '1024', '1025', '1026', '1027', '1028', '1029'])
        
        # Устанавливаем соединение
        connection = get_connection()
        # Если соединение установлено, получаем значения
        if connection.is_open:
            # Цикл по адресам, для чтения данных
            for key in data:
                regs = connection.read_holding_registers(int(key), 1)
                if regs:
                    data[key] = regs
                else:
                    data[key] = 'read error'
        data['connection'] = connection.is_open

        connection.close()
        return data
    
    def setDataVentilation(addr, value)->dict:
        '''Устанавливает значения в контроллера'''
        result = False
        connection = get_connection()
        if connection.is_open:
            if connection.write_multiple_registers(addr, [value]):
                result = True
        is_open = connection.is_open
        connection.close()
        return {'result':result, 'connection':is_open}
    
    def make_response(addr_str, value_str)->dict:
        '''Проверки перед установкой значений'''

        if not addr_str or not value_str:
            return {'error': 'Не указаны параметры addr или value'}
        else:
            # Проверка на ввод корректного значения адреса
            try:
                addr = int(addr_str)
            except:
                return {'error': 'Введен некорректный адрес'}
            # Проверка на ввод корректного значения значения
            try:
                value = int(value_str)
            except:
                return {'error': 'Введено некорректное значение'}

            # Проверка на ввод адреса, который можно менять
            avail_addr = ['521', '525', '526', '533', '536', '537', '545', '546', '547', '1024', '1025', '1026', '1027', '1028', '1029']
            if not addr_str in avail_addr:
                return {'error': 'Введен некорректный адрес'}

            # Проверки закончены, возвращаем
            return setDataVentilation(addr, value)

    if request.method == 'GET':
        data = getDataVentilation()
        return JsonResponse(data)
    elif request.method == 'POST':
        # Получим параметры из запроса
        addr_str = request.GET.get('addr', False)
        value_str = request.GET.get('value', False)
        data = make_response(addr_str, value_str)
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Неизвестный метод'})

@csrf_exempt
def yandex_forms(request):

    if request.method == 'POST':
        json_b = request.body
        try:
            data_json = json.loads(json_b)
            return JsonResponse(data_json, safe=False, status=status.HTTP_200_OK)
        except NameError:
            json_r = {'error': NameError}
            return JsonResponse(json_r, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def mqtt_publish(request):

     if request.method == 'POST':

        request_data = json.loads(request.body)
        rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])

        return JsonResponse(rc, safe=False, status=status.HTTP_200_OK)

