from django.shortcuts import render
from django.http import JsonResponse
from pyModbusTCP.client import ModbusClient
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'main/index.html')

@csrf_exempt
def ventilation(request):

    def get_connection():
        connection = ModbusClient(host="10.30.0.30", port=502, unit_id=16, auto_open=True)
        return connection

    def getDataVentilation()->dict:
        data = dict.fromkeys(['512', '513', '514', '515', '516', '517', '518', '519', 
                                '520', '521', '522', '523', '524', '525', '526', '527', '528', '529', 
                                '530', '531', '532', '533', '534',
                                '1024', '1025', '1026', '1027', '1028', '1029'])
        # TCP auto connect on first modbus request
        connection = get_connection()

        for key in data:
            regs = connection.read_holding_registers(int(key), 1)
            if regs:
                data[key] = regs
            else:
                data[key] = 'read error'
        return data
    
    def setDataVentilation(addr, value)->dict:
        connection = get_connection()
        if connection.write_multiple_registers(addr, [value]):
            result = True
        else:
            result = False
        return {'result':result}

    if request.method == 'GET':
        data = getDataVentilation()
        return JsonResponse(data)
    elif request.method == 'POST':

        addr_str = request.GET.get('addr', False)
        value_str = request.GET.get('value', False)
        if not addr_str or not value_str:
            data = {'error': 'Не указаны параметры addr или value'}
        else:
            try:
                addr = int(addr_str)
            except:
                data = {'error': 'Введен некорректный адрес'}
                return JsonResponse(data)

            try:
                value = int(value_str)
            except:
                data = {'error': 'Введено некорректное значение'}
                return JsonResponse(data)

            avail_addr = ['521', '525', '526', '533', '1024', '1025', '1026', '1027', '1028', '1029']
            if not addr_str in avail_addr:
                data = {'error': 'Введен некорректный адрес'}
                return JsonResponse(data)

            data = setDataVentilation(addr, value)
        
        return JsonResponse(data)
    else:
        data = {'error': 'Неизвестный метод'}
        return JsonResponse(data)
